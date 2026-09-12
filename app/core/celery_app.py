from celery import Celery

from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


celery_app = Celery("EmployeeManagementSystem", broker=redis_url, backend=redis_url)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    imports=("app.tasks.email_task")
)
