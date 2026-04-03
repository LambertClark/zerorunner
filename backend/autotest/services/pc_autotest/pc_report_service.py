# -*- coding: utf-8 -*-
import os
import typing

from loguru import logger

from config import config
from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_report_models import UiReports, UiReportDetail
from autotest.schemas.pc_autotest.pc_report_schemas import (
    UiReportQuery, UiReportId, UiReportDetailQuery, UiReportSaveSchema, SikuliXOperationResultDTO,
)
from autotest.utils.common import get_time
from zerorunner.models.result_model import TestCaseSummary, StepResult


class UiReportService:
    """PC执行报告服务"""

    @staticmethod
    async def list(params: UiReportQuery):
        return await UiReports.get_list(params)

    @staticmethod
    async def save_report(
        summary: TestCaseSummary,
        run_type=10,
        project_id=None,
        module_id=None,
        env_id=None,
        **kwargs,
    ):
        report_schema = UiReportSaveSchema()
        report = await UiReportService.save_report_info(report_schema)
        await UiReportService.save_report_detail(summary, report["id"], **kwargs)
        return report

    @staticmethod
    async def save_report_info(params: UiReportSaveSchema) -> dict:
        report_info = params.dict()
        return await UiReports.create_or_update(report_info)

    @staticmethod
    async def save_report_detail(summary, report_id: int, **kwargs):
        exec_user_id = kwargs.get("exec_user_id")
        exec_user_name = kwargs.get("exec_user_name")
        step_records = await UiReportService.parser_summary(summary.step_results)
        DetailModel = UiReportDetail.model(report_id)
        for record in step_records:
            record["report_id"] = report_id
            if exec_user_id:
                record["exec_user_id"] = exec_user_id
            if exec_user_name:
                record["exec_user_name"] = exec_user_name
            await DetailModel.create_or_update(record)

    @staticmethod
    async def parser_summary(step_results: typing.List[StepResult]) -> typing.List[dict]:
        """递归展开嵌套 step_result，处理截图，返回 list[dict]"""
        from autotest.services.system.file import FileService

        records: typing.List[dict] = []

        def _walk(results: typing.List[StepResult]):
            for result in results:
                new_step = result.dict()
                # 格式化 start_time
                start_time = new_step.get("start_time")
                if isinstance(start_time, float):
                    import datetime
                    new_step["start_time"] = datetime.datetime.fromtimestamp(start_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                # 截图 base64 保存
                ui_session_data = getattr(result, "session_data", None)
                if ui_session_data and getattr(ui_session_data, "screenshot_file_base64", None):
                    file_name = f"{result.name}{get_time()}_screenshot.png"
                    try:
                        import asyncio
                        file_info = asyncio.get_event_loop().run_until_complete(
                            FileService.save_base64_file(
                                ui_session_data.screenshot_file_base64,
                                file_name,
                            )
                        )
                        if file_info:
                            new_step["screenshot_file_id"] = file_info.get("id")
                    except Exception as e:
                        logger.warning(f"截图保存失败: {e}")
                    new_step.update(ui_session_data.dict())

                # 递归子步骤
                sub = result.step_result or []
                if sub:
                    _walk(sub)

                records.append(new_step)

        _walk(step_results)
        return records

    @staticmethod
    async def deleted(params: UiReportId):
        return await UiReports.delete(params.id)

    @staticmethod
    async def detail(params: UiReportDetailQuery):
        return await UiReportDetail.model(params.report_id).get_details(params)

    @staticmethod
    async def statistics(params: UiReportDetailQuery):
        return await UiReportDetail.model(params.report_id).statistics(params)

    @staticmethod
    async def get_report_result(
        summary: TestCaseSummary,
        project_id,
        module_id,
        env_id,
        exec_user_id=None,
        exec_user_name=None,
    ) -> UiReportSaveSchema:
        return UiReportSaveSchema(
            name=summary.name,
            start_time=str(summary.start_time),
            duration=int(summary.duration * 1000),
            case_id=summary.case_id,
            run_mode=10,
            success=summary.success,
            run_count=summary.run_count,
            run_success_count=summary.run_success_count,
            run_fail_count=summary.run_fail_count,
            run_skip_count=summary.run_skip_count,
            run_err_count=summary.run_err_count,
            run_log=summary.log,
            project_id=project_id,
            module_id=module_id,
            env_id=env_id,
            exec_user_id=exec_user_id,
            exec_user_name=exec_user_name,
        )

    @staticmethod
    async def save_report_step_detail(params: SikuliXOperationResultDTO) -> dict:
        """接收 Agent 回传步骤结果，写明细，最后一步时汇总主报告"""
        report_id = params.report_id
        DetailModel = UiReportDetail.model(report_id)

        detail_data = {
            "case_id": params.case_id,
            "report_id": params.report_id,
            "original_image_path": params.original_image_path,
            "state_image": params.state_image,
            "operation_type": params.operation_type,
            "operation_state": params.operation_state,
            "step_id": params.step_id,
            "error_type": params.error_type,
            "duration": params.duration,
            "success": params.success,
            "is_lase_step": params.is_lase_step,
            "is_template": params.is_template,
        }
        await DetailModel.create_or_update(detail_data)

        if params.is_lase_step:
            detail_params = UiReportDetailQuery(report_id=report_id)
            all_details = await DetailModel.get_list(detail_params)
            items = all_details.get("items", []) if isinstance(all_details, dict) else (all_details or [])
            total_duration = sum((item.get("duration") or 0) for item in items)
            # 优先用 success 字段判断，success 为 None 时回退到 operation_state（均为 bool）
            is_all_success = all(
                bool(item.get("success") if item.get("success") is not None else item.get("operation_state", False))
                for item in items
            )
            await UiReports.create_or_update({
                "id": report_id,
                "success": is_all_success,
                "status": 1 if is_all_success else 0,
                "duration": total_duration,
            })

        return {"report_id": report_id}

    # 向后兼容别名
    save_step_result = save_report_step_detail

    @staticmethod
    def _extract_upload_filename(file_url: str) -> typing.Optional[str]:
        """从 URL 中提取上传文件名（仅识别 /api/pc/fm/download/ 路径）"""
        marker = "/api/pc/fm/download/"
        if file_url and marker in file_url:
            return file_url.split(marker)[-1]
        return None

    @staticmethod
    async def cleanup_by_case_id(case_id: int) -> dict:
        """清理用例关联的所有报告及步骤明细文件"""
        reports = await UiReports.get_reports_by_case_id(case_id)
        report_ids = []
        detail_count = 0
        file_names_to_delete: typing.List[str] = []

        for report in (reports or []):
            rid = report.get("id") if isinstance(report, dict) else getattr(report, "id", None)
            if not rid:
                continue
            report_ids.append(rid)
            DetailModel = UiReportDetail.model(rid)
            detail_params = UiReportDetailQuery(report_id=rid)
            details_result = await DetailModel.get_list(detail_params)
            items = details_result.get("items", []) if isinstance(details_result, dict) else (details_result or [])
            for item in items:
                for field in ("state_image", "original_image_path"):
                    url = item.get(field) if isinstance(item, dict) else getattr(item, field, None)
                    if url:
                        fname = UiReportService._extract_upload_filename(url)
                        if fname:
                            file_names_to_delete.append(fname)
                detail_count += 1
                await DetailModel.delete(item.get("id") if isinstance(item, dict) else item.id)

        for rid in report_ids:
            await UiReports.delete(rid)

        file_count = 0
        upload_dir = config.UPLOAD_DIR
        for fname in file_names_to_delete:
            fpath = os.path.join(upload_dir, fname)
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                    file_count += 1
                except Exception as e:
                    logger.warning(f"删除文件失败 [{fpath}]: {e}")

        return {
            "report_count": len(report_ids),
            "detail_count": detail_count,
            "file_count": file_count,
        }


# 向后兼容别名
PcReportService = UiReportService
