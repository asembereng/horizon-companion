"""
Enterprise Django settings — extends the Django variant settings
with Celery and Redis configuration.
"""

# Re-use all Django variant settings
import sys
from pathlib import Path

# Add the Django variant to the path so we can import its settings
_django_dir = Path(__file__).resolve().parent.parent / "django"
if str(_django_dir) not in sys.path:
    sys.path.insert(0, str(_django_dir))

from horizon_project.settings import *  # noqa: F401,F403

# ── Celery ──────────────────────────────────────────────────────

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")  # noqa: F405
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")  # noqa: F405
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# ── Redis Cache ─────────────────────────────────────────────────

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://redis:6379/1"),  # noqa: F405
    }
}
