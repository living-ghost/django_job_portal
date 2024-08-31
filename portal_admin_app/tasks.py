from celery import shared_task
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_job_email(subscriber_email, job_id, unsubscribe_url, site_url):
    logger.info(f"Sending email to {subscriber_email}")
    try:
        subject = "New Job Posting"
        message = f"""
        Hi there,

        A new job posting has been added. 

        Job ID: {job_id}
        Unsubscribe: {unsubscribe_url}
        Visit our site: {site_url}
        """
        from_email = "akhiiltkaniiparampiil@gmail.com"
        email = EmailMessage(subject, message, from_email, [subscriber_email])
        email.send()
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {e}")