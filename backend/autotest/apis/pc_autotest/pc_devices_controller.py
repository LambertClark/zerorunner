# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.schemas.pc_autotest.pc_info import PcDeviceQuery, PcDeviceIn, PcDeviceId
from autotest.services.pc_autotest.pc_devices_service import PcDeviceService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取PC设备列表")
async def get_device_list(params: PcDeviceQuery):
    data = await PcDeviceService.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存/更新PC设备")
async def save_or_update(params: PcDeviceIn):
    data = await PcDeviceService.save_or_update(params)
    return partner_success(data)


@router.post("/deleted", description="删除PC设备")
async def deleted(params: PcDeviceId):
    data = await PcDeviceService.deleted(params.id)
    return partner_success(data)


@router.post("/getById", description="根据ID获取PC设备")
async def get_by_id(params: PcDeviceId):
    data = await PcDeviceService.get_by_id(params)
    return partner_success(data)
