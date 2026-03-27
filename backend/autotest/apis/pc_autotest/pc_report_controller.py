# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_report_schemas import (
    UiReportQuery, UiReportId, UiReportDetailQuery, SikuliXOperationResultDTO,
)
from autotest.services.pc_autotest.pc_report_service import UiReportService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post('/list', description="获取PC报告列表")
async def report_list(params: UiReportQuery):
    data = await UiReportService.list(params)
    return partner_success(data=data)


@router.post('/deleted', description="删除PC报告")
async def deleted(params: UiReportId):
    data = await UiReportService.deleted(params)
    return partner_success(data)


@router.post('/getPcReportDetail', description="获取PC报告步骤明细")
async def get_report_detail(params: UiReportDetailQuery):
    data = await UiReportService.detail(params)
    return partner_success(data)


@router.post('/getPcReportStatistics', description="PC报告统计")
async def get_report_statistics(params: UiReportDetailQuery):
    data = await UiReportService.statistics(params)
    return partner_success(data)


@router.post('/saveReportStepDetail', description="Agent回传步骤结果")
async def save_report_step_detail(params: SikuliXOperationResultDTO):
    print(params)
    data = await UiReportService.save_report_step_detail(params)
    return partner_success(data)
