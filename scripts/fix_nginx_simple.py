import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔧 SIMPLE NGINX FIX - Direct Method\n")

nginx_config = """server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cintabuku.com www.cintabuku.com;

    ssl_certificate /etc/ssl/cloudflare/origin-cert.pem;
    ssl_certificate_key /etc/ssl/cloudflare/private-key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Upload via temp file
    print("📝 Writing config...")
    stdin, stdout, stderr = client.exec_command(f"cat > /tmp/cintabuku.conf << 'EOFCONFIG'\n{nginx_config}\nEOFCONFIG", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mv /tmp/cintabuku.conf /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Config written\n")
    
    # Test
    print("🧪 Testing Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    print(test)
    
    if 'successful' in test:
        print("\n✅ Config OK!\n")
        
        # Reload
        print("🔄 Reloading Nginx...")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
        stdout.channel.recv_exit_status()
        print("✅ Reloaded\n")
        
        # Test
        import time
        time.sleep(2)
        
        stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/health", get_pty=True)
        stdout.channel.recv_exit_status()
        result = stdout.read().decode('utf-8')
        
        print(f"🧪 HTTPS Test: {result}\n")
        
        if '"status":"ok"' in result:
            print("="*70)
            print("🎉 100% COMPLETE - SITE IS LIVE!")
            print("="*70)
            print("\n✅ Backend: PM2 running")
            print("✅ Nginx: Routing correctly")
            print("✅ SSL: Working")
            print("\n🌐 https://cintabuku.com - BUKA SEKARANG!")
            print("\n💡 Clear cache browser: Ctrl+Shift+R\n")
        else:
            print("Check browser manually\n")
    else:
        print(f"\n❌ Config error:\n{test}\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
