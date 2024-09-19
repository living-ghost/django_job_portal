# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf 0.12.6 and its dependencies
RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    fontconfig \
    libxrender1 \
    libxext6 \
    libfreetype6 \
    libjpeg62-turbo \
    libx11-6 \
    xfonts-75dpi \
    xfonts-base && \
    https://ubuntu.pkgs.org/20.04/ubuntu-main-amd64/libssl1.1_1.1.1f-1ubuntu2_amd64.deb.html && \
    https://ubuntu.pkgs.org/22.04/ubuntu-main-amd64/libjpeg-turbo8_2.1.2-0ubuntu1_amd64.deb.html && \
    wget https://github.com/living-ghost/releases/releases/download/v0.12.6/wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    apt-get install -f -y && \
    rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Clean up the apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
# Ensure to include .git if needed for versioning
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]