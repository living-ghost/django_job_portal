# ================================
#          Django Imports
# ================================

from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.conf import settings

# ================================
#          Utility Functions
# ================================

def generate_otp():
    """
    Generate a random OTP (One-Time Password) consisting of 6 digits.

    Returns:
        str: A 6-digit OTP as a string.
    """
    return get_random_string(6, '1234567890')

def send_otp_email(email, otp):
    """
    Send an OTP code to the specified email address.

    Args:
        email (str): The recipient's email address.
        otp (str): The OTP code to be sent.
    """
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}.',
        'akhiiltkaniiparampiil@gmail.com',
        [email],
        fail_silently=False,
    )

def send_account_created_email(email):
    """
    Send an account creation confirmation email to the user.

    Args:
        email (str): The recipient's email address.
    """
    subject = 'Freshers Park'
    from_email = 'akhiiltkaniiparampiil@gmail.com'
    to_email = [email]

    # Render the HTML content from the template
    html_content = render_to_string('portal_user_app/users/user_ac_created.html', {'email': email})
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()

def send_subscription_email(email):
    """
    Send a subscription confirmation email to the subscriber.

    Args:
        email (str): The recipient's email address.
    """
    subject = 'Freshers Park'
    from_email = 'akhiiltkaniiparampiil@gmail.com'
    to_email = [email]

    # Render the HTML content from the template
    html_content = render_to_string('portal_user_app/emails/subscribed.html', {'email': email})
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()

def generate_password():
    """
    Generate a random password consisting of lowercase letters and digits.

    Returns:
        str: A random password with a length of 6 characters.
    """
    return get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890')

def send_reset_email(email, temp_pwd):
    """
    Send a password reset email containing the temporary password.

    Args:
        email (str): The recipient's email address.
        temp_pwd (str): The temporary password to be sent.
    """
    subject = 'Your temporary Password'
    message = (
        f'Your temporary Password is {temp_pwd}.'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False
    )