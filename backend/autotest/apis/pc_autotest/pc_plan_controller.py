# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_plan import PcPlanQuery, PcPlanIn, PcPlanId, PcPlanRun
from autotest.services.pc_autotest.pc_plan_service import PcPlanService
from autotest.utils.response.http_response import partner_success, respond_with_data

router = APIRouter()


@router.post('/list', description="获取PC测试计划列表")
async def get_pc_plan_list(params: PcPlanQuery):
    return await respond_with_data(PcPlanService.list, params)


@router.post('/copyPcPlan', description="复制PC测试计划")
async def copy_pc_plan(params: PcPlanQuery):
    await PcPlanService.copy(params)
    return partner_success()


@router.post('/saveOrUpdate', description="保存/更新PC测试计划")
async def save_or_update_pc_plan(params: PcPlanIn):
    data = await PcPlanService.save_or_update(params)
    return partner_success(data)


@router.post('/deletePcPlan', description="删除PC测试计划")
async def delete_pc_plan(params: PcPlanQuery):
    data = await PcPlanService.delete(params.id)
    return partner_success(data)


@router.post('/getPcPlanInfo', description="获取PC计划详情")
async def get_plan_info(params: PcPlanId):
    data = await PcPlanService.get_plan_info(params)
    return partner_success(data)


@router.post('/getPcPlanDetail', description="获取PC计划详情（查询版）")
async def get_plan_detail(params: PcPlanQuery):
    data = await PcPlanService.detail(params)
    return partner_success(data)


@router.post('/runPlanCases', description="执行PC测试计划")
async def run_plan_cases(params: PcPlanRun):
    data = await PcPlanService.run_plan(params)
    return partner_success(data=data)
