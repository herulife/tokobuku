# Cloudflare DNS Setup - cintabuku.com

## Step 1: DNS A Record

Di Cloudflare Dashboard → DNS → Records:

### Add A Record:
```
Type: A
Name: @ (root domain)
IPv4 address: 103.107.206.10
Proxy status: ✅ Proxied (orange cloud)
TTL: Auto
```

### Add www subdomain (optional):
```
Type: CNAME
Name: www
Target: cintabuku.com
Proxy status: ✅ Proxied
TTL: Auto
```

**Result:**
- `cintabuku.com` → 103.107.206.10
- `www.cintabuku.com` → cintabuku.com → 103.107.206.10

---

## Step 2: SSL/TLS Configuration

Di Cloudflare Dashboard → SSL/TLS:

### Overview:
- **Encryption Mode:** Full (strict) ✅
  
### Edge Certificates:
- ✅ Always Use HTTPS: ON
- ✅ Automatic HTTPS Rewrites: ON
- ✅ Minimum TLS Version: TLS 1.2
- ✅ Opportunistic Encryption: ON
- ✅ TLS 1.3: ON

**Certificate:** Universal SSL certificate (auto-generated oleh Cloudflare)

---

## Step 3: Security Settings

### Firewall Rules (Optional):
Di Cloudflare Dashboard → Security → WAF:

```
Rule 1: Block bad bots
Expression: (cf.bot_management.score lt 30)
Action: Block

Rule 2: Rate limiting backup (jika perlu)
Expression: (http.request.uri.path contains "/api/")
Action: Challenge if > 100 req/min
```

### Security Level:
- Medium (recommended) atau High

---

## Step 4: Performance Optimization

### Caching:
Di Cloudflare Dashboard → Caching → Configuration:

- **Caching Level:** Standard
- **Browser Cache TTL:** 4 hours

### Add Page Rules:
```
Rule 1: Static Assets
URL: cintabuku.com/assets/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 1 month

Rule 2: API No Cache
URL: cintabuku.com/api/*
Settings:
  - Cache Level: Bypass
```

---

## Step 5: Speed Optimization

Di Cloudflare Dashboard → Speed:

- ✅ Auto Minify: JavaScript, CSS, HTML
- ✅ Brotli: ON
- ✅ Early Hints: ON
- ✅ Rocket Loader: OFF (untuk React/Next.js)

---

## DNS Propagation Check

Setelah setup, verify DNS sudah propagate:

```bash
# Windows PowerShell
nslookup cintabuku.com

# Atau online tools:
# https://dnschecker.org/#A/cintabuku.com
# https://www.whatsmydns.net/#A/cintabuku.com
```

**Expected result:**
```
Name:    cintabuku.com
Address: 103.107.206.10 (via Cloudflare proxy)
```

---

## Cloudflare Benefits for Cintabuku

✅ **Free SSL Certificate** - HTTPS otomatis  
✅ **Global CDN** - Assets di-cache di 300+ data centers worldwide  
✅ **DDoS Protection** - Auto mitigation  
✅ **Always Online** - Serve cached version jika VPS down  
✅ **Analytics** - Traffic insights gratis  
✅ **Firewall** - WAF untuk block malicious traffic  

---

## Next Steps After DNS Setup

1. ⏳ Wait 5-10 minutes untuk DNS propagation
2. ✅ Verify domain resolves to VPS IP
3. 🚀 Deploy aplikasi ke VPS
4. 🔧 Configure Nginx dengan domain cintabuku.com
5. ✅ Test HTTP access (Cloudflare auto-redirect ke HTTPS)
6. 🎉 Production ready!

**Note:** Cloudflare akan auto-handle SSL certificate, jadi tidak perlu setup Certbot manual di VPS!
