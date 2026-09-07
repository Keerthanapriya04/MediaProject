import os

from celery import Celery


# Tell Celery which Django settings to use
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Mediaproject.settings"
)


# Create Celery application
app = Celery("Mediaproject")


# Load Celery settings from Django settings
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)


# Automatically find tasks.py in Django apps
app.autodiscover_tasks()