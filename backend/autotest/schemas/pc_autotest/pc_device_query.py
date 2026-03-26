# -*- coding: utf-8 -*-
# 复用 pc_info.py 中已定义的设备查询 schema，此文件作为向后兼容入口
from autotest.schemas.pc_autotest.pc_info import PcDeviceQuery, PcDeviceIn, PcDeviceId

__all__ = ["PcDeviceQuery", "PcDeviceIn", "PcDeviceId"]
