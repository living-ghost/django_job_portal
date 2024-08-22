# settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # MY APP's
    'portal_user_app',
    'portal_admin_app',
    'portal_resume_app',
    'portal_converter_app',

    # DRF
    'rest_framework',
]   

# Set the SITE_ID variable
SITE_ID = 1

HTTP_SCHEME = 'http'  # Protocol scheme for HTTP requests

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Provides security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages user sessions
    'django.middleware.common.CommonMiddleware',  # Adds various common middleware functionalities
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Adds CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Handles authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Manages message flashing
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protects against clickjacking
    'django.middleware.gzip.GZipMiddleware',  # Compresses content for improved performance
    'job_portal.middleware.NoCacheMiddleware',  # Custom middleware to disable caching
    'job_portal.middleware.SkipAdminLoginMiddleware',
    'job_portal.middleware.SkipUserLoginMiddleware',
    'job_portal.middleware.SkipResumeLoginMiddleware',
    'job_portal.middleware.SkipConverterLoginMiddleware',
]

LOGIN_URL = 'portal_admin_app:admin_login'  # URL to redirect users for login
LOGIN_URL = 'portal_user_app:user_index'  # URL to redirect users for login

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend for authentication
    'portal_admin_app.backends.AdminBackend',  # Custom backend for additional authentication
    'portal_user_app.backends.UserBackend',
]

ROOT_URLCONF = 'job_portal.urls'  # Root URL configuration module

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

WSGI_APPLICATION = 'job_portal.wsgi.application'  # WSGI application entry point

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# URL for accessing static files
STATIC_URL = '/static/'

# Directory where static files will be collected
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional directories where static files are located
STATICFILES_DIRS = [
    BASE_DIR / 'portal_user_app' / 'static',  # Directory where your static files are located
    BASE_DIR / 'portal_admin_app' / 'static',
    BASE_DIR / 'portal_resume_app' / 'static',
    BASE_DIR / 'portal_converter_app' / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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