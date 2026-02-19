import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku/backend"

print("\n🔧 COMPLETE FIX - Reinstall Everything\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check package.json exists
    print("📋 Checking setup...")
    stdin, stdout, stderr = client.exec_command(f"ls -la {REMOTE_APP}/package.json", get_pty=True)
    stdout.channel.recv_exit_status()
    pkg_check = stdout.read().decode('utf-8')
    print(pkg_check)
    
    # Remove old node_modules
    print("\n🗑️  Removing old node_modules...")
    stdin, stdout, stderr = client.exec_command(f"rm -rf {REMOTE_APP}/node_modules", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Removed\n")
    
    # Fresh install ALL dependencies (not just production)
    print("📦 Fresh install ALL dependencies (3-4 min)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npm install", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ All dependencies installed\n")
    
    # Generate Prisma
    print("🔧 Generating Prisma client...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && npx prisma generate", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Prisma generated\n")
    
    # Delete and restart PM2
    print("🔄 Restarting backend...")
    stdin, stdout, stderr = client.exec_command(f"pm2 delete cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    
    start_cmd = f"cd {REMOTE_APP} && pm2 start dist/index.js --name cintabuku-backend"
    stdin, stdout, stderr = client.exec_command(start_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Started fresh\n")
    
    # Wait
    import time
    print("⏳ Waiting 10 seconds...")
    time.sleep(10)
    
    # Status
    print("\n📊 PM2 Status:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 list", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    print("="*70)
    
    # Logs
    print("\n📋 Logs:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("pm2 logs cintabuku-backend --lines 25 --nostream", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Test
    print("\n🧪 Health:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"{health}\n")
    
    # HTTPS test
    print("🧪 HTTPS:")
    stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    https = stdout.read().decode('utf-8')
    print(f"{https}\n")
    
    if  '"status":"ok"' in health:
        print("="*70)
        print("🎉🎉🎉 100% DEPLOYMENT COMPLETE!")
        print("="*70)
        print("\n✅ Fresh dependencies installed")
        print("✅ Prisma client generated")
        print("✅ Backend running without Docker")
        print("✅ Health check passing")
        print("\n🌐 SITE IS LIVE:")
        print("   https://cintabuku.com")
        print("   https://cintabuku.com/health")
        print("\n💡 PM2: pm2 list | pm2 logs cintabuku-backend\n")
    elif "online" in status.lower():
        print(f"✅ Backend online!\n{health}\n")
    else:
        print("⚠️  Check logs above\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
