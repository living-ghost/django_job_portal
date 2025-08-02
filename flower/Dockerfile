FROM python:3.9-slim

WORKDIR /app

COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["celery", "-A", "job_portal", "flower", "--port=5555"]