# ================================
#          Django Imports
# ================================

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime

# ================================
#          Custom User Manager
# ================================

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model with methods for creating users.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and username.
        
        Args:
            username (str): The username for the user.
            email (str): The email address for the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields to set on the user.

        Raises:
            ValueError: If email or username is not provided.

        Returns:
            User: The created user instance.
        """
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# ================================
#          Custom User Model
# ================================

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports authentication using email and username.
    """
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=datetime.now)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Required for admin access

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_user_permissions_set',
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """
        Return the string representation of the user.
        """
        return self.username

# ================================
#          Subscriber Model
# ================================

class Subscriber(models.Model):
    """
    Model to manage subscribers with email and OTP verification.
    """
    subscriber_email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=datetime.now)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Return the string representation of the subscriber.
        """
        return self.subscriber_email
    
class ContactUs(models.Model):
    """
    Model to manage contact us form.
    """
    name = models.CharField()
    email = models.EmailField()
    project_tech = models.CharField()
    description = models.CharField()