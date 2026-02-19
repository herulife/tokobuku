import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🔧 FINAL FIX: Rename Dockerfile + Rebuild + Deploy\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Rename Dockerfile
    print("📝 Renaming Dockerfile.production → Dockerfile...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP}/backend && mv -f Dockerfile.production Dockerfile", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Renamed\n")
    
    # Rebuild
    print("🏗️  Rebuilding Docker image (3-4 min)...")
    build_cmd = f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend ."
    stdin, stdout, stderr = client.exec_command(build_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Image rebuilt\n")
    
    # Redeploy
    print("🔄 Redeploying...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    
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
    log_cmd = f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 20"
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
    
    # Test
    print("\n🧪 Health Test:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"{health}\n")
    
    # Results
    if "Process will keep running" in logs and '"status":"ok"' in health:
        print("="*70)
        print("🎉🎉🎉 DEPLOYMENT 100% SUCCESS!")
        print("="*70)
        print("\n✅ OpenSSL fix applied")
        print("✅ Prisma working")
        print("✅ Backend stable")
        print("✅ Health endpoint responding\n")
        print("🌐 TEST NOW: https://cintabuku.com\n")
    elif "libssl" in logs:
        print("⚠️  Still has OpenSSL error - checking build...\n")
    elif "Restarting" in status:
        print("⚠️  Backend restarting - check logs for error\n")
    else:
        print("ℹ️  Status unclear - manual check needed\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
