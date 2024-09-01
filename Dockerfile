# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Ensure celeryuser owns the entire /app directory
RUN adduser --disabled-password --gecos '' celeryuser && \
    chown -R celeryuser:celeryuser /app

# Switch to non-root user
USER celeryuser

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables from build arguments
ARG SECRET_KEY
ARG ALLOWED_HOSTS
ARG DEBUG
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG PGADMIN_DEFAULT_EMAIL
ARG PGADMIN_DEFAULT_PASSWORD
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ARG DEFAULT_FROM_EMAIL
ARG WKHTMLTOPDF_PATH
ARG WKHTMLTOIMAGE_PATH

ENV SECRET_KEY=${SECRET_KEY}
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}
ENV DEBUG=${DEBUG}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV PGADMIN_DEFAULT_EMAIL=${PGADMIN_DEFAULT_EMAIL}
ENV PGADMIN_DEFAULT_PASSWORD=${PGADMIN_DEFAULT_PASSWORD}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
ENV DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
ENV WKHTMLTOPDF_PATH=${WKHTMLTOPDF_PATH}
ENV WKHTMLTOIMAGE_PATH=${WKHTMLTOIMAGE_PATH}

# Echo the values to verify them
RUN echo "SECRET_KEY=${SECRET_KEY}" && \
    echo "ALLOWED_HOSTS=${ALLOWED_HOSTS}" && \
    echo "DEBUG=${DEBUG}" && \
    echo "DB_NAME=${DB_NAME}" && \
    echo "DB_USER=${DB_USER}" && \
    echo "DB_PASSWORD=${DB_PASSWORD}" && \
    echo "DB_HOST=${DB_HOST}" && \
    echo "DB_PORT=${DB_PORT}" && \
    echo "PGADMIN_DEFAULT_EMAIL=${PGADMIN_DEFAULT_EMAIL}" && \
    echo "PGADMIN_DEFAULT_PASSWORD=${PGADMIN_DEFAULT_PASSWORD}" && \
    echo "EMAIL_HOST_USER=${EMAIL_HOST_USER}" && \
    echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" && \
    echo "DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}" && \
    echo "WKHTMLTOPDF_PATH=${WKHTMLTOPDF_PATH}" && \
    echo "WKHTMLTOIMAGE_PATH=${WKHTMLTOIMAGE_PATH}"

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]