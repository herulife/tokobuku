import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("\n🚀 Final Deploy - Using ts-node Runtime\n")

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Create Dockerfile for ts-node runtime
    print("📝 Creating ts-node Dockerfile...")
    
    dockerfile = """FROM node:20-alpine

WORKDIR /app

# Install dependencies  
COPY package*.json ./
COPY prisma ./prisma/
RUN npm ci && npx prisma generate

# Install ts-node globally
RUN npm install -g ts-node typescript

# Copy source code
COPY tsconfig.json ./
COPY src ./src

# Create directories
RUN mkdir -p /app/uploads /app/logs

EXPOSE 5000

# Run with ts-node (no build needed!)
CMD ["npx", "ts-node", "src/index.ts"]
"""
    
    stdin, stdout, stderr = client.exec_command(f"cat > {REMOTE_APP}/backend/Dockerfile.tsnode << 'EOF'\n{dockerfile}\nEOF", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Dockerfile created\n")
    
    # Build image
    print("🏗️  Building (2-3 minutes)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend -f Dockerfile.tsnode .", get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8')
    
    if 'Successfully built' in output or 'Successfully tagged' in output:
        print("✅ Build success!\n")
    else:
        print(output[-500:])
    
    # Start backend
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
    print(stdout.read().decode('utf-8'))
    
    time.sleep(15)
    
    # Migrations
    print("\n📊 Running migrations...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Verify
    print("\n✅ Verification:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    print(result)
    
    if 'cintabuku-backend' in result and 'cintabuku-db' in result:
        print("\n🎉 DEPLOYMENT COMPLETE!")
        print(f"\n📍 Services:")
        print(f"   - Database: port 5433")
        print(f"   - Backend: port 5000")
        print(f"\n🌐 Next: Configure DNS cintabuku.com → {VPS_IP}")
        print(f"\nTest: http://{VPS_IP}:5000/health\n")
    else:
        print("\n⚠️  Backend may not have started. Check logs:")
        print(f"   sudo docker logs cintabuku-backend\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
