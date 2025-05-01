# Celery retry configuration

from celery import Celery
from kombu.exceptions import OperationalError

app = Celery('job_portal')

app.config_from_object({
    'broker_url': 'amqp://guest:guest@freshersparkrabbitmq.victoriousocean-8dff7969.centralindia.azurecontainerapps.io:5672//',
    'result_backend': 'rpc://',
    'task_default_retry_delay': 30,  # Retry every 30 seconds
    'task_max_retries': 10,  # Max retries before failing
})

# Task with retry logic
@app.task(bind=True)
def my_task(self):
    try:
        # Your task code here
        pass
    except OperationalError as exc:
        raise self.retry(exc=exc)
