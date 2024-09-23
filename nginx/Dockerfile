FROM nginx:latest

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration
COPY ./conf.d/my_nginx.conf /etc/nginx/conf.d/

# Copy static files if necessary (optional)
# COPY ./static /usr/share/nginx/html/static