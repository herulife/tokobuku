import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 Final Fix: Write Nginx Config Properly\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Write config line by line
    commands = [
        "echo 'server {' | sudo tee /etc/nginx/sites-available/cintabuku.com",
        "echo '    listen 80;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    listen [::]:80;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    server_name cintabuku.com www.cintabuku.com;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    return 301 https://\$host\$request_uri;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '}' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo 'server {' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    listen 443 ssl http2;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    listen [::]:443 ssl http2;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    server_name cintabuku.com www.cintabuku.com;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    ssl_certificate /etc/ssl/cloudflare/origin-cert.pem;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    ssl_certificate_key /etc/ssl/cloudflare/private-key.pem;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    ssl_protocols TLSv1.2 TLSv1.3;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    location / {' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '        proxy_pass http://localhost:5000;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '        proxy_http_version 1.1;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '        proxy_set_header Host \$host;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '        proxy_set_header X-Real-IP \$remote_addr;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '        proxy_set_header X-Forwarded-Proto \$scheme;' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '    }' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
        "echo '}' | sudo tee -a /etc/nginx/sites-available/cintabuku.com",
    ]
    
    print("📝 Writing config...")
    for cmd in commands:
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        stdout.channel.recv_exit_status()
    print("✅ Config written\n")
    
    # Verify
    print("🔍 Verifying...")
    stdin, stdout, stderr = client.exec_command("wc -l /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    lines = stdout.read().decode('utf-8')
    print(f"Lines: {lines}")
    
    # Show first few lines
    stdin, stdout, stderr = client.exec_command("head -n 10 /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    preview = stdout.read().decode('utf-8')
    print(f"Preview:\n{preview}\n")
    
    # Test
    print("🧪 Testing...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    
    if 'successful' in test:
        print("✅ Test PASSED!\n")
        
        # Reload
        print("🔄 Reloading...")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Reloaded\n")
        
        print("="*70)
        print("🎉 SUCCESS!")
        print("="*70)
        print("\nTest NOW:")
        print("  https://cintabuku.com")
        print("  https://cintabuku.com/health\n")
    else:
        print(f"Test result: {test}\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
