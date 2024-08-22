# Standard Library Imports
from datetime import datetime, timedelta

# Third-Party Imports
from django.utils.timezone import make_aware

# Django App Imports
from .models import Subscriber, User
from .utils import send_subscription_email

#

def verify_otp(request, otp):
    session_otp = request.session.get('otp')
    session_otp_created_at = request.session.get('otp_created_at')

    if not otp or not session_otp or not session_otp_created_at:
        return False

    otp_created_at = datetime.fromisoformat(session_otp_created_at)
    now = make_aware(datetime.now())

    if otp == session_otp and otp_created_at + timedelta(minutes=5) > now:
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=int(user_id))
                user.is_active = True
                user.save()

                # Clear the session data after successful activation
                request.session.pop('otp', None)
                request.session.pop('otp_created_at', None)
                request.session.pop('user_id', None)

                return True
            except User.DoesNotExist:
                return False
    return False

#

def handle_successful_otp_verification(email):
    Subscriber.objects.create(subscriber_email=email)
    send_subscription_email(email)