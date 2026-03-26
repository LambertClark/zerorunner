# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_report_schemas import (
    PcReportQuery, PcReportId, PcReportDetailQuery, PcStepResultIn,
)
from autotest.services.pc_autotest.pc_report_service import PcReportService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取PC报告列表")
async def get_report_list(params: PcReportQuery):
    data = await PcReportService.list(params)
    return partner_success(data)


@router.post("/getById", description="根据ID获取PC报告")
async def get_report_by_id(params: PcReportId):
    data = await PcReportService.get_by_id(params)
    return partner_success(data)


@router.post("/deleted", description="删除PC报告")
async def deleted(params: PcReportId):
    data = await PcReportService.deleted(params.id)
    return partner_success(data)


@router.post("/detailList", description="获取PC报告步骤明细")
async def get_detail_list(params: PcReportDetailQuery):
    data = await PcReportService.get_detail_list(params)
    return partner_success(data)


@router.post("/saveReportStepDetail", description="Agent回传步骤结果（供外部PC Agent调用）")
async def save_report_step_detail(params: PcStepResultIn):
    """PC Agent 回传步骤结果的接收端点"""
    data = await PcReportService.save_step_result(params)
    return partner_success(data)


@router.post("/statistics", description="用例报告统计")
async def get_statistics(params: PcReportQuery):
    if not params.case_id:
        return partner_success({})
    data = await PcReportService.get_statistics(params.case_id)
    return partner_success(data)
