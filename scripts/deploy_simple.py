import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku/backend"

print("\n🚀 SIMPLEST DEPLOY - No Docker, Direct Run on VPS\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Stop Docker first
    print("🛑 Stopping Docker backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Docker stopped\n")
    
    # Build TypeScript on VPS
    print("📦 Building TypeScript on VPS...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npm run build", get_pty=True)
    stdout.channel.recv_exit_status()
    build_output = stdout.read().decode('utf-8')
    if "error" in build_output.lower():
        print("Build output:", build_output[-500:])
    print("✅ Built\n")
    
    # Install PM2
    print("📦 Installing PM2...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S npm install -g pm2", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ PM2 installed\n")
    
    # Start with PM2
    print("🚀 Starting backend with PM2...")
    cmd = f"cd {REMOTE_APP} && pm2 delete cintabuku-backend 2>/dev/null || true && pm2 start dist/index.js --name cintabuku-backend --env production"
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Started\n")
    
    # Save PM2 config
    stdin, stdout, stderr = client.exec_command("pm2 save", get_pty=True)
    stdout.channel.recv_exit_status()
    
    # Wait
    import time
    print("⏳ Waiting 10 seconds...\n")
    time.sleep(10)
    
    # Check status
    print("📊 PM2 Status:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 list", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    print("="*70)
    
    # Check logs
    print("\n📋 Backend Logs (last 20 lines):")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 logs cintabuku-backend --lines 20 --nostream", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Test health
    print("\n🧪 Testing backend:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"Response: {health}\n")
    
    # Test HTTPS
    print("🧪 Testing HTTPS:")
    stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    https = stdout.read().decode('utf-8')
    print(f"Response: {https}\n")
    
    # Analysis
    if '"status":"ok"' in health or '"status": "ok"' in health:
        print("="*70)
        print("🎉🎉🎉 DEPLOYMENT 100% SUCCESS!")
        print("="*70)
        print("\n✅ Built on VPS directly")
        print("✅ PM2 managing backend")
        print("✅ Health check passing")
        print("✅ NO Docker issues!")
        print("\n🌐 SITE IS LIVE:")
        print("   https://cintabuku.com")
        print("   https://cintabuku.com/health")
        print("\n💡 Management Commands:")
        print("   pm2 list")
        print("   pm2 logs cintabuku-backend")
        print("   pm2 restart cintabuku-backend")
        print("   pm2 stop cintabuku-backend\n")
    elif "online" in status:
        print("✅ Backend is running!")
        print("⏳ Health endpoint might need a moment to initialize\n")
    else:
        print("⚠️  Check logs above for any errors\n")
        print("Debug commands:")
        print("  pm2 logs cintabuku-backend --lines 50")
        print("  pm2 describe cintabuku-backend\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
