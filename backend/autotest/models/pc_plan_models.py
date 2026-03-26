# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, JSON, Text, select
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.api_models import ProjectInfo
from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_plan import PcPlanQuery


class PcPlan(Base):
    """PC测试计划表"""
    __tablename__ = 'pc_plan'

    name = mapped_column(String(255), nullable=False, comment='计划名称', index=True)
    project_id = mapped_column(Integer, comment='项目ID')
    case_ids = mapped_column(JSON, comment='关联用例ID列表(JSON数组)')
    pc_device_identity = mapped_column(String(255), comment='默认执行设备标识')
    remarks = mapped_column(Text, comment='备注')

    @classmethod
    async def get_list(cls, params: PcPlanQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                ProjectInfo.name.label('project_name'),
                u.nickname.label('updated_by_name'),
                User.nickname.label('created_by_name'),
            )
            .where(*q)
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.created_by)
            .order_by(cls.id.desc())
        )
        return await cls.pagination(stmt)
