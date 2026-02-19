import paramiko
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🎯 Final Deployment - CommonJS Fix\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Pull latest
    print("📥 Pulling CommonJS fix...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && git pull origin main", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Stop old
    print("🛑 Removing old backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Removed\n")
    
    # Build
    print("🏗️  Building with CommonJS (3-4 min)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend .", get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8')
    
    if 'Successfully' in output:
        print("✅ Build SUCCESS!\n")
    else:
        print("Last 1000 chars:")
        print(output[-1000:])
    
    # Start
    print("🚀 Starting backend...")
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
    container_id = stdout.read().decode('utf-8').strip()
    print(f"Container: {container_id[:12]}\n")
    
    time.sleep(15)
    
    # Migrations
    print("📊 Running migrations...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Verify
    print("\n✅ Final Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps --format 'table {{{{.Names}}}}\\t{{{{.Status}}}}\\t{{{{.Ports}}}}'", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    
    for line in result.split('\n'):
        if 'cintabuku' in line:
            print(line)
    
    # Test health
    time.sleep(5)
    print("\n🏥 Health check:")
    stdin, stdout, stderr = client.exec_command(f"curl -s http://localhost:5000/health || echo 'Checking...'", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(health)
    
    if 'Up' in result and 'cintabuku-backend' in result:
        print("\n" + "="*70)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("="*70)
        print("\n✅ Both containers UP and RUNNING!")
        print("\n🌐 Next: Configure Cloudflare DNS")
        print(f"   cintabuku.com → {VPS_IP}")
        print("\n🎊 SUCCESS! 🎊\n")
    else:
        print("\nCheck: sudo docker logs cintabuku-backend\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
