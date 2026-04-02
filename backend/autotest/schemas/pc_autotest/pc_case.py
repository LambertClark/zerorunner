# -*- coding: utf-8 -*-
import typing

from pydantic import Field

from autotest.schemas.base import BaseSchema
from autotest.schemas.pc_autotest.pc_info import PcInfoIn
from autotest.schemas.step_data import TStepData


class PcCaseQuery(BaseSchema):
    """PC用例查询参数"""
    id: typing.Optional[int] = Field(None, description="用例ID")
    title: typing.Optional[str] = Field(None, description="用例标题")
    is_template: typing.Optional[int] = Field(None, description="是否模板")
    priority: typing.Optional[int] = Field(None, description="优先级")
    prioritys: typing.Optional[typing.List[int]] = Field(None, description="优先级列表")
    suite: typing.Optional[str] = Field(None, description="套件")
    module: typing.Optional[str] = Field(None, description="模块")
    step_data: typing.Optional[typing.Any] = Field(None, description="步骤数据")
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
    page: int = Field(1, description="页码")
    pageSize: int = Field(20, description="每页数量")


class PcCaseIn(BaseSchema):
    """PC用例入参"""
    id: typing.Optional[int] = Field(None, description="用例ID")
    is_template: typing.Optional[int] = Field(None, description="是否模板")
    title: typing.Optional[str] = Field(None, description="用例标题")
    priority: typing.Optional[int] = Field(None, description="优先级")
    suite: typing.Optional[str] = Field(None, description="套件")
    module: typing.Optional[str] = Field(None, description="模块")
    step_data: typing.Optional[typing.List[PcInfoIn]] = Field([], description="步骤树")
    desc: typing.Optional[str] = Field(None, description="描述")
    events: typing.Optional[typing.Any] = Field(None, description="事件")
    platforms: typing.Optional[typing.Any] = Field(None, description="平台")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    run_user_id: typing.Optional[int] = Field(None, description="执行用户ID")
    run_user_name: typing.Optional[str] = Field(None, description="执行用户名")
    created_by: typing.Optional[int] = Field(None, description="创建人ID")
    created_by_name: typing.Optional[str] = Field(None, description="创建人名称")
    case_category: typing.Optional[str] = Field(None, description="用例分类")


class PcCaseId(BaseSchema):
    """用例ID"""
    id: int = Field(..., description="用例ID")


class PcRunCaseRequest(BaseSchema):
    """PC用例执行请求"""
    case_id: int = Field(..., description="用例ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="执行设备标识")
    report_name: typing.Optional[str] = Field(None, description="报告名称")


# ---------- 向后兼容别名（现有代码仍可直接导入） ----------

class PcTestcaseQuery(PcCaseQuery):
    """向后兼容：PC用例查询参数"""
    name: typing.Optional[str] = Field(None, description="用例名称（兼容旧字段）")
    pc_device_identity: typing.Optional[str] = Field(None, description="绑定设备标识")


class PcTestcaseIn(BaseSchema):
    """向后兼容：PC用例入参"""
    id: typing.Optional[int] = Field(None, description="用例ID")
    name: typing.Optional[str] = Field(None, description="用例名称")
    project_id: typing.Optional[int] = Field(None, description="项目ID")
    module_id: typing.Optional[int] = Field(None, description="模块ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="绑定执行设备标识")
    step_data: typing.Optional[typing.List[TStepData]] = Field([], description="步骤树")
    remarks: typing.Optional[str] = Field(None, description="备注")
    tags: typing.Optional[typing.List[str]] = Field(None, description="标签")
    enabled_flag: int = Field(1, description="是否启用")


class PcTestcaseId(PcCaseId):
    """向后兼容：用例ID"""
    pass


class PcTestcaseRunIn(BaseSchema):
    """向后兼容：PC用例执行入参"""
    id: int = Field(..., description="用例ID")
    pc_device_identity: typing.Optional[str] = Field(None, description="覆盖执行设备标识")
