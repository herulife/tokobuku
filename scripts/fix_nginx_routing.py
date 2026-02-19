import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 FIX NGINX ROUTING TO BACKEND\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check current Nginx config
    print("📋 Current cintabuku.com config:")
    stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    current = stdout.read().decode('utf-8')
    print(current[:500])
    
    # Create fresh correct config
    print("\n📝 Creating correct Nginx config...")
    
    config = """server {
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
    
    # Write line by line to avoid issues
    lines = config.split('\n')
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    
    for line in lines:
        escaped = line.replace("'", "'\\''")
        cmd = f"echo '{VPS_PASS}' | sudo -S bash -c \"echo '{escaped}' >> /etc/nginx/sites-available/cintabuku.com\""
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        stdout.channel.recv_exit_status()
    
    print("✅ Config written\n")
    
    # Test config
    print("🧪 Testing Nginx config...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    print(test)
    
    if 'successful' in test:
        print("\n✅ Config test PASSED\n")
        
        # Reload Nginx
        print("🔄 Reloading Nginx...")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Nginx reloaded\n")
        
        # Test
        import time
        time.sleep(2)
        
        print("🧪 Testing HTTPS → Backend:")
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/health", get_pty=True)
        stdout.channel.recv_exit_status()
        result = stdout.read().decode('utf-8')
        print(f"{result}\n")
        
        if '"status":"ok"' in result:
            print("="*70)
            print("🎉🎉🎉 NGINX → BACKEND WORKING!")
            print("="*70)
            print("\n✅ Nginx configured correctly")
            print("✅ SSL working")
            print("✅ Proxying to PM2 backend")
            print("\n🌐 TEST NOW:")
            print("   https://cintabuku.com")
            print("   https://cintabuku.com/health")
            print("\n💡 Clear browser cache: Ctrl+Shift+R\n")
        else:
            print("⚠️  Nginx reloaded but test pending. Try browser.\n")
    else:
        print(f"\n❌ Config test failed:\n{test}\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
