# -*- coding: utf-8 -*-
from loguru import logger


class ScheduleTaskServer:
    """定时任务服务"""

    @staticmethod
    async def execute_schedule_task(task_name: str, params: dict = None):
        method_map = {
            'cleanup_unbound_pc_pictures': ScheduleTaskServer._cleanup_unbound_pc_pictures,
        }
        handler = method_map.get(task_name)
        if not handler:
            raise ValueError(f'未知任务: {task_name}')
        return await handler(params or {})

    @staticmethod
    async def _cleanup_unbound_pc_pictures(params: dict):
        from celery_worker.tasks.pc_picture import cleanup_unbound_pictures

        def parse_bool(value, default=False):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes')
            return default

        expire_days = int(params.get('expire_days', 7))
        dry_run = parse_bool(params.get('dry_run'), default=False)
        hard_delete = parse_bool(params.get('hard_delete'), default=True)

        task = cleanup_unbound_pictures.delay(
            expire_days=expire_days,
            dry_run=dry_run,
            hard_delete=hard_delete,
        )
        return {
            'accepted': True,
            'task_id': task.id,
            'expire_days': expire_days,
            'dry_run': dry_run,
            'hard_delete': hard_delete,
        }
