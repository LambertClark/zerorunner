# -*- coding: utf-8 -*-
import typing

from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_plan_models import PcPlan
from autotest.schemas.pc_autotest.pc_plan import PcPlanQuery, PcPlanIn, PcPlanId, PcPlanRun


class PcPlanService:
    """PC测试计划服务"""

    @staticmethod
    async def save_or_update(params: PcPlanIn):
        print(params)
        return await PcPlan.create_or_update(params.dict())

    @staticmethod
    async def list(params: PcPlanQuery):
        return await PcPlan.get_list(params)

    @staticmethod
    async def detail(params: PcPlanQuery):
        return await PcPlan.get_plan_by_id(params.id)

    @staticmethod
    async def delete(id: int):
        return await PcPlan.delete(id)

    @staticmethod
    async def copy(params: PcPlanQuery):
        source_plan_info = await PcPlan.get(params.id, to_dict=True)
        if not source_plan_info:
            raise ParameterError('计划不存在!')
        source_plan_info.pop('id', None)
        plan_info = PcPlanQuery.parse_obj(source_plan_info)
        title = f'copy_{plan_info.title}'
        copy_dict = source_plan_info.copy()
        copy_dict['title'] = title
        return await PcPlan.create_or_update(copy_dict)

    @staticmethod
    async def get_all():
        return await PcPlan.get_all()

    @staticmethod
    async def get_plan_info(params: PcPlanId):
        plan = await PcPlan.get(params.id, to_dict=True)
        if not plan:
            raise ValueError('不存在当前计划！')
        return plan

    @staticmethod
    async def run_plan(params: PcPlanRun):
        from autotest.schemas.pc_autotest.pc_case import PcRunCaseRequest
        from autotest.services.pc_autotest.pc_testcase_service import PcTestcaseService
        from autotest.utils.common import get_time

        plan = await PcPlan.get(params.plan_id, to_dict=True)
        cases = plan.get('cases') if plan else None
        if not cases:
            raise ParameterError('计划不存在或没有关联用例')

        results = []
        for case_item in cases:
            if isinstance(case_item, int):
                case_id = case_item
            elif isinstance(case_item, dict):
                case_id = case_item.get('id') or case_item.get('case_id')
            else:
                continue
            if not case_id:
                continue
            req = PcRunCaseRequest(
                case_id=case_id,
                pc_device_identity=params.pc_device_identity,
                report_name=f'{case_id}_{get_time(1)}',
            )
            try:
                resp = await PcTestcaseService.run_pc_cases(req)
            except Exception as e:
                resp = {'error': str(e)}
            results.append({'case_id': case_id, 'result': resp})
        return results
