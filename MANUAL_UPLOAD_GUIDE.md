# Manual Upload Guide - Cintabuku ke VPS

## 📦 File yang Perlu Di-Upload

**Source Code Archive:**
- File: `cintabuku_source_1771199915.zip` 
- Ukuran: ~1.27 MB
- Lokasi lokal: `d:\uma\cintabuku\cintabuku_source_1771199915.zip`

**Configuration Files:**
- `d:\uma\cintabuku\docker-compose.cintabuku.yml`
- `d:\uma\cintabuku\nginx-cintabuku.conf`
- `d:\uma\cintabuku\backend\Dockerfile.production`

---

## 📍 Direktori Tujuan di VPS

### Upload ke temporary directory dulu:
```
/tmp/cintabuku_deploy/
```

Buat direktori ini di VPS dulu:
```bash
ssh -p 2480 ubuntu24@103.107.206.10
mkdir -p /tmp/cintabuku_deploy
```

---

## 🚀 Cara Upload Manual

### Option 1: Menggunakan WinSCP (Recommended)

1. **Download WinSCP** (jika belum ada): https://winscp.net

2. **Buat New Connection:**
   - File Protocol: `SCP`
   - Host name: `103.107.206.10`
   - Port number: `2480`
   - User name: `ubuntu24`
   - Password: `Ubuntu@2025`

3. **Upload Files:**
   - Klik "Login"
   - Di panel kiri (local): Navigate ke `d:\uma\cintabuku`
   - Di panel kanan (remote): Navigate ke `/tmp/cintabuku_deploy/`
   - Drag & drop file-file ini:
     - `cintabuku_source_1771199915.zip`
     - `docker-compose.cintabuku.yml`
     - `nginx-cintabuku.conf`
     - `backend\Dockerfile.production`

---

### Option 2: Menggunakan Command Line (PowerShell)

```powershell
# Upload source archive
scp -P 2480 d:\uma\cintabuku\cintabuku_source_1771199915.zip ubuntu24@103.107.206.10:/tmp/cintabuku_deploy/

# Upload configs
scp -P 2480 d:\uma\cintabuku\docker-compose.cintabuku.yml ubuntu24@103.107.206.10:/tmp/cintabuku_deploy/
scp -P 2480 d:\uma\cintabuku\nginx-cintabuku.conf ubuntu24@103.107.206.10:/tmp/cintabuku_deploy/
scp -P 2480 d:\uma\cintabuku\backend\Dockerfile.production ubuntu24@103.107.206.10:/tmp/cintabuku_deploy/
```

Password: `Ubuntu@2025`

---

### Option 3: Menggunakan FileZilla

1. **Download FileZilla** (jika belum ada): https://filezilla-project.org

2. **Setup Connection:**
   - Host: `sftp://103.107.206.10`
   - Username: `ubuntu24`
   - Password: `Ubuntu@2025`
   - Port: `2480`

3. **Upload:**
   - Navigate remote directory ke `/tmp/cintabuku_deploy/`
   - Upload semua file yang disebutkan di atas

---

## ✅ Setelah Upload Selesai

SSH ke VPS dan jalankan deployment script:

```bash
ssh -p 2480 ubuntu24@103.107.206.10
```

Lalu jalankan command berikut di VPS:

```bash
# 1. Extract source code
cd /tmp/cintabuku_deploy
unzip -o cintabuku_source_1771199915.zip

# 2. Setup direktori cintabuku
mkdir -p /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend
mkdir -p /home/ubuntu24/my-docker-apps/apps/cintabuku/backend
mkdir -p /home/ubuntu24/my-docker-apps/apps/cintabuku/uploads
mkdir -p /home/ubuntu24/my-docker-apps/apps/cintabuku/logs

# 3. Copy files ke lokasi final
cp -r frontend/* /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/
cp -r backend/* /home/ubuntu24/my-docker-apps/apps/cintabuku/backend/
cp Dockerfile.production /home/ubuntu24/my-docker-apps/apps/cintabuku/backend/

# 4. Set permissions
chmod 755 /home/ubuntu24/my-docker-apps/apps/cintabuku
chmod 777 /home/ubuntu24/my-docker-apps/apps/cintabuku/uploads
chmod 777 /home/ubuntu24/my-docker-apps/apps/cintabuku/logs
```

Setelah itu, saya bisa lanjutkan dengan automated deployment steps via SSH!

---

## 📋 Quick Summary

**Upload ini:**
1. `cintabuku_source_1771199915.zip` → `/tmp/cintabuku_deploy/`
2. `docker-compose.cintabuku.yml` → `/tmp/cintabuku_deploy/`
3. `nginx-cintabuku.conf` → `/tmp/cintabuku_deploy/`
4. `Dockerfile.production` → `/tmp/cintabuku_deploy/`

**Pakai:** WinSCP / FileZilla / SCP command

**Setelah upload:** Kabari saya, lalu saya lanjutkan deployment via script! ✅
