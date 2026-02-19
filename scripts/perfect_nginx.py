import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 NGINX REDIRECT PERFECTION\n")

# Using raw string and escaping $ carefully for bash
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

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Save to temp file
    # We use quoted EOF to prevent shell expansion of $
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
    
    # Final health test
    print("🧪 Final HTTPS health test:")
    stdin, stdout, stderr = client.exec_command("curl -k -s -H 'Host: cintabuku.com' https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
