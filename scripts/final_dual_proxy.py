import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 APPLYING FINAL DUAL-REVERSE PROXY CONFIG\n")

nginx_config = """server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cintabuku.com www.cintabuku.com;

    ssl_certificate /etc/ssl/cloudflare/origin-cert.pem;
    ssl_certificate_key /etc/ssl/cloudflare/private-key.pem;

    # API Backend
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health Check
    location /health {
        proxy_pass http://localhost:5000/health;
        proxy_set_header Host $host;
    }

    # Static Uploads
    location /uploads/ {
        proxy_pass http://localhost:5000/uploads/;
        proxy_set_header Host $host;
    }

    # Next.js Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Next.js specific settings
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
    }
}
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Save to temp file
    print("📝 Writing clean config...")
    stdin, stdout, stderr = client.exec_command("cat > /tmp/cintabuku.conf << 'EOF'\n" + nginx_config + "\nEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mv /tmp/cintabuku.conf /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Config written\n")
    
    # Reload
    print("🔄 Reloading Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t && echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx reloaded\n")
    
    # Final checks
    print("🧪 Checking site availability...")
    # Test frontend
    stdin, stdout, stderr = client.exec_command("curl -k -s -I -H 'Host: cintabuku.com' https://localhost/", get_pty=True)
    stdout.channel.recv_exit_status()
    print("Frontend URL Check (Should be 200 or 30x):")
    print(stdout.read().decode('utf-8'))

    # Test backend
    stdin, stdout, stderr = client.exec_command("curl -k -s -H 'Host: cintabuku.com' https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    print("\nBackend Health Check (Should be ok):")
    print(stdout.read().decode('utf-8'))

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
