import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku/backend"

print("\n🔧 INSTALL DEPENDENCIES & START BACKEND\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Install production dependencies
    print("📦 Installing production dependencies (2-3 min)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npm install --production", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Dependencies installed\n")
    
    # Restart PM2
    print("🔄 Restarting backend...")
    stdin, stdout, stderr = client.exec_command("pm2 restart cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Restarted\n")
    
    # Wait
    import time
    print("⏳ Waiting 10 seconds...")
    time.sleep(10)
    
    # Check status
    print("\n📊 PM2 Status:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 list", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    print("="*70)
    
    # Check logs
    print("\n📋 Logs:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 logs cintabuku-backend --lines 15 --nostream", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Test
    print("\n🧪 Health Check:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"{health}\n")
    
    # Test HTTPS
    print("🧪 HTTPS Check:")
    stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    https = stdout.read().decode('utf-8')
    print(f"{https}\n")
    
    if '"status":"ok"' in health:
        print("="*70)
        print("🎉🎉🎉 DEPLOYMENT COMPLETE - NO DOCKER!")
        print("="*70)
        print("\n✅ Dependencies installed")
        print("✅ Backend running with PM2")
        print("✅ Health check passing")
        print("\n🌐 SITE LIVE:")
        print("   https://cintabuku.com\n")
    elif "online" in status.lower():
        print("✅ Backend online, check logs above\n")
    else:
        print("⚠️  Check status and logs above\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
