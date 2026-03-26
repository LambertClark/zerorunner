# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcPlanReportQuery(BaseSchema):
    """PC计划报告查询"""
    id: typing.Optional[int] = Field(None, description="计划报告ID")
    plan_id: typing.Optional[int] = Field(None, description="计划ID")
    report_name: typing.Optional[str] = Field(None, description="报告名称")
    status: typing.Optional[int] = Field(None, description="状态 0失败 1成功 2执行中")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcPlanReportId(BaseSchema):
    """计划报告ID"""
    id: int = Field(..., description="计划报告ID")


class PcPlanReportDetailQuery(BaseSchema):
    """计划报告子用例明细查询"""
    plan_report_id: int = Field(..., description="计划报告ID")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")
