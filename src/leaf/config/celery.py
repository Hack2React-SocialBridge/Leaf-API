from __future__ import annotations

from celery import Celery

from leaf.config.config import get_settings
from leaf.tasks import resize_image, send_mail

settings = get_settings()


celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_pool_limit=0,
)
celery.task(send_mail)
celery.task(resize_image)
