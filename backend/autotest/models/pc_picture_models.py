# -*- coding: utf-8 -*-
import typing
from datetime import datetime, timedelta

from sqlalchemy import String, BigInteger, Text, select, update, insert, delete, func, or_, and_
from sqlalchemy.orm import mapped_column

from autotest.models.base import Base


class PictureInfo(Base):
    """PC素材信息表"""
    __tablename__ = 'pc_picture_info'

    tree_id = mapped_column(BigInteger, comment='所属标签树节点ID', index=True)
    name = mapped_column(String(255), nullable=False, comment='素材名称', index=True)
    image_url = mapped_column(Text, comment='素材URL')
    table_type = mapped_column(String(16), comment='绑定类型：tree/case')
    table_id = mapped_column(BigInteger, comment='绑定对象id')

    @classmethod
    async def create_or_update(cls, params: dict) -> dict:
        # 兼容旧版 url 字段名
        if 'url' in params and 'image_url' not in params:
            params = dict(params)
            params['image_url'] = params.pop('url')
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        params = await cls.handle_params(params)
        id_ = params.get('id', None)
        if id_:
            params.pop('created_by', None)
            stmt = update(cls).where(cls.id == id_).values(**params)
            await cls.execute(stmt)
        else:
            stmt = insert(cls).values(**params)
            result = await cls.execute(stmt)
            (primary_key,) = result.inserted_primary_key
            params['id'] = primary_key
        return params

    @classmethod
    async def get_picture_by_tree_id(cls, tree_id: int) -> typing.List[dict]:
        """兼容 table_type == 'tree' 和 table_type is None and tree_id is not None"""
        q = [
            cls.enabled_flag == 1,
            cls.tree_id == tree_id,
            or_(
                cls.table_type == 'tree',
                and_(cls.table_type.is_(None), cls.tree_id.isnot(None)),
            ),
        ]
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def delete_picture(cls, params: dict):
        id_ = params.get('id') if isinstance(params, dict) else getattr(params, 'id', None)
        return await cls.delete(id_)

    @classmethod
    async def get_picture_by_name(cls, picture_name: str) -> typing.List[dict]:
        """兼容 table_type == 'tree' 和 table_type is None and tree_id is not None"""
        q = [
            cls.enabled_flag == 1,
            cls.name.like(f'%{picture_name}%'),
            or_(
                cls.table_type == 'tree',
                and_(cls.table_type.is_(None), cls.tree_id.isnot(None)),
            ),
        ]
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.desc())
        return await cls.get_result(stmt)

    @classmethod
    async def batch_delete_by_tree_id(cls, ids: typing.List[int], _hard: bool = False) -> int:
        if not ids:
            return 0
        if _hard:
            stmt = delete(cls).where(cls.tree_id.in_(ids))
            result = await cls.execute(stmt)
            return result.rowcount
        stmt = update(cls).where(cls.tree_id.in_(ids), cls.enabled_flag == 1).values(enabled_flag=0)
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def get_list(cls, params: dict) -> dict:
        from autotest.models.pc_testcase_models import PcCase
        q = [cls.enabled_flag == 1]
        name = params.get('name')
        id_ = params.get('id')
        if name:
            q.append(cls.name.like(f'%{name}%'))
        if id_:
            q.append(cls.id == id_)
        stmt = (
            select(
                cls.get_table_columns(),
                PcCase.title.label('case_title'),
                TagTree.full_path.label('tree_full_path'),
            )
            .where(*q)
            .outerjoin(PcCase, and_(PcCase.id == cls.table_id, cls.table_type == 'case'))
            .outerjoin(TagTree, TagTree.id == func.coalesce(cls.table_id, cls.tree_id))
            .order_by(cls.id.desc())
        )
        return await cls.pagination(stmt)

    @classmethod
    async def clear_case_bindings(cls, case_id: int) -> int:
        """把当前 case 的绑定置空：table_type = None, table_id = None"""
        stmt = (
            update(cls)
            .where(cls.table_type == 'case', cls.table_id == case_id, cls.enabled_flag == 1)
            .values(table_type=None, table_id=None)
        )
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def bind_case_by_image_urls(cls, image_urls: typing.List[str], case_id: int) -> int:
        """只绑定 enabled_flag == 1, table_type is None, table_id is None"""
        if not image_urls:
            return 0
        stmt = (
            update(cls)
            .where(
                cls.image_url.in_(image_urls),
                cls.enabled_flag == 1,
                cls.table_type.is_(None),
                cls.table_id.is_(None),
            )
            .values(table_type='case', table_id=case_id)
        )
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def get_unbound_pictures(cls, expire_days: int) -> typing.List[dict]:
        """筛选 table_type is None, table_id is None, tree_id is None, creation_date <= cutoff_time"""
        cutoff_time = datetime.now() - timedelta(days=expire_days)
        q = [
            cls.enabled_flag == 1,
            cls.table_type.is_(None),
            cls.table_id.is_(None),
            cls.tree_id.is_(None),
            cls.creation_date <= cutoff_time,
        ]
        stmt = select(cls.get_table_columns()).where(*q).order_by(cls.id.desc())
        return await cls.get_result(stmt)


class TagTree(Base):
    """PC素材标签树表"""
    __tablename__ = 'pc_picture_tag_tree'

    parent_id = mapped_column(BigInteger, default=0, comment='父节点ID，0为根')
    full_path = mapped_column(String(1024), comment='完整路径（id链）')
    name = mapped_column(String(255), nullable=False, comment='节点名称', index=True)

    @classmethod
    async def get_menu_all(cls) -> typing.List[dict]:
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.id.asc())
        return await cls.get_result(stmt)

    @classmethod
    async def convert_to_tree(cls) -> typing.List[dict]:
        """构造含 full_path 名称链的树形结构"""
        all_nodes = await cls.get_menu_all()
        id_to_node = {node['id']: node for node in all_nodes}

        def build_full_path_name(node_id: int) -> str:
            parts = []
            current_id = node_id
            visited = set()
            while current_id and current_id not in visited:
                visited.add(current_id)
                node = id_to_node.get(current_id)
                if not node:
                    break
                parts.append(node['name'])
                current_id = node.get('parent_id') or 0
            return '/'.join(reversed(parts))

        def build_children(parent_id: int) -> typing.List[dict]:
            children = []
            for node in all_nodes:
                if node.get('parent_id') == parent_id:
                    node_id = node['id']
                    full_path_name = build_full_path_name(node_id)
                    children.append({
                        'parent_id': node.get('parent_id'),
                        'id': node_id,
                        'label': node['name'],
                        'name': node['name'],
                        'full_path': full_path_name,
                        'children': build_children(node_id),
                    })
            return children

        return build_children(0)

    @classmethod
    async def create_or_update(cls, params: dict) -> dict:
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        params = await cls.handle_params(params)
        id_ = params.get('id', None)
        if id_:
            params.pop('created_by', None)
            stmt = update(cls).where(cls.id == id_).values(**params)
            await cls.execute(stmt)
        else:
            stmt = insert(cls).values(**params)
            result = await cls.execute(stmt)
            (primary_key,) = result.inserted_primary_key
            params['id'] = primary_key
        return params

    @classmethod
    async def get_tree_by_ids(cls, tree_ids: typing.List[int]) -> typing.List[dict]:
        if not tree_ids:
            return []
        stmt = select(cls.get_table_columns()).where(cls.id.in_(tree_ids), cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_tree_by_id(cls, id: int) -> typing.Optional[dict]:
        stmt = select(cls.get_table_columns()).where(cls.id == id, cls.enabled_flag == 1)
        return await cls.get_result(stmt, first=True)

    @classmethod
    async def deleted(cls, params) -> int:
        id_ = params.get('id') if isinstance(params, dict) else getattr(params, 'id', None)
        return await cls.delete(id_)

    @classmethod
    async def full_path_like_id(cls, params) -> typing.List:
        """查找以当前 id 为根的所有子树节点（包含自身）"""
        id_ = params.get('id') if isinstance(params, dict) else getattr(params, 'id', None)
        if not id_:
            return []
        node = await cls.get_tree_by_id(id_)
        if not node:
            return []
        node_full_path = node.get('full_path') or str(id_)
        q = [
            cls.enabled_flag == 1,
            or_(
                cls.id == id_,
                cls.full_path.like(f'{node_full_path}/%'),
            ),
        ]
        stmt = select(cls).where(*q)
        result = await cls.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def check_root_name_exists(cls, name: str, exclude_id: typing.Optional[int] = None) -> bool:
        """检查根节点（parent_id == 0）名称是否已存在"""
        q = [cls.enabled_flag == 1, cls.parent_id == 0, cls.name == name]
        if exclude_id:
            q.append(cls.id != exclude_id)
        stmt = select(func.count(cls.id)).where(*q)
        result = await cls.execute(stmt)
        count = result.scalar()
        return (count or 0) > 0

    @classmethod
    async def batch_delete(cls, ids: typing.List[int]) -> int:
        if not ids:
            return 0
        stmt = update(cls).where(cls.id.in_(ids), cls.enabled_flag == 1).values(enabled_flag=0)
        result = await cls.execute(stmt)
        return result.rowcount


# 向后兼容别名
PcPictureInfo = PictureInfo
PcPictureBinding = PictureInfo
PcTagTree = TagTree
