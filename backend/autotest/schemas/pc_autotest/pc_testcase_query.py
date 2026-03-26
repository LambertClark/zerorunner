# -*- coding: utf-8 -*-
# 复用 pc_case.py 中已定义的用例查询 schema，此文件作为向后兼容入口
from autotest.schemas.pc_autotest.pc_case import (
    PcTestcaseQuery, PcTestcaseIn, PcTestcaseId, PcTestcaseRunIn,
)

__all__ = ["PcTestcaseQuery", "PcTestcaseIn", "PcTestcaseId", "PcTestcaseRunIn"]
