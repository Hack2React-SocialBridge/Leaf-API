from celery import Celery

from leaf.tasks import resize_image, send_mail
from leaf.dependencies import get_settings


settings = get_settings()


celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_pool_limit=0
)
celery.task(send_mail)
celery.task(resize_image)
