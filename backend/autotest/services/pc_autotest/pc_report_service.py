# -*- coding: utf-8 -*-
import typing

from loguru import logger

from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_report_models import PcReport, get_pc_report_detail_model
from autotest.schemas.pc_autotest.pc_report_schemas import (
    PcReportQuery, PcReportId, PcReportDetailQuery, PcStepResultIn,
)


class PcReportService:
    """PC执行报告服务"""

    @staticmethod
    async def list(params: PcReportQuery):
        return await PcReport.get_list(params)

    @staticmethod
    async def get_by_id(params: PcReportId) -> dict:
        report = await PcReport.get(params.id, to_dict=True)
        if not report:
            raise ParameterError("报告不存在")
        return report

    @staticmethod
    async def deleted(id: int):
        report = await PcReport.get(id)
        if not report:
            raise ParameterError("报告不存在")
        return await PcReport.delete(id)

    @staticmethod
    async def get_detail_list(params: PcReportDetailQuery):
        """获取报告步骤明细列表（查对应分表）"""
        DetailModel = get_pc_report_detail_model(params.report_id)
        q = [DetailModel.enabled_flag == 1, DetailModel.report_id == params.report_id]
        from sqlalchemy import select
        stmt = (
            select(DetailModel.get_table_columns())
            .where(*q)
            .order_by(DetailModel.id.asc())
        )
        return await DetailModel.pagination(stmt)

    @staticmethod
    async def save_step_result(params: PcStepResultIn) -> dict:
        """
        接收 Agent 回传的步骤结果：
        - 保存到分表
        - 若 is_lase_step=True，汇总主报告 status/success/duration
        """
        report_id = params.report_id
        DetailModel = get_pc_report_detail_model(report_id)

        detail_data = params.dict(exclude={"is_lase_step"})
        detail_data["report_id"] = report_id
        await DetailModel.create_or_update(detail_data)

        if params.is_lase_step:
            await PcReportService._finalize_report(report_id)

        return {"report_id": report_id}

    @staticmethod
    async def _finalize_report(report_id: int):
        """
        当收到最后一步结果时，统计所有步骤，写回主报告。
        success = 所有步骤均成功，duration = 累计耗时
        """
        from sqlalchemy import select, func
        DetailModel = get_pc_report_detail_model(report_id)

        stmt = select(
            func.count(DetailModel.id).label("total"),
            func.sum(
                # 使用 CASE WHEN 统计 success=True 的数量
                DetailModel.success.cast(typing.cast(typing.Any, None))  # placeholder
            ).label("ok_count"),
            func.sum(DetailModel.duration).label("total_duration"),
        ).where(DetailModel.report_id == report_id, DetailModel.enabled_flag == 1)

        # 简化版：直接查所有明细再 Python 汇总（避免跨 DB 类型 CAST 问题）
        all_stmt = select(DetailModel.success, DetailModel.duration).where(
            DetailModel.report_id == report_id,
            DetailModel.enabled_flag == 1,
        )
        result = await DetailModel.execute(all_stmt)
        rows = result.fetchall()

        total_duration = sum((r[1] or 0) for r in rows)
        all_success = all(r[0] is True for r in rows) if rows else False
        status = 1 if all_success else 0

        await PcReport.create_or_update({
            "id": report_id,
            "status": status,
            "success": all_success,
            "duration": total_duration,
        })
        logger.info(f"PC报告 [{report_id}] 汇总完成: status={status}, duration={total_duration}ms")

    @staticmethod
    async def get_statistics(case_id: int) -> dict:
        """获取某用例最近 N 次报告的成功率统计"""
        from sqlalchemy import select, func
        stmt = (
            select(
                func.count(PcReport.id).label("total"),
                func.sum(PcReport.success.cast(typing.cast(typing.Any, None))).label("ok"),
            )
            .where(PcReport.case_id == case_id, PcReport.enabled_flag == 1)
        )
        # 直接 Python 统计
        list_stmt = select(PcReport.success).where(
            PcReport.case_id == case_id, PcReport.enabled_flag == 1
        ).order_by(PcReport.id.desc()).limit(20)
        result = await PcReport.execute(list_stmt)
        rows = result.fetchall()
        total = len(rows)
        ok = sum(1 for r in rows if r[0] is True)
        return {"total": total, "success": ok, "fail": total - ok}
