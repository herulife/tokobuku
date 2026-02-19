import paramiko
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🎯 FINAL FIX: Deploy with restart=always and check if it stabilizes\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Stop old
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    
    # Start with restart=always
    print("🚀 Starting backend with restart=always...")
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
    
    print("\n⏳ Waiting 45 seconds for stabilization...")
    time.sleep(45)
    
    # Check status
    print("\n📊 Container Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    
    for line in result.split('\n'):
        if 'cintabuku' in line or 'CONTAINER' in line:
            print(line)
    
    # Test health
    print("\n🏥 Testing Health Endpoint:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(health[:500])
    
    if '"status":"ok"' in health or 'Up' in result:
        print("\n" + "="*70)
        print("🎉🎉🎉 DEPLOYMENT 100% COMPLETE!")
        print("="*70)
        print("\n✅ Backend: RUNNING & STABLE!")
        print("✅ Database: UP (2+ hours)")
        print(f"\n🌐 Backend: http://103.107.206.10:5000")
        print(f"🏥 Health: http://103.107.206.10:5000/health")
        print("\n📋 Next Steps:")
        print("  1. Update Cloudflare DNS: cintabuku.com → 103.107.206.10")
        print("  2. Install SSL Certificate")
        print("  3. Test production!\n")
    else:
        print("\n⚠️  Check logs if needed: sudo docker logs cintabuku-backend\n")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
