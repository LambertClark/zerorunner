# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, Text, select
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_info import PcDeviceQuery


class PcDevice(Base):
    """PC执行设备表"""
    __tablename__ = 'pc_devices'

    name = mapped_column(String(255), nullable=False, comment='设备名称', index=True)
    identity = mapped_column(String(255), nullable=False, unique=True, comment='设备唯一标识')
    ipv4_addresses = mapped_column(String(1024), comment='IP地址列表，逗号分隔')
    port = mapped_column(Integer, default=8088, comment='Agent端口')
    remarks = mapped_column(Text, comment='备注')

    @classmethod
    async def get_list(cls, params: PcDeviceQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.identity:
            q.append(cls.identity == params.identity)
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
    async def get_by_identity(cls, identity: str) -> typing.Optional["PcDevice"]:
        """按 identity 查询设备"""
        stmt = select(cls).where(cls.identity == identity, cls.enabled_flag == 1)
        result = await cls.execute(stmt)
        return result.scalar()
