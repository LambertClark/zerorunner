# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema
from autotest.schemas.step_data import TStepData, ApiBaseSchema


class PcDeviceQuery(BaseSchema):
    """PC执行设备查询参数"""
    id: typing.Optional[int] = Field(None, description="设备ID")
    name: typing.Optional[str] = Field(None, description="设备名称")
    identity: typing.Optional[str] = Field(None, description="设备标识")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcDeviceIn(BaseSchema):
    """PC执行设备入参"""
    id: typing.Optional[int] = Field(None, description="设备ID")
    name: str = Field(..., description="设备名称")
    identity: str = Field(..., description="设备标识(唯一)")
    ipv4_addresses: typing.Optional[str] = Field(None, description="IP地址列表，逗号分隔")
    port: int = Field(8088, description="Agent端口")
    remarks: typing.Optional[str] = Field(None, description="备注")
    enabled_flag: int = Field(1, description="是否启用")


class PcDeviceId(BaseSchema):
    """设备ID"""
    id: int = Field(..., description="设备ID")


class PcInfoIn(TStepData):
    """PC用例单步骤节点入参"""
    id: typing.Optional[int] = Field(None, description="步骤ID")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    status: typing.Optional[int] = Field(None, description="状态")
    env_id: typing.Optional[int] = Field(None, description="环境ID")
    code_id: typing.Optional[int] = Field(None, description="代码ID")
    code: typing.Optional[str] = Field(None, description="代码")
    priority: typing.Optional[int] = Field(None, description="优先级")
    method: typing.Optional[str] = Field(None, description="请求方法")
    url: typing.Optional[str] = Field(None, description="请求URL")
    tags: typing.Optional[typing.List[str]] = Field(None, description="标签")
    remarks: typing.Optional[str] = Field(None, description="备注")
    headers: typing.Optional[typing.List[ApiBaseSchema]] = Field(None, description="请求头")
    children_steps: typing.List["PcInfoIn"] = Field([], description="子步骤")
    children: typing.List["PcInfoIn"] = Field([], description="子节点（兼容树形结构）")
    case_template_id: typing.Optional[int] = Field(None, description="模板用例ID")


PcInfoIn.update_forward_refs()
