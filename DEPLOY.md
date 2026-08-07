# Production Deployment Instructions: `bahari_inventory` on Hostinger (`inventory.tamris.org`)

Follow these commands on your Hostinger server to deploy `bahari_inventory` with Docker, Nginx, and Let's Encrypt SSL.

---

### Step 1: Create Nginx Site Configuration

Create the reverse proxy configuration for Nginx mapping port `8085`:

```bash
cat << 'EOF' > /etc/nginx/sites-available/inventory.tamris.org.conf
server {
    listen 80;
    server_name inventory.tamris.org www.inventory.tamris.org;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8085;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

---

### Step 2: Enable Configuration and Reload Nginx

```bash
# Enable the configuration site
ln -sf /etc/nginx/sites-available/inventory.tamris.org.conf /etc/nginx/sites-enabled/

# Test Nginx syntax
nginx -t

# Reload Nginx
systemctl reload nginx
```

---

### Step 3: Clone Code & Start Docker Containers

Navigate to your target directory on the server and launch Docker Compose:

```bash
# Clone repository if not already present
cd ~/projects/
git clone <your-bahari-inventory-repo-url> bahari_inventory
cd bahari_inventory

# Start Docker containers in background
docker compose up -d --build
```

---

### Step 4: Verify Container Status & Create Superuser

```bash
# View running containers
docker compose ps

# Create Admin Superuser inside running web container
docker compose exec web python manage.py createsuperuser
```

---

### Step 5: Issue / Update SSL Certificate with Certbot

Run Certbot to update your SSL certificates including `inventory.tamris.org`:

```bash
certbot --nginx \
  -d tamris.org -d www.tamris.org \
  -d live.tamris.org -d www.live.tamris.org \
  -d demo.tamris.org -d www.demo.tamris.org \
  -d rtis.tamris.org -d www.rtis.tamris.org \
  -d todolist.tamris.org -d www.todolist.tamris.org \
  -d inventory.tamris.org -d www.inventory.tamris.org
```
