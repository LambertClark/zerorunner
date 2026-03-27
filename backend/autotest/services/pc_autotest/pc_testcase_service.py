# -*- coding: utf-8 -*-
import json
import typing

import requests
from loguru import logger

from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_picture_models import PcPictureBinding as PictureInfo
from autotest.models.pc_testcase_models import PcCase
from autotest.schemas.pc_autotest.pc_case import PcCaseQuery, PcCaseIn, PcCaseId, PcRunCaseRequest
from autotest.services.api.module import ModuleService

IMAGE_FIELDS = ("image", "dragImage", "referenceImage", "targetImage", "trackImage", "parentImage")
CHILD_KEYS = ("children", "children_steps", "sub_steps")


def get_step_data_tree(step_data: typing.List[dict]) -> typing.List[str]:
    """递归扫描步骤树，提取 IMAGE_FIELDS 中的 URL，去重后返回"""
    urls: typing.Set[str] = set()

    def _walk(steps: typing.List[dict]):
        for step in steps:
            request = step.get("request") or {}
            for field in IMAGE_FIELDS:
                val = request.get(field)
                if val and isinstance(val, str):
                    urls.add(val)
            for child_key in CHILD_KEYS:
                children = step.get(child_key) or []
                if children:
                    _walk(children)

    _walk(step_data)
    return list(urls)


class PcTestcaseService:
    """PC自动化用例服务"""

    @staticmethod
    async def save_or_update(params: PcCaseIn) -> dict:
        result = await PcCase.create_or_update(params.dict())
        case_id = result.get("id")
        image_urls = get_step_data_tree(params.step_data or [])
        await PictureInfo.clear_case_bindings(case_id)
        await PictureInfo.bind_case_by_image_urls(image_urls, case_id)
        return result

    @staticmethod
    async def list(params: PcCaseQuery):
        return await PcCase.get_list(params)

    @staticmethod
    async def detail(params: PcCaseQuery):
        return await PcCase.get_case_by_id(params.id)

    @staticmethod
    async def delete(id: int):
        await PictureInfo.clear_case_bindings(id)
        from autotest.services.pc_autotest.pc_report_service import UiReportService
        await UiReportService.cleanup_by_case_id(id)
        return await PcCase.delete(id)

    @staticmethod
    async def copy(params: PcCaseQuery):
        source_case_info = await PcCase.get(params.id, to_dict=True)
        if not source_case_info:
            raise ParameterError("用例不存在!")
        source_case_info.pop("id", None)
        case_info = PcCaseQuery.parse_obj(source_case_info)
        title = f"copy_{case_info.title}"
        copy_dict = source_case_info.copy()
        copy_dict["title"] = title
        return await PcCase.create_or_update(copy_dict)

    @staticmethod
    async def get_all():
        return await PcCase.get_all()

    @staticmethod
    async def get_cases_module_tree():
        all_cases = await PcCase.get_all()
        all_modules = await ModuleService.get_all()

        # 收集有用例的 module_id
        used_module_ids = set()
        for case in (all_cases or []):
            mid = case.get("module_id") if isinstance(case, dict) else getattr(case, "module_id", None)
            if mid:
                used_module_ids.add(mid)

        module_list = all_modules if isinstance(all_modules, list) else (all_modules or [])
        children = []
        for module in module_list:
            mid = module.get("id") if isinstance(module, dict) else getattr(module, "id", None)
            label = module.get("name") if isinstance(module, dict) else getattr(module, "name", "")
            children.append({
                "id": mid,
                "label": label,
                "children": [{"id": "", "label": "全部"}],
            })

        return {"id": "", "label": "选择模块", "children": children}

    @staticmethod
    async def get_case_info(params: PcCaseId):
        case_info = await PcCase.get(params.id, to_dict=True)
        if not case_info:
            raise ValueError('不存在当前套件！')
        return case_info

    @staticmethod
    async def run_pc_cases(params: PcRunCaseRequest):
        if not params.case_id:
            raise ParameterError("case_id 不能为空")

        case_info = await PcCase.get(params.case_id, to_dict=True)
        if not case_info:
            raise ParameterError("用例不存在")

        from autotest.services.pc_autotest.pc_devices_service import PcDevicesService
        pc_device_info = await PcDevicesService.get(params.pc_device_identity)
        if not pc_device_info:
            raise ParameterError(f"设备 [{params.pc_device_identity}] 不存在")

        ip_list = [ip.strip() for ip in (pc_device_info.ipv4_addresses or "").split(",") if ip.strip()]
        base_url_template = "http://{}:8080"
        ping = "/api/v1/ping"
        run = "/api/v1/pc_ui_case/execute"

        from autotest.schemas.pc_autotest.pc_report_schemas import UiReportSaveSchema
        from autotest.services.pc_autotest.pc_report_service import UiReportService

        for ip in ip_list:
            ping_url = base_url_template.format(ip) + ping
            run_url = base_url_template.format(ip) + run
            try:
                resp = requests.get(ping_url, timeout=5)
                if resp.status_code != 200:
                    continue
            except Exception as e:
                print(f"ping {ping_url} failed: {e}")
                continue

            # 创建报告
            report = await UiReportService.save_report_info(
                UiReportSaveSchema(
                    name=params.report_name,
                    case_id=params.case_id,
                    status="EXECUTE",
                )
            )

            case_dict = {
                "id": case_info.get("id"),
                "title": case_info.get("title"),
                "step_data": case_info.get("step_data"),
            }
            data = {
                "case_info": json.dumps(case_dict, ensure_ascii=False),
                "report_name": params.report_name,
                "report_id": report["id"],
            }

            try:
                requests.post(run_url, json=data, timeout=30)
            except Exception as e:
                print(f"run {run_url} failed: {e}")

            return {"report_id": report["id"]}

        raise ParameterError("所有 IP 均不可达，无法执行用例")
