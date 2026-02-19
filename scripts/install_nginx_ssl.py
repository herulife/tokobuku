import paramiko
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

# Nginx config
nginx_config = """server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;

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
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
"""

print("\n🔧 Installing Nginx + SSL on VPS\n")
print("⚠️  PREREQUISITES:")
print("   1. DNS must point to VPS: ping cintabuku.com → 103.107.206.10")
print("   2. Wait 5-10 minutes after DNS update")
print("\nContinue? (yes/no): ", end='')

confirm = input().lower()
if confirm != 'yes':
    print("Cancelled.")
    exit(0)

print("\nℹ️  You will need to provide email for SSL certificate\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected to VPS\n")
    
    # Install Nginx
    print("📦 Installing Nginx & Certbot...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S apt update", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S apt install nginx certbot python3-certbot-nginx -y", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx & Certbot installed\n")
    
    # Create Nginx config
    print("📝 Creating Nginx configuration...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tee /etc/nginx/sites-available/cintabuku.com > /dev/null << 'NGINXEOF'\n{nginx_config}\nNGINXEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Config created\n")
    
    # Enable site
    print("🔗 Enabling site...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ln -sf /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    
    # Remove default
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm -f /etc/nginx/sites-enabled/default", get_pty=True)
    stdout.channel.recv_exit_status()
    
    # Test config
    print("🧪 Testing Nginx config...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    
    if 'successful' in result:
        print("✅ Config test passed\n")
    else:
        print(f"❌ Config test failed:\n{result}")
        exit(1)
    
    # Reload Nginx
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx reloaded\n")
    
    # Test HTTP
    print("🌐 Testing HTTP access...")
    time.sleep(2)
    stdin, stdout, stderr = client.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    http_code = stdout.read().decode('utf-8').strip()
    
    if '200' in http_code:
        print(f"✅ HTTP working (code: {http_code})\n")
    else:
        print(f"⚠️  HTTP response: {http_code}\n")
    
    print("="*70)
    print("📋 NEXT STEP: Install SSL Certificate")
    print("="*70)
    print("\nRun this command ON THE VPS (via SSH):")
    print(f"\n  ssh -p 2480 ubuntu24@{VPS_IP}")
    print("  sudo certbot --nginx -d cintabuku.com -d www.cintabuku.com\n")
    print("You'll be prompted for:")
    print("  1. Email address")
    print("  2. Agree to terms (yes)")
    print("  3. Newsletter (no)")
    print("  4. Redirect HTTP→HTTPS (2 for yes)\n")
    print("After SSL installed:")
    print("  - Test: https://cintabuku.com")
    print("  - Enable Cloudflare proxy (orange cloud)")
    print("  - Run migrations: sudo docker exec cintabuku-backend npx prisma migrate deploy\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
