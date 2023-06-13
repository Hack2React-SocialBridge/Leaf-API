from os import environ

from celery import Celery

CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND")

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    broker_pool_limit=0
)
