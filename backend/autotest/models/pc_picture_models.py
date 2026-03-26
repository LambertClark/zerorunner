# -*- coding: utf-8 -*-
import typing

from sqlalchemy import String, Integer, BigInteger, Text, select, delete, insert
from sqlalchemy.orm import aliased, mapped_column

from autotest.models.base import Base
from autotest.models.system_models import User
from autotest.schemas.pc_autotest.pc_picture_tag_tree_schemas import (
    PcTagTreeQuery, PcPictureQuery,
)


class PcTagTree(Base):
    """PC素材标签树表"""
    __tablename__ = 'pc_picture_tag_tree'

    name = mapped_column(String(255), nullable=False, comment='节点名称', index=True)
    parent_id = mapped_column(BigInteger, default=0, comment='父节点ID，0为根')
    project_id = mapped_column(Integer, comment='项目ID')
    remarks = mapped_column(String(255), comment='备注')

    @classmethod
    async def get_list(cls, params: PcTagTreeQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        if params.parent_id is not None:
            q.append(cls.parent_id == params.parent_id)
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.asc())
        return await cls.get_result(stmt)


class PcPictureInfo(Base):
    """PC素材信息表"""
    __tablename__ = 'pc_picture_info'

    name = mapped_column(String(255), nullable=False, comment='素材名称', index=True)
    url = mapped_column(Text, nullable=False, comment='素材URL')
    tag_id = mapped_column(BigInteger, comment='标签节点ID')
    project_id = mapped_column(Integer, comment='项目ID')
    remarks = mapped_column(String(255), comment='备注')

    @classmethod
    async def get_list(cls, params: PcPictureQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.tag_id:
            q.append(cls.tag_id == params.tag_id)
        if params.project_id:
            q.append(cls.project_id == params.project_id)
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                PcTagTree.name.label('tag_name'),
                u.nickname.label('updated_by_name'),
                User.nickname.label('created_by_name'),
            )
            .where(*q)
            .outerjoin(PcTagTree, PcTagTree.id == cls.tag_id)
            .outerjoin(u, u.id == cls.updated_by)
            .outerjoin(User, User.id == cls.created_by)
            .order_by(cls.id.desc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def get_by_url(cls, url: str) -> typing.Optional["PcPictureInfo"]:
        stmt = select(cls).where(cls.url == url, cls.enabled_flag == 1)
        result = await cls.execute(stmt)
        return result.scalar()


class PcPictureBinding(Base):
    """PC素材绑定关系表（素材 <-> 用例/树节点）"""
    __tablename__ = 'pc_picture_binding'

    picture_id = mapped_column(BigInteger, nullable=False, comment='素材ID', index=True)
    table_type = mapped_column(String(32), nullable=False, comment='绑定类型 case/tree')
    table_id = mapped_column(BigInteger, nullable=False, comment='绑定对象ID')

    @classmethod
    async def clear_case_bindings(cls, case_id: int) -> int:
        """清空某用例的所有素材绑定"""
        stmt = (
            delete(cls)
            .where(cls.table_type == 'case', cls.table_id == case_id)
        )
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def bind_case_by_image_urls(cls, image_urls: typing.List[str], case_id: int) -> int:
        """
        根据 URL 列表找到对应素材并建立 case 绑定。
        URL 不存在于素材表时跳过（不强制要求素材存在）。
        """
        if not image_urls:
            return 0
        # 查找所有匹配 URL 的素材 ID
        stmt = select(PcPictureInfo.id).where(
            PcPictureInfo.url.in_(image_urls),
            PcPictureInfo.enabled_flag == 1,
        )
        result = await cls.execute(stmt)
        picture_ids = [row[0] for row in result.fetchall()]
        if not picture_ids:
            return 0
        rows = [
            {"picture_id": pid, "table_type": "case", "table_id": case_id}
            for pid in picture_ids
        ]
        rows = await cls.handle_params(rows)
        ins_stmt = insert(cls).values(rows)
        ins_result = await cls.execute(ins_stmt)
        return ins_result.rowcount

    @classmethod
    async def get_unbound_picture_ids(cls) -> typing.List[int]:
        """获取所有未被任何 case/tree 绑定的素材 ID"""
        bound_ids_stmt = select(cls.picture_id).distinct()
        bound_result = await cls.execute(bound_ids_stmt)
        bound_ids = {row[0] for row in bound_result.fetchall()}

        all_stmt = select(PcPictureInfo.id).where(PcPictureInfo.enabled_flag == 1)
        all_result = await cls.execute(all_stmt)
        all_ids = [row[0] for row in all_result.fetchall()]

        return [pid for pid in all_ids if pid not in bound_ids]
