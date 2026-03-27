# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, JSON, Text, DateTime, Boolean, BigInteger, select, update, insert, func
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_plan import PcPlanQuery


class PcPlan(Base):
    """PC测试计划表"""
    __tablename__ = 'pc_plan'

    title = mapped_column(String(255), nullable=False, comment='计划标题', index=True)
    cases = mapped_column(JSON, comment='关联用例列表(JSON)')
    desc = mapped_column(Text, comment='描述')

    @classmethod
    async def get_list(cls, params: PcPlanQuery, order_by: str = "asc"):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.title:
            q.append(cls.title.like(f'%{params.title}%'))
        if params.desc:
            q.append(cls.desc.like(f'%{params.desc}%'))
        if params.enabled_flag is not None:
            q.append(cls.enabled_flag == params.enabled_flag)
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.updated_by:
            q.append(cls.updated_by == params.updated_by)

        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                u.nickname.label('updated_by_name'),
                User.nickname.label('created_by_name'),
            )
            .where(*q)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.created_by)
            .order_by(cls.id.desc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def get_plan_by_id(cls, id: int) -> typing.Optional[typing.Dict]:
        q = [cls.enabled_flag == 1, cls.id == id]
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                u.nickname.label('updated_by_name'),
                User.nickname.label('created_by_name'),
            )
            .where(*q)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.created_by)
        )
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def create_or_update(cls, params: dict) -> dict:
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
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

    @classmethod
    async def delete(cls, id: int) -> int:
        return await cls.logic_delete(id)
