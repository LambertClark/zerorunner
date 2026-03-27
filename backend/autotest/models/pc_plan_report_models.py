# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, BigInteger, Boolean, Text, select, update, insert
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_plan_report import PcPlanReportQuery, PcPlanReportDetailQuery


class PcPlanReports(Base):
    """PC计划执行报告主表"""
    __tablename__ = 'pc_plan_reports'

    name = mapped_column(String(255), comment='报告名称', index=True)
    project_id = mapped_column(Integer, comment='项目ID')
    module_id = mapped_column(Integer, comment='模块ID')
    success = mapped_column(Boolean, default=None, comment='是否成功')
    status = mapped_column(String(32), default='EXECUTE', comment='状态')
    duration = mapped_column(Integer, default=0, comment='总耗时(ms)')
    case_id = mapped_column(BigInteger, comment='关联用例ID')
    remarks = mapped_column(Text, comment='备注')
    start_time = mapped_column(String(32), comment='开始时间')
    run_count = mapped_column(Integer, default=0, comment='运行步骤总数')
    run_success_count = mapped_column(Integer, default=0, comment='成功步骤数')
    run_fail_count = mapped_column(Integer, default=0, comment='失败步骤数')
    run_skip_count = mapped_column(Integer, default=0, comment='跳过步骤数')
    run_err_count = mapped_column(Integer, default=0, comment='错误步骤数')
    run_log = mapped_column(Text, comment='运行日志')
    env_id = mapped_column(Integer, comment='环境ID')
    exec_user_id = mapped_column(BigInteger, comment='执行用户ID')
    exec_user_name = mapped_column(String(128), comment='执行用户名')
    run_mode = mapped_column(String(32), comment='运行模式')

    @classmethod
    async def get_list(cls, params: PcPlanReportQuery, order_by: str = "desc"):
        try:
            q = [cls.enabled_flag == 1]
            if params.id:
                q.append(cls.id == params.id)
            if params.name:
                q.append(cls.name.like(f'%{params.name}%'))
            if params.project_id:
                q.append(cls.project_id == params.project_id)
            if params.module_id:
                q.append(cls.module_id == params.module_id)
            if params.status is not None:
                q.append(cls.status == params.status)
            if params.success is not None:
                q.append(cls.success == params.success)
            if params.exec_user_name:
                q.append(cls.exec_user_name.like(f'%{params.exec_user_name}%'))
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
        except ProgrammingError as e:
            err_msg = str(e).lower()
            if "doesn't exist" in err_msg or "no such table" in err_msg:
                # 表不存在时动态建表后重新查询
                from autotest.db.session import provide_async_session
                async with provide_async_session() as session:
                    await session.execute(
                        __import__("sqlalchemy", fromlist=["text"]).text(
                            f"CREATE TABLE IF NOT EXISTS `{cls.__tablename__}` LIKE `{cls.__tablename__}`"
                        )
                    )
                stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.id.desc())
                return await cls.pagination(stmt)
            raise

    @classmethod
    async def get_report_by_id(cls, id: int) -> typing.Optional[typing.Dict]:
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


class PcPlanReportDetailBase(Base):
    """PC计划报告步骤明细基类（不直接映射，子类动态绑定表名）"""
    __abstract__ = True

    name = mapped_column(String(255), comment='步骤名称', index=True)
    index = mapped_column(Integer, default=0, comment='步骤序号')
    variables = mapped_column(Text, comment='变量(JSON)')
    data = mapped_column(Text, comment='请求数据')
    action = mapped_column(String(128), comment='动作')
    location_method = mapped_column(String(64), comment='定位方法')
    location_value = mapped_column(Text, comment='定位值')
    report_id = mapped_column(BigInteger, comment='报告ID', index=True)
    success = mapped_column(Boolean, default=None, comment='是否成功')
    status = mapped_column(String(32), comment='状态')
    cases = mapped_column(Text, comment='关联用例(JSON)')
    remarks = mapped_column(Text, comment='备注')
    start_time = mapped_column(String(32), comment='开始时间')
    duration = mapped_column(Integer, default=0, comment='耗时(ms)')
    setup_hook_results = mapped_column(Text, comment='前置hook结果(JSON)')
    teardown_hook_results = mapped_column(Text, comment='后置hook结果(JSON)')
    validator_results = mapped_column(Text, comment='校验结果(JSON)')
    screenshot_file_id = mapped_column(BigInteger, comment='截图文件ID')
    log = mapped_column(Text, comment='执行日志')
    message = mapped_column(Text, comment='错误信息')

    @classmethod
    async def get_list(cls, params: PcPlanReportDetailQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.status is not None:
            q.append(cls.status == params.status)
        if params.success is not None:
            q.append(cls.success == params.success)
        stmt = (
            select(cls.get_table_columns())
            .where(*q)
            .order_by(cls.id.asc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def get_details(cls, params: PcPlanReportDetailQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        stmt = (
            select(cls.get_table_columns())
            .where(*q)
            .order_by(cls.id.asc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def statistics(cls, params: PcPlanReportDetailQuery):
        from sqlalchemy import func
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]
        stmt = select(
            func.count(cls.id).label("total"),
            func.sum(cls.duration).label("total_duration"),
        ).where(*q)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def create_or_update(cls, params: dict) -> dict:
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        params = await cls.handle_params(params)
        id = params.get("id", None)
        if id:
            stmt = update(cls).where(cls.id == id).values(**params)
            await cls.execute(stmt)
        else:
            stmt = insert(cls).values(**params)
            result = await cls.execute(stmt)
            (primary_key,) = result.inserted_primary_key
            params["id"] = primary_key
        return params


class PcPlanReportDetail:
    """PC计划报告步骤明细动态分表工厂"""
    _mapper: typing.Dict[str, typing.Type[PcPlanReportDetailBase]] = {}

    @classmethod
    def model(cls, id: int) -> typing.Type[PcPlanReportDetailBase]:
        table_index = id % 1
        class_name = f'pc_plan_report_detail_{table_index}'
        if class_name not in cls._mapper:
            model = type(
                class_name,
                (PcPlanReportDetailBase,),
                {'__tablename__': class_name},
            )
            cls._mapper[class_name] = model  # type: ignore
        return cls._mapper[class_name]

    @classmethod
    async def get_list(cls, params: PcPlanReportDetailQuery):
        return await cls.model(params.report_id).get_list(params)

    @classmethod
    async def get_details(cls, params: PcPlanReportDetailQuery):
        return await cls.model(params.report_id).get_details(params)

    @classmethod
    async def statistics(cls, params: PcPlanReportDetailQuery):
        return await cls.model(params.report_id).statistics(params)

    @classmethod
    async def create_or_update(cls, report_id: int, params: dict) -> dict:
        return await cls.model(report_id).create_or_update(params)


# 向后兼容别名（pc_plan_report_service 等使用旧名）
PcPlanReport = PcPlanReports
