# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class UiReportQuery(BaseSchema):
    """PC报告查询"""
    id: typing.Optional[int] = Field(None, description="报告ID")
    ids: typing.Optional[typing.List[int]] = Field(None, description="报告ID列表")
    project_name: typing.Optional[str] = Field(None, description="项目名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    exec_user_name: typing.Optional[str] = Field(None, description="执行用户名")
    min_and_max: typing.Optional[typing.List[typing.Any]] = Field(None, description="时间范围[min, max]")
    report_type: typing.Optional[str] = Field(None, description="报告类型")
    name: typing.Optional[str] = Field(None, description="报告名称")
    user_ids: typing.Optional[typing.List[int]] = Field(None, description="用户ID列表")
    created_by: typing.Optional[int] = Field(None, description="创建人ID")
    project_ids: typing.Optional[typing.List[int]] = Field(None, description="项目ID列表")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class UiReportSaveSchema(BaseSchema):
    """PC报告保存"""
    id: typing.Optional[int] = Field(None, description="报告ID")
    name: typing.Optional[str] = Field(None, description="报告名称")
    start_time: typing.Optional[str] = Field(None, description="开始时间")
    duration: typing.Optional[float] = Field(None, description="耗时（秒）")
    case_id: typing.Optional[int] = Field(None, description="用例ID")
    run_mode: typing.Optional[str] = Field(None, description="运行模式")
    success: typing.Optional[bool] = Field(None, description="是否成功")
    status: typing.Optional[int] = Field(None, description="状态 0失败 1成功 2执行中")
    run_count: typing.Optional[int] = Field(None, description="运行步骤总数")
    run_success_count: typing.Optional[int] = Field(None, description="成功步骤数")
    run_fail_count: typing.Optional[int] = Field(None, description="失败步骤数")
    run_skip_count: typing.Optional[int] = Field(None, description="跳过步骤数")
    run_err_count: typing.Optional[int] = Field(None, description="错误步骤数")
    run_log: typing.Optional[str] = Field(None, description="运行日志")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    env_id: typing.Optional[int] = Field(None, description="环境ID")
    exec_user_id: typing.Optional[int] = Field(None, description="执行用户ID")
    exec_user_name: typing.Optional[str] = Field(None, description="执行用户名")


class UiReportMakeSchema(BaseSchema):
    """PC报告生成"""
    pass


class UiReportId(BaseSchema):
    """报告ID"""
    id: int = Field(..., description="报告ID")


class UiReportDetailQuery(BaseSchema):
    """PC报告步骤明细查询"""
    report_id: int = Field(..., description="报告ID")
    name: typing.Optional[str] = Field(None, description="步骤名称")
    step_type: typing.Optional[str] = Field(None, description="步骤类型")
    status_list: typing.Optional[typing.List[int]] = Field(None, description="状态筛选列表")
    parent_step_id: typing.Optional[int] = Field(None, description="父步骤ID")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class SikuliXOperationResultDTO(BaseSchema):
    """Agent 回传步骤结果 DTO"""
    operation_state: typing.Optional[bool] = Field(None, description="操作状态（是否成功）")
    operation_type: typing.Optional[str] = Field(None, description="操作类型")
    expect_value: typing.Optional[str] = Field(None, description="预期值")
    actual_value: typing.Optional[str] = Field(None, description="实际值")
    state_image: typing.Optional[str] = Field(None, description="状态截图路径")
    exception_message: typing.Optional[str] = Field(None, description="异常信息")
    error_type: typing.Optional[str] = Field(None, description="错误类型")
    operation_context: typing.Optional[str] = Field(None, description="操作上下文")
    case_id: typing.Optional[int] = Field(None, description="用例ID")
    step_id: typing.Optional[int] = Field(None, description="步骤ID")
    success: typing.Optional[bool] = Field(None, description="是否成功")
    report_id: typing.Optional[int] = Field(None, description="报告ID")
    report_name: typing.Optional[str] = Field(None, description="报告名称")
    original_image_path: typing.Optional[str] = Field(None, description="原始截图路径")
    duration: typing.Optional[float] = Field(None, description="耗时（秒）")
    is_lase_step: typing.Optional[bool] = Field(False, description="是否最后一步")
    is_template: typing.Optional[bool] = Field(False, description="是否模板步骤")


# ---------- 向后兼容别名 ----------

# pc_report_controller / pc_report_service / pc_report_models 使用旧名称
PcReportQuery = UiReportQuery
PcReportId = UiReportId
PcReportDetailQuery = UiReportDetailQuery
PcStepResultIn = SikuliXOperationResultDTO
