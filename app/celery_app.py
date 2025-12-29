import os

from celery import Celery
from kombu import Queue

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery.conf.update(
    task_default_queue="default",
    task_queues=[
        Queue("default"),
        Queue("fast"),
        Queue("priority"),
    ]
)

celery.autodiscover_tasks(["app.tasks.tasks"])