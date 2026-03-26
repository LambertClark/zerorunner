# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_case import PcTestcaseQuery, PcTestcaseIn, PcTestcaseId, PcTestcaseRunIn
from autotest.services.pc_autotest.pc_testcase_service import PcTestcaseService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取PC用例列表")
async def get_case_list(params: PcTestcaseQuery):
    data = await PcTestcaseService.list(params)
    return partner_success(data)


@router.post("/getById", description="根据ID获取PC用例")
async def get_case_by_id(params: PcTestcaseId):
    data = await PcTestcaseService.get_case_by_id(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存/更新PC用例")
async def save_or_update(params: PcTestcaseIn):
    data = await PcTestcaseService.save_or_update(params)
    return partner_success(data)


@router.post("/deleted", description="删除PC用例")
async def deleted(params: PcTestcaseId):
    data = await PcTestcaseService.deleted(params.id)
    return partner_success(data)


@router.post("/copy", description="复制PC用例")
async def copy_case(params: PcTestcaseId):
    data = await PcTestcaseService.copy(params)
    return partner_success(data)


@router.post("/run", description="执行PC用例")
async def run_case(params: PcTestcaseRunIn):
    data = await PcTestcaseService.run(params)
    return partner_success(data)
