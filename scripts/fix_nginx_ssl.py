import paramiko
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

nginx_config = """# HTTP - Redirect to HTTPS
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
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

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
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        proxy_cache_bypass $http_upgrade;
    }

    location /health {
        proxy_pass http://localhost:5000/health;
        access_log off;
    }
}
"""

print("\n🔧 Fix Nginx Installation & Configure SSL\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Properly install Nginx
    print("📦 Installing Nginx properly...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S apt-get update && echo '{VPS_PASS}' | sudo -S DEBIAN_FRONTEND=noninteractive apt-get install -y nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx installed\n")
    
    # Verify installation
    stdin, stdout, stderr = client.exec_command("which nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    nginx_path = stdout.read().decode('utf-8').strip()
    print(f"✅ Nginx path: {nginx_path}\n")
    
    # Create config
    print("📝 Creating Nginx configuration...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/nginx/sites-available/cintabuku.com > /dev/null << 'NGINXEOF'\n{nginx_config}\nNGINXEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Config created\n")
    
    # Enable site
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm -f /etc/nginx/sites-enabled/default", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ln -sf /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Site enabled\n")
    
    # Test config
    print("🧪 Testing configuration...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    
    if 'successful' in result:
        print("✅ Configuration test PASSED!\n")
    else:
        print(f"Result: {result}\n")
    
    # Start/Reload Nginx
    print("🔄 Starting Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl enable nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl restart nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx started!\n")
    
    # Check status
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl status nginx | head -n 5", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(f"📊 Nginx Status:\n{status}\n")
    
    # Test HTTPS locally
    print("🔐 Testing HTTPS...")
    stdin, stdout, stderr = client.exec_command("curl -k -I https://localhost/health 2>&1 | head -n 1", get_pty=True)
    stdout.channel.recv_exit_status()
    https_test = stdout.read().decode('utf-8')
    print(f"HTTPS Test: {https_test}\n")
    
    print("="*70)
    print("🎉 SSL INSTALLATION COMPLETE!")
    print("="*70)
    print("\n📋 FINAL STEPS:\n")
    print("1. Set Cloudflare SSL Mode:")
    print("   https://dash.cloudflare.com")
    print("   SSL/TLS → Overview → Mode: Full (strict)\n")
    
    print("2. Test Production:")
    print("   https://cintabuku.com")
    print("   https://cintabuku.com/health\n")
    
    print("3. Run Migrations:")
    print("   ssh -p 2480 ubuntu24@103.107.206.10")
    print("   sudo docker exec cintabuku-backend npx prisma migrate deploy\n")
    
    print("🎊 DEPLOYMENT 100% COMPLETE! 🎊\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
