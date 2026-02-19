import paramiko
from scp import SCPClient
import os

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔐 Re-Upload SSL Certificates + Nginx Config\n")

# Check local files
if not os.path.exists('origin-cert.pem'):
    print("❌ origin-cert.pem not found!\n")
    exit(1)

if not os.path.exists('private-key.pem'):
    print("❌ private-key.pem not found!\n")
    exit(1)

print("✅ Certificate files found locally\n")

# Create nginx config
nginx_config = """server {
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

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""

with open('nginx_cintabuku.conf', 'w') as f:
    f.write(nginx_config)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Create SSL directory
    print("📁 Creating SSL directory...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mkdir -p /etc/ssl/cloudflare", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Created\n")
    
    # Upload certificates via SCP
    print("📤 Uploading certificates...")
    with SCPClient(client.get_transport()) as scp:
        scp.put('origin-cert.pem', '/tmp/')
        scp.put('private-key.pem', '/tmp/')
    print("✅ Uploaded to /tmp\n")
    
    # Move with sudo
    print("🔐 Moving certificates...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mv /tmp/origin-cert.pem /etc/ssl/cloudflare/", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mv /tmp/private-key.pem /etc/ssl/cloudflare/", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Moved\n")
    
    # Set permissions
    print("🔒 Setting permissions...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S chmod 600 /etc/ssl/cloudflare/*", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Done\n")
    
    # Upload nginx config
    print("📤 Uploading Nginx config...")
    with SCPClient(client.get_transport()) as scp:
        scp.put('nginx_cintabuku.conf', '/tmp/cintabuku.com')
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mv /tmp/cintabuku.com /etc/nginx/sites-available/", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Uploaded\n")
    
    # Verify certificates exist
    print("🔍 Verifying certificates...")
    stdin, stdout, stderr = client.exec_command("ls -lh /etc/ssl/cloudflare/", get_pty=True)
    stdout.channel.recv_exit_status()
    cert_list = stdout.read().decode('utf-8')
    print(cert_list)
    
    # Test nginx
    print("\n🧪 Testing Nginx config...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    
    if 'successful' in test:
        print("✅ TEST PASSED!\n")
        
        # Reload
        print("🔄 Reloading Nginx...")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Nginx reloaded!\n")
        
        print("="*70)
        print("🎉🎉🎉 COMPLETE SETUP DONE! 🎉🎉🎉")
        print("="*70)
        print("\n✅ SSL Certificates: Uploaded")
        print("✅ Nginx Config: Uploaded")
        print("✅ Nginx: Reloaded\n")
        print("🌐 TEST NOW:")
        print("   https://cintabuku.com")
        print("   https://cintabuku.com/health\n")
        print("Clear cache: Ctrl+Shift+R\n")
    else:
        print(f"Test failed:\n{test}\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
    
# Cleanup
os.remove('nginx_cintabuku.conf')
print("✅ Cleanup done\n")
