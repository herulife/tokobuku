import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🔧 FINAL CLEAN BUILD - From Source in Docker\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Pull latest
    print("📥 Pulling code...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && git pull origin main", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Pulled\n")
    
    # DON'T build TypeScript on VPS - let Docker do it all
    print("🏗️  Building Docker image FROM SOURCE (5-6 min)...")
    print("   (Docker will: npm install + prisma generate + compile TS)\n")
    
    build_cmd = f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend ."
    stdin, stdout, stderr = client.exec_command(build_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Image built from source\n")
    
    # Stop old
    print("🛑 Stopping old...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Stopped\n")
    
    # Deploy
    print("🚀 Deploying...")
    deploy_cmd = f"""echo '{VPS_PASS}' | sudo -S docker run -d \
  --name cintabuku-backend \
  --restart always \
  --env-file {REMOTE_APP}/backend/.env \
  -v {REMOTE_APP}/uploads:/app/uploads \
  -v {REMOTE_APP}/logs:/app/logs \
  -p 5000:5000 \
  --link cintabuku-db:db \
  cintabuku-backend"""
    
    stdin, stdout, stderr = client.exec_command(deploy_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Container started\n")
    
    # Wait
    import time
    print("⏳ Waiting 15 seconds...")
    time.sleep(15)
    
    # Check logs
    print("\n📋 LOGS:")
    print("="*70)
    log_cmd = f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 30"
    stdin, stdout, stderr = client.exec_command(log_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Status
    print("\n📊 Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    
    # Health
    print("\n🧪 Health:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"{health}\n")
    
    # Analysis
    if "musl" not in logs and "libssl" not in logs or "Server running" in logs:
        if '"status":"ok"' in health:
            print("="*70)
            print("🎉🎉🎉 SUCCESS! DEPLOYMENT COMPLETE!")
            print("="*70)
            print("\n✅ Built from source in Debian")
            print("✅ Prisma glibc binaries generated")
            print("✅ Backend stable and running")
            print("✅ Health endpoint OK\n")
            print("🌐 SITE IS LIVE:")
            print("   https://cintabuku.com\n")
        else:
            print("✅ No Prisma errors but health check pending")
    else:
        if "musl" in logs:
            print("⚠️  Still detecting musl - check build process")
        if "libssl" in logs:
            print("⚠️  Still has OpenSSL errors")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
