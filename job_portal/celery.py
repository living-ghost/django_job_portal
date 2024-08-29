import os
from celery import Celery
from kombu import Exchange, Queue

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')

app = Celery('job_portal')

# Configuring Celery to use the settings from Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Broker settings
app.conf.update(
    broker_connection_retry_on_startup=True,  # Retry connecting to the broker on startup
    broker_connection_timeout=30,  # Set broker connection timeout
    broker_heartbeat=10,  # Ensure broker connection is kept alive (tune this value as needed)
)

# Set up a custom queue with specific exchange and routing key if needed
app.conf.task_queues = (
    Queue('celery', Exchange('celery'), routing_key='celery'),
)

# Set task result expiration (time after which task results will be deleted)
app.conf.result_expires = 3600  # 1 hour

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Enable detailed logging for debugging
app.conf.update(
    task_track_started=True,
    worker_redirect_stdouts=True,
    worker_redirect_stdouts_level='INFO',
    worker_prefetch_multiplier=1,  # Control how many tasks are prefetched by each worker
    task_acks_late=True,  # Ensure tasks are acknowledged after they are completed
)

# Optional: Use a custom worker name if running multiple workers
# app.conf.worker_name = 'worker1@%h'