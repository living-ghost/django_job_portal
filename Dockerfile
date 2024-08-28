# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pycairo
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# In your Dockerfile, after installing all dependencies
RUN adduser --disabled-password --gecos '' celeryuser
USER celeryuser

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables from build arguments
ARG SECRET_KEY
ARG DEBUG
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ARG DEFAULT_FROM_EMAIL
ARG WKHTMLTOPDF_PATH
ARG WKHTMLTOIMAGE_PATH

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
ENV DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
ENV WKHTMLTOPDF_PATH=${WKHTMLTOPDF_PATH}
ENV WKHTMLTOIMAGE_PATH=${WKHTMLTOIMAGE_PATH}

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]