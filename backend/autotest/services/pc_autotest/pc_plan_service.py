# -*- coding: utf-8 -*-
import typing

from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_plan_models import PcPlan
from autotest.schemas.pc_autotest.pc_plan import PcPlanQuery, PcPlanIn, PcPlanId, PcPlanRunIn


class PcPlanService:
    """PC测试计划服务"""

    @staticmethod
    async def list(params: PcPlanQuery):
        return await PcPlan.get_list(params)

    @staticmethod
    async def get_by_id(params: PcPlanId) -> dict:
        plan = await PcPlan.get(params.id, to_dict=True)
        if not plan:
            raise ParameterError("测试计划不存在")
        return plan

    @staticmethod
    async def save_or_update(params: PcPlanIn) -> dict:
        data = params.dict()
        return await PcPlan.create_or_update(data)

    @staticmethod
    async def deleted(id: int):
        plan = await PcPlan.get(id)
        if not plan:
            raise ParameterError("测试计划不存在")
        return await PcPlan.delete(id)

    @staticmethod
    async def run(params: PcPlanRunIn) -> dict:
        """
        执行测试计划：
        - 查询计划，获取 case_ids
        - 逐一调用 pc_testcase_service.run
        - 创建计划报告主表
        """
        from autotest.models.pc_plan_report_models import PcPlanReport, PcPlanReportDetail
        from autotest.schemas.pc_autotest.pc_case import PcTestcaseRunIn
        from autotest.services.pc_autotest.pc_testcase_service import PcTestcaseService
        from autotest.utils.current_user import current_user

        plan = await PcPlan.get(params.id)
        if not plan:
            raise ParameterError("测试计划不存在")

        case_ids: typing.List[int] = plan.case_ids or []
        if not case_ids:
            raise ParameterError("测试计划中无关联用例")

        identity = params.pc_device_identity or plan.pc_device_identity
        current_user_info = await current_user()
        executor_id = current_user_info.get("id") if current_user_info else 0

        # 创建计划报告主表
        plan_report_data = {
            "report_name": f"{plan.name}_计划报告",
            "plan_id": plan.id,
            "plan_name": plan.name,
            "status": 2,
            "total_count": len(case_ids),
            "executor_id": executor_id,
            "device_identity": identity,
        }
        plan_report = await PcPlanReport.create_or_update(plan_report_data)
        plan_report_id = plan_report["id"]

        # 逐个执行用例
        for case_id in case_ids:
            try:
                run_result = await PcTestcaseService.run(
                    PcTestcaseRunIn(id=case_id, pc_device_identity=identity)
                )
                await PcPlanReportDetail.create_or_update({
                    "plan_report_id": plan_report_id,
                    "case_id": case_id,
                    "report_id": run_result["report_id"],
                    "status": 2,
                })
            except Exception as e:
                await PcPlanReportDetail.create_or_update({
                    "plan_report_id": plan_report_id,
                    "case_id": case_id,
                    "status": 0,
                    "success": False,
                })

        return {"plan_report_id": plan_report_id}
