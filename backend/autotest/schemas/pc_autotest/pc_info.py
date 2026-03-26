# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


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
