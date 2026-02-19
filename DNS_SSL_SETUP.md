# DNS & SSL Setup untuk Cintabuku.com

## 📍 Current Status
- Domain: `cintabuku.com`
- Current IP: `104.21.28.125` (Cloudflare)
- Target IP: `103.107.206.10` (VPS kita)
- Backend Running: ✅ http://103.107.206.10:5000

---

## Step 1: Update DNS di Cloudflare (5 menit)

### Login & Navigate
1. Buka: https://dash.cloudflare.com
2. Pilih domain: **cintabuku.com**
3. Klik tab **DNS** di menu samping

### Update A Record
4. Cari record dengan:
   - **Type:** A
   - **Name:** @ atau cintabuku.com
   - **Content:** 104.21.28.125 (IP lama)

5. Klik **Edit** pada record tersebut

6. Update:
   - **IPv4 address:** Ganti ke `103.107.206.10`
   - **Proxy status:** **OFF** (abu-abu/DNS only) untuk install SSL
   - **TTL:** Auto

7. Klik **Save**

### Test DNS Update
Tunggu 5-10 menit, lalu test:
```bash
ping cintabuku.com
```

Harus muncul: `103.107.206.10`

---

## Step 2: Install Nginx + SSL di VPS (15 menit)

### SSH ke VPS
```bash
ssh -p 2480 ubuntu24@103.107.206.10
# Password: Ubuntu@2025
```

### Install Nginx & Certbot
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y
```

### Buat Nginx Config
```bash
sudo nano /etc/nginx/sites-available/cintabuku.com
```

Paste konfigurasi ini:
```nginx
server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;

    # Proxy ke backend
    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Save: `Ctrl+O`, Enter, `Ctrl+X`

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Install SSL Certificate
```bash
sudo certbot --nginx -d cintabuku.com -d www.cintabuku.com
```

Ikuti prompts:
- Email: (masukkan email Bapak)
- Terms: Yes
- Newsletter: No (optional)
- Redirect HTTP to HTTPS: Yes (pilih 2)

---

## Step 3: Enable Cloudflare Proxy (Optional)

Setelah SSL terinstall:

1. Kembali ke Cloudflare DNS
2. Edit A record cintabuku.com
3. **Proxy status:** ON (orange cloud) ☁️
4. Save

5. SSL/TLS Settings:
   - Tab **SSL/TLS**
   - Mode: **Full (strict)**

---

## Step 4: Run Database Migrations

```bash
ssh -p 2480 ubuntu24@103.107.206.10
sudo docker exec cintabuku-backend npx prisma migrate deploy
```

---

## Step 5: Test Production!

### Test URLs:
- http://cintabuku.com (redirect ke https)
- https://cintabuku.com
- https://cintabuku.com/health

### Verify:
```bash
curl https://cintabuku.com/health
```

Should return:
```json
{
  "status": "ok",
  "timestamp": "...",
  "uptime": ...,
  "environment": "production"
}
```

---

## ✅ Checklist

- [ ] DNS updated di Cloudflare
- [ ] Ping test → 103.107.206.10
- [ ] Nginx installed
- [ ] Site config created
- [ ] SSL certificate installed
- [ ] HTTPS working
- [ ] Cloudflare proxy enabled (optional)
- [ ] Migrations run
- [ ] Production tested

---

## 🔧 Troubleshooting

**DNS not updating?**
- Wait 10-15 minutes
- Clear DNS cache: `ipconfig /flushdns` (Windows)
- Try: `nslookup cintabuku.com`

**Certbot fails?**
- Make sure DNS points to VPS (ping test)
- Port 80 must be open
- Nginx must be running

**Nginx error?**
- Check config: `sudo nginx -t`
- Check logs: `sudo tail -f /var/log/nginx/error.log`

**Backend not responding?**
- Check container: `sudo docker ps`
- Check logs: `sudo docker logs cintabuku-backend`

---

**Next:** Saya buatkan script otomatis untuk install Nginx+SSL?
