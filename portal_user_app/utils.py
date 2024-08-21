from django.core.mail import send_mail 
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# generating otp

def generate_otp():
    return get_random_string(6, '1234567890')

# Sending otp to email id

def send_otp_email(email, otp):
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}.',
        'akhiiltkaniiparampiil@gmail.com',
        [email],
        fail_silently=False,
    )

# Sending Confirmation email to User

def send_account_created_email(email):

    subject = 'Freshers Park'
    from_email = 'akhiiltkaniiparampiil@gmail.com'
    to_email = [email]

    html_content = render_to_string('portal_user_app/users/user_ac_created.html', {'email': email})
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()

# Sending Confirmation email to Subscriber

def send_subscription_email(email):
    subject = 'Freshers Park'
    from_email = 'akhiiltkaniiparampiil@gmail.com'
    to_email = [email]

    # Render the HTML content from the template
    html_content = render_to_string('portal_user_app/emails/subscribed.html', {'email': email})
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()

# Random password if user clicked forgot password

def generate_password():
    return get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890')

# Send username and password after reset

def send_reset_email(email, temp_pwd):
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