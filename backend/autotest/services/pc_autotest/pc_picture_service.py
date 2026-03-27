# -*- coding: utf-8 -*-
import typing

from autotest.exceptions.exceptions import RootNodeNameExistsError
from autotest.models.pc_picture_models import PictureInfo, TagTree
from autotest.schemas.pc_autotest.pc_picture_tag_tree_schemas import PictureTreeIn


class PcPictureService:
    """PC素材服务"""

    @staticmethod
    async def all_menu():
        return await TagTree.get_menu_all()

    @staticmethod
    async def get_tree():
        return await TagTree.convert_to_tree()

    @staticmethod
    async def create_or_update_tree(params: PictureTreeIn):
        exclude_id = params.id if params.id else None
        if not params.parent_id:
            exists = await TagTree.check_root_name_exists(params.name, exclude_id)
            if exists:
                raise RootNodeNameExistsError(params.name)
        res = await TagTree.create_or_update(params.dict())
        node_id = res.get('id')
        parent_id = res.get('parent_id') or 0
        if parent_id:
            parent = await TagTree.get_tree_by_id(parent_id)
            if parent:
                parent_path = parent.get('full_path') or str(parent_id)
            else:
                parent_path = str(parent_id)
            full_path = f'{parent_path}/{node_id}'
        else:
            full_path = str(node_id)
        res['full_path'] = full_path
        await TagTree.create_or_update(res)
        return res

    @staticmethod
    async def create_or_update_picture(params):
        return await PictureInfo.create_or_update(params.dict())

    @staticmethod
    async def get_picture_by_tree_id(tree_id: int):
        return await PictureInfo.get_picture_by_tree_id(tree_id)

    @staticmethod
    async def delete_picture(params):
        return await PictureInfo.delete(params.id)

    @staticmethod
    async def get_picture_by_name(picture_name: str):
        pictures = await PictureInfo.get_picture_by_name(picture_name)
        tree_map: typing.Dict[typing.Optional[int], typing.List] = {}
        for pic in (pictures or []):
            tid = pic.get('tree_id')
            if tid not in tree_map:
                tree_map[tid] = []
            tree_map[tid].append(pic)
        result = []
        for tid, pic_list in tree_map.items():
            tree_name = None
            if tid:
                tree = await TagTree.get_tree_by_id(tid)
                if tree:
                    tree_name = tree.get('name')
            result.append({'tree_name': tree_name, 'picture_data': pic_list})
        return result

    @staticmethod
    async def get_tree_by_ids(tree_ids: typing.List[int]):
        return await TagTree.get_tree_by_ids(tree_ids)

    @staticmethod
    async def get_tree_by_id(id: int):
        return await TagTree.get_tree_by_id(id)

    @staticmethod
    async def deleted_tree(params):
        nodes = await TagTree.full_path_like_id(params)
        id_list = [node.id for node in nodes]
        await PictureInfo.batch_delete_by_tree_id(id_list)
        await TagTree.batch_delete(id_list)

    @staticmethod
    async def get_list(params):
        rows = await PictureInfo.get_list(params.dict())
        return await PcPictureService.fill_tree_path(rows)

    @staticmethod
    async def fill_tree_path(rows):
        if not rows:
            return rows
        row_list = rows.get('rows') if isinstance(rows, dict) else rows
        for row in (row_list or []):
            if isinstance(row, dict):
                if row.get('table_type') == 'tree':
                    row['tree_path'] = row.get('tree_full_path')
                else:
                    row['tree_path'] = None
        return rows

    @staticmethod
    async def build_tree_name_map_by_full_paths(full_paths: typing.List[str]) -> typing.Dict[int, str]:
        """解析 full_path 中所有 id，查树节点，返回 {id: name} 映射"""
        all_ids: typing.Set[int] = set()
        for fp in (full_paths or []):
            if fp:
                for part in fp.split('/'):
                    try:
                        all_ids.add(int(part))
                    except (ValueError, TypeError):
                        pass
        if not all_ids:
            return {}
        nodes = await TagTree.get_tree_by_ids(list(all_ids))
        return {node['id']: node['name'] for node in (nodes or [])}

    @staticmethod
    def format_tree_path(full_path: str, id_to_name: typing.Dict[int, str]) -> str:
        """返回以 / 拼接的树路径"""
        if not full_path:
            return ''
        parts = []
        for part in full_path.split('/'):
            try:
                node_id = int(part)
                parts.append(id_to_name.get(node_id, part))
            except (ValueError, TypeError):
                parts.append(part)
        return '/'.join(parts)

    @staticmethod
    async def get_unbound_picture_cleanup_candidates(expire_days: int = 7) -> typing.List[dict]:
        """筛选 table_type is None, table_id is None, tree_id is None, creation_date <= cutoff_time"""
        return await PictureInfo.get_unbound_pictures(expire_days)

    @staticmethod
    async def cleanup_unbound_pictures(expire_days: int = 7, dry_run: bool = True, hard_delete: bool = True) -> dict:
        candidates = await PcPictureService.get_unbound_picture_cleanup_candidates(expire_days)
        candidate_ids = [c['id'] for c in (candidates or [])]
        result = {
            'expire_days': expire_days,
            'dry_run': dry_run,
            'hard_delete': hard_delete,
            'candidate_count': len(candidate_ids),
            'candidate_ids': candidate_ids,
            'deleted_count': 0,
        }
        if dry_run or not candidate_ids:
            return result
        deleted_count = 0
        for picture_id in candidate_ids:
            await PictureInfo.delete(picture_id, _hard=hard_delete)
            deleted_count += 1
        result['deleted_count'] = deleted_count
        return result
