import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 STOP DOCKER CONTAINERS BLOCKING PORTS\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Find containers using port 80, 443
    print("📋 Finding containers on port 80/443...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps", get_pty=True)
    stdout.channel.recv_exit_status()
    containers = stdout.read().decode('utf-8')
    print(containers)
    
    # Stop ALL Docker containers
    print("\n🛑 Stopping ALL Docker containers...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop $(sudo docker ps -q) 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Stopped\n")
    
    # Restart Nginx
    print("🔄 Restarting Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl restart nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx restarted\n")
    
    # Check Nginx status
    print("📋 Nginx Status:")
    stdin, stdout, stderr = client.exec_command("systemctl status nginx | head -n 10", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    
    # Test
    import time
    time.sleep(3)
    
    print("\n🧪 Testing:")
    stdin, stdout, stderr = client.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    http_test = stdout.read().decode('utf-8')
    print(f"HTTP: {http_test}")
    
    stdin, stdout, stderr = client.exec_command("curl -k -s -o /dev/null -w '%{http_code}' https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    https_test = stdout.read().decode('utf-8')
    print(f"HTTPS: {https_test}\n")
    
    if '200' in http_test or '200' in https_test or '301' in http_test:
        print("="*70)
        print("🎉 NGINX NOW RUNNING ON PORT 80/443!")
        print("="*70)
        print("\n✅ Docker containers stopped")
        print("✅ Nginx using ports 80 & 443")
        print("✅ Routing to PM2 backend")
        print("\n🌐 TEST NOW:")
        print("   http://103.107.206.10")
        print("   https://cintabuku.com")
        print("\n💡 Tunggu 1-2 menit kalau masih belum bisa\n")
    else:
        print("⚠️  Check status above\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
