# AstroJyothi Muhurtha Engine — Technical Installation & Deployment Guide

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS |
| Node.js | 18.x | 20.x LTS |
| RAM | 1 GB | 2 GB |
| CPU | 1 vCPU | 2 vCPUs |
| Disk | 10 GB | 20 GB SSD |
| PHP (WordPress) | 7.4 | 8.2 |
| Nginx | 1.18 | 1.24 |

---

## PART 1: Backend Node.js Setup

### Step 1 — Install Node.js 20.x

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version   # Should print v20.x.x
npm --version    # Should print 10.x.x
```

### Step 2 — Install PM2 globally

```bash
sudo npm install -g pm2
pm2 --version   # Verify installation
```

### Step 3 — Clone & configure project

```bash
sudo mkdir -p /var/www/astrojyothi/backend
sudo chown $USER:$USER /var/www/astrojyothi/backend
cd /var/www/astrojyothi/backend

git clone https://github.com/yourorg/astrojyothi.git .

# Create environment file
cat > .env.production << 'EOF'
NODE_ENV=production
PORT=4000
HOST=127.0.0.1
ALLOWED_ORIGINS=https://astrojyothi.com,https://www.astrojyothi.com
LOG_LEVEL=warn
EOF

chmod 600 .env.production
```

### Step 4 — Install dependencies & build

```bash
cd /var/www/astrojyothi/backend

# Install production dependencies
npm ci --omit=dev

# Build TypeScript
npm run build

# Verify build output
ls dist/
# Expected: app.js  modules/  server.js  types/
```

### Step 5 — Create log directory

```bash
sudo mkdir -p /var/log/astrojyothi
sudo chown $USER:$USER /var/log/astrojyothi
```

### Step 6 — Start with PM2

```bash
cd /var/www/astrojyothi/backend

# Start in production mode (uses ecosystem.config.js)
pm2 start ecosystem.config.js --env production

# Verify all instances are online
pm2 list

# Check logs
pm2 logs astrojyothi-muhurtha --lines 50

# Test health endpoint
curl http://localhost:4000/health
# Expected: {"status":"ok","service":"AstroJyothi Muhurtha Engine","version":"1.0.0"}
```

### Step 7 — Configure PM2 startup on boot

```bash
pm2 startup systemd -u $USER --hp $HOME
# Run the command that PM2 prints

pm2 save
# This saves the current process list for auto-restart on reboot
```

---

## PART 2: Frontend React (Vite) Setup

### Step 1 — Build frontend

```bash
cd /var/www/astrojyothi/frontend

npm ci
npm run build
# Output: dist/ directory

# Verify build
ls dist/
# Expected: index.html  assets/
```

### Step 2 — Configure environment variables for Vite

```bash
# Create .env.production in frontend root
cat > .env.production << 'EOF'
VITE_API_URL=https://api.astrojyothi.com
EOF
```

---

## PART 3: Nginx Reverse Proxy

### Step 1 — Install Nginx

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Step 2 — Install Certbot (SSL/TLS)

```bash
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificates (replace with your domain)
sudo certbot certonly --nginx \
  -d astrojyothi.com \
  -d www.astrojyothi.com \
  -d api.astrojyothi.com \
  --email your-email@domain.com \
  --agree-tos \
  --non-interactive
```

### Step 3 — Install Nginx configuration

```bash
sudo cp /var/www/astrojyothi/backend/nginx/muhurtha.conf /etc/nginx/conf.d/muhurtha.conf

# Test configuration syntax
sudo nginx -t
# Expected: nginx: configuration file /etc/nginx/nginx.conf test is successful

# Reload Nginx
sudo systemctl reload nginx
```

### Step 4 — Verify endpoints

```bash
# Test API through Nginx
curl https://api.astrojyothi.com/health

# Test categories endpoint
curl https://api.astrojyothi.com/api/muhurtha/categories

# Test muhurtha search
curl -X POST https://api.astrojyothi.com/api/muhurtha/search \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-14",
    "time": "10:30",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata",
    "category": "marriage"
  }'
```

---

## PART 4: WordPress Plugin Installation

### Step 1 — Copy plugin files

```bash
# Copy plugin to WordPress installation
sudo cp -r /var/www/astrojyothi/backend/wp-content/plugins/astrojyothi-muhurtha \
           /var/www/html/wp-content/plugins/

sudo chown -R www-data:www-data /var/www/html/wp-content/plugins/astrojyothi-muhurtha
```

### Step 2 — Activate in WordPress Admin

1. Log in to **WordPress Admin** → **Plugins** → **Installed Plugins**
2. Find **AstroJyothi Muhurtha Engine** and click **Activate**

### Step 3 — Configure plugin settings

1. Navigate to **Settings** → **AstroJyothi Muhurtha**
2. Set **Backend URL**: `https://api.astrojyothi.com`
3. Set **API Timeout**: `30` (seconds)
4. Click **Save Changes**

### Step 4 — Test WordPress REST endpoints

```bash
# Test categories via WordPress REST API
curl https://yourwordpresssite.com/wp-json/astrojyothi/v1/muhurtha/categories

# Test search via WordPress REST API
curl -X POST https://yourwordpresssite.com/wp-json/astrojyothi/v1/muhurtha/search \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-14",
    "time": "10:30",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata",
    "category": "marriage"
  }'
```

---

## PART 5: PM2 Management Commands

```bash
# View all running processes
pm2 list

# View real-time logs
pm2 logs astrojyothi-muhurtha

# View real-time monitoring dashboard
pm2 monit

# Restart after code update
pm2 restart astrojyothi-muhurtha

# Zero-downtime reload (keeps existing connections alive)
pm2 reload astrojyothi-muhurtha

# Stop
pm2 stop astrojyothi-muhurtha

# Delete from PM2 (does not delete files)
pm2 delete astrojyothi-muhurtha

# View process details
pm2 show astrojyothi-muhurtha

# Flush logs
pm2 flush astrojyothi-muhurtha
```

---

## PART 6: Updating the Application

```bash
cd /var/www/astrojyothi/backend

# Pull latest code
git pull origin main

# Install any new dependencies
npm ci --omit=dev

# Rebuild TypeScript
npm run build

# Zero-downtime reload
pm2 reload ecosystem.config.js --env production

# Verify health
curl http://localhost:4000/health
```

---

## PART 7: Log Rotation

```bash
# Install logrotate config
cat > /etc/logrotate.d/astrojyothi << 'EOF'
/var/log/astrojyothi/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    copytruncate
    sharedscripts
    postrotate
        pm2 reloadLogs
    endscript
}
EOF
```

---

## PART 8: Security Checklist

- [ ] `.env.production` permissions set to `600`
- [ ] SSL/TLS certificates installed (Let's Encrypt or commercial)
- [ ] Nginx rate limiting configured (30 req/min for API endpoints)
- [ ] `ALLOWED_ORIGINS` set to production domains only
- [ ] WordPress plugin `astrojyothi_api_key` set in options table
- [ ] PM2 runs as non-root user
- [ ] UFW firewall: only ports 80, 443, 22 (SSH) open
- [ ] Regular `npm audit` checks scheduled

---

## PART 9: Monitoring & Alerting

```bash
# PM2 with keymetrics (optional cloud monitoring)
pm2 link <secret> <public>

# Health check cron (every 5 minutes)
echo "*/5 * * * * curl -sf http://localhost:4000/health > /dev/null || pm2 restart astrojyothi-muhurtha" | crontab -

# Disk & memory alerts via UptimeRobot or similar:
# Monitor: https://api.astrojyothi.com/health
# Expected response: {"status":"ok"}
```

---

## Quick Reference: API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/muhurtha/categories` | All 37 muhurtha categories |
| POST | `/api/muhurtha/search` | Muhurtha evaluation with score & windows |
| POST | `/api/muhurtha/details` | Full rule-by-rule breakdown |
| POST | `/api/muhurtha/ai` | AI-optimized JSON for LLM consumption |
| GET | `/wp-json/astrojyothi/v1/muhurtha/categories` | WordPress bridge — categories |
| POST | `/wp-json/astrojyothi/v1/muhurtha/search` | WordPress bridge — search |
| POST | `/wp-json/astrojyothi/v1/muhurtha/details` | WordPress bridge — details |
| POST | `/wp-json/astrojyothi/v1/muhurtha/ai` | WordPress bridge — AI payload |
