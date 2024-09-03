"""
Django settings for job_portal project.

This file contains the configurations for the Django project, including
installed apps, middleware, database settings, and more.

Environment variables are used to secure sensitive information like secret
keys and database credentials. The dotenv library is used to load these
variables from a .env file.

For more information on this file, see:
https://docs.djangoproject.com/en/5.0/topics/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the dev.env file
load_dotenv(dotenv_path=os.path.join(BASE_DIR, 'dev.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Security key for the Django project
SECRET_KEY = os.getenv('SECRET_KEY')

# Debug mode - should be False in production
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Fetch the ALLOWED_HOSTS environment variable, default to an empty string if not set
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '')

# Split the string into a list by commas
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Custom Apps
    'portal_user_app',
    'portal_admin_app',
    'portal_resume_app',
    'portal_converter_app',

    # Django REST Framework (DRF)
    'rest_framework',

    # Prometheus
    'django_prometheus',

    # Celery
    'celery',
]

# Site ID for the Sites framework
SITE_ID = 1

# Protocol scheme for HTTP requests
HTTP_SCHEME = 'http'

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware', # Prometheus middleware for monitoring

    'django.middleware.security.SecurityMiddleware',  # Provides security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages user sessions
    'django.middleware.common.CommonMiddleware',  # Adds various common middleware functionalities
    'django.middleware.csrf.CsrfViewMiddleware',  # Adds CSRF protection (commented out for specific cases)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Handles authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Manages message flashing
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protects against clickjacking
    'django.middleware.gzip.GZipMiddleware',  # Compresses content for improved performance

    'job_portal.middleware.NoCacheMiddleware',  # Custom middleware to disable caching
    'job_portal.middleware.SkipAdminLoginMiddleware',  # Custom middleware for admin login bypass
    'job_portal.middleware.SkipUserLoginMiddleware',  # Custom middleware for user login bypass
    'job_portal.middleware.SkipResumeLoginMiddleware',  # Custom middleware for resume login bypass
    'job_portal.middleware.SkipConverterLoginMiddleware',  # Custom middleware for converter login bypass

    'django_prometheus.middleware.PrometheusAfterMiddleware', # Prometheus middleware for monitoring
]

# URL to redirect users for login
LOGIN_URL = 'portal_user_app:user_index'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend for authentication
    'portal_admin_app.backends.AdminBackend',  # Custom backend for admin authentication
    'portal_user_app.backends.UserBackend',  # Custom backend for user authentication
]

# Root URL configuration module
ROOT_URLCONF = 'job_portal.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template backend for rendering
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Directories to search for templates
        'APP_DIRS': True,  # Enables loading templates from application directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Adds debug information to context
                'django.template.context_processors.request',  # Adds request information to context
                'django.contrib.auth.context_processors.auth',  # Adds user authentication information to context
                'django.contrib.messages.context_processors.messages',  # Adds message information to context
            ],
        },
    },
]

# WSGI application entry point
WSGI_APPLICATION = 'job_portal.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'akhiiltkaniiparampiil@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'akhiiltkaniiparampiil@gmail.com'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization settings
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'  # URL for accessing static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where static files will be collected
STATICFILES_DIRS = [
    BASE_DIR / 'portal_user_app' / 'static',  # Static files for the user app
    BASE_DIR / 'portal_admin_app' / 'static',  # Static files for the admin app
    BASE_DIR / 'portal_resume_app' / 'static',  # Static files for the resume app
    BASE_DIR / 'portal_converter_app' / 'static',  # Static files for the converter app
]

# Media files configuration
MEDIA_URL = '/media/'  # URL for accessing media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory where media files are stored

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Path to wkhtmltopdf executable
PDFKIT_CONFIG = {
    'wkhtmltopdf': os.getenv('WKHTMLTOPDF_PATH', r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'),
}

# Path to wkhtmltoimage executable
IMGKIT_CONFIG = {
    'wkhtmltoimage': os.getenv('WKHTMLTOIMAGE_PATH', r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'),
}