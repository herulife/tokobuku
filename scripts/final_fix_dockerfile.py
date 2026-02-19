import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

# Dockerfile that builds from TypeScript source
dockerfile_content = """FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install ALL dependencies (including dev for TypeScript compiler)
RUN npm ci

# Generate Prisma client
RUN npx prisma generate

# Copy TypeScript source
COPY tsconfig.json ./
COPY src ./src

# Build TypeScript to JavaScript
RUN npm run build

# Production stage - slim image
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install production dependencies only
RUN npm ci --only=production && npx prisma generate

# Copy built JavaScript from builder
COPY --from=builder /app/dist ./dist

# Create app user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
RUN mkdir -p /app/uploads /app/logs && chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 5000

CMD ["node", "dist/index.js"]
"""

print("\n🔧 Creating Production Dockerfile on VPS...\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Write Dockerfile
    stdin, stdout, stderr = client.exec_command(f"cat > {REMOTE_APP}/backend/Dockerfile << 'DOCKEREOF'\n{dockerfile_content}\nDOCKEREOF")
    stdout.channel.recv_exit_status()
    print("✅ Dockerfile created\n")
    
    # Stop old container
    print("🛑 Stopping old backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Removed\n")
    
    # Build
    print("🏗️  Building (3-5 minutes)...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend .", get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8')
    
    if 'Successfully' in output:
        print("✅ Build SUCCESS!\n")
    else:
        print("Build output (last 1500 chars):")
        print(output[-1500:])
    
    # Start
    print("🚀 Starting backend...")
    import time
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
    
    # Status
    print("\n✅ Final Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps --format 'table {{{{.Names}}}}\\t{{{{.Status}}}}' | grep cintabuku", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    print(result)
    
    if 'Up' in result and 'cintabuku-backend' in result:
        print("\n🎉 DEPLOYMENT SUCCESS! Both containers UP!\n")
        print("Next: Configure Cloudflare DNS cintabuku.com → 103.107.206.10\n")
    else:
        print("\nCheck logs: sudo docker logs cintabuku-backend\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
