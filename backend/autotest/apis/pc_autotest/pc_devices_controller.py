# -*- coding: utf-8 -*-
from fastapi import APIRouter

from autotest.apis.pc_autotest.pc_testcase_controller import respond_with_data
from autotest.schemas.pc_autotest.pc_device_query import PcDeviceQuery
from autotest.services.pc_autotest.pc_devices_service import PcDevicesService

router = APIRouter()


@router.post('/getPcDevices', description="获取PC执行设备列表")
async def get_devices(params: PcDeviceQuery):
    return await respond_with_data(PcDevicesService.list, params)


@router.post('/updatePcDevice', description="上报/更新PC执行设备")
async def update_device(params: PcDeviceQuery):
    return await respond_with_data(PcDevicesService.save_or_update, params)
