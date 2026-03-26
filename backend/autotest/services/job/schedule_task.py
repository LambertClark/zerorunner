# -*- coding: utf-8 -*-
"""
定时任务入口 —— 由 Celery Beat 调用
新增：PC 未绑定素材清理任务
"""
from loguru import logger


async def cleanup_unbound_pc_pictures():
    """异步版：清理未绑定 PC 素材（可在非 Celery 环境中直接 await 调用）"""
    from autotest.services.pc_autotest.pc_picture_service import PcPictureService
    count = await PcPictureService.cleanup_unbound()
    logger.info(f"cleanup_unbound_pc_pictures: 清理 {count} 条")
    return count
