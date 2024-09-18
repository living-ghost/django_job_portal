# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies for wkhtmltopdf
RUN apt-get update && apt-get install -y \
    xfonts-75dpi \
    xfonts-base \
    fontconfig \
    libxrender1 \
    libxext6 \
    wget \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Download and install wkhtmltopdf from the official source
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bullseye_amd64.deb && \
    apt-get install -y ./wkhtmltox_0.12.6-1.bullseye_amd64.deb && \
    rm wkhtmltox_0.12.6-1.bullseye_amd64.deb

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]