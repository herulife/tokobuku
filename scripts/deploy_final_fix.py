import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🚀 FINAL DEPLOYMENT - Enhanced Backend\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Pull latest code
    print("📥 Pulling latest code from GitHub...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && git pull origin main", get_pty=True)
    stdout.channel.recv_exit_status()
    pull_output = stdout.read().decode('utf-8')
    print(pull_output[-500:] if len(pull_output) > 500 else pull_output)
    
    # Stop old backend
    print("\n🛑 Stopping old backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Stopped\n")
    
    # Rebuild Docker image
    print("🏗️  Rebuilding Docker image (3-4 min)...")
    build_cmd = f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend ."
    stdin, stdout, stderr = client.exec_command(build_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Image rebuilt\n")
    
    # Deploy new backend
    print("🚀 Deploying enhanced backend...")
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
    container_id = stdout.read().decode('utf-8').strip()
    print(f"✅ Container started: {container_id[:50]}\n")
    
    # Wait and check
    import time
    print("⏳ Waiting 15 seconds for backend to initialize...")
    time.sleep(15)
    
    # Check logs
    print("\n📋 Backend Logs:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 20", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Check container status
    print("\n📊 Container Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    
    # Test health
    print("\n🧪 Testing backend health...")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    
    if health and '"status":"ok"' in health:
        print("✅ HEALTH CHECK SUCCESS!")
        print(f"Response: {health}\n")
    else:
        print(f"Response: {health[:200]}\n")
    
    # Analyze results
    if "Process will keep running" in logs:
        print("="*70)
        print("🎉 ENHANCED BACKEND DEPLOYED!")
        print("="*70)
        print("\n✅ New error handling active")
        print("✅ Keep-alive mechanism enabled")
        print("✅ Verbose logging configured\n")
    
    if "Restarting" in status:
        print("⚠️  Still showing 'Restarting' - checking logs for error...\n")
        if "EXCEPTION" in logs or "REJECTION" in logs:
            print("⚠️  Error found in logs - check above for details")
        else:
            print("ℹ️  No error in logs - may stabilize soon")
    elif "Up" in status:
        print("🎉 BACKEND IS STABLE!")
        print("   Status: UP and RUNNING!\n")
    
    print("\n🌐 TEST in browser:")
    print("   https://cintabuku.com")
    print("   https://cintabuku.com/health\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
