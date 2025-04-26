import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')

app = Celery('job_portal')

# Configuring Celery to use the settings from Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional: Updated result_backend for more robustness
app.conf.update(

    broker_connection_retry_on_startup=True,
)

# Set broker connection timeout
app.conf.broker_connection_timeout = 30

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Optional: Enable detailed logging for debugging
app.conf.update(
    task_track_started=True,
    worker_redirect_stdouts=True,
    worker_redirect_stdouts_level='INFO',
)
