# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_picture_tag_tree_schemas import (
    PcTagTreeQuery, PcTagTreeIn, PcTagTreeId,
    PcPictureQuery, PcPictureIn, PcPictureId,
)
from autotest.services.pc_autotest.pc_picture_service import PcTagTreeService, PcPictureService
from autotest.utils.response.http_response import partner_success

router = APIRouter()

# ---- 标签树 ----

@router.post("/tree/list", description="获取素材标签树列表")
async def get_tag_tree_list(params: PcTagTreeQuery):
    data = await PcTagTreeService.list(params)
    return partner_success(data)


@router.post("/tree/saveOrUpdate", description="保存/更新素材标签树节点")
async def save_or_update_tag(params: PcTagTreeIn):
    data = await PcTagTreeService.save_or_update(params)
    return partner_success(data)


@router.post("/tree/deleted", description="删除素材标签树节点")
async def deleted_tag(params: PcTagTreeId):
    data = await PcTagTreeService.deleted(params.id)
    return partner_success(data)


# ---- 素材 ----

@router.post("/list", description="获取素材列表")
async def get_picture_list(params: PcPictureQuery):
    data = await PcPictureService.list(params)
    return partner_success(data)


@router.post("/getById", description="根据ID获取素材")
async def get_picture_by_id(params: PcPictureId):
    data = await PcPictureService.get_by_id(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存/更新素材信息")
async def save_or_update_picture(params: PcPictureIn):
    data = await PcPictureService.save_or_update(params)
    return partner_success(data)


@router.post("/deleted", description="删除素材")
async def deleted_picture(params: PcPictureId):
    data = await PcPictureService.deleted(params.id)
    return partner_success(data)
