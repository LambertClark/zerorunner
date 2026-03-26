# -*- coding: utf-8 -*-
import typing

from loguru import logger

from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_device_models import PcDevice
from autotest.models.pc_picture_models import PcPictureBinding
from autotest.models.pc_report_models import PcReport
from autotest.models.pc_testcase_models import PcCase
from autotest.schemas.pc_autotest.pc_case import PcTestcaseQuery, PcTestcaseIn, PcTestcaseId, PcTestcaseRunIn
from autotest.utils.async_http import AsyncHttp
from autotest.utils.current_user import current_user

# PC Agent 协议路径
_AGENT_PING_PATH = "/api/v1/ping"
_AGENT_EXECUTE_PATH = "/api/v1/pc_ui_case/execute"

# PC 步骤中涉及图片的字段名
_PC_IMAGE_FIELDS = (
    "image", "dragImage", "referenceImage",
    "targetImage", "trackImage", "parentImage",
)


def _extract_image_urls(step_list: typing.List[dict]) -> typing.List[str]:
    """递归提取步骤树中所有图片 URL（去重）"""
    urls: typing.Set[str] = set()

    def _walk(steps: typing.List[dict]):
        for step in steps:
            request = step.get("request") or {}
            for field in _PC_IMAGE_FIELDS:
                val = request.get(field)
                if val and isinstance(val, str):
                    urls.add(val)
            # 递归子步骤
            for sub_key in ("children_steps", "setup_hooks", "teardown_hooks"):
                sub = step.get(sub_key) or []
                if sub:
                    _walk(sub)

    _walk(step_list)
    return list(urls)


class PcTestcaseService:
    """PC自动化用例服务"""

    @staticmethod
    async def list(params: PcTestcaseQuery):
        return await PcCase.get_list(params)

    @staticmethod
    async def get_case_by_id(params: PcTestcaseId) -> dict:
        case_info = await PcCase.get_case_by_id(params.id)
        if not case_info:
            raise ParameterError("PC用例不存在")
        return case_info

    @staticmethod
    async def save_or_update(params: PcTestcaseIn) -> dict:
        """保存/更新用例，并同步更新素材绑定关系"""
        data = params.dict(exclude_none=False)
        # step_data 需序列化为 dict list 存 JSON
        if params.step_data:
            data["step_data"] = [s.dict() for s in params.step_data]

        result = await PcCase.create_or_update(data)
        case_id = result["id"]

        # 更新素材绑定
        step_list = data.get("step_data") or []
        image_urls = _extract_image_urls(step_list)
        await PcPictureBinding.clear_case_bindings(case_id)
        await PcPictureBinding.bind_case_by_image_urls(image_urls, case_id)

        return await PcTestcaseService.get_case_by_id(PcTestcaseId(id=case_id))

    @staticmethod
    async def deleted(id: int):
        """删除用例并清理素材绑定"""
        case_info = await PcCase.get(id)
        if not case_info:
            raise ParameterError("PC用例不存在")
        await PcPictureBinding.clear_case_bindings(id)
        return await PcCase.delete(id)

    @staticmethod
    async def copy(params: PcTestcaseId) -> dict:
        """复制用例"""
        case_info = await PcCase.get_case_by_id(params.id)
        if not case_info:
            raise ParameterError("PC用例不存在")
        case_info.pop("id", None)
        case_info["name"] = f"{case_info['name']}_copy"
        result = await PcCase.create_or_update(case_info)
        return result

    # ------------------------------------------------------------------
    # 执行主链路
    # ------------------------------------------------------------------

    @staticmethod
    async def run(params: PcTestcaseRunIn) -> dict:
        """
        执行 PC 用例：
        1. 查询用例
        2. 确定执行设备 identity
        3. 解析设备 IP 列表
        4. 对每个 IP: ping → execute
        5. 创建报告主表
        6. 返回 report_id
        """
        case_info = await PcCase.get_case_by_id(params.id)
        if not case_info:
            raise ParameterError("PC用例不存在")

        identity = params.pc_device_identity or case_info.get("pc_device_identity")
        if not identity:
            raise ParameterError("未指定执行设备标识")

        device = await PcDevice.get_by_identity(identity)
        if not device:
            raise ParameterError(f"未找到设备 [{identity}]")

        ip_list = [ip.strip() for ip in (device.ipv4_addresses or "").split(",") if ip.strip()]
        if not ip_list:
            raise ParameterError(f"设备 [{identity}] 未配置 IP 地址")

        port = device.port or 8088

        # 选取第一个可 ping 通的 IP
        target_ip = await PcTestcaseService._pick_available_ip(ip_list, port)
        if not target_ip:
            raise ParameterError(f"设备 [{identity}] 所有 IP 均不可达: {ip_list}")

        # 创建报告主表
        current_user_info = await current_user()
        executor_id = current_user_info.get("id") if current_user_info else 0
        report_name = f"{case_info['name']}_执行报告"
        report_params = {
            "report_name": report_name,
            "case_id": case_info["id"],
            "case_name": case_info["name"],
            "project_id": case_info.get("project_id"),
            "status": 2,  # 执行中
            "executor_id": executor_id,
            "device_identity": identity,
        }
        report_result = await PcReport.create_or_update(report_params)
        report_id = report_result["id"]

        # 异步调用 Agent（fire-and-forget，不阻塞接口返回）
        import asyncio
        asyncio.create_task(
            PcTestcaseService._call_agent_execute(
                ip=target_ip,
                port=port,
                case_info=case_info,
                report_id=report_id,
                report_name=report_name,
            )
        )

        return {"report_id": report_id, "report_name": report_name}

    @staticmethod
    async def _pick_available_ip(ip_list: typing.List[str], port: int) -> typing.Optional[str]:
        """遍历 IP 列表，返回第一个 ping 通的 IP"""
        for ip in ip_list:
            if await PcTestcaseService._ping_agent(ip, port):
                return ip
        return None

    @staticmethod
    async def _ping_agent(ip: str, port: int) -> bool:
        """健康检查 Agent"""
        url = f"http://{ip}:{port}{_AGENT_PING_PATH}"
        try:
            async with AsyncHttp() as session:
                resp = await session.get(url, timeout=5)
                return resp.status == 200
        except Exception as e:
            logger.warning(f"PC Agent ping 失败 [{url}]: {e}")
            return False

    @staticmethod
    async def _call_agent_execute(
        ip: str,
        port: int,
        case_info: dict,
        report_id: int,
        report_name: str,
    ):
        """调用 Agent 执行接口"""
        url = f"http://{ip}:{port}{_AGENT_EXECUTE_PATH}"
        payload = {
            "case_info": case_info,
            "report_name": report_name,
            "report_id": report_id,
        }
        try:
            async with AsyncHttp() as session:
                resp = await session.post(url, json=payload, timeout=300)
                logger.info(f"PC Agent execute 响应 [{url}]: {resp.status}")
        except Exception as e:
            logger.error(f"PC Agent execute 调用失败 [{url}]: {e}")
            # 调用失败时把报告状态更新为失败
            await PcReport.create_or_update({"id": report_id, "status": 0, "success": False})
