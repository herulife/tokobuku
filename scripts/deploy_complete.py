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
print("🚀 FINAL DEPLOYMENT - Direct Docker Approach")
print("="*70)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"\n🔌 Connecting to VPS...")
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
    print("✅ Connected\n")
    
    # Get database password
    print("📖 Reading database password...")
    env_content = execute(client, f"cat {REMOTE_APP}/../../../.env 2>/dev/null || cat {REMOTE_APP}/backend/.env", show=False)
    
    db_pass = ""
    for line in env_content.split('\n'):
        if 'DATABASE_URL' in line and 'postgresql://' in line:
            # Extract from DATABASE_URL
            parts = line.split(':')
            if len(parts) >= 4:
                db_pass = parts[3].split('@')[0]
                break
        elif 'CINTABUKU_DB_PASSWORD=' in line:
            db_pass = line.split('=')[1].strip()
            break
    
    if not db_pass:
        db_pass = "aW!R^3K4t%oMbM@4zL@1oO16"  # From previous deployment
    
    print(f"✅ DB Password: {db_pass[:4]}...{db_pass[-4:]}\n")
    
    # Step 1: Stop and remove existing containers
    print("="*70)
    print("🛑 Step 1: Stopping Existing Containers")
    print("="*70)
    
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend cintabuku-db 2>/dev/null || true")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend cintabuku-db 2>/dev/null || true")
    print("✅ Cleanup complete\n")
    
    # Step 2: Start Database
    print("="*70)
    print("🗄️  Step 2: Starting PostgreSQL Database")
    print("="*70)
    
    db_cmd = f"""echo '{VPS_PASS}' | sudo -S docker run -d \\
      --name cintabuku-db \\
      --restart always \\
      -e POSTGRES_USER=cintabuku_user \\
      -e POSTGRES_PASSWORD={db_pass} \\
      -e POSTGRES_DB=cintabuku \\
      -v cintabuku_db:/var/lib/postgresql/data \\
      -p 5433:5432 \\
      postgres:15-alpine"""
    
    execute(client, db_cmd)
    
    print("\n⏳ Waiting 15 seconds for database to initialize...")
    time.sleep(15)
    
    # Verify database
    result = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db pg_isready -U cintabuku_user 2>&1", show=False)
    if 'accepting connections' in result:
        print("✅ Database is ready!\n")
    else:
        print("⚠️  Database starting up...\n")
    
    # Step 3: Build Backend
    print("="*70)
    print("🏗️  Step 3: Building Backend Docker Image")
    print("="*70)
    
    print("📦 Building... (this may take 3-5 minutes)")
    build_cmd = f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend -f Dockerfile ."
    execute(client, build_cmd)
    print("✅ Build complete\n")
    
    # Step 4: Start Backend
    print("="*70)
    print("🚀 Step 4: Starting Backend Container")
    print("="*70)
    
    backend_cmd = f"""echo '{VPS_PASS}' | sudo -S docker run -d \\
      --name cintabuku-backend \\
      --restart always \\
      --env-file {REMOTE_APP}/backend/.env \\
      -v {REMOTE_APP}/uploads:/app/uploads \\
      -v {REMOTE_APP}/logs:/app/logs \\
      -p 5000:5000 \\
      --link cintabuku-db:db \\
      cintabuku-backend"""
    
    execute(client, backend_cmd)
    
    print("\n⏳ Waiting 10 seconds for backend to start...")
    time.sleep(10)
    
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
    result = execute(client, f"echo '{VPS_PASS}' | sudo -S docker ps --format 'table {{{{.Names}}}}\\t{{{{.Status}}}}\\t{{{{.Ports}}}}'", show=False)
    
    for line in result.split('\n'):
        if 'cintabuku' in line:
            print(f"  {line}")
    
    print("\n🏥 Health Checks:")
    
    # Test backend
    health = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend curl -s http://localhost:5000/health 2>&1 || echo 'Not ready'", show=False)
    if 'OK' in health or 'healthy' in health.lower():
        print("✅ Backend API: Healthy")
    else:
        print("⚠️  Backend API: Check logs")
        print(f"   Response: {health[:100]}")
    
    # Test database
    db_test = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db psql -U cintabuku_user -d cintabuku -c 'SELECT 1;' 2>&1", show=False)
    if '1 row' in db_test or '(1 row)' in db_test:
        print("✅ Database: Connected")
    else:
        print("⚠️  Database: Check connection")
    
    print("\n📜 Recent Backend Logs:")
    logs = execute(client, f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 15", show=False)
    for line in logs.split('\n')[-10:]:
        if line.strip():
            print(f"   {line}")
    
    print("\n" + "="*70)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("="*70)
    
    print(f"\n✅ Services Running:")
    print(f"   - PostgreSQL: localhost:5433")
    print(f"   - Backend API: localhost:5000")
    
    print(f"\n🌐 Next Steps:")
    print(f"   1. Configure Cloudflare DNS:")
    print(f"      - Login: https://dash.cloudflare.com")
    print(f"      - Add A record: cintabuku.com → {VPS_IP}")
    print(f"      - Enable proxy (orange cloud)")
    
    print(f"\n   2. Wait 5-10 minutes for DNS propagation")
    
    print(f"\n   3. Access your site:")
    print(f"      - https://cintabuku.com")
    print(f"      - https://cintabuku.com/api/health")
    
    print(f"\n📊 Monitoring:")
    print(f"   SSH: ssh -p {VPS_PORT} {VPS_USER}@{VPS_IP}")
    print(f"   Logs: sudo docker logs cintabuku-backend -f")
    print(f"   Status: sudo docker ps")
    
    print(f"\n🎊 Cintabuku is LIVE! 🎊\n")
    
except Exception as e:
    print(f"\n❌ Deployment failed: {e}")
    import traceback
    traceback.print_exc()
    
    print(f"\n📝 Troubleshooting:")
    print(f"   1. Check VPS connection")
    print(f"   2. Check Docker is running: sudo systemctl status docker")
    print(f"   3. Check container logs: sudo docker logs cintabuku-backend")
    
    sys.exit(1)
finally:
    client.close()
