# -*- coding: utf-8 -*-
from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_picture_models import PcPictureInfo, PcTagTree, PcPictureBinding
from autotest.schemas.pc_autotest.pc_picture_tag_tree_schemas import (
    PcTagTreeQuery, PcTagTreeIn, PcTagTreeId,
    PcPictureQuery, PcPictureIn, PcPictureId,
)


class PcTagTreeService:
    """素材标签树服务"""

    @staticmethod
    async def list(params: PcTagTreeQuery):
        return await PcTagTree.get_list(params)

    @staticmethod
    async def save_or_update(params: PcTagTreeIn):
        return await PcTagTree.create_or_update(params.dict())

    @staticmethod
    async def deleted(id: int):
        node = await PcTagTree.get(id)
        if not node:
            raise ParameterError("标签节点不存在")
        return await PcTagTree.delete(id)


class PcPictureService:
    """PC素材服务"""

    @staticmethod
    async def list(params: PcPictureQuery):
        return await PcPictureInfo.get_list(params)

    @staticmethod
    async def get_by_id(params: PcPictureId) -> dict:
        pic = await PcPictureInfo.get(params.id, to_dict=True)
        if not pic:
            raise ParameterError("素材不存在")
        return pic

    @staticmethod
    async def save_or_update(params: PcPictureIn) -> dict:
        return await PcPictureInfo.create_or_update(params.dict())

    @staticmethod
    async def deleted(id: int):
        pic = await PcPictureInfo.get(id)
        if not pic:
            raise ParameterError("素材不存在")
        # 清理绑定关系（物理删除绑定行，因为素材已被逻辑删除）
        from sqlalchemy import delete
        stmt = delete(PcPictureBinding).where(PcPictureBinding.picture_id == id)
        await PcPictureBinding.execute(stmt)
        return await PcPictureInfo.delete(id)

    @staticmethod
    async def cleanup_unbound() -> int:
        """清理未绑定任何用例/树的素材（逻辑删除）"""
        unbound_ids = await PcPictureBinding.get_unbound_picture_ids()
        if not unbound_ids:
            return 0
        count = 0
        for pid in unbound_ids:
            await PcPictureInfo.delete(pid)
            count += 1
        return count
