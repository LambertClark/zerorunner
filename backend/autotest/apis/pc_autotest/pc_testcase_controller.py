# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_case import PcCaseQuery, PcCaseIn, PcCaseId, PcRunCaseRequest
from autotest.services.pc_autotest.pc_testcase_service import PcTestcaseService
from autotest.utils.common import get_time
from autotest.utils.response.http_response import partner_success, respond_with_data

router = APIRouter()


@router.post('/getPcCaseList', description="获取PC用例列表")
async def get_event_tracking_cases(params: PcCaseQuery):
    return await respond_with_data(PcTestcaseService.list, params)


@router.post('/getPcCaseTemplateList', description="获取PC用例模板列表")
async def get_event_tracking_cases(params: PcCaseQuery):
    return await respond_with_data(PcTestcaseService.list, params)


@router.post('/copyPcCase', description="复制PC用例")
async def copy_et_case(params: PcCaseQuery):
    await PcTestcaseService.copy(params)
    return partner_success()


@router.post('/saveOrUpdate', description="保存/更新PC用例")
async def save_or_update_pc_case(params: PcCaseIn):
    data = await PcTestcaseService.save_or_update(params)
    return partner_success(data)


@router.post('/deletePcCase', description="删除PC用例")
async def delete_event_tracking_case(params: PcCaseQuery):
    data = await PcTestcaseService.delete(params.id)
    return partner_success(data)


@router.post('/getPcCasesModuleTree', description="获取PC用例模块树")
async def get_cases_module_tree():
    data = await PcTestcaseService.get_cases_module_tree()
    return partner_success(data)


@router.post('/runCases', description="执行PC用例")
async def run_pc_cases(params: PcRunCaseRequest):
    params.report_name = f"{params.case_id}_{get_time(1)}"
    data = await PcTestcaseService.run_pc_cases(params)
    return partner_success(data)


@router.post('/getCaseInfo', description="获取PC用例详情")
async def get_case_info(params: PcCaseId):
    data = await PcTestcaseService.get_case_info(params)
    return partner_success(data)
