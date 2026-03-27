# -*- coding: utf-8 -*-
from celery_worker.base import run_async
from celery_worker.worker import celery


@celery.task(name='pc_picture.cleanup_unbound_pictures')
def cleanup_unbound_pictures(expire_days=7, dry_run=False, hard_delete=True, **kwargs):
    from autotest.services.pc_autotest.pc_picture_service import PcPictureService
    return run_async(PcPictureService.cleanup_unbound_pictures(
        expire_days=expire_days,
        dry_run=dry_run,
        hard_delete=hard_delete,
    ))
