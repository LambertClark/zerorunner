# -*- coding: utf-8 -*-
"""
PC 素材定时清理任务
"""
from loguru import logger

from celery_worker.base import run_async
from celery_worker.worker import celery


@celery.task(name="celery_worker.tasks.pc_picture.cleanup_unbound_pc_pictures")
def cleanup_unbound_pc_pictures():
    """清理未绑定任何用例/树节点的 PC 图片素材"""
    from autotest.services.pc_autotest.pc_picture_service import PcPictureService
    count = run_async(PcPictureService.cleanup_unbound())
    logger.info(f"PC素材定时清理完成，共清理 {count} 条未绑定素材")
    return count
