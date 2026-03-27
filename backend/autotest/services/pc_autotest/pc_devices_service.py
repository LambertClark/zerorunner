# -*- coding: utf-8 -*-
from autotest.exceptions.exceptions import ParameterError
from autotest.models.pc_device_models import PcDevice
from autotest.models.pc_testcase_models import PcCase  # noqa: 历史依赖，保留
from autotest.schemas.pc_autotest.pc_device_query import PcDeviceQuery
from autotest.schemas.pc_autotest.pc_info import PcDeviceIn, PcDeviceId


class PcDevicesService:
    """PC执行设备服务"""

    @staticmethod
    async def save_or_update(params: PcDeviceQuery):
        return await PcDevice.create_or_update(params.dict())

    @staticmethod
    async def list(params: PcDeviceQuery):
        return await PcDevice.get_list(params)

    @staticmethod
    async def detail(params: PcDeviceQuery):
        return await PcDevice.get_plan_by_id(params.id)

    @staticmethod
    async def delete(id: int):
        return await PcDevice.delete(id)

    @classmethod
    async def get(cls, pc_id):
        return await PcDevice.get(pc_id)
