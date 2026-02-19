import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 MENGUMPULKAN DATA INFRASTRUKTUR VPS\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # 1. PM2 Apps
    print("📋 Mengambil data PM2...")
    stdin, stdout, stderr = client.exec_command("pm2 jlist")
    pm2_data = stdout.read().decode()
    
    # 2. Docker Containers
    print("📋 Mengambil data Docker...")
    stdin, stdout, stderr = client.exec_command("docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'")
    docker_data = stdout.read().decode()
    
    # 3. Nginx Sites
    print("📋 Mengambil data Nginx...")
    stdin, stdout, stderr = client.exec_command("ls -l /etc/nginx/sites-enabled/")
    nginx_enabled = stdout.read().decode()
    stdin, stdout, stderr = client.exec_command("ls /etc/nginx/sites-available/")
    nginx_available = stdout.read().decode()
    
    # 4. Directory Structure (Apps)
    print("📋 Mengambil struktur folder apps...")
    stdin, stdout, stderr = client.exec_command("find /home/ubuntu24/my-docker-apps -maxdepth 4 -not -path '*/.*'")
    folders_data = stdout.read().decode()
    
    # 5. OS & Hardware
    print("📋 Mengambil spek VPS...")
    stdin, stdout, stderr = client.exec_command("lsb_release -d && free -h && df -h /")
    specs_data = stdout.read().decode()

    # Simpan ke file lokal sementara untuk diproses
    with open("vps_raw_data.txt", "w", encoding="utf-8") as f:
        f.write("--- PM2 ---\n")
        f.write(pm2_data + "\n")
        f.write("--- DOCKER ---\n")
        f.write(docker_data + "\n")
        f.write("--- NGINX ---\n")
        f.write(nginx_enabled + "\n")
        f.write("--- AVAILABLE ---\n")
        f.write(nginx_available + "\n")
        f.write("--- FOLDERS ---\n")
        f.write(folders_data + "\n")
        f.write("--- SPECS ---\n")
        f.write(specs_data + "\n")

    print(f"\n✅ Data terkumpul di vps_raw_data.txt")

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
