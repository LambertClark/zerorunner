# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, BigInteger, Boolean, Text, JSON, select
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_plan_report import PcPlanReportQuery, PcPlanReportDetailQuery


class PcPlanReport(Base):
    """PC计划执行报告主表"""
    __tablename__ = 'pc_plan_reports'

    report_name = mapped_column(String(255), comment='报告名称', index=True)
    plan_id = mapped_column(BigInteger, comment='关联计划ID')
    plan_name = mapped_column(String(255), comment='计划名称')
    project_id = mapped_column(Integer, comment='项目ID')
    status = mapped_column(Integer, default=2, comment='状态 0失败 1成功 2执行中')
    success = mapped_column(Boolean, default=None, comment='是否成功')
    duration = mapped_column(Integer, default=0, comment='总耗时(ms)')
    total_count = mapped_column(Integer, default=0, comment='用例总数')
    success_count = mapped_column(Integer, default=0, comment='成功数')
    fail_count = mapped_column(Integer, default=0, comment='失败数')
    executor_id = mapped_column(BigInteger, comment='执行人ID')
    device_identity = mapped_column(String(255), comment='执行设备标识')

    @classmethod
    async def get_list(cls, params: PcPlanReportQuery):
        q = [cls.enabled_flag == 1]
        if params.plan_id:
            q.append(cls.plan_id == params.plan_id)
        if params.report_name:
            q.append(cls.report_name.like(f'%{params.report_name}%'))
        if params.status is not None:
            q.append(cls.status == params.status)
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                u.nickname.label('updated_by_name'),
                User.nickname.label('executor_name'),
            )
            .where(*q)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.executor_id)
            .order_by(cls.id.desc())
        )
        return await cls.pagination(stmt)


class PcPlanReportDetail(Base):
    """PC计划报告子用例明细表"""
    __tablename__ = 'pc_plan_report_detail'

    plan_report_id = mapped_column(BigInteger, comment='计划报告ID', index=True)
    case_id = mapped_column(BigInteger, comment='用例ID')
    case_name = mapped_column(String(255), comment='用例名称')
    report_id = mapped_column(BigInteger, comment='关联单用例报告ID')
    status = mapped_column(Integer, default=2, comment='状态 0失败 1成功 2执行中')
    success = mapped_column(Boolean, default=None, comment='是否成功')
    duration = mapped_column(Integer, default=0, comment='耗时(ms)')

    @classmethod
    async def get_list(cls, params: PcPlanReportDetailQuery):
        q = [cls.enabled_flag == 1, cls.plan_report_id == params.plan_report_id]
        stmt = (
            select(cls.get_table_columns())
            .where(*q)
            .order_by(cls.id.asc())
        )
        return await cls.pagination(stmt)
