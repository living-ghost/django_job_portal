# ================================
#         Django Imports
# ================================

from django.contrib.auth.backends import BaseBackend
from .models import Admin

# ================================
#       Custom Authentication
# ================================

class AdminBackend(BaseBackend):
    """
    Custom authentication backend for the Admin model.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate an admin based on username and password.
        """
        try:
            admin = Admin.objects.get(username=username)
            if admin.check_password(password):
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Retrieve an admin instance by user ID.
        """
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None