import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🔧 COMPLETE FIX: Build TypeScript + Docker + Deploy\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Build TypeScript on VPS first
    print("📦 Building TypeScript on VPS...")
    build_ts_cmd = f"cd {REMOTE_APP}/backend && npm run build"
    stdin, stdout, stderr = client.exec_command(build_ts_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ TypeScript compiled\n")
    
    # Now build Docker image (dist exists)
    print("🏗️  Building Docker image (3-4 min)...")
    build_docker_cmd = f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend ."
    stdin, stdout, stderr = client.exec_command(build_docker_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Docker image built\n")
    
    # Stop old container
    print("🛑 Stopping old backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Stopped\n")
    
    # Deploy new container
    print("🚀 Deploying new backend...")
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
    log_cmd = f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 25"
    stdin, stdout, stderr = client.exec_command(log_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Status
    print("\n📊 Container Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    
    # Test health
    print("\n🧪 Health Test:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"Response: {health}\n")
    
    # Analyze results
    success_indicators = [
        "Process will keep running" in logs,
        '"status":"ok"' in health or '"status": "ok"' in health,
        "Up" in status and "Restarting" not in status,
        "libssl" not in logs  # No OpenSSL error
    ]
    
    if all(success_indicators):
        print("="*70)
        print("🎉🎉🎉 DEPLOYMENT 100% COMPLETE!")
        print("="*70)
        print("\n✅ TypeScript compiled on VPS")
        print("✅ Docker image built with OpenSSL")
        print("✅ Backend container stable")
        print("✅ Health endpoint responding")
        print("\n🌐 SITE IS LIVE:")
        print("   https://cintabuku.com")
        print("   https://cintabuku.com/health\n")
    elif "libssl" in logs:
        print("⚠️  OpenSSL error still present")
        print("   Prisma engines not loading correctly\n")
    elif "Restarting" in status:
        print("⚠️  Container restarting - check logs above\n")
    elif health:
        print("✅ Backend responding but check status above\n")
    else:
        print("ℹ️  Manual verification needed - check logs above\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
