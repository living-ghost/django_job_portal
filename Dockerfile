# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Update and install necessary packages for wkhtmltopdf
RUN apt-get update && \
    apt-get install -y wget xz-utils fontconfig libxrender1 libxext6 \
    libfreetype6 libjpeg62-turbo libpng16-16 libx11-6 libxcb1 xfonts-75dpi xfonts-base

# Install wkhtmltopdf specific to Ubuntu Bionic
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb
    
# Clean up the apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
# Ensure to include .git if needed for versioning
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]