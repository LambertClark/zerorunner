# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema


class PcCaseQuery(BaseSchema):
    """PC用例查询参数"""
    id: typing.Optional[int] = Field(None, description="用例ID")
    title: typing.Optional[str] = Field(None, description="用例标题")
    priority: typing.Optional[int] = Field(None, description="优先级")
    prioritys: typing.Optional[typing.List[int]] = Field(None, description="优先级列表")
    suite: typing.Optional[str] = Field(None, description="套件")
    module: typing.Optional[str] = Field(None, description="模块")
    steps: typing.Optional[typing.Any] = Field(None, description="步骤数据")
    desc: typing.Optional[str] = Field(None, description="描述")
    tags: typing.Optional[typing.List[str]] = Field(None, description="标签")
    events: typing.Optional[typing.Any] = Field(None, description="事件")
    platforms: typing.Optional[typing.Any] = Field(None, description="平台")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    run_user_id: typing.Optional[int] = Field(None, description="执行用户ID")
    run_user_name: typing.Optional[str] = Field(None, description="执行用户名")
    created_by: typing.Optional[int] = Field(None, description="创建人ID")
    created_by_name: typing.Optional[str] = Field(None, description="创建人名称")
    case_category: typing.Optional[str] = Field(None, description="用例分类")
    is_template: typing.Optional[int] = Field(None, description="是否模板")
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")
