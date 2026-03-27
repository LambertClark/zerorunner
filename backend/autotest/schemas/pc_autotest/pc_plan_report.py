# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcPlanReportQuery(BaseSchema):
    """PC计划报告查询"""
    id: typing.Optional[int] = Field(None, description="计划报告ID")
    name: typing.Optional[str] = Field(None, description="报告名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    status: typing.Optional[int] = Field(None, description="状态 0失败 1成功 2执行中")
    success: typing.Optional[bool] = Field(None, description="是否成功")
    exec_user_name: typing.Optional[str] = Field(None, description="执行用户名")
    created_by: typing.Optional[int] = Field(None, description="创建人ID")
    created_by_name: typing.Optional[str] = Field(None, description="创建人名称")
    updated_by: typing.Optional[int] = Field(None, description="更新人ID")
    updated_by_name: typing.Optional[str] = Field(None, description="更新人名称")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcPlanReportIn(BaseSchema):
    """PC计划报告保存入参"""
    id: typing.Optional[int] = Field(None, description="计划报告ID")
    name: typing.Optional[str] = Field(None, description="报告名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    success: typing.Optional[bool] = Field(None, description="是否成功")
    status: typing.Optional[int] = Field(None, description="状态 0失败 1成功 2执行中")
    duration: typing.Optional[int] = Field(None, description="耗时(ms)")
    case_id: typing.Optional[int] = Field(None, description="用例ID")
    remarks: typing.Optional[str] = Field(None, description="备注")
    start_time: typing.Optional[str] = Field(None, description="开始时间")
    run_count: typing.Optional[int] = Field(None, description="运行步骤总数")
    run_success_count: typing.Optional[int] = Field(None, description="成功步骤数")
    run_fail_count: typing.Optional[int] = Field(None, description="失败步骤数")
    run_skip_count: typing.Optional[int] = Field(None, description="跳过步骤数")
    run_err_count: typing.Optional[int] = Field(None, description="错误步骤数")
    run_log: typing.Optional[str] = Field(None, description="运行日志")
    env_id: typing.Optional[int] = Field(None, description="环境ID")
    exec_user_id: typing.Optional[int] = Field(None, description="执行用户ID")
    exec_user_name: typing.Optional[str] = Field(None, description="执行用户名")
    run_mode: typing.Optional[str] = Field(None, description="运行模式")
    created_by: typing.Optional[int] = Field(None, description="创建人ID")
    created_by_name: typing.Optional[str] = Field(None, description="创建人名称")
    updated_by: typing.Optional[int] = Field(None, description="更新人ID")
    updated_by_name: typing.Optional[str] = Field(None, description="更新人名称")


class PcPlanReportId(BaseSchema):
    """计划报告ID"""
    id: int = Field(..., description="计划报告ID")


class PcPlanReportDetailQuery(BaseSchema):
    """计划报告子用例明细查询"""
    report_id: int = Field(..., description="计划报告ID")
    name: typing.Optional[str] = Field(None, description="用例名称")
    status: typing.Optional[int] = Field(None, description="状态 0失败 1成功 2执行中")
    success: typing.Optional[bool] = Field(None, description="是否成功")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")
