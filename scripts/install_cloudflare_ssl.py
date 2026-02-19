import paramiko
import os

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

# Nginx config with Cloudflare Origin Certificate
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

print("\n🔐 Install Cloudflare Origin Certificate on VPS\n")
print("📋 PREREQUISITES:")
print("   1. Generate Origin Certificate di Cloudflare:")
print("      - SSL/TLS → Origin Server → Create Certificate")
print("      - Save as: origin-cert.pem & private-key.pem")
print("      - Put files in current directory\n")

# Check for certificate files
if not os.path.exists('origin-cert.pem'):
    print("❌ File 'origin-cert.pem' not found!")
    print("   Generate certificate di Cloudflare dulu.\n")
    exit(1)

if not os.path.exists('private-key.pem'):
    print("❌ File 'private-key.pem' not found!")
    print("   Save private key dari Cloudflare.\n")
    exit(1)

print("✅ Certificate files found\n")

# Read certificate files
with open('origin-cert.pem', 'r') as f:
    cert_content = f.read()

with open('private-key.pem', 'r') as f:
    key_content = f.read()

print("Continue with installation? (yes/no): ", end='')
confirm = input().lower()
if confirm != 'yes':
    print("Cancelled.")
    exit(0)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("\n✅ Connected to VPS\n")
    
    # Create SSL directory
    print("📁 Creating SSL directory...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mkdir -p /etc/ssl/cloudflare", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Directory created\n")
    
    # Upload certificate
    print("📤 Uploading origin certificate...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/ssl/cloudflare/origin-cert.pem > /dev/null << 'CERTEOF'\n{cert_content}\nCERTEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Certificate uploaded\n")
    
    # Upload private key
    print("🔑 Uploading private key...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/ssl/cloudflare/private-key.pem > /dev/null << 'KEYEOF'\n{key_content}\nKEYEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Private key uploaded\n")
    
    # Set permissions
    print("🔒 Setting permissions...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S chmod 600 /etc/ssl/cloudflare/*", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Permissions set\n")
    
    # Install Nginx
    print("📦 Installing Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S apt update && echo '{VPS_PASS}' | sudo -S apt install nginx -y", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx installed\n")
    
    # Create Nginx config
    print("📝 Creating Nginx configuration...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/nginx/sites-available/cintabuku.com > /dev/null << 'NGINXEOF'\n{nginx_config}\nNGINXEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Config created\n")
    
    # Remove default, enable site
    print("🔗 Enabling site...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm -f /etc/nginx/sites-enabled/default", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ln -sf /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Site enabled\n")
    
    # Test config
    print("🧪 Testing Nginx configuration...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    
    if 'successful' in result:
        print("✅ Configuration test passed!\n")
    else:
        print(f"❌ Configuration test failed:\n{result}\n")
        exit(1)
    
    # Reload Nginx
    print("🔄 Reloading Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx reloaded\n")
    
    # Test HTTPS
    import time
    print("⏳ Waiting 5 seconds for Nginx to stabilize...")
    time.sleep(5)
    
    print("\n" + "="*70)
    print("🎉 SSL INSTALLATION COMPLETE!")
    print("="*70)
    
    print("\n📋 Next Steps:")
    print("\n1. Set Cloudflare SSL Mode:")
    print("   - Cloudflare Dashboard → SSL/TLS")
    print("   - Mode: Full (strict) ✅\n")
    
    print("2. Verify Proxy Status:")
    print("   - DNS Records → Proxy: ON (orange cloud)\n")
    
    print("3. Run Migrations:")
    print("   ssh -p 2480 ubuntu24@103.107.206.10")
    print("   sudo docker exec cintabuku-backend npx prisma migrate deploy\n")
    
    print("4. Test Production:")
    print("   - https://cintabuku.com")
    print("   - https://cintabuku.com/health\n")
    
    print("🎊 SUCCESS! Your site will be live with HTTPS! 🎊\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
