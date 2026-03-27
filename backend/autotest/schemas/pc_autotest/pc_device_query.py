# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcDeviceQuery(BaseSchema):
    """PC设备状态/指标查询"""
    id: typing.Optional[int] = Field(None, description="设备ID")
    identity: typing.Optional[str] = Field(None, description="设备唯一标识")
    ip: typing.Optional[str] = Field(None, description="设备IP地址")
    recent_minutes: typing.Optional[int] = Field(None, ge=1, description="最近N分钟内上报的数据")
    collection_time: typing.Optional[str] = Field(None, description="采集时间")
    os_name: typing.Optional[str] = Field(None, description="操作系统名称")
    os_version: typing.Optional[str] = Field(None, description="操作系统版本")
    os_arch: typing.Optional[str] = Field(None, description="系统架构")
    user_name: typing.Optional[str] = Field(None, description="登录用户名")
    ipv4_addresses: typing.Optional[str] = Field(None, description="IPv4地址列表，逗号分隔")
    total_disk_gb: typing.Optional[float] = Field(None, description="磁盘总量(GB)")
    used_disk_gb: typing.Optional[float] = Field(None, description="磁盘已用(GB)")
    partitions: typing.Optional[str] = Field(None, description="磁盘分区信息")
    cpu_vendor: typing.Optional[str] = Field(None, description="CPU厂商")
    cpu_model: typing.Optional[str] = Field(None, description="CPU型号")
    physical_cores: typing.Optional[int] = Field(None, description="CPU物理核心数")
    logical_cores: typing.Optional[int] = Field(None, description="CPU逻辑核心数")
    cpu_temperature: typing.Optional[float] = Field(None, description="CPU温度(℃)")
    total_memory_gb: typing.Optional[float] = Field(None, description="内存总量(GB)")
    used_memory_gb: typing.Optional[float] = Field(None, description="内存已用(GB)")
    available_memory_gb: typing.Optional[float] = Field(None, description="内存可用(GB)")
    display_width: typing.Optional[int] = Field(None, description="显示器宽度(px)")
    display_height: typing.Optional[int] = Field(None, description="显示器高度(px)")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")
