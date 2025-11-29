from config import Config
from celery import Celery

# Initialize Celery app
celery_app = Celery(
    "usm_workers",
    broker=Config.BROKER_URL,
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone=Config.TIMEZONE,
    enable_utc=False,
    imports=[],  # Import Tasks
)

# celery cmd
# celery -A async_tasks.celery_init:celery_app worker -l info -P gevent -Q summarization_queue
