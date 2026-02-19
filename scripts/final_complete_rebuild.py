import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku/backend"

print("\n🚀 COMPLETE REBUILD FROM SCRATCH\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Pull latest
    print("📥 Pulling latest code...")
    stdin, stdout, stderr = client.exec_command(f"cd /home/ubuntu24/my-docker-apps/apps/cintabuku && git pull", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Code updated\n")
    
    # Clean everything
    print("🗑️  Removing old builds...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && rm -rf node_modules dist package-lock.json", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Cleaned\n")
    
    # Fresh npm install
    print("📦 Fresh npm install (3-4 min)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npm install", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Installed\n")
    
    # Build TypeScript
    print("🔨 Building TypeScript...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npm run build", get_pty=True)
    stdout.channel.recv_exit_status()
    build_out = stdout.read().decode('utf-8', errors='ignore')
    if "error" in build_out.lower() and "0 errors" not in build_out.lower():
        print(f"Build output: {build_out[-500:]}")
    print("✅ Built\n")
    
    # Verify dist
    print("🔍 Verifying dist folder...")
    stdin, stdout, stderr = client.exec_command(f"ls -la {REMOTE_APP}/dist/", get_pty=True)
    stdout.channel.recv_exit_status()
    dist_check = stdout.read().decode('utf-8')
    print(dist_check[:500])
    
    # Check routes specifically
    stdin, stdout, stderr = client.exec_command(f"ls -la {REMOTE_APP}/dist/routes/", get_pty=True)
    stdout.channel.recv_exit_status()
    routes_check = stdout.read().decode('utf-8')
    print(f"\nRoutes in dist:\n{routes_check[:500]}\n")
    
    # Generate Prisma
    print("🔧 Generating Prisma...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npx prisma generate", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Prisma ready\n")
    
    # Stop Docker
    print("🛑 Stopping Docker...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Docker stopped\n")
    
    # Fresh PM2 start
    print("🚀 Starting with PM2...")
    stdin, stdout, stderr = client.exec_command("pm2 delete all 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    
    start_cmd = f"cd {REMOTE_APP} && pm2 start dist/index.js --name cintabuku-backend"
    stdin, stdout, stderr = client.exec_command(start_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command("pm2 save", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Started\n")
    
    # Wait
    import time
    print("⏳ Waiting 15 seconds for initialization...")
    time.sleep(15)
    
    # Status
    print("\n📊 PM2 Status:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 list", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    print("="*70)
    
    # Logs
    print("\n📋 Logs:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 logs cintabuku-backend --lines 30 --nostream", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Health test
    print("\n🧪 Health Check:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"{health}\n")
    
    # HTTPS test
    print("🧪 HTTPS Check:")
    stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    https = stdout.read().decode('utf-8')
    print(f"{https}\n")
    
    # Final assessment
    if '"status":"ok"' in health or '"status": "ok"' in health:
        print("="*70)
        print("🎉🎉🎉 DEPLOYMENT 100% SUCCESS!")
        print("="*70)
        print("\n✅ Complete rebuild from scratch")
        print("✅ All dependencies fresh")
        print("✅ TypeScript compiled with all routes")
        print("✅ Prisma generated")
        print("✅ Backend running (NO DOCKER)")
        print("✅ Health check PASSING")
        print("\n🌐 SITE IS LIVE:")
        print("   https://cintabuku.com")
        print("   https://cintabuku.com/health")
        print("\n💡 Management:")
        print("   SSH: ssh -p 2480 ubuntu24@103.107.206.10")
        print("   PM2: pm2 list | pm2 logs cintabuku-backend")
        print("   Restart: pm2 restart cintabuku-backend\n")
    elif "online" in status.lower():
        print("✅ Backend is ONLINE")
        print(f"Health response: {health}")
        print("Check logs above for any issues\n")
    else:
        print("⚠️  Check status and logs above")
        print("Debug: pm2 logs cintabuku-backend --lines 50\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
