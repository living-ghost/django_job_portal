# Django
docker build -t living9host/job_portal -f django/Dockerfile .
docker push living9host/job_portal

# Nginx
docker build -t yourusername/job_portal_nginx -f nginx/Dockerfile .
docker push yourusername/jobportal-nginx

# Celery
docker build -t yourusername/job_portal_celery -f celery/Dockerfile .
docker push living9host/job_portal_celery

# Flower
docker build -t yourusername/jobportal-flower -f flower/Dockerfile .
docker push yourusername/jobportal-flower