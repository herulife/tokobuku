# Dokumentasi Infrastruktur VPS - Cintabuku & Multi-Apps

Dokumen ini berisi rincian teknis mengenai struktur server, aplikasi yang berjalan, dan konfigurasi penting untuk mempermudah pemeliharaan (maintenance) dan troubleshooting di masa mendatang.

---

## 🖥️ Informasi Server (VPS)
- **Sistem Operasi:** Ubuntu 22.04.5 LTS (Jammy Jellyfish)
- **User Utama:** `ubuntu24`
- **Direktori Utama Projek:** `/home/ubuntu24/my-docker-apps`
- **Manajer Proses:** PM2 (untuk Node.js) & Docker (untuk DB & WP)
- **Web Server:** Nginx (Sistem Native)

---

## 🌐 Daftar Website & Layanan

### 1. Cintabuku (Utama)
Aplikasi E-commerce Buku (Fullstack JavaScript).
- **Domain:** [https://cintabuku.com](https://cintabuku.com)
- **Frontend:** Next.js (Port 3000 via PM2)
  - Lokasi: `/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend`
- **Backend (API):** Express.js (Port 5000 via PM2)
  - Lokasi: `/home/ubuntu24/my-docker-apps/apps/cintabuku/backend`
- **Database:** PostgreSQL (Port 5433 via Docker)
  - Nama Container: `cintabuku-db`

### 2. WordPress (Multi-Site)
- **WordPress 1 (Default):** Menggunakan PHP-FPM & MariaDB.
- **WordPress Yestina:** [https://yestina.my.id](https://yestina.my.id) (Container: `wordpress-yestina`)
- **Database WP:** MariaDB (Container: `wordpress-db`)

### 3. Aplikasi Lainnya
- **E-Raport:** Berjalan di Port 3001 (Container: `web-eraport`)
- **Web Sekolah:** Lokasi `/home/ubuntu24/my-docker-apps/apps/web-sekolah`
- **PHPMyAdmin:** Diakses via Port 8080 (Container: `phpmyadmin`)

---

## 📂 Struktur Folder Penting

```text
/home/ubuntu24/my-docker-apps/
├── apps/
│   ├── cintabuku/              # Projek Utama Cintabuku
│   │   ├── frontend/           # Source code Next.js
│   │   ├── backend/            # Source code Express & Prisma
│   │   └── uploads/            # Folder penyimpanan gambar buku/user
│   ├── web-sekolah/            # Website profil sekolah
│   ├── web-eraport/            # Aplikasi E-Raport
│   └── web-ppdb/               # Aplikasi PPDB
├── wordpress/                  # File inti WordPress
└── docker-compose.yml          # Konfigurasi container DB & WP
```

---

## 🔧 Konfigurasi Nginx & SSL

- **File Konfigurasi:** `/etc/nginx/sites-available/cintabuku.com`
- **Fungsi:** Mengatur reverse proxy dari Port 80/443 ke Port 3000 (UI) & 5000 (API).
- **SSL:** Menggunakan **Sertifikat Origin Cloudflare**.
  - Lokasi Cert: `/etc/ssl/cloudflare/origin-cert.pem`
  - Lokasi Key: `/etc/ssl/cloudflare/private-key.pem`
  - **PENTING:** Cloudflare SSL Mode harus diset ke **Full (Strict)**.

---

## 💡 Perintah Troubleshooting Cepat

### Mengelola Aplikasi Node.js (Cintabuku)
```bash
# Melihat aplikasi yang jalan
pm2 status

# Restart UI/API jika ada error
pm2 restart cintabuku-frontend
pm2 restart cintabuku-backend

# Melihat log error secara real-time
pm2 logs
```

### Mengelola Database & WordPress (Docker)
```bash
# Melihat container yang jalan
docker ps

# Restart database jika koneksi putus
docker restart cintabuku-db

# Melihat log database
docker logs cintabuku-db
```

### Mengelola Web Server (Nginx)
```bash
# Tes konfigurasi (lakukan ini sebelum restart)
sudo nginx -t

# Reload konfigurasi setelah perubahan
sudo systemctl reload nginx
```

---
*Dibuat oleh: Antigravity AI (16 Februari 2026)*
