# -*- coding: utf-8 -*-
from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_plan_report_models import PcPlanReport, PcPlanReportDetail
from autotest.schemas.pc_autotest.pc_plan_report import (
    PcPlanReportQuery, PcPlanReportId, PcPlanReportDetailQuery,
)


class PcPlanReportService:
    """PC计划报告服务"""

    @staticmethod
    async def list(params: PcPlanReportQuery):
        return await PcPlanReport.get_list(params)

    @staticmethod
    async def get_by_id(params: PcPlanReportId) -> dict:
        report = await PcPlanReport.get(params.id, to_dict=True)
        if not report:
            raise ParameterError("计划报告不存在")
        return report

    @staticmethod
    async def deleted(id: int):
        report = await PcPlanReport.get(id)
        if not report:
            raise ParameterError("计划报告不存在")
        return await PcPlanReport.delete(id)

    @staticmethod
    async def get_detail_list(params: PcPlanReportDetailQuery):
        return await PcPlanReportDetail.get_list(params)
