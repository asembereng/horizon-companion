"""
Celery application configuration.

Chapter 25 (DevOps Agent): the worker command in docker-compose.yml
references ``celery -A horizon worker -l info``.
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horizon_project.settings")

app = Celery("horizon")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
