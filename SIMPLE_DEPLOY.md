# 🎯 SIMPLE SOLUTION - 3 Commands to Deploy Cintabuku

## Situasi

✅ **Berhasil:**
- Code di VPS: `/home/ubuntu24/my-docker-apps/apps/cintabuku`
- `.env` configured
- Database password ready

❌ **Issue:** 
Docker compose merge automation complex

✅ **Solusi:**
Start containers langsung via Docker (skip docker-compose)

---

## ⚡ 3 Commands - Done!

### COPY PASTE INI KE SSH:

```bash
# 1. SSH to VPS
ssh -p 2480 ubuntu24@103.107.206.10

# 2. Start Database
sudo docker run -d \
  --name cintabuku-db \
  --restart always \
  -e POSTGRES_USER=cintabuku_user \
  -e POSTGRES_PASSWORD=aW!R^3K4t%oMbM@4zL@1oO16 \
  -e POSTGRES_DB=cintabuku \
  -v cintabuku_db:/var/lib/postgresql/data \
  -p 5433:5432 \
  postgres:15-alpine

# 3. Build Backend
cd /home/ubuntu24/my-docker-apps/apps/cintabuku/backend
sudo docker build -t cintabuku-backend -f Dockerfile .

# 4. Start Backend
sudo docker run -d \
  --name cintabuku-backend \
  --restart always \
  --env-file /home/ubuntu24/my-docker-apps/apps/cintabuku/backend/.env \
  -v /home/ubuntu24/my-docker-apps/apps/cintabuku/uploads:/app/uploads \
  -v /home/ubuntu24/my-docker-apps/apps/cintabuku/logs:/app/logs \
  -p 5000:5000 \
  --link cintabuku-db:cintabuku-db \
  cintabuku-backend

# 5. Run Migrations
sleep 10
sudo docker exec cintabuku-backend npx prisma migrate deploy

# 6. Check Status
sudo docker ps | grep cintabuku
```

**DONE!** ✅

---

## Verify

```bash
# Check containers
sudo docker ps

# Check logs
sudo docker logs cintabuku-backend

# Test API
curl http://localhost:5000/health
```

---

## Next: DNS

1. Cloudflare → DNS Settings
2. Add A record:
   - Name: `cintabuku.com`
   - IPv4: `103.107.206.10`
   - Proxy: ON
3. Wait 10 minutes
4. Visit: `https://cintabuku.com`

---

## Why This Works

- No docker-compose conflicts
- Direct Docker commands
- Simple & reliable
- All dependencies in place

**Time:** 5 minutes total! 🚀
