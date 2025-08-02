# 🚀 Django Docker App Deployment with NGINX + HTTPS on Azure VM

## 🧾 Prerequisites

- Azure VM with public IP and Ubuntu installed
- Docker & Docker Compose installed
- Django running inside a Docker container (mapped to port 8000)
- Domain purchased from GoDaddy (e.g. `fresherspark.in`)

---

## 1️⃣ Point GoDaddy Domain to Azure VM

### A. Update DNS Records

Log in to **GoDaddy DNS settings** and set:

| Type | Host | Value (Azure VM IP) | TTL  |
|------|------|----------------------|------|
| A    | @    | `<your-public-IP>`   | 600  |
| A    | www  | `<your-public-IP>`   | 600  |

Wait for propagation (~5–10 mins).

---

## 2️⃣ Install & Enable NGINX on VM

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl enable nginx
```

Check status:
```bash
sudo systemctl status nginx
```

---

## 3️⃣ Create NGINX HTML Directory (Optional)

```bash
sudo mkdir -p /var/www/fresherspark.in/html
sudo nano /var/www/fresherspark.in/html/index.html
```

Example content for testing:
```html
<html><h1>Welcome to fresherspark.in</h1></html>
```

---

## 4️⃣ Configure NGINX for Your Domain

```bash
sudo nano /etc/nginx/sites-available/fresherspark.in
```

Paste this config (update paths if needed):

```nginx
server {
    listen 80;
    server_name fresherspark.in www.fresherspark.in;

    location /static/ {
        alias /var/www/job_portal/static/;
    }

    location /media/ {
        alias /var/www/job_portal/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the config:
```bash
sudo ln -s /etc/nginx/sites-available/fresherspark.in /etc/nginx/sites-enabled/
```

Test & restart:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 5️⃣ Ensure Django is Running in Docker

Check container:
```bash
docker ps
```

You should see:
```
0.0.0.0:8000->8000/tcp
```

---

## 6️⃣ Update `ALLOWED_HOSTS` in Django

Edit your `settings.py`:
```python
ALLOWED_HOSTS = ['fresherspark.in', 'www.fresherspark.in']
```

Restart the container:
```bash
docker restart <container_name_or_id>
```

---

## 7️⃣ Install HTTPS (SSL) with Certbot

Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx -y
```

Generate SSL cert:
```bash
sudo certbot --nginx -d fresherspark.in -d www.fresherspark.in
```

Certbot will:
- Generate SSL certificate
- Auto-update NGINX config for HTTPS
- Set up auto-renewal

Test HTTPS:
```bash
curl -I https://fresherspark.in
```

Expected:
```
HTTP/1.1 200 OK
```

---

## 8️⃣ Auto-Renewal Test (Optional)

Let’s Encrypt certificates expire every 90 days. Test renewal:
```bash
sudo certbot renew --dry-run
```

---

## ✅ Success!

Your Django site is now live at:

🔗 [https://fresherspark.in](https://fresherspark.in)

With:
- Dockerized backend
- NGINX reverse proxy
- HTTPS via Let's Encrypt