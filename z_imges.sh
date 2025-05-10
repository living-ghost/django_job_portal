# Django
docker build -t living9host/job_portal -f django/Dockerfile .
docker push living9host/job_portal

# Nginx
docker build -t living9host/job_portal_nginx -f nginx/Dockerfile .
docker push living9host/job_portal_nginx

# Celery
docker build -t living9host/job_portal_celery -f celery/Dockerfile .
docker push living9host/job_portal_celery

# Flower
docker build -t yourusername/jobportal-flower -f flower/Dockerfile .
docker push yourusername/jobportal-flower


azureuser@freshersparkvm:~/fresherspark$ sudo certbot --nginx -d fresherspark.in -d www.fresherspark.in
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for fresherspark.in and www.fresherspark.in

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/fresherspark.in/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/fresherspark.in/privkey.pem
This certificate expires on 2025-08-07.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for fresherspark.in to /etc/nginx/sites-enabled/default
Successfully deployed certificate for www.fresherspark.in to /etc/nginx/sites-enabled/default
Congratulations! You have successfully enabled HTTPS on https://fresherspark.in and https://www.fresherspark.in

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
azureuser@freshersparkvm:~/fresherspark$
