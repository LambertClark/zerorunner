# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, Float, Text, select, update, insert, text
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_device_query import PcDeviceQuery

# 历史写法，保留兼容性
# from autotest.schemas.app_autotest.app_autotest import *


class PcDevice(Base):
    """PC执行设备表（设备是拿 identity 来判断唯一性的）"""
    __tablename__ = 'pc_devices'

    identity = mapped_column(String(255), nullable=False, unique=True, comment='设备唯一标识(UUID)')
    ip = mapped_column(String(64), comment='设备IP地址')
    collection_time = mapped_column(String(32), comment='最近采集时间')
    os_name = mapped_column(String(64), comment='操作系统名称')
    os_version = mapped_column(String(128), comment='操作系统版本')
    os_arch = mapped_column(String(32), comment='系统架构')
    user_name = mapped_column(String(128), comment='登录用户名')
    ipv4_addresses = mapped_column(String(1024), comment='IPv4地址列表，逗号分隔')
    total_disk_gb = mapped_column(Float, comment='磁盘总量(GB)')
    used_disk_gb = mapped_column(Float, comment='磁盘已用(GB)')
    partitions = mapped_column(Text, comment='磁盘分区信息(JSON)')
    cpu_vendor = mapped_column(String(128), comment='CPU厂商')
    cpu_model = mapped_column(String(255), comment='CPU型号')
    physical_cores = mapped_column(Integer, comment='CPU物理核心数')
    logical_cores = mapped_column(Integer, comment='CPU逻辑核心数')
    cpu_temperature = mapped_column(Float, comment='CPU温度(℃)')
    total_memory_gb = mapped_column(Float, comment='内存总量(GB)')
    used_memory_gb = mapped_column(Float, comment='内存已用(GB)')
    available_memory_gb = mapped_column(Float, comment='内存可用(GB)')
    display_width = mapped_column(Integer, comment='显示器宽度(px)')
    display_height = mapped_column(Integer, comment='显示器高度(px)')

    @classmethod
    async def get(cls, identity: str, to_dict: bool = False):
        """按 identity 查询设备（不是按自增 id 查）"""
        from autotest.utils.serialize import unwrap_scalars
        if not identity:
            return None
        stmt = select(cls).where(cls.identity == identity, cls.enabled_flag == 1)
        result = await cls.execute(stmt)
        data = result.scalar()
        return data if not to_dict else unwrap_scalars(data)

    @classmethod
    async def create_or_update(cls, params: dict) -> dict:
        """以 identity 判断插入或更新（设备是拿 UUID 来判断的）"""
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        params = await cls.handle_params(params)
        identity = params.get("identity")
        existing = None
        if identity:
            stmt = select(cls).where(cls.identity == identity, cls.enabled_flag == 1)
            result = await cls.execute(stmt)
            existing = result.scalar()
        if existing:
            stmt = update(cls).where(cls.identity == identity).values(**params)
            await cls.execute(stmt)
            params["id"] = existing.id
        else:
            stmt = insert(cls).values(**params)
            result = await cls.execute(stmt)
            (primary_key,) = result.inserted_primary_key
            params["id"] = primary_key
        return params

    @classmethod
    async def get_list(cls, params: PcDeviceQuery, order_by: str = "asc"):
        q = [cls.enabled_flag == 1]
        if params.identity:
            q.append(cls.identity == params.identity)
        if params.ip:
            q.append(cls.ip.like(f'%{params.ip}%'))
        if params.recent_minutes:
            q.append(
                text(
                    f"STR_TO_DATE(pc_devices.collection_time, '%Y-%m-%d %H:%i:%s') "
                    f">= NOW() - INTERVAL {int(params.recent_minutes)} MINUTE"
                )
            )
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
            .order_by(cls.collection_time.desc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def get_plan_by_id(cls, id: int) -> typing.Optional[typing.Dict]:
        """按 id 查设备详情"""
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
