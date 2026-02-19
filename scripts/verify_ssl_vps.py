import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 VERIFIKASI SSL DI VPS\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Terhubung ke VPS\n")
    
    # 1. Cek isi folder SSL
    print("📋 Mengecek file sertifikat...")
    stdin, stdout, stderr = client.exec_command(f"ls -l /etc/ssl/cloudflare/", get_pty=True)
    print(stdout.read().decode())
    
    # 2. Cek apakah sertifikat bisa dibaca (validasi format)
    print("📋 Validasi sertifikat (OpenSSL)...")
    stdin, stdout, stderr = client.exec_command(f"openssl x509 -in /etc/ssl/cloudflare/origin-cert.pem -text -noout | grep 'Subject:\|Not After'", get_pty=True)
    print(stdout.read().decode())
    
    # 3. Cek konfigurasi Nginx aktif
    print("📋 Mengecek config Nginx aktif...")
    stdin, stdout, stderr = client.exec_command(f"cat /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    print(stdout.read().decode())
    
    # 4. Test Nginx
    print("📋 Mengetes Nginx (sudo)...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    print(stdout.read().decode())
    print(stderr.read().decode())

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
