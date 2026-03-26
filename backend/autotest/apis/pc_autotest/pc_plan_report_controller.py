# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_plan_report import (
    PcPlanReportQuery, PcPlanReportId, PcPlanReportDetailQuery,
)
from autotest.services.pc_autotest.pc_plan_report_service import PcPlanReportService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取PC计划报告列表")
async def get_plan_report_list(params: PcPlanReportQuery):
    data = await PcPlanReportService.list(params)
    return partner_success(data)


@router.post("/getById", description="根据ID获取PC计划报告")
async def get_plan_report_by_id(params: PcPlanReportId):
    data = await PcPlanReportService.get_by_id(params)
    return partner_success(data)


@router.post("/deleted", description="删除PC计划报告")
async def deleted(params: PcPlanReportId):
    data = await PcPlanReportService.deleted(params.id)
    return partner_success(data)


@router.post("/detailList", description="获取PC计划报告子用例明细")
async def get_detail_list(params: PcPlanReportDetailQuery):
    data = await PcPlanReportService.get_detail_list(params)
    return partner_success(data)
