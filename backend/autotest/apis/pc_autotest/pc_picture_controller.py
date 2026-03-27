# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List, Dict

from fastapi import APIRouter
from loguru import logger

from autotest.exceptions.exceptions import RootNodeNameExistsError
from autotest.schemas.pc_autotest.pc_picture_tag_tree_schemas import (
    PictureTreeIn, PictureIn, PictureDeleteIn, PictureId, PcPictureQuery,
)
from autotest.services.pc_autotest.pc_picture_service import PcPictureService
from autotest.utils.response.codes import CodeEnum
from autotest.utils.response.http_response import partner_success, resp_500, resp_400

router = APIRouter()


@router.post('/allMenu', description="获取素材全部菜单")
async def all_menu():
    data = await PcPictureService.all_menu()
    return partner_success(data)


@router.post('/getTree', description="获取素材标签树")
async def get_tree():
    data = await PcPictureService.get_tree()
    return partner_success(data)


@router.post('/saveOrUpdateTree', description="保存/更新素材标签树节点")
async def get_tree(params: PictureTreeIn):
    try:
        data = await PcPictureService.create_or_update_tree(params)
        return partner_success(data)
    except RootNodeNameExistsError as e:
        return partner_success(msg=str(e), code=CodeEnum.ROOT_NODE_NAME_EXISTS.code)
    except Exception as e:
        logger.exception(e)
        return resp_500(data="操作失败")


@router.post('/deletedTree', description="删除素材标签树节点")
async def get_tree(params: PictureId):
    data = await PcPictureService.deleted_tree(params)
    return partner_success(data)


@router.post('/saveOrUpdatePicture', description="保存/更新素材")
async def get_tree(params: PictureIn):
    data = await PcPictureService.create_or_update_picture(params)
    return partner_success(data)


@router.post('/deletePicture', description="删除素材")
async def delete_picture(params: PictureDeleteIn):
    data = await PcPictureService.delete_picture(params)
    return partner_success(data)


@router.post('/list', description="获取素材列表")
async def picture_list(params: PcPictureQuery):
    data = await PcPictureService.get_list(params)
    return partner_success({"rows": data, "rowTotal": len(data) if isinstance(data, list) else 0})


@router.get('/pictureByTreeId', description="按标签树节点获取素材")
async def get_picture_by_tree_id(tree_id: int):
    data = await PcPictureService.get_picture_by_tree_id(tree_id)
    return partner_success(data)


@router.get('/pictureByName', description="按名称获取素材")
async def get_picture_by_name(picture_name: str):
    if not picture_name:
        return partner_success(None)
    data = await PcPictureService.get_picture_by_name(picture_name)
    return partner_success(data)
