# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, BigInteger, Text, Boolean, Float, select, func, delete
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User, FileInfo
from autotest.schemas.pc_autotest.pc_report_schemas import UiReportQuery, UiReportDetailQuery


class UiReportDetailBase(Base):
    """PC报告步骤明细基类（不直接映射，子类动态绑定表名）"""
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
    case_id = mapped_column(BigInteger, comment='用例ID')
    step_id = mapped_column(BigInteger, comment='步骤ID')
    remarks = mapped_column(Text, comment='备注')
    start_time = mapped_column(String(32), comment='开始时间')
    duration = mapped_column(Integer, default=0, comment='耗时(ms)')
    setup_hook_results = mapped_column(Text, comment='前置hook结果(JSON)')
    teardown_hook_results = mapped_column(Text, comment='后置hook结果(JSON)')
    validator_results = mapped_column(Text, comment='校验结果(JSON)')
    screenshot_file_id = mapped_column(BigInteger, comment='截图文件ID')
    log = mapped_column(Text, comment='执行日志')
    message = mapped_column(Text, comment='错误信息')
    original_image_path = mapped_column(Text, comment='原始截图路径')
    state_image = mapped_column(Text, comment='状态截图路径')
    operation_type = mapped_column(String(64), comment='操作类型')
    operation_state = mapped_column(String(64), comment='操作状态')
    error_type = mapped_column(String(128), comment='错误类型')
    is_lase_step = mapped_column(Boolean, default=False, comment='是否最后一步')
    is_template = mapped_column(Boolean, default=False, comment='是否模板步骤')

    @classmethod
    async def get_list(cls, params: UiReportDetailQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.step_type:
            q.append(cls.action == params.step_type)
        if params.parent_step_id is not None:
            q.append(cls.step_id == params.parent_step_id)
        stmt = (
            select(cls.get_table_columns())
            .where(*q)
            .order_by(cls.id.asc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def get_details(cls, params: UiReportDetailQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.status_list:
            q.append(cls.operation_state.in_(params.status_list))
        stmt = (
            select(
                cls.get_table_columns(),
                func.concat('static/', 'files/', FileInfo.name).label("screenshot_url"),
            )
            .where(*q)
            .outerjoin(FileInfo, FileInfo.id == cls.screenshot_file_id)
            .order_by(cls.id.asc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def statistics(cls, params: UiReportDetailQuery):
        q = [cls.enabled_flag == 1, cls.report_id == params.report_id]
        stmt = select(
            func.count(cls.id).label("total"),
            func.sum(cls.duration).label("total_duration"),
        ).where(*q)
        result = await cls.get_result(stmt, first=True)
        return result


class UiReportDetail:
    """PC报告步骤明细动态分表工厂"""
    _mapper: typing.Dict[str, typing.Type[UiReportDetailBase]] = {}

    @classmethod
    def model(cls, id: int) -> typing.Type[UiReportDetailBase]:
        table_index = id % 1
        class_name = f'pc_report_detail_{table_index}'
        if class_name not in cls._mapper:
            model = type(
                class_name,
                (UiReportDetailBase,),
                {'__tablename__': class_name},
            )
            cls._mapper[class_name] = model  # type: ignore
        return cls._mapper[class_name]

    @classmethod
    async def get_list(cls, params: UiReportDetailQuery):
        return await cls.model(params.report_id).get_list(params)

    @classmethod
    async def get_details(cls, params: UiReportDetailQuery):
        return await cls.model(params.report_id).get_details(params)

    @classmethod
    async def statistics(cls, params: UiReportDetailQuery):
        return await cls.model(params.report_id).statistics(params)


class UiReports(Base):
    """PC用例执行报告主表"""
    __tablename__ = 'pc_reports'

    name = mapped_column(String(255), comment='报告名称', index=True)
    start_time = mapped_column(String(32), comment='开始时间')
    duration = mapped_column(Integer, default=0, comment='总耗时(ms)')
    case_id = mapped_column(BigInteger, comment='关联用例ID')
    run_mode = mapped_column(String(32), comment='运行模式')
    success = mapped_column(Boolean, default=None, comment='是否成功')
    status = mapped_column(String(32), default='EXECUTE', comment='状态')
    run_count = mapped_column(Integer, default=0, comment='运行步骤总数')
    run_success_count = mapped_column(Integer, default=0, comment='成功步骤数')
    run_fail_count = mapped_column(Integer, default=0, comment='失败步骤数')
    run_skip_count = mapped_column(Integer, default=0, comment='跳过步骤数')
    run_err_count = mapped_column(Integer, default=0, comment='错误步骤数')
    run_log = mapped_column(Text, comment='运行日志')
    project_id = mapped_column(Integer, comment='项目ID')
    module_id = mapped_column(Integer, comment='模块ID')
    env_id = mapped_column(Integer, comment='环境ID')
    exec_user_id = mapped_column(BigInteger, comment='执行用户ID')
    exec_user_name = mapped_column(String(128), comment='执行用户名')

    @classmethod
    async def get_list(cls, params: UiReportQuery):
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.module_id:
            q.append(cls.module_id == params.module_id)
        if params.exec_user_name:
            q.append(cls.exec_user_name.like(f'%{params.exec_user_name}%'))
        if params.report_type:
            q.append(cls.run_mode == params.report_type)
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))
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
    async def get_project_by_name(cls, project_name: str):
        stmt = select(cls.get_table_columns()).where(cls.name == project_name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def get_report_by_id(cls, report_id: int):
        stmt = select(cls.get_table_columns()).where(cls.id == report_id, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def get_report_by_time(cls, begin_time: str, end_time: str):
        q = [cls.enabled_flag == 1]
        if begin_time:
            q.append(cls.start_time >= begin_time)
        if end_time:
            q.append(cls.start_time <= end_time)
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def statistic_report(cls, start_time=None, end_time=None):
        q = [cls.enabled_flag == 1]
        if start_time:
            q.append(cls.start_time >= start_time)
        if end_time:
            q.append(cls.start_time <= end_time)
        stmt = select(
            func.count(cls.id).label("total"),
            func.sum(cls.run_success_count).label("success_count"),
            func.sum(cls.run_fail_count).label("fail_count"),
        ).where(*q)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def get_statistic_report(cls, start_time=None, end_time=None):
        return await cls.statistic_report(start_time, end_time)

    @classmethod
    async def get_reports_by_case_id(cls, case_id: int) -> typing.List[dict]:
        stmt = (
            select(cls.get_table_columns())
            .where(cls.case_id == case_id, cls.enabled_flag == 1)
            .order_by(cls.id.desc())
        )
        return await cls.get_result(stmt)


# ---------- 向后兼容别名 ----------
# pc_report_controller / pc_report_service 仍使用旧名
PcReport = UiReports


def get_pc_report_detail_model(report_id: int) -> typing.Type[UiReportDetailBase]:
    """根据 report_id 获取对应分表 Model 类（向后兼容）"""
    return UiReportDetail.model(report_id)
