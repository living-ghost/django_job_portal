# ================================
#          Standard Library Imports
# ================================

from datetime import datetime, timedelta

# ================================
#          Third-Party Imports
# ================================

from django.utils.timezone import make_aware

# ================================
#          Django App Imports
# ================================

from .models import Subscriber, User
from .utils import send_subscription_email

# ================================
#          Verify OTP Function
# ================================

def verify_otp(request, otp):
    """
    Verify the OTP provided by the user. This function checks if the provided OTP matches
    the OTP stored in the session and if it is within the valid time window.

    Args:
        request (HttpRequest): The request object containing session data.
        otp (str): The OTP provided by the user.

    Returns:
        bool: True if the OTP is valid and the user is activated, False otherwise.
    """
    session_otp = request.session.get('otp')
    session_otp_created_at = request.session.get('otp_created_at')

    # Check if OTP and session data are present
    if not otp or not session_otp or not session_otp_created_at:
        return False

    otp_created_at = datetime.fromisoformat(session_otp_created_at)
    now = make_aware(datetime.now())

    # Validate OTP and check if it is within the allowed time frame
    if otp == session_otp and otp_created_at + timedelta(minutes=5) > now:
        user_id = request.session.get('user_id')
        if user_id:
            try:
                # Activate the user account
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

# ================================
#          Handle Successful OTP Verification
# ================================

def handle_successful_otp_verification(email):
    """
    Handle successful OTP verification by creating a subscriber record and sending a
    subscription email.

    Args:
        email (str): The email address to be subscribed.
    """
    # Create a new subscriber record
    Subscriber.objects.create(subscriber_email=email)
    
    # Send a subscription confirmation email
    send_subscription_email(email)