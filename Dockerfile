# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf 0.12.6 and its dependencies
# Install dependencies for Wine and Wine itself
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
    wget \
    fontconfig \
    libxrender1 \
    libxext6 \
    libfreetype6 \
    libjpeg-turbo8 \
    libx11-6 \
    xfonts-75dpi \
    xfonts-base \
    wine \
    wine32 \
    wine64 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Download wkhtmltopdf .exe file and install it using Wine
RUN wget https://github.com/living-ghost/releases/releases/download/v0.12.6/wkhtmltox-0.12.6-1.msvc2015-win64.exe -O /app/wkhtmltox.exe && \
    wine /app/wkhtmltox.exe

# Clean up the apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
# Ensure to include .git if needed for versioning
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]