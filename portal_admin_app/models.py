# ================================
#         Django Imports
# ================================

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime

# ================================
#         Custom Admin Manager
# ================================

class CustomAdminManager(BaseUserManager):
    """
    Custom manager for Admin model with methods to create admin and superadmin.
    """
    def create_admin(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular admin with a username and email.
        """
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        admin = self.model(username=username, email=email, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superadmin(self, username, email, password=None, **extra_fields):
        """
        Create and return a superadmin with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superadmin must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superadmin must have is_superuser=True.')
        return self.create_admin(username, email, password, **extra_fields)

# ================================
#            Admin Model
# ================================

class Admin(AbstractBaseUser, PermissionsMixin):
    """
    Custom Admin model extending AbstractBaseUser with additional fields.
    """
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_user_set',  # Unique related_name for Admin model
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_user_permissions_set',  # Unique related_name for Admin model
        blank=True,
    )

    objects = CustomAdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# ================================
#             Job Model
# ================================

class Job(models.Model):
    """
    Model representing a job posting with various attributes.
    """
    JOB_TYPE_CHOICES = [
        ('fresher', 'Fresher'),
        ('featured', 'Featured'),
        ('experienced', 'Experienced'),
    ]

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='fresher')
    job_heading = models.CharField(max_length=200)
    job_eligibility = models.TextField()
    job_description = models.TextField(default='Click on Apply Now to know more!')
    job_details = models.TextField(default='#')
    job_created_at = models.DateTimeField(default=datetime.now)
    job_added_by = models.CharField(null=True, max_length=100)
    job_updated_by = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.job_heading