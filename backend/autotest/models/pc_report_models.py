# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, Text, BigInteger, Boolean, select, text
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_report_schemas import PcReportQuery, PcReportDetailQuery


class PcReport(Base):
    """PC用例执行报告主表"""
    __tablename__ = 'pc_reports'

    report_name = mapped_column(String(255), comment='报告名称', index=True)
    case_id = mapped_column(BigInteger, comment='关联用例ID')
    case_name = mapped_column(String(255), comment='用例名称')
    project_id = mapped_column(Integer, comment='项目ID')
    status = mapped_column(Integer, default=2, comment='状态 0失败 1成功 2执行中')
    success = mapped_column(Boolean, default=None, comment='是否成功')
    duration = mapped_column(Integer, default=0, comment='总耗时(ms)')
    detail_table = mapped_column(String(64), comment='步骤明细分表名')
    executor_id = mapped_column(BigInteger, comment='执行人ID')
    device_identity = mapped_column(String(255), comment='执行设备标识')

    @classmethod
    async def get_list(cls, params: PcReportQuery):
        q = [cls.enabled_flag == 1]
        if params.case_id:
            q.append(cls.case_id == params.case_id)
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


def get_pc_report_detail_table_name(report_id: int) -> str:
    """根据 report_id 计算分表名（按 id % 10 散列）"""
    return f"pc_report_detail_{report_id % 10}"


class PcReportDetailBase(Base):
    """PC报告步骤明细基类（不直接映射，子类动态绑定表名）"""
    __abstract__ = True

    report_id = mapped_column(BigInteger, comment='报告ID', index=True)
    case_id = mapped_column(BigInteger, comment='用例ID')
    step_id = mapped_column(BigInteger, comment='步骤ID')
    report_name = mapped_column(String(255), comment='报告名称')
    operation_state = mapped_column(String(64), comment='操作状态')
    operation_type = mapped_column(String(64), comment='操作类型')
    expect_value = mapped_column(Text, comment='预期值')
    actual_value = mapped_column(Text, comment='实际值')
    state_image = mapped_column(Text, comment='状态截图路径')
    exception_message = mapped_column(Text, comment='异常信息')
    error_type = mapped_column(String(128), comment='错误类型')
    operation_context = mapped_column(Text, comment='操作上下文(JSON)')
    success = mapped_column(Boolean, default=None, comment='是否成功')
    original_image_path = mapped_column(Text, comment='原始截图路径')
    duration = mapped_column(Integer, default=0, comment='耗时(ms)')
    is_template = mapped_column(Boolean, default=False, comment='是否模板步骤')


# 预生成 10 张分表模型（pc_report_detail_0 ~ pc_report_detail_9）
_PC_REPORT_DETAIL_MODELS: typing.Dict[str, typing.Type[PcReportDetailBase]] = {}

for _i in range(10):
    _table_name = f"pc_report_detail_{_i}"
    _model = type(
        f"PcReportDetail{_i}",
        (PcReportDetailBase,),
        {"__tablename__": _table_name},
    )
    _PC_REPORT_DETAIL_MODELS[_table_name] = _model  # type: ignore


def get_pc_report_detail_model(report_id: int) -> typing.Type[PcReportDetailBase]:
    """根据 report_id 获取对应分表 Model 类"""
    table_name = get_pc_report_detail_table_name(report_id)
    return _PC_REPORT_DETAIL_MODELS[table_name]
