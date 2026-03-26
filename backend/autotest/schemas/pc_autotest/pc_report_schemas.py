# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcReportQuery(BaseSchema):
    """PC报告查询"""
    id: typing.Optional[int] = Field(None, description="报告ID")
    case_id: typing.Optional[int] = Field(None, description="用例ID")
    report_name: typing.Optional[str] = Field(None, description="报告名称")
    status: typing.Optional[int] = Field(None, description="状态 0失败 1成功 2执行中")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcReportId(BaseSchema):
    """报告ID"""
    id: int = Field(..., description="报告ID")


class PcReportDetailQuery(BaseSchema):
    """PC报告步骤明细查询"""
    report_id: int = Field(..., description="报告ID")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


# Agent 回传的步骤结果 DTO
class PcStepResultIn(BaseSchema):
    """PC Agent回传步骤结果"""
    report_id: int = Field(..., description="报告ID")
    report_name: typing.Optional[str] = Field(None, description="报告名称")
    case_id: typing.Optional[int] = Field(None, description="用例ID")
    step_id: typing.Optional[int] = Field(None, description="步骤ID")
    operation_state: typing.Optional[str] = Field(None, description="操作状态")
    operation_type: typing.Optional[str] = Field(None, description="操作类型")
    expect_value: typing.Optional[str] = Field(None, description="预期值")
    actual_value: typing.Optional[str] = Field(None, description="实际值")
    state_image: typing.Optional[str] = Field(None, description="状态截图路径")
    exception_message: typing.Optional[str] = Field(None, description="异常信息")
    error_type: typing.Optional[str] = Field(None, description="错误类型")
    operation_context: typing.Optional[str] = Field(None, description="操作上下文")
    success: typing.Optional[bool] = Field(None, description="是否成功")
    original_image_path: typing.Optional[str] = Field(None, description="原始截图路径")
    duration: typing.Optional[int] = Field(None, description="耗时(ms)")
    is_lase_step: typing.Optional[bool] = Field(False, description="是否最后一步")
    is_template: typing.Optional[bool] = Field(False, description="是否模板步骤")
