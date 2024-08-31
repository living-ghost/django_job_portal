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
        subject = 'New Job Posted'
        message = (
            f'Job Name : {job_id}'
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [subscriber_email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {e}")