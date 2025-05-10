FROM nginx:latest

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY nginx/default.conf /etc/nginx/conf.d/

# Copy static files from build context to Nginx html directory
COPY staticfiles/ /usr/share/nginx/html/