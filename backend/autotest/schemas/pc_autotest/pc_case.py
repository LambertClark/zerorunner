# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema
from autotest.schemas.step_data import TStepData


class PcTestcaseQuery(BaseSchema):
    """PC用例查询参数"""
    id: typing.Optional[int] = Field(None, description="用例ID")
    name: typing.Optional[str] = Field(None, description="用例名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="绑定设备标识")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcTestcaseIn(BaseSchema):
    """PC用例入参"""
    id: typing.Optional[int] = Field(None, description="用例ID")
    name: str = Field(..., description="用例名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="绑定执行设备标识")
    step_data: typing.Optional[typing.List[TStepData]] = Field([], description="步骤树")
    remarks: typing.Optional[str] = Field(None, description="备注")
    tags: typing.Optional[typing.List[str]] = Field(None, description="标签")
    enabled_flag: int = Field(1, description="是否启用")


class PcTestcaseId(BaseSchema):
    """用例ID"""
    id: int = Field(..., description="用例ID")


class PcTestcaseRunIn(BaseSchema):
    """PC用例执行入参"""
    id: int = Field(..., description="用例ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="覆盖执行设备标识")
