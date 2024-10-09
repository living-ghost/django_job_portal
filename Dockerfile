# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and LibreOffice
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Essential packages
    wget \
    curl \
    gnupg \
    ca-certificates \
    # LibreOffice dependencies
    libssl3 \
    xz-utils \
    fontconfig \
    libxrender1 \
    libxext6 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libx11-6 \
    libxcb1 \
    xfonts-75dpi \
    xfonts-base \
    cabextract \
    libxinerama1 \
    libxrandr2 \
    libxml2 \
    libxrender1 \
    libxrandr2 \
    libx11-6 \
    libxext6 \
    libfontconfig1 \
    libfreetype6 \
    libsm6 \
    libice6 \
    libglib2.0-0 \
    libglib2.0-bin \
    libatk1.0-0 \
    libatk-bridge2.0-0  \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libfontenc1 \
    libgbm1 \
    libglib2.0-data \
    libgnutls30 \
    libgssapi-krb5-2 \
    libgtk-3-0 \
    liblzma5 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpcre3 \
    libpixman-1-0 \
    libpng16-16 \
    libsm6 \
    libsasl2-2 \
    libsasl2-modules \
    libsdl1.2debian \
    libsqlite3-0 \
    libudev1 \
    libvorbis0a \
    libvorbisenc2 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxinerama1 \
    libxkbcommon0 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    zlib1g \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf specific to Ubuntu Bionic
RUN wget https://github.com/living-ghost/releases/releases/download/v0.12.6/libjpeg-turbo8_2.1.2-0ubuntu1_amd64.deb && \
    wget https://github.com/living-ghost/releases/releases/download/v0.12.6/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    wget http://ftp.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.8_all.deb && \
    wget https://github.com/living-ghost/releases/releases/download/v0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    wget https://download.oracle.com/java/23/latest/jdk-23_linux-x64_bin.deb && \
    dpkg -i libjpeg-turbo8_2.1.2-0ubuntu1_amd64.deb libssl1.1_1.1.1f-1ubuntu2_amd64.deb ttf-mscorefonts-installer_3.8_all.deb wkhtmltox_0.12.6-1.bionic_amd64.deb jdk-23_linux-x64_bin.deb

# Install LibreOffice 24.8.2
RUN wget https://github.com/living-ghost/releases/releases/download/v0.12.6/LibreOffice_24.8.2_Linux_x86-64_deb.tar.gz && \
    tar -xvzf LibreOffice_24.8.2_Linux_x86-64_deb.tar.gz && \
    dpkg -i LibreOffice_24.8.2.*/DEBS/*.deb

# Clean up the apt cache and tarballs
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf LibreOffice_24.8.2_Linux_x86-64_deb.tar.gz LibreOffice_24.8.2.*

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Ensure LibreOffice is accessible via 'soffice' command
# RUN ln -s /usr/bin/libreoffice /usr/bin/soffice

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]