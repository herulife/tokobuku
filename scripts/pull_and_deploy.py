import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🚀 Pull Latest Code & Deploy Backend\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Pull latest code
    print("📥 Pulling latest code from GitHub...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && git pull origin main", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Stop and remove old container
    print("\n🛑 Stopping old backend container...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Old container removed\n")
    
    # Build new image
    print("🏗️  Building backend (2-3 minutes)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend -f Dockerfile .", get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8')
    
    if 'Successfully built' in output or 'Successfully tagged' in output:
        print("✅ Build successful!\n")
    else:
        print("Last 1000 chars of build output:")
        print(output[-1000:])
    
    # Start new container
    print("🚀 Starting backend container...")
    start_cmd = f"""echo '{VPS_PASS}' | sudo -S docker run -d \\
      --name cintabuku-backend \\
      --restart always \\
      --env-file {REMOTE_APP}/backend/.env \\
      -v {REMOTE_APP}/uploads:/app/uploads \\
      -v {REMOTE_APP}/logs:/app/logs \\
      -p 5000:5000 \\
      --link cintabuku-db:db \\
      cintabuku-backend"""
    
    stdin, stdout, stderr = client.exec_command(start_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    time.sleep(10)
    
    # Run migrations
    print("\n📊 Running Prisma migrations...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Verify
    print("\n✅ Checking containers...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    print(result)
    
    # Test health endpoint
    print("\n🏥 Testing health endpoint...")
    time.sleep(5)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend curl -s http://localhost:5000/health || echo 'Not ready yet'", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"Health response: {health}")
    
    if 'cintabuku-backend' in result and 'Up' in result:
        print("\n" + "="*70)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("="*70)
        print(f"\n✅ Both containers running:")
        print(f"   - Database: cintabuku-db (port 5433)")
        print(f"   - Backend: cintabuku-backend (port 5000)")
        print(f"\n🌐 Next: Configure Cloudflare DNS")
        print(f"   - Point cintabuku.com to {VPS_IP}")
        print(f"   - Enable proxy (orange cloud)")
        print(f"\n🎊 SUCCESS! 🎊\n")
    else:
        print("\n⚠️  Backend may need troubleshooting. Check logs:")
        print(f"   sudo docker logs cintabuku-backend\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
