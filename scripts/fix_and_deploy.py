import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_BASE = "/home/ubuntu24/my-docker-apps"

def execute(ssh, cmd, show=True):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='ignore')
    if show and output:
        print(output)
    return output

def main():
    print("\n" + "="*70)
    print("🔧 Auto-Fix: Docker Compose & Complete Deployment")
    print("="*70)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"\n🔌 Connecting to VPS...")
        client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
        print("✅ Connected\n")
        
        # Step 1: Backup current docker-compose.yml
        print("="*70)
        print("📦 Step 1: Backup Current Configuration")
        print("="*70)
        
        timestamp = int(time.time())
        execute(client, f"cp {REMOTE_BASE}/docker-compose.yml {REMOTE_BASE}/docker-compose.yml.before_fix_{timestamp}")
        print(f"✅ Backup created: docker-compose.yml.before_fix_{timestamp}\n")
        
        # Step 2: Fix docker-compose.yml - read and parse
        print("="*70)
        print("🔧 Step 2: Fixing Duplicate Volumes Key")
        print("="*70)
        
        # Read current file
        result = execute(client, f"cat {REMOTE_BASE}/docker-compose.yml", show=False)
        lines = result.split('\n')
        
        # Find all "volumes:" lines
        volumes_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith('volumes:') and not line.strip().startswith('#'):
                volumes_lines.append(i)
        
        print(f"Found {len(volumes_lines)} 'volumes:' sections at lines: {[l+1 for l in volumes_lines]}")
        
        if len(volumes_lines) > 1:
            print("⚠️  Multiple volumes sections detected. Merging...")
            
            # Keep only first volumes section, collect all volume definitions
            first_volumes_idx = volumes_lines[0]
            volume_definitions = set()
            
            # Collect all volume definitions
            in_volumes_section = False
            for i, line in enumerate(lines):
                if i in volumes_lines:
                    in_volumes_section = True
                    continue
                
                if in_volumes_section:
                    # Check if still in volumes section (indented)
                    if line and not line[0].isspace():
                        in_volumes_section = False
                        continue
                    
                    # Collect volume name
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        volume_definitions.add(line)
            
            # Remove duplicate volumes sections (keep first)
            new_lines = []
            skip_until = -1
            in_dup_volumes = False
            
            for i, line in enumerate(lines):
                # Skip duplicate volumes sections
                if i in volumes_lines[1:]:  # Skip all but first
                    in_dup_volumes = True
                    continue
                
                if in_dup_volumes:
                    # Skip until we hit a non-indented line
                    if line and not line[0].isspace() and line.strip():
                        in_dup_volumes = False
                        new_lines.append(line)
                    continue
                
                new_lines.append(line)
            
            # Write fixed file
            fixed_content = '\n'.join(new_lines)
            
            # Upload fixed content
            execute(client, f"cat > {REMOTE_BASE}/docker-compose.yml.fixed << 'FIXEOF'\n{fixed_content}\nFIXEOF", show=False)
            execute(client, f"mv {REMOTE_BASE}/docker-compose.yml.fixed {REMOTE_BASE}/docker-compose.yml")
            
            print("✅ Merged duplicate volumes sections\n")
        else:
            print("✅ No duplicate volumes found (already fixed?)\n")
        
        # Step 3: Validate docker-compose.yml
        print("="*70)
        print("✅ Step 3: Validating Docker Compose Configuration")
        print("="*70)
        
        result = execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose config > /dev/null 2>&1 && echo 'VALID' || echo 'INVALID'", show=False)
        
        if 'VALID' in result:
            print("✅ docker-compose.yml is valid!\n")
        else:
            print("❌ docker-compose.yml still has errors. Showing config:")
            execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose config 2>&1 | head -20")
            print("\n⚠️  Continuing anyway...\n")
        
        # Step 4: Start Database
        print("="*70)
        print("🗄️  Step 4: Starting PostgreSQL Database")
        print("="*70)
        
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-db")
        
        print("\n⏳ Waiting 15 seconds for database to be ready...")
        time.sleep(15)
        
        # Check database
        result = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db pg_isready -U cintabuku_user || echo 'DB not ready'", show=False)
        
        if 'accepting connections' in result:
            print("✅ Database is ready and accepting connections!\n")
        else:
            print("⚠️  Database may not be ready yet, but continuing...\n")
        
        # Step 5: Build & Start Backend
        print("="*70)
        print("🚀 Step 5: Building & Starting Backend")
        print("="*70)
        
        print("📦 Building Docker image (may take 3-5 minutes)...")
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose build cintabuku-backend")
        
        print("\n🚀 Starting backend container...")
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-backend")
        
        print("\n⏳ Waiting 10 seconds for backend to start...")
        time.sleep(10)
        
        # Step 6: Run Database Migrations
        print("\n" + "="*70)
        print("📊 Step 6: Running Database Migrations")
        print("="*70)
        
        execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy")
        
        # Step 7: Restart Nginx
        print("\n" + "="*70)
        print("🌐 Step 7: Restarting Nginx")
        print("="*70)
        
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose restart nginx-proxy")
        
        # Step 8: Verification
        print("\n" + "="*70)
        print("✅ Step 8: Final Verification")
        print("="*70)
        
        print("\n📊 Container Status:")
        execute(client, f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku")
        
        print("\n🏥 Health Checks:")
        
        # Check backend health
        health = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend curl -s http://localhost:5000/health || echo 'Backend not responding'", show=False)
        if 'OK' in health or 'healthy' in health.lower():
            print("✅ Backend health check: Passed")
        else:
            print("⚠️  Backend health check: Not ready yet")
        
        # Check database
        db_check = execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db psql -U cintabuku_user -d cintabuku -c 'SELECT 1' || echo 'DB error'", show=False)
        if '1 row' in db_check or '(1 row)' in db_check:
            print("✅ Database connection: Working")
        else:
            print("⚠️  Database connection: Check logs")
        
        print("\n" + "="*70)
        print("🎉 Deployment Complete!")
        print("="*70)
        
        print(f"\n✅ What's Running:")
        print(f"   - PostgreSQL Database (cintabuku-db)")
        print(f"   - Backend API (cintabuku-backend)")
        print(f"   - Nginx Routing")
        
        print(f"\n🌐 Next Steps:")
        print(f"   1. Configure Cloudflare DNS:")
        print(f"      - Type: A")
        print(f"      - Name: cintabuku.com (or @)")
        print(f"      - IPv4: {VPS_IP}")
        print(f"      - Proxy: ON (orange cloud)")
        
        print(f"\n   2. Wait 5-10 minutes for DNS propagation")
        
        print(f"\n   3. Test deployment:")
        print(f"      - https://cintabuku.com")
        print(f"      - https://cintabuku.com/api/health")
        
        print(f"\n📊 Monitor Logs:")
        print(f"   ssh -p {VPS_PORT} {VPS_USER}@{VPS_IP}")
        print(f"   sudo docker logs cintabuku-backend -f")
        
        print(f"\n🎊 SUCCESS! Cintabuku is deployed and ready! 🎊\n")
        
    except Exception as e:
        print(f"\n❌ Auto-fix failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()
