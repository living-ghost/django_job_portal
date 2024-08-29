# job_portal/celery.py
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')

app = Celery('job_portal')

# Configuring Celery to use the settings from Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Optional: Enable detailed logging for debugging
app.conf.update(
    task_track_started=True,
    worker_redirect_stdouts=True,
    worker_redirect_stdouts_level='INFO',
)