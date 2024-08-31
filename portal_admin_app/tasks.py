from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import logging
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task
def send_job_email(subscriber_email, job_id, unsubscribe_url, site_url):
    logger.info(f"Sending email to {subscriber_email}")
    try:
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {job_id}.',
            'akhiiltkaniiparampiil@gmail.com',
            [subscriber_email],
            fail_silently=False,
        )
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {e}")