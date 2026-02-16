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

print("\n🔧 Fixing Backend & Completing Deployment\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Create fixed Dockerfile that builds from source
    print("📝 Creating build-from-source Dockerfile...")
    
    dockerfile_content = """FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install dependencies and generate Prisma client
RUN npm ci && npx prisma generate

# Copy source code
COPY tsconfig.json ./
COPY src ./src

# Build TypeScript
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install production dependencies only
RUN npm ci --only=production && npx prisma generate

# Copy built files from builder
COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Create directories
RUN mkdir -p /app/uploads /app/logs && chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 5000

CMD ["node", "dist/index.js"]
"""
    
    execute(client, f"cat > {REMOTE_APP}/backend/Dockerfile.fixed << 'EOFDF'\n{dockerfile_content}\nEOFDF", show=False)
    print("✅ Created fixed Dockerfile\n")
    
    # Build with fixed Dockerfile
    print("🏗️  Building backend (3-5 minutes)...")
    build_cmd = f"cd {REMOTE_APP}/backend && echo '{VPS_PASS}' | sudo -S docker build -t cintabuku-backend -f Dockerfile.fixed ."
    execute(client, build_cmd)
    print("✅ Build complete\n")
    
    # Start backend
    print("🚀 Starting backend...")
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
    
    time.sleep(15)
    
    # Run migrations
    print("\n📊 Running migrations...")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy")
    
    # Verify
    print("\n✅ Final Check:")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku")
    
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print(f"\n📍 Access:")
    print(f"   - Database: localhost:5433")
    print(f"   - Backend: localhost:5000")
    print(f"\n🌐 Next: Configure DNS cintabuku.com → {VPS_IP}\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
