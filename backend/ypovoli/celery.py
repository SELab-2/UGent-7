import os

from celery import Celery
from celery.app.task import Task
from django.conf import settings

Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore[attr-defined]

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ypovoli.settings")

app = Celery("ypovoli")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
# Will only load tasks defined in a tasks.py file, not a module
app.autodiscover_tasks()

# Load tasks from all installed apps defined inside a module called tasks
for app_name in settings.INSTALLED_APPS:
    if app_name.startswith('django'):
        continue
    for root, dirs, files in os.walk(app_name + '/tasks'):
        for file in files:
            if file.startswith('__') or file.endswith('.pyc') or not file.endswith('.py'):
                continue
            file = file[:-3]
            app.autodiscover_tasks([app_name + '.tasks'], related_name=file)
