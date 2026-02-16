# 🚀 Cintabuku - Quick Deployment Guide

Complete automated deployment system untuk Cintabuku e-commerce ke VPS.

---

## 📋 Prerequisites

- ✅ Python 3.8+ dengan pip
- ✅ Domain cintabuku.com di Cloudflare
- ✅ VPS access (103.107.206.10:2480)

### Install Dependencies

```bash
pip install paramiko scp
```

---

## 🎯 Deployment Commands

### 1. Build Production Bundle

```bash
cd d:\uma\cintabuku
python scripts\build_cintabuku.py
```

**Output:** Creates `build_output/` dengan frontend + backend production builds.

### 2. Deploy to VPS

```bash
python scripts\deploy_cintabuku_docker.py
```

Script akan:
- Upload files ke VPS
- Setup Docker containers (PostgreSQL + Backend)
- Configure Nginx routing
- Run database migrations  
- Auto-generate JWT_SECRET & passwords

**Time:** ~10-15 minutes

### 3. Configure DNS

Di Cloudflare Dashboard:

```
Type: A
Name: cintabuku.com
IP: 103.107.206.10
Proxy: ✅ ON (orange cloud)
```

Wait 5-10 minutes untuk DNS propagation.

### 4. Verify

```bash
python scripts\verify_deployment.py
```

Test access:
```
https://cintabuku.com
```

---

## 📁 Generated Files

| File | Purpose |
|------|---------|
| `backend/Dockerfile.production` | Production Docker image |
| `docker-compose.cintabuku.yml` | Service definitions |
| `nginx-cintabuku.conf` | Nginx routing config |
| `scripts/build_cintabuku.py` | Build automation |
| `scripts/deploy_cintabuku_docker.py` | Deployment automation |
| `scripts/verify_deployment.py` | Health check |
| `DEPLOYMENT_GUIDE.md` | Complete manual |
| `CLOUDFLARE_DNS_SETUP.md` | DNS setup guide |

---

## 🏗️ Architecture

```
Cloudflare (SSL + CDN)
    ↓
cintabuku.com → VPS (103.107.206.10)
    ↓
nginx-proxy (Docker)
    ├─ Frontend (Static)
    └─ Backend API → PostgreSQL
```

**VPS Structure:**
```
/home/ubuntu24/my-docker-apps/
├── docker-compose.yml (extended)
├── nginx/nginx.conf (extended)
└── apps/cintabuku/
    ├── frontend/dist/
    ├── backend/
    ├── uploads/
    └── logs/
```

---

## 🔍 Quick Commands

### Check Status
```bash
ssh -p 2480 ubuntu24@103.107.206.10
cd ~/my-docker-apps
sudo docker ps | grep cintabuku
```

### View Logs
```bash
sudo docker logs cintabuku-backend -f
```

### Restart
```bash
sudo docker compose restart cintabuku-backend
```

### Health Check
```bash
curl http://103.107.206.10/health
```

---

## 🛠️ Troubleshooting

**Container not running?**
```bash
sudo docker logs cintabuku-backend
sudo docker compose restart cintabuku-backend
```

**Database issues?**
```bash
sudo docker exec cintabuku-db pg_isready -U cintabuku_user
```

**502 Bad Gateway?**
- Wait 30 seconds (backend starting)
- Check logs: `sudo docker logs cintabuku-backend`

---

## 🔄 Rollback

```bash
ssh -p 2480 ubuntu24@103.107.206.10
cd ~/my-docker-apps

# Stop cintabuku
sudo docker compose stop cintabuku-backend cintabuku-db

# Restore configs (find latest backup timestamp)
cp docker-compose.yml.backup_XXXXXX docker-compose.yml
cp nginx/nginx.conf.backup_XXXXXX nginx/nginx.conf

# Restart nginx
sudo docker compose restart nginx
```

---

## 📖 Full Documentation

- **`DEPLOYMENT_GUIDE.md`** - Complete step-by-step guide
- **`CLOUDFLARE_DNS_SETUP.md`** - Cloudflare configuration
- See walkthrough.md artifact for architecture details

---

## 🎉 Success!

After deployment:
- Frontend: https://cintabuku.com
- Backend API: https://cintabuku.com/api
- Health: https://cintabuku.com/health

**Ready to go live!** 🚀📚
