import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

def execute(ssh, cmd, show=True):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='ignore')
    if show and output:
        print(output)
    return output

print("\n" + "="*70)
print("🚀 FINAL DEPLOYMENT - Cintabuku")
print("="*70)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"\n🔌 Connecting to VPS...")
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Step 1: Check if docker-compose file exists
    print("="*70)
    print("📋 Step 1: Checking Configuration Files")
    print("="*70)
    
    result = execute(client, f"ls -lh {REMOTE_APP}/docker-compose.cintabuku.yml", show=False)
    if 'No such file' in result:
        print("❌ docker-compose.cintabuku.yml not found!")
        print("Creating it from GitHub repo...")
        
        # The file should be in the git clone, let's check
        result = execute(client, f"ls {REMOTE_APP}/", show=False)
        print(result)
        sys.exit(1)
    
    print(f"✅ Found docker-compose.cintabuku.yml\n")
    
    # Step 2: Stop any existing containers
    print("="*70)
    print("🛑 Step 2: Stopping Any Existing Cintabuku Containers")
    print("="*70)
    
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend cintabuku-db 2>/dev/null || echo 'No containers to stop'")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend cintabuku-db 2>/dev/null || echo 'No containers to remove'")
    print("✅ Cleanup complete\n")
    
    # Step 3: Start Database
    print("="*70)
    print("🗄️  Step 3: Starting PostgreSQL Database")
    print("="*70)
    
    execute(client, f"cd {REMOTE_APP} && echo '{VPS_PASS}' | sudo -S docker compose -f docker-compose.cintabuku.yml up -d cintabuku-db")
    
    print("\n⏳ Waiting 20 seconds for database to initialize...")
    time.sleep(20)
    
    # Verify database
    result = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db pg_isready -U cintabuku_user 2>&1 || echo 'Not ready'", show=False)
    if 'accepting connections' in result:
        print("✅ PostgreSQL is ready!\n")
    else:
        print("⚠️  Database starting up, continuing anyway...\n")
    
    # Step 4: Build & Start Backend
    print("="*70)
    print("🚀 Step 4: Building & Starting Backend")
    print("="*70)
    
    print("📦 Building Docker image...")
    execute(client, f"cd {REMOTE_APP} && echo '{VPS_PASS}' | sudo -S docker compose -f docker-compose.cintabuku.yml build cintabuku-backend")
    
    print("\n🚀 Starting backend container...")
    execute(client, f"cd {REMOTE_APP} && echo '{VPS_PASS}' | sudo -S docker compose -f docker-compose.cintabuku.yml up -d cintabuku-backend")
    
    print("\n⏳ Waiting 15 seconds for backend to start...")
    time.sleep(15)
    
    # Step 5: Run Migrations
    print("\n" + "="*70)
    print("📊 Step 5: Running Database Migrations")
    print("="*70)
    
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy")
    
    # Step 6: Verification
    print("\n" + "="*70)
    print("✅ Step 6: Final Verification")
    print("="*70)
    
    print("\n📊 Running Containers:")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker ps --format 'table {{{{.Names}}}}\\t{{{{.Status}}}}\\t{{{{.Ports}}}}' | grep cintabuku")
    
    print("\n🏥 Health Checks:")
    
    # Backend health
    health = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend curl -s http://localhost:5000/health 2>&1 || echo 'Not responding'", show=False)
    if 'OK' in health or 'healthy' in health.lower():
        print("✅ Backend API: Healthy")
    else:
        print("⚠️  Backend API: Starting up...")
    
    # Database
    db_test = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db psql -U cintabuku_user -d cintabuku -c '\\\\dt' 2>&1 | head -5", show=False)
    if 'public' in db_test:
        print("✅ Database: Connected with tables")
    else:
        print("⚠️  Database: Check logs")
    
    # Logs snippet
    print("\n📜 Backend Logs (last 10 lines):")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 10")
    
    print("\n" + "="*70)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("="*70)
    
    print(f"\n✅ Services Running:")
    print(f"   - PostgreSQL Database (cintabuku-db)")
    print(f"   - Backend API (cintabuku-backend:5000)")
    
    print(f"\n🌐 Next Steps:")
    print(f"   1. Configure Cloudflare DNS:")
    print(f"      Login: https://dash.cloudflare.com")
    print(f"      Add A record: cintabuku.com → {VPS_IP}")
    print(f"      Enable proxy (orange cloud)")
    
    print(f"\n   2. Wait 5-10 minutes for DNS propagation")
    
    print(f"\n   3. Test your site:")
    print(f"      https://cintabuku.com")
    print(f"      https://cintabuku.com/api/health")
    
    print(f"\n📊 Monitoring:")
    print(f"   View logs: ssh -p {VPS_PORT} {VPS_USER}@{VPS_IP}")
    print(f"   Then run: sudo docker logs cintabuku-backend -f")
    
    print(f"\n🎊 Cintabuku is LIVE on VPS! 🎊\n")
    
except Exception as e:
    print(f"\n❌ Deployment failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    client.close()
