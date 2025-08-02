
# Docker Container Setup for Job Portal Infrastructure

## Create Docker Network
```bash
docker network create job_portal_net
```

## PostgreSQL Container
```bash
docker run -d --name db --network job_portal_net \
  -e POSTGRES_DB=jobportal \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

## RabbitMQ Container
```bash
docker run -d --name rabbitmq \
  --network job_portal_net \
  --env-file .env \
  -p 15672:15672 \
  -v rabbitmqdata:/var/lib/rabbitmq \
  rabbitmq:3-management
```

## Django Container (Using the pushed image)
```bash
docker run -d --name django \
  --network job_portal_net \
  -p 8000:8000 \
  -v ./django/static:/app/staticfiles \
  --env-file .env \
  living9host/job_portal

docker exec -it django bash
```

## Nginx Container
```bash
docker run -d --name nginx \
  --network job_portal_net \
  -p 80:80 \
  -v $(pwd)/staticfiles:/usr/share/nginx/html/staticfiles \
  living9host/job_portal_nginx
```

## Celery Container
```bash
docker run -d --name celery \
  --network job_portal_net \
  --env-file .env \
  living9host/job_portal_celery
```

## Flower Container
```bash
docker run -d --name flower \
  --network job_portal_net \
  -p 5555:5555 \
  yourusername/jobportal-flower
```

## Optional: pgAdmin
```bash
docker run -d --name pgadmin \
  --network job_portal_net \
  --env-file .env \
  -p 8089:80 \
  dpage/pgadmin4
```

## Prometheus
```bash
docker run -d --name prometheus \
  --network job_portal_net \
  -p 9090:9090 \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

## Grafana
```bash
docker run -d --name grafana \
  --network job_portal_net \
  -p 3000:3000 \
  grafana/grafana
```

---

## ✅ Option 1: Rename Variables in .env for Simplicity

Update `.env` like this:

```env
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Then run the containers with:

### PostgreSQL
```bash
docker run -d --name db \
  --network my_network \
  --env-file .env \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

### pgAdmin
```bash
docker run -d --name pgadmin \
  --network my_network \
  -e PGADMIN_DEFAULT_EMAIL=${PGADMIN_EMAIL} \
  -e PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD} \
  -p 8089:80 \
  dpage/pgadmin4
```
