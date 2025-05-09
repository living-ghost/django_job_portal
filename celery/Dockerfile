FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install base packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install requirements (using --no-cache-dir to reduce image size)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY . .

# Set PATH for user-installed packages
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

# Explicit Celery worker command with all necessary parameters
CMD ["celery", "-A", "job_portal", "worker", "--pool=solo", "-l", "info", "--without-gossip", "--without-mingle", "--without-heartbeat"]