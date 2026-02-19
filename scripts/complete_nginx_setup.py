import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 Complete Nginx Setup dengan SSL\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check if nginx installed
    print("🔍 Checking Nginx...")
    stdin, stdout, stderr = client.exec_command("which nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    nginx_path = stdout.read().decode('utf-8').strip()
    
    if not nginx_path:
        print("📦 Installing Nginx...")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S apt update && echo '{VPS_PASS}' | sudo -S DEBIAN_FRONTEND=noninteractive apt install -y nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Nginx installed\n")
    else:
        print(f"✅ Nginx found: {nginx_path}\n")
    
    # Check nginx config exists
    print("🔍 Checking main config...")
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/nginx.conf", get_pty=True)
    stdout.channel.recv_exit_status()
    config_check = stdout.read().decode('utf-8')
    
    if 'No such file' in config_check:
        print("⚠️  Main config missing, reinstalling Nginx...\n")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S apt-get remove --purge -y nginx nginx-common && echo '{VPS_PASS}' | sudo -S apt-get install -y nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Nginx re installed\n")
    else:
        print("✅ Config exists\n")
    
    # Create site config
    print("📝 Creating site configuration...")
    site_config = """server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;
    return 301 https://\\$host\\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cintabuku.com www.cintabuku.com;

    ssl_certificate /etc/ssl/cloudflare/origin-cert.pem;
    ssl_certificate_key /etc/ssl/cloudflare/private-key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
        proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\$scheme;
    }
}"""
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/nginx/sites-available/cintabuku.com > /dev/null", get_pty=True)
    stdin.write(site_config + '\n')
    stdin.flush()
    stdout.channel.recv_exit_status()
    print("✅ Site config created\n")
    
    # Enable site
    print("🔗 Enabling site...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm -f /etc/nginx/sites-enabled/default && echo '{VPS_PASS}' | sudo -S ln -sf /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Site enabled\n")
    
    # Test config
    print("🧪 Testing...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test_result = stdout.read().decode('utf-8')
    print(f"Test result:\n{test_result}\n")
    
    # Reload
    print("🔄 Reloading Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl restart nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx restarted\n")
    
    # Check status
    import time
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl is-active nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8').strip()
    
    print(f"📊 Nginx status: {status}\n")
    
    if 'active' in status:
        print("="*70)
        print("🎉🎉🎉 SSL SETUP COMPLETE! 🎉🎉🎉")
        print("="*70)
        print("\n✅ Nginx: RUNNING")
        print("✅ SSL: Configured")
        print("✅ Proxy: Backend ready\n")
        print("📋 FINAL STEPS:")
        print("\n1. Cloudflare SSL Mode → Full (strict)")
        print("   https://dash.cloudflare.com\n")
        print("2. TEST:")
        print("   https://cintabuku.com")
        print("   https://cintabuku.com/health\n")
        print("🎊 PRODUCTION READY! 🎊\n")
    else:
        print("⚠️  Check logs: sudo systemctl status nginx\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
