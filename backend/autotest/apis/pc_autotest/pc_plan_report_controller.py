# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_plan_report import (
    PcPlanReportQuery, PcPlanReportId, PcPlanReportDetailQuery, PcPlanReportIn,
)
from autotest.services.pc_autotest.pc_plan_report_service import PcPlanReportService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post('/list', description="获取PC计划报告列表")
async def report_list(params: PcPlanReportQuery):
    data = await PcPlanReportService.list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="保存/更新PC计划报告")
async def save_or_update_report(params: PcPlanReportIn):
    data = await PcPlanReportService.save_or_update(params)
    return partner_success(data)


@router.post('/deleted', description="删除PC计划报告")
async def deleted(params: PcPlanReportId):
    data = await PcPlanReportService.delete(params.id)
    return partner_success(data)


@router.post('/getPcPlanReportDetail', description="获取PC计划报告步骤明细")
async def get_report_detail(params: PcPlanReportDetailQuery):
    data = await PcPlanReportService.get_report_detail(params)
    return partner_success(data)


@router.post('/getPcPlanReportStatistics', description="PC计划报告统计")
async def get_report_statistics(params: PcPlanReportDetailQuery):
    data = await PcPlanReportService.get_report_statistics(params)
    return partner_success(data)


@router.post('/savePcPlanReportStepDetail', description="保存PC计划报告步骤明细")
async def save_report_step_detail(params: dict):
    print(params)
    data = await PcPlanReportService.save_report_detail(params)
    return partner_success(data)


@router.post('/getPcPlanReportInfo', description="获取PC计划报告信息")
async def get_report_info(params: PcPlanReportQuery):
    data = await PcPlanReportService.detail(params)
    return partner_success(data)
