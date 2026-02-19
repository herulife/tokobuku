# Setup SSL dengan Cloudflare Origin Certificate

## 🎯 Overview
Cara ini sama seperti darussunnahparung.com - menggunakan Cloudflare Origin Certificate yang gratis & permanent.

**Keuntungan:**
- ✅ Tidak perlu disable proxy
- ✅ Certificate langsung dari Cloudflare (15 tahun validity)
- ✅ Auto-trusted oleh Cloudflare
- ✅ Setup sekali jadi

---

## Step 1: Generate Certificate di Cloudflare (3 menit)

### 1.1 Login & Navigate
1. Login: https://dash.cloudflare.com
2. Pilih domain: **cintabuku.com**
3. Sidebar → **SSL/TLS**
4. Tab → **Origin Server**

### 1.2 Create Certificate
5. Klik **Create Certificate**

6. Configure:
   - **Private key type:** RSA (2048)
   - **Hostnames:** 
     - `cintabuku.com`
     - `*.cintabuku.com` (wildcard for www, api, etc)
   - **Certificate Validity:** 15 years (default)

7. Klik **Create**

### 1.3 Save Certificate & Key
**IMPORTANT:** Simpan kedua file ini!

**File 1: Origin Certificate**
- Copy seluruh isi (mulai dari `-----BEGIN CERTIFICATE-----`)
- Simpan sebagai: `origin-cert.pem`

**File 2: Private Key**
- Copy seluruh isi (mulai dari `-----BEGIN PRIVATE KEY-----`)
- Simpan sebagai: `private-key.pem`

⚠️ **PENTING:** Private key hanya muncul sekali! Jangan close window sebelum save!

8. Klik **OK** setelah save

---

## Step 2: Upload Certificate ke VPS (5 menit)

### Option A: Via Script (Recommended)

Jalankan script ini dari komputer lokal:

```bash
python scripts/install_cloudflare_ssl.py
```

Script akan:
1. Upload certificates ke VPS
2. Install Nginx
3. Configure untuk HTTPS
4. Test configuration

### Option B: Manual Upload

**2.1 Create Certificate Directory di VPS**
```bash
ssh -p 2480 ubuntu24@103.107.206.10
sudo mkdir -p /etc/ssl/cloudflare
```

**2.2 Upload Files**
Dari komputer lokal (PowerShell):
```powershell
scp -P 2480 origin-cert.pem ubuntu24@103.107.206.10:/tmp/
scp -P 2480 private-key.pem ubuntu24@103.107.206.10:/tmp/
```

**2.3 Move to Proper Location**
Di VPS:
```bash
sudo mv /tmp/origin-cert.pem /etc/ssl/cloudflare/
sudo mv /tmp/private-key.pem /etc/ssl/cloudflare/
sudo chmod 600 /etc/ssl/cloudflare/*
```

---

## Step 3: Install & Configure Nginx (7 menit)

### 3.1 Install Nginx
```bash
ssh -p 2480 ubuntu24@103.107.206.10
sudo apt update
sudo apt install nginx -y
```

### 3.2 Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/cintabuku.com
```

Paste configuration ini:

```nginx
# HTTP - Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name cintabuku.com www.cintabuku.com;
    
    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}

# HTTPS - Main Configuration
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name cintabuku.com www.cintabuku.com;

    # Cloudflare Origin Certificate
    ssl_certificate /etc/ssl/cloudflare/origin-cert.pem;
    ssl_certificate_key /etc/ssl/cloudflare/private-key.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to Backend
    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        
        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        
        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        proxy_cache_bypass $http_upgrade;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:5000/health;
        access_log off;
    }
}
```

Save: `Ctrl+O`, Enter, `Ctrl+X`

### 3.3 Enable Site
```bash
# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Enable cintabuku.com
sudo ln -s /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Step 4: Configure Cloudflare SSL Settings (2 menit)

### 4.1 Set SSL/TLS Mode
1. Cloudflare Dashboard → **SSL/TLS**
2. Overview tab
3. **SSL/TLS encryption mode:** 
   - Select **Full (strict)** ✅
   - (Bukan "Full", harus "Full (strict)")

### 4.2 Verify Settings
- **Proxy Status:** ON (orange cloud) ✅
- **SSL Mode:** Full (strict) ✅
- **Origin Certificate:** Installed ✅

---

## Step 5: Run Database Migrations (2 menit)

```bash
ssh -p 2480 ubuntu24@103.107.206.10
sudo docker exec cintabuku-backend npx prisma migrate deploy
```

---

## Step 6: Test Production! 🎉

### Test URLs:
1. **HTTP Redirect:** http://cintabuku.com
   - Should redirect to HTTPS ✅
   
2. **HTTPS:** https://cintabuku.com
   - Should show your app ✅
   
3. **Health Check:** https://cintabuku.com/health
   - Should return JSON ✅

4. **WWW:** https://www.cintabuku.com
   - Should work sama ✅

### Verify SSL:
```bash
# From VPS
curl -I https://cintabuku.com

# Should show: HTTP/2 200
```

---

## ✅ Success Checklist

- [ ] Origin certificate generated di Cloudflare
- [ ] Certificate & key saved
- [ ] Files uploaded ke VPS
- [ ] Nginx installed
- [ ] Site configured
- [ ] Nginx test passed
- [ ] SSL mode: Full (strict)
- [ ] Proxy: ON (orange cloud)
- [ ] HTTP redirects ke HTTPS
- [ ] HTTPS working
- [ ] Migrations run
- [ ] Production tested

---

## 🔧 Troubleshooting

**"Too many redirects"**
- SSL mode harus **Full (strict)**, bukan "Flexible"

**"Bad Gateway 502"**
- Check backend running: `sudo docker ps`
- Check logs: `sudo docker logs cintabuku-backend`

**Certificate error**
- Verify file paths di nginx config
- Check permissions: `ls -la /etc/ssl/cloudflare/`

**Nginx won't start**
- Test config: `sudo nginx -t`
- Check logs: `sudo tail -f /var/log/nginx/error.log`

---

## 📋 Quick Commands untuk Maintenance

```bash
# Restart Nginx
sudo systemctl restart nginx

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Test Nginx config
sudo nginx -t

# Reload Nginx (no downtime)
sudo systemctl reload nginx

# Check SSL certificate
openssl x509 -in /etc/ssl/cloudflare/origin-cert.pem -text -noout
```

---

**Ready?** Sekarang generate certificate di Cloudflare, lalu jalankan script atau setup manual!
