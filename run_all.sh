#!/bin/bash

# Load environment variables
source .env

# Create Docker network if it doesn't exist
docker network inspect my_network >/dev/null 2>&1 || \
docker network create my_network

echo "✅ Network 'my_network' ready."

# Start PostgreSQL
docker run -d --name db --network my_network \
  -e POSTGRES_DB=$DB_NAME \
  -e POSTGRES_PASSWORD=$DB_PASSWORD \
  -e POSTGRES_USER=$DB_USER \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

echo "🚀 PostgreSQL started."

# Start RabbitMQ
docker run -d --name rabbitmq --network my_network \
  -p 5672:5672 -p 15672:15672 \
  -v rabbitmqdata:/var/lib/rabbitmq \
  rabbitmq:3-management

echo "🚀 RabbitMQ started."

# Start PgAdmin
docker run -d --name pgadmin --network my_network \
  -p 8089:80 \
  -e PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL \
  -e PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD \
  dpage/pgadmin4

echo "🚀 PgAdmin started."

# Build Django image
docker build -t django_app_image .

# Start Django
docker run -d --name django_app --network my_network \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e SECRET_KEY=$SECRET_KEY \
  -e ALLOWED_HOSTS=$ALLOWED_HOSTS \
  -e DEBUG=$DEBUG \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASSWORD=$DB_PASSWORD \
  -e DB_HOST=db \
  -e DB_PORT=$DB_PORT \
  -e EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
  -e CELERY_BROKER_URL=amqp://guest:guest@rabbitmq// \
  django_app_image \
  bash -c "python manage.py makemigrations portal_admin_app && \
           python manage.py makemigrations portal_user_app && \
           python manage.py makemigrations portal_converter_app && \
           python manage.py makemigrations portal_resume_app && \
           python manage.py migrate && \
           python manage.py collectstatic --noinput && \
           gunicorn --bind 0.0.0.0:8000 job_portal.wsgi:application"

echo "🚀 Django app started."

# Build and run Nginx
docker build -t nginx_image ./nginx

docker run -d --name nginx --network my_network \
  -p 80:80 \
  -v $(pwd)/nginx/conf.d:/etc/nginx/conf.d \
  -v $(pwd)/staticfiles:/usr/share/nginx/html/staticfiles \
  -v $(pwd)/media:/usr/share/nginx/html/media \
  nginx_image

echo "🚀 Nginx started."

# Start Celery worker
docker run -d --name celery_worker --network my_network \
  -v $(pwd):/app \
  -e SECRET_KEY=$SECRET_KEY \
  -e EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
  -e CELERY_BROKER_URL=amqp://guest:guest@rabbitmq// \
  -e CELERY_ACCEPT_CONTENT=application/json \
  -e CELERY_RESULT_SERIALIZER=json \
  -e CELERY_TASK_SERIALIZER=json \
  -e CELERY_TIMEZONE=Asia/Kolkata \
  -e CELERY_RESULT_BACKEND=rpc:// \
  django_app_image \
  celery -A job_portal.celery worker --pool=solo -l info

echo "🚀 Celery worker started."

# Start Flower
docker run -d --name celery_flower --network my_network \
  -p 5555:5555 \
  -v $(pwd):/app \
  -e EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
  -e CELERY_BROKER_URL=amqp://guest:guest@rabbitmq// \
  -e CELERY_ACCEPT_CONTENT=application/json \
  -e CELERY_RESULT_SERIALIZER=json \
  -e CELERY_TASK_SERIALIZER=json \
  -e CELERY_TIMEZONE=Asia/Kolkata \
  -e CELERY_RESULT_BACKEND=rpc:// \
  django_app_image \
  celery -A job_portal flower

echo "🚀 Flower started."

# Start Prometheus
docker run -d --name prometheus --network my_network \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

echo "🚀 Prometheus started."

# Start Grafana
docker run -d --name grafana --network my_network \
  -p 3002:3000 \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana

echo "🚀 Grafana started."

echo "🎉 All services are up and running!"
