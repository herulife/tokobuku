import paramiko
from scp import SCPClient

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

# Proper Nginx config
nginx_config_content = """server {
    listen 80;
    listen [::]:80;
    server_name cintabuku.com www.cintabuku.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name cintabuku.com www.cintabuku.com;

    ssl_certificate /etc/ssl/cloudflare/origin-cert.pem;
    ssl_certificate_key /etc/ssl/cloudflare/private-key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
"""

print("\n🔧 Upload Nginx Config via SCP\n")

# Create temp file locally
with open('cintabuku_nginx.conf', 'w') as f:
    f.write(nginx_config_content)
print("✅ Config created locally\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Upload via SCP
    print("📤 Uploading config...")
    with SCPClient(client.get_transport()) as scp:
        scp.put('cintabuku_nginx.conf', '/tmp/cintabuku.com')
    print("✅ Uploaded to /tmp\n")
    
    # Move to proper location
    print("📋 Moving to sites-available...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mv /tmp/cintabuku.com /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Moved\n")
    
    # Verify
    print("🔍 Verifying...")
    stdin, stdout, stderr = client.exec_command("wc -l /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    lines = stdout.read().decode('utf-8')
    print(f"Lines: {lines}")
    
    # Test
    print("🧪 Testing...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    
    if 'successful' in test:
        print("✅ PASSED!\n")
        
        # Reload
        print("🔄 Reloading Nginx...")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Reloaded!\n")
        
        print("="*70)
        print("🎉 CONFIG UPLOADED & NGINX RELOADED!")
        print("="*70)
        print("\nTest browser NOW:")
        print("  https://cintabuku.com")
        print("  https://cintabuku.com/health\n")
        print("Clear cache: Ctrl+Shift+R\n")
    else:
        print(f"Test: {test}\n")
    
except Exception as e:
    print(f"\n⚠️  Error: {e}")
    print("\nFallback: Use SSH manual method from MANUAL_SSL_SETUP.md\n")
finally:
    client.close()
    
# Cleanup
import os
os.remove('cintabuku_nginx.conf')
print("✅ Cleanup done\n")
