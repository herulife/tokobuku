# 🚀 Cintabuku - Deployment Guide

Complete guide untuk deploy aplikasi Cintabuku e-commerce ke VPS.

---

## 📋 Prerequisites

✅ Domain `cintabuku.com` sudah di Cloudflare  
✅ VPS accessible (103.107.206.10:2480)  
✅ Python 3.8+ installed locally  
✅ Dependencies: `pip install paramiko scp`  

---

## 🏗️ Step 1: Build Production Bundle

```bash
cd d:\uma\cintabuku
python scripts\build_cintabuku.py
```

**What it does:**
- Cleans previous builds
- Builds Next.js frontend (`npm run build`)
- Compiles TypeScript backend (`npm run build`)
- Generates Prisma client
- Packages everything into `build_output/`

**Expected output:**
```
✅ Frontend build complete
✅ Backend build complete
✅ Prisma client generated
✅ Build Complete!

📊 Build Sizes:
   Frontend: ~10 MB
   Backend:  ~15 MB
   Total:    ~25 MB
```

---

## 🚀 Step 2: Deploy to VPS

```bash
python scripts\deploy_cintabuku_docker.py
```

**Confirmation prompt:**
```
📡 Target VPS: 103.107.206.10
📁 Deployment path: /home/ubuntu24/my-docker-apps/apps/cintabuku

⚠️  Continue with deployment? [y/N]:
```

Type `y` and press Enter.

### Deployment Steps (Automated):

**Step 1-5: Upload & Extract**
- Creates deployment archive ZIP
- Uploads to VPS `/tmp/`
- Extracts to `/home/ubuntu24/my-docker-apps/apps/cintabuku/`
- Organizes frontend, backend, uploads, logs folders

**Step 6: Environment Configuration**
- Auto-generates strong JWT_SECRET (40 chars)
- Auto-generates PostgreSQL password (24 chars)
- Reads KOMSHIP_API_KEY from local .env
- Creates `.env.production` on VPS

**Step 7-8: Configuration Updates**
- Merges cintabuku services into `docker-compose.yml`
- Backs up original config (`docker-compose.yml.backup_TIMESTAMP`)
- Appends cintabuku server block to nginx.conf
- Backs up nginx config (`nginx.conf.backup_TIMESTAMP`)

**Step 9-10: Docker Deployment**
- Builds `cintabuku-backend` Docker image
- Starts `cintabuku-db` (PostgreSQL container)
- Waits 10 seconds for DB ready
- Starts `cintabuku-backend` container
- Runs Prisma migrations (`migrate deploy`)
- Seeds database (`db seed`)

**Step 11: Nginx Restart**
- Restarts nginx-proxy to load new routing

**Step 12: Verification**
- Checks container status
- Tests database connection
- Calls backend health endpoint

**Step 13: Cleanup**
- Removes local ZIP archive
- Removes temp files on VPS

---

## 🌐 Step 3: Configure Cloudflare DNS

### In Cloudflare Dashboard:

1. Go to **DNS > Records**
2. Add A Record:
   ```
   Type: A
   Name: @ (or cintabuku.com)
   IPv4: 103.107.206.10
   Proxy: ✅ Proxied (orange cloud)
   TTL: Auto
   ```

3. (Optional) Add www:
   ```
   Type: CNAME
   Name: www
   Target: cintabuku.com
   Proxy: ✅ Proxied
   ```

### SSL/TLS Settings:

1. Go to **SSL/TLS > Overview**
2. Set Encryption Mode: **Full** (or Full Strict)
3. Go to **Edge Certificates**
4. Enable:
   - ✅ Always Use HTTPS
   - ✅ Automatic HTTPS Rewrites
   - ✅ TLS 1.3

### Performance (Optional):

1. Go to **Speed > Optimization**
2. Enable:
   - ✅ Auto Minify (JS, CSS, HTML)
   - ✅ Brotli
   - ✅ Early Hints

---

## ✅ Step 4: Verify Deployment

### Wait for DNS Propagation

Check if DNS has propagated (5-10 minutes):

```bash
nslookup cintabuku.com
```

Expected: IP should be Cloudflare proxy IP (not 103.107.206.10 directly)

### Test Access

**Via IP (immediate):**
```
http://103.107.206.10/health
```

**Via Domain (after DNS):**
```
https://cintabuku.com
```

Cloudflare will auto-redirect HTTP → HTTPS.

---

## 🔍 Monitoring & Logs

### Check Container Status

SSH to VPS:
```bash
ssh -p 2480 ubuntu24@103.107.206.10
```

Check running containers:
```bash
cd ~/my-docker-apps
sudo docker ps | grep cintabuku
```

Expected output:
```
cintabuku-backend   Up X minutes   5000/tcp
cintabuku-db        Up X minutes   5432/tcp
```

### View Logs

**Backend logs:**
```bash
sudo docker logs cintabuku-backend -f
```

**Database logs:**
```bash
sudo docker logs cintabuku-db -f
```

**All containers:**
```bash
sudo docker compose logs -f cintabuku-backend cintabuku-db
```

**Log files on VPS:**
```bash
tail -f ~/my-docker-apps/apps/cintabuku/logs/error.log
tail -f ~/my-docker-apps/apps/cintabuku/logs/combined.log
```

---

## 🐛 Troubleshooting

### Container not starting?

```bash
# Check container status
sudo docker ps -a | grep cintabuku

# Check logs for errors
sudo docker logs cintabuku-backend

# Restart container
cd ~/my-docker-apps
sudo docker compose restart cintabuku-backend
```

### Database connection issues?

```bash
# Check if database is ready
sudo docker exec cintabuku-db pg_isready -U cintabuku_user

# Check database exists
sudo docker exec cintabuku-db psql -U cintabuku_user -l

# Re-run migrations
sudo docker exec cintabuku-backend npx prisma migrate deploy
```

### Nginx not routing?

```bash
# Test nginx config
sudo docker exec nginx-proxy nginx -t

# Check nginx logs
sudo docker logs nginx-proxy -f

# Restart nginx
cd ~/my-docker-apps
sudo docker compose restart nginx
```

### 502 Bad Gateway?

Usually means backend not ready yet. Wait 30 seconds and retry.

If persists:
```bash
# Check backend is listening
sudo docker exec cintabuku-backend netstat -tlnp | grep 5000

# Check health endpoint
sudo docker exec cintabuku-backend wget -q -O- http://localhost:5000/health
```

---

## 🔄 Rollback Plan

If deployment fails, rollback is safe:

```bash
# SSH to VPS
ssh -p 2480 ubuntu24@103.107.206.10

# Stop cintabuku containers
cd ~/my-docker-apps
sudo docker compose stop cintabuku-backend cintabuku-db

# Restore configs (find latest backup)
ls -lt docker-compose.yml.backup_*
cp docker-compose.yml.backup_XXXXXXX docker-compose.yml

ls -lt nginx/nginx.conf.backup_*
cp nginx/nginx.conf.backup_XXXXXXX nginx/nginx.conf

# Restart nginx
sudo docker compose restart nginx

# (Optional) Remove containers completely
sudo docker compose rm -f cintabuku-backend cintabuku-db
sudo docker volume rm my-docker-apps_cintabuku_db
```

**No impact on existing services!** Other websites continue running.

---

## 🔐 Security Notes

**Generated Secrets:**
- JWT_SECRET: 40 characters, crypto-random
- DB_PASSWORD: 24 characters, crypto-random

**Environment Files:**
- `.env.production` on VPS contains sensitive data
- Only readable by ubuntu24 user
- Not exposed in Docker images

**Cloudflare Protection:**
- DDoS protection enabled
- WAF rules active
- SSL/TLS encryption
- Rate limiting via Cloudflare + backend

---

## 📊 Post-Deployment Checklist

After deployment completes:

- [ ] DNS propagated (test `nslookup cintabuku.com`)
- [ ] HTTPS accessible (`https://cintabuku.com`)
- [ ] Homepage loads correctly
- [ ] Product listing works
- [ ] Cart functionality working
- [ ] Checkout flow completes
- [ ] Admin login works
- [ ] Image uploads functional
- [ ] API rate limiting active (test with 100+ requests)
- [ ] Health check returns 200 (`/health`)
- [ ] Logs being written (`~/my-docker-apps/apps/cintabuku/logs/`)

---

## 🎯 Architecture Summary

```
Cloudflare (CDN + SSL + DDoS)
    ↓
cintabuku.com → 103.107.206.10:80/443
    ↓
nginx-proxy (Docker)
    ↓ /api/*
    cintabuku-backend:5000 (Node.js + Express)
        ↓
    cintabuku-db:5432 (PostgreSQL)
    
    ↓ /*
    Static files (/usr/share/nginx/html/cintabuku)
    
    ↓ /uploads/*
    Upload directory (/usr/share/nginx/html/cintabuku-uploads)
```

---

## 📞 Support Commands

**Quick health check:**
```bash
curl http://103.107.206.10/health
```

**Database check:**
```bash
ssh -p 2480 ubuntu24@103.107.206.10 \
  "sudo docker exec cintabuku-db psql -U cintabuku_user -d cintabuku -c 'SELECT COUNT(*) FROM \"User\";'"
```

**Restart all cintabuku services:**
```bash
ssh -p 2480 ubuntu24@103.107.206.10 \
  "cd ~/my-docker-apps && sudo docker compose restart cintabuku-backend cintabuku-db"
```

---

## 🎉 Success!

If all checks pass, your Cintabuku e-commerce platform is now live at:

### 🌐 https://cintabuku.com

Congratulations! 🚀📚
