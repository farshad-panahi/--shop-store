import os

from celery import Celery
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    # "config", broker="redis://localhost:6379", backend="redis://localhost:6379"
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
