# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, JSON, Boolean, Text, select, update, insert, func
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.api_models import ProjectInfo, ModuleInfo
from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_testcase_query import PcCaseQuery


class PcCase(Base):
    """PC自动化用例表"""
    __tablename__ = 'pc_case'

    title = mapped_column(String(255), nullable=False, comment='用例标题', index=True)
    is_template = mapped_column(Integer, default=0, comment='是否模板 0否 1是')
    priority = mapped_column(Integer, default=0, comment='优先级')
    suite = mapped_column(String(255), comment='套件')
    module = mapped_column(String(255), comment='模块名称')
    step_data = mapped_column(JSON, comment='步骤树(JSON)')
    desc = mapped_column(Text, comment='描述')
    events = mapped_column(JSON, comment='事件')
    platforms = mapped_column(JSON, comment='平台')
    project_id = mapped_column(Integer, comment='项目ID')
    module_id = mapped_column(Integer, comment='模块ID')

    @classmethod
    async def get_list(cls, params: PcCaseQuery, order_by: str = "desc"):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.title:
            q.append(cls.title.like(f'%{params.title}%'))
        if params.prioritys:
            q.append(cls.priority.in_(params.prioritys))
        if params.suite:
            q.append(cls.suite == params.suite)
        if params.module:
            q.append(cls.module_id == params.module)
        if params.is_template:
            q.append(cls.is_template == params.is_template)
        else:
            q.append(cls.is_template == 0)
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.created_by_name:
            q.append(User.nickname.like(f'%{params.created_by_name}%'))

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

    @classmethod
    async def create_or_update(cls, params: dict) -> dict:
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        step_data = params.get("step_data")
        print(step_data)
        params = await cls.handle_params(params)
        id = params.get("id", None)
        if id:
            params.pop("created_by", None)
            params.pop("created_by_name", None)
            stmt = update(cls).where(cls.id == id).values(**params)
            await cls.execute(stmt)
        else:
            stmt = insert(cls).values(**params)
            result = await cls.execute(stmt)
            (primary_key,) = result.inserted_primary_key
            params["id"] = primary_key
        return params
