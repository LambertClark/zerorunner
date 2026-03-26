# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcPlanQuery(BaseSchema):
    """PC测试计划查询"""
    id: typing.Optional[int] = Field(None, description="计划ID")
    name: typing.Optional[str] = Field(None, description="计划名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcPlanIn(BaseSchema):
    """PC测试计划入参"""
    id: typing.Optional[int] = Field(None, description="计划ID")
    name: str = Field(..., description="计划名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    case_ids: typing.Optional[typing.List[int]] = Field([], description="关联用例ID列表")
    pc_device_identity: typing.Optional[str] = Field(None, description="默认执行设备标识")
    remarks: typing.Optional[str] = Field(None, description="备注")
    enabled_flag: int = Field(1, description="是否启用")


class PcPlanId(BaseSchema):
    """计划ID"""
    id: int = Field(..., description="计划ID")


class PcPlanRunIn(BaseSchema):
    """PC计划执行入参"""
    id: int = Field(..., description="计划ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="覆盖执行设备标识")
