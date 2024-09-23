# ================================
#          Django Imports
# ================================

from django.contrib.auth.backends import BaseBackend
from .models import User

# ================================
#          Custom Authentication Backend
# ================================

class UserBackend(BaseBackend):
    """
    Custom authentication backend that supports authentication using either email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user using email or username and password.
        
        Args:
            request (HttpRequest): The request object.
            username (str): The email or username of the user.
            password (str): The password of the user.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The authenticated user if credentials are valid, otherwise None.
        """
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
        """
        Retrieve a user instance by their ID.
        
        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user instance if found, otherwise None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None