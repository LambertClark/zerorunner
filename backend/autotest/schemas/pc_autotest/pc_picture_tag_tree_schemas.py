# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcTagTreeQuery(BaseSchema):
    """素材标签树查询"""
    id: typing.Optional[int] = Field(None, description="节点ID")
    name: typing.Optional[str] = Field(None, description="节点名称")
    parent_id: typing.Optional[int] = Field(None, description="父节点ID")
    project_id: typing.Optional[int] = Field(None, description="项目ID")


class PcTagTreeIn(BaseSchema):
    """素材标签树节点入参"""
    id: typing.Optional[int] = Field(None, description="节点ID")
    name: str = Field(..., description="节点名称")
    parent_id: typing.Optional[int] = Field(0, description="父节点ID，0为根节点")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    remarks: typing.Optional[str] = Field(None, description="备注")


class PcTagTreeId(BaseSchema):
    """节点ID"""
    id: int = Field(..., description="节点ID")


class PcPictureQuery(BaseSchema):
    """素材查询"""
    id: typing.Optional[int] = Field(None, description="素材ID")
    name: typing.Optional[str] = Field(None, description="素材名称")
    tag_id: typing.Optional[int] = Field(None, description="标签节点ID")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcPictureIn(BaseSchema):
    """素材入参"""
    id: typing.Optional[int] = Field(None, description="素材ID")
    name: str = Field(..., description="素材名称")
    url: str = Field(..., description="素材URL")
    tag_id: typing.Optional[int] = Field(None, description="标签节点ID")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    remarks: typing.Optional[str] = Field(None, description="备注")


class PcPictureId(BaseSchema):
    """素材ID"""
    id: int = Field(..., description="素材ID")
