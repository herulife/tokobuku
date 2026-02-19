import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

# Proper Nginx config
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

print("\n🔧 Recreating Cintabuku Nginx Config\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Write config
    print("📝 Writing proper config...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/nginx/sites-available/cintabuku.com > /dev/null << 'CONFIGEOF'\n{nginx_config}\nCONFIGEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Config written\n")
    
    # Verify config
    print("🔍 Verifying config content...")
    stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    content = stdout.read().decode('utf-8')
    print(f"Config size: {len(content)} bytes")
    print(f"First 200 chars:\n{content[:200]}\n")
    
    # Test
    print("🧪 Testing...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    
    if 'successful' in test:
        print("✅ Config test PASSED!\n")
    else:
        print(f"Test result: {test}\n")
    
    # Reload
    print("🔄 Reloading Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx reloaded\n")
    
    # Test backend
    import time
    time.sleep(2)
    print("🧪 Testing HTTPS locally...")
    stdin, stdout, stderr = client.exec_command("curl -k -I https://localhost/health 2>&1 | head -n 3", get_pty=True)
    stdout.channel.recv_exit_status()
    local_test = stdout.read().decode('utf-8')
    print(f"Local HTTPS test:\n{local_test}\n")
    
    print("="*70)
    print("🎉 CONFIG FIXED!")
    print("="*70)
    print("\nNow test in browser:")
    print("  https://cintabuku.com")
    print("  https://cintabuku.com/health\n")
    print("Clear cache (Ctrl+Shift+R) jika masih ada issue.\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
