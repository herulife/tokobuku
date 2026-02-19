import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_FRONTEND = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend"

print("\n📦 BUILDING FRONTEND ON VPS\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # 1. Create .env file for production
    print("📝 Creating .env file...")
    # NOTE: NEXT_PUBLIC_API_URL should be the public URL
    env_content = """NEXT_PUBLIC_API_URL=https://cintabuku.com/api/v1
NEXT_PUBLIC_STORAGE_URL=https://cintabuku.com/uploads
NODE_ENV=production
"""
    stdin, stdout, stderr = client.exec_command(f"cat > {REMOTE_FRONTEND}/.env << 'EOF'\n{env_content}\nEOF")
    stdout.channel.recv_exit_status()
    print("✅ .env created\n")
    
    # 2. Install dependencies
    print("📦 Installing dependencies (may take time)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_FRONTEND} && npm install --production=false", get_pty=True)
    # We need the full install for building
    
    # Monitor output for install
    while True:
        line = stdout.readline()
        if not line:
            break
        print(f"   {line.strip()}")
    
    stdout.channel.recv_exit_status()
    print("✅ Dependencies installed\n")
    
    # 3. Build
    print("🔨 Running npm run build...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_FRONTEND} && npm run build", get_pty=True)
    
    # Monitor output for build
    while True:
        line = stdout.readline()
        if not line:
            break
        print(f"   {line.strip()}")
        
    stdout.channel.recv_exit_status()
    print("✅ Build complete\n")
    
    # 4. Start with PM2
    print("🚀 Starting frontend with PM2...")
    # Check if process exists first
    stdin, stdout, stderr = client.exec_command("pm2 delete cintabuku-frontend || true")
    stdout.channel.recv_exit_status()
    
    # Next.js start command for PM2
    start_cmd = f"cd {REMOTE_FRONTEND} && pm2 start npm --name 'cintabuku-frontend' -- start -- -p 3000"
    stdin, stdout, stderr = client.exec_command(start_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Started frontend on port 3000\n")
    
    # 5. Save PM2
    client.exec_command("pm2 save")
    print("✅ PM2 saved\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
