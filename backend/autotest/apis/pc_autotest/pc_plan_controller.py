# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_plan import PcPlanQuery, PcPlanIn, PcPlanId, PcPlanRunIn
from autotest.services.pc_autotest.pc_plan_service import PcPlanService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取PC测试计划列表")
async def get_plan_list(params: PcPlanQuery):
    data = await PcPlanService.list(params)
    return partner_success(data)


@router.post("/getById", description="根据ID获取PC测试计划")
async def get_plan_by_id(params: PcPlanId):
    data = await PcPlanService.get_by_id(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存/更新PC测试计划")
async def save_or_update(params: PcPlanIn):
    data = await PcPlanService.save_or_update(params)
    return partner_success(data)


@router.post("/deleted", description="删除PC测试计划")
async def deleted(params: PcPlanId):
    data = await PcPlanService.deleted(params.id)
    return partner_success(data)


@router.post("/run", description="执行PC测试计划")
async def run_plan(params: PcPlanRunIn):
    data = await PcPlanService.run(params)
    return partner_success(data)
