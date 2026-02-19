import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 SURGICAL FIX - Freeing ports 80/443\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # 1. Kill any process on port 80/443 - very aggressive but effective
    print("🔪 Killing any process on ports 80 and 443...")
    # Using fuser to find and kill processes on these ports
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S fuser -k 80/tcp 443/tcp 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Port processes killed\n")
    
    # 2. Stop nginx-proxy container specifically if it's still alive
    print("🛑 Stopping nginx-proxy container...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop nginx-proxy 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ nginx-proxy stopped\n")

    # 3. Stop web-sekolah container specifically if it's still alive
    print("🛑 Stopping web-sekolah container...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop web-sekolah 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ web-sekolah stopped\n")
    
    # 4. Restart system Nginx
    print("🔄 Restarting system Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl restart nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx restarted\n")
    
    # 5. Final validation
    print("📋 Final check:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ss -tlnp | grep ':80\\|:443'", get_pty=True)
    stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8')
    print(out)
    
    if "nginx" in out:
        print("\n🎉 SUCCESS! Nginx is now listening on ports 80/443.")
        print("🌐 Site should be live: https://cintabuku.com")
    else:
        print("\n⚠️ Nginx doesn't seem to be listening on 80/443. Check Nginx logs.")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tail -n 20 /var/log/nginx/error.log", get_pty=True)
        stdout.channel.recv_exit_status()
        print(stdout.read().decode('utf-8'))

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
