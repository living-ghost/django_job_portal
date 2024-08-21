from django.contrib.auth.backends import BaseBackend
from .models import User

class UserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the input is an email or a username
        if '@' in username:
            # Email authentication
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # Username authentication
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        # Verify password
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None