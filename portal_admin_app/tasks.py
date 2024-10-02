from celery import shared_task
import logging

# ================================
#          Django Imports
# ================================

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

@shared_task
def send_job_email(subscriber_email, job_heading, job_eligibility, job_created_at, unsubscribe_url, site_url):
    logger.info(f"Sending email to {subscriber_email}")
    try:
        subject = 'Freshers Park'
        from_email = 'admin@fresherspark.in'
        to_email = [subscriber_email]
        html_content = render_to_string('portal_user_app/emails/post_updates.html', {'job_heading': job_heading, 'job_eligibility': job_eligibility, 'job_created_at': job_created_at, 'unsubscribe_url': unsubscribe_url, 'site_url': site_url})
        email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
        email_message.attach_alternative(html_content, 'text/html')
        email_message.send()
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {e} , {subscriber_email}")