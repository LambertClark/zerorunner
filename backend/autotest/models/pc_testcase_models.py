# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, JSON, select, func, Text
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.api_models import ProjectInfo, ModuleInfo
from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_case import PcTestcaseQuery


class PcCase(Base):
    """PC自动化用例表"""
    __tablename__ = 'pc_case'

    name = mapped_column(String(255), nullable=False, comment='用例名称', index=True)
    project_id = mapped_column(Integer, comment='项目ID')
    module_id = mapped_column(Integer, comment='模块ID')
    pc_device_identity = mapped_column(String(255), comment='绑定执行设备标识')
    step_data = mapped_column(JSON, comment='步骤树(JSON)')
    tags = mapped_column(JSON, comment='标签')
    remarks = mapped_column(Text, comment='备注')

    @classmethod
    async def get_list(cls, params: PcTestcaseQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.pc_device_identity:
            q.append(cls.pc_device_identity == params.pc_device_identity)
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                ProjectInfo.name.label('project_name'),
                ModuleInfo.name.label('module_name'),
                u.nickname.label('updated_by_name'),
                User.nickname.label('created_by_name'),
            )
            .where(*q)
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id)
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.created_by)
            .order_by(cls.id.desc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def get_case_by_id(cls, id: int) -> typing.Optional[typing.Dict]:
        q = [cls.enabled_flag == 1, cls.id == id]
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                ProjectInfo.name.label('project_name'),
                ModuleInfo.name.label('module_name'),
                u.nickname.label('updated_by_name'),
                User.nickname.label('created_by_name'),
            )
            .where(*q)
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id)
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.created_by)
        )
        return await cls.get_result(stmt, first=True)
