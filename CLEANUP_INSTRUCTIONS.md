
# Daftar File/Folder yang Bisa Dihapus di VPS

Berikut adalah daftar file dan folder yang teridentifikasi sebagai file sementara atau backup lama yang aman untuk dihapus.

**Lokasi: `/home/ubuntu24/my-docker-apps`**

1.  **Backup Docker Compose Lama:**
    - `docker-compose.yml.backup_1771202093`
    - `docker-compose.yml.bak`
    - `docker-compose.yml.before_fix_1771207479`

2.  **File Konfigurasi Sementara:**
    - `uploads.ini.bak_limit`

**Lokasi: `/tmp` (Folder Sementara)**
- Semua file berekstensi `.ts`, `.b64`, `.py`, `.zip` yang merupakan sisa proses upload deployment sebelumnya.

---

## Perintah Hapus (Syntax)

Anda dapat menjalankan perintah berikut di terminal VPS untuk menghapus file-file tersebut sekaligus:

```bash
# Masuk ke direktori aplikasi
cd /home/ubuntu24/my-docker-apps

# Hapus backup docker-compose lama
rm docker-compose.yml.backup_* docker-compose.yml.bak docker-compose.yml.before_fix_*

# Hapus backup konfigurasi lain
rm uploads.ini.bak_limit

# Bersihkan folder tmp (HATI-HATI: pastikan tidak ada proses lain yang butuh)
sudo rm -f /tmp/*.ts /tmp/*.b64 /tmp/*.zip /tmp/*.tar.gz /tmp/*.py
```

---

## Informasi Tambahan: Sinkronisasi Darussunnah2
Saya juga telah menyiapkan konfigurasi untuk menyinkronkan folder lokal `darussunnah2` ke VPS (`web-sekolah`). Jika Anda ingin melanjutkan proses sinkronisasi ini, jalankan script deployment yang akan saya buatkan sesaat lagi.
