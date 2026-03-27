# -*- coding: utf-8 -*-
import typing

from autotest.models.pc_plan_report_models import PcPlanReports, PcPlanReportDetail
from autotest.schemas.pc_autotest.pc_plan_report import (
    PcPlanReportQuery, PcPlanReportIn, PcPlanReportDetailQuery,
)


class PcPlanReportService:
    """PC计划报告服务"""

    @staticmethod
    async def list(params: PcPlanReportQuery):
        return await PcPlanReports.get_list(params)

    @staticmethod
    async def save_or_update(params: PcPlanReportIn):
        print(params)
        return await PcPlanReports.create_or_update(params.dict())

    @staticmethod
    async def detail(params: PcPlanReportQuery):
        return await PcPlanReports.get_report_by_id(params.id)

    @staticmethod
    async def delete(id: int):
        return await PcPlanReports.delete(id)

    @staticmethod
    async def get_report_detail(params: PcPlanReportDetailQuery):
        return await PcPlanReportDetail.model(params.report_id).get_details(params)

    @staticmethod
    async def get_report_statistics(params: PcPlanReportDetailQuery):
        return await PcPlanReportDetail.model(params.report_id).statistics(params)

    @staticmethod
    async def save_report_detail(params: typing.Dict):
        report_id = params.get('report_id')
        if not report_id:
            raise ValueError('报告ID不能为空')
        return await PcPlanReportDetail.model(report_id).create_or_update(params)
