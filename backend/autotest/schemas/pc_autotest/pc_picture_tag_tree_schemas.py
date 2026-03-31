# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PictureId(BaseSchema):
    """图片ID"""
    id: int = Field(..., description="图片ID")


class PictureTreeIn(BaseSchema):
    """图片标签树节点入参"""
    id: typing.Optional[int] = Field(None, description="节点ID")
    parent_id: typing.Optional[int] = Field(None, description="父节点ID")
    full_path: typing.Optional[str] = Field(None, description="完整路径")
    name: typing.Optional[str] = Field(None, description="节点名称")


class PictureIn(BaseSchema):
    """图片入参"""
    id: typing.Optional[int] = Field(None, description="图片ID")
    tree_id: typing.Optional[int] = Field(None, description="所属标签树节点ID")
    name: typing.Optional[str] = Field(None, description="图片名称")
    image_url: typing.Optional[str] = Field(None, description="图片URL")
    table_type: typing.Optional[str] = Field(None, description="关联表类型")
    table_id: typing.Optional[int] = Field(None, description="关联表记录ID")


class PictureDeleteIn(BaseSchema):
    """图片删除入参"""
    id: int = Field(..., description="图片ID")


class PcPictureQuery(BaseSchema):
    """素材查询"""
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")
    name: typing.Optional[str] = Field(None, description="素材名称")
    id: typing.Optional[int] = Field(None, description="素材ID")


# ---------- 向后兼容别名（models / service / controller 使用旧名称）----------

class PcTagTreeQuery(BaseSchema):
    """素材标签树查询（兼容旧名）"""
    id: typing.Optional[int] = Field(None, description="节点ID")
    name: typing.Optional[str] = Field(None, description="节点名称")
    parent_id: typing.Optional[int] = Field(None, description="父节点ID")
    project_id: typing.Optional[int] = Field(None, description="项目ID")


class PcTagTreeIn(BaseSchema):
    """素材标签树节点入参（兼容旧名）"""
    id: typing.Optional[int] = Field(None, description="节点ID")
    name: str = Field(..., description="节点名称")
    parent_id: typing.Optional[int] = Field(0, description="父节点ID，0为根节点")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    remarks: typing.Optional[str] = Field(None, description="备注")


class PcTagTreeId(BaseSchema):
    """节点ID（兼容旧名）"""
    id: int = Field(..., description="节点ID")


class PcPictureIn(BaseSchema):
    """素材入参（兼容旧名）"""
    id: typing.Optional[int] = Field(None, description="素材ID")
    name: str = Field(..., description="素材名称")
    url: str = Field(..., description="素材URL")
    tag_id: typing.Optional[int] = Field(None, description="标签节点ID")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    remarks: typing.Optional[str] = Field(None, description="备注")


class PcPictureId(BaseSchema):
    """素材ID（兼容旧名）"""
    id: int = Field(..., description="素材ID")


class PictureByTreeIdIn(BaseSchema):
    """按树节点ID查询素材入参"""
    tree_id: int = Field(..., description="树节点ID")


class PictureByNameIn(BaseSchema):
    """按名称查询素材入参"""
    picture_name: str = Field(..., description="素材名称")
