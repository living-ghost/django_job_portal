#!/bin/bash

# Run Django commands
python manage.py makemigrations portal_admin_app
python manage.py makemigrations portal_user_app
python manage.py makemigrations portal_converter_app
python manage.py makemigrations portal_resume_app
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn --bind 0.0.0.0:8000 job_portal.wsgi:application
