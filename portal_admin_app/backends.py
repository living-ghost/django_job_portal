from django.contrib.auth.backends import BaseBackend
from . models import Admin


class AdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(username=username)
            if admin.check_password(password):
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None
