# -*- coding: utf-8 -*-
from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_device_models import PcDevice
from autotest.schemas.pc_autotest.pc_info import PcDeviceQuery, PcDeviceIn, PcDeviceId


class PcDeviceService:
    """PC执行设备服务"""

    @staticmethod
    async def list(params: PcDeviceQuery):
        return await PcDevice.get_list(params)

    @staticmethod
    async def save_or_update(params: PcDeviceIn):
        # identity 唯一性校验（新增时）
        if not params.id:
            existing = await PcDevice.get_by_identity(params.identity)
            if existing:
                raise ParameterError(f"设备标识 [{params.identity}] 已存在")
        return await PcDevice.create_or_update(params.dict())

    @staticmethod
    async def deleted(id: int):
        device = await PcDevice.get(id)
        if not device:
            raise ParameterError("设备不存在")
        return await PcDevice.delete(id)

    @staticmethod
    async def get_by_id(params: PcDeviceId):
        device = await PcDevice.get(params.id, to_dict=True)
        if not device:
            raise ParameterError("设备不存在")
        return device
