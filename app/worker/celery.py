import os

from celery import Celery

worker = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["worker.tasks"],
)

worker.conf.update(
    task_serializer="json",
    result_expires=3600,
)

if __name__ == "__main__":
    worker.start()
