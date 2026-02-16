# 🚀 FINAL STEP: Deploy Cintabuku Using Pre-Built docker-compose.yml

## Situasi Saat Ini

✅ **Sudah Selesai:**
- Code di GitHub: https://github.com/herulife/tokobuku
- Code di VPS: `/home/ubuntu24/my-docker-apps/apps/cintabuku/`
- Environment configured
- Credentials generated

❌ **Yang Masih Perlu:**
- Use pre-built docker-compose configuration (cintabuku already provided this)

---

## ⚡ Solution: Use docker-compose.cintabuku.yml

### Option 1: Deploy Using Separate Compose File (RECOMMENDED) ⭐

File `docker-compose.cintabuku.yml` sudah ada di VPS. Kita tinggal gunakan!

```bash
# SSH to VPS
ssh -p 2480 ubuntu24@103.107.206.10

# Navigate to directory
cd /home/ubuntu24/my-docker-apps/apps/cintabuku

# Start with separate compose file
sudo docker compose -f /home/ubuntu24/my-docker-apps/apps/cintabuku/docker-compose.cintabuku.yml up -d

# Wait for database
sleep 20

# Run migrations
sudo docker exec cintabuku-backend npx prisma migrate deploy

# Check status
sudo docker ps | grep cintabuku
```

**Done! That's it!** 🎉

---

## Verification

```bash
# Check containers
sudo docker ps | grep cintabuku
# Should see:
# cintabuku-backend   Up
# cintabuku-db        Up

# Check logs
sudo docker logs cintabuku-backend --tail 50

# Test health
sudo docker exec cintabuku-backend curl http://localhost:5000/health
```

---

## Next: Configure DNS

1. Login to Cloudflare
2. Add DNS A record:
   - Name: **cintabuku.com** (or @)
   - IPv4: **103.107.206.10**
   - Proxy: **ON** (orange cloud)
3. Visit: `https://cintabuku.com`

---

## Why This Works

The `docker-compose.cintabuku.yml` file is already correct and contains:
- PostgreSQL database service
- Backend with proper build context
- All environment variables
- Correct volumes

No need to merge with main docker-compose.yml - just run it separately!

---

## If You Still Want to Merge

If you prefer to have everything in one docker-compose.yml:

```bash
# Restore backup
cd /home/ubuntu24/my-docker-apps
cp docker-compose.yml.before_fix_* docker-compose.yml

# Use the prepared file from cintabuku directory
cat /home/ubuntu24/my-docker-apps/apps/cintabuku/docker-compose.cintabuku.yml

# Manually copy the services section to main docker-compose.yml
```

But honestly, using `-f docker-compose.cintabuku.yml` is cleaner and easier! ✅
