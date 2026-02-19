# Manual SSL Setup - Direct Commands

## Certificates sudah uploaded! Tinggal configure Nginx.

### Step 1: SSH ke VPS
```bash
ssh -p 2480 ubuntu24@103.107.206.10
# Password: Ubuntu@2025
```

### Step 2: Install Nginx
```bash
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y nginx
```

### Step 3: Create Nginx Config
```bash
sudo tee /etc/nginx/sites-available/cintabuku.com > /dev/null << 'EOF'
# HTTP - Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name cintabuku.com www.cintabuku.com;
    
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
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;

    # Proxy to Backend
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
EOF
```

### Step 4: Enable Site
```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Set Cloudflare SSL Mode
1. https://dash.cloudflare.com
2. SSL/TLS → Mode: **Full (strict)**

### Step 6: Test!
```bash
curl -k https://localhost/health
```

Buka browser: **https://cintabuku.com**

✅ **DONE!**
