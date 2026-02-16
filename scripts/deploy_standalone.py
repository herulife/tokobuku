import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"
REMOTE_BASE = "/home/ubuntu24/my-docker-apps"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("\n🚀 Final Deploy - Standalone Approach\n")

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Get DB password from .env
    stdin, stdout, stderr = client.exec_command(f"grep CINTABUKU_DB_PASSWORD {REMOTE_BASE}/.env")
    stdout.channel.recv_exit_status()
    env_line = stdout.read().decode('utf-8')
    db_pass = env_line.split('=')[1].strip() if '=' in env_line else "defaultpass"
    
    print(f"🔐 DB Pass: {db_pass[:4]}...{db_pass[-4:]}\n")
    
    # Create simple standalone docker-compose
    compose = f"""version: '3.8'

services:
  cintabuku-db:
    image: postgres:15-alpine
    container_name: cintabuku-db
    restart: always
    environment:
      POSTGRES_USER: cintabuku_user
      POSTGRES_PASSWORD: {db_pass}
      POSTGRES_DB: cintabuku
    volumes:
      - cintabuku_db:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  cintabuku-backend:
    build:
      context: {REMOTE_APP}/backend
      dockerfile: Dockerfile
    container_name: cintabuku-backend
    restart: always
    env_file:
      - {REMOTE_APP}/backend/.env
    volumes:
      - {REMOTE_APP}/uploads:/app/uploads
      - {REMOTE_APP}/logs:/app/logs
    ports:
      - "5000:5000"
    depends_on:
      - cintabuku-db

volumes:
  cintabuku_db:
"""
    
    # Write compose file
    print("📝 Creating standalone docker-compose...")
    stdin, stdout, stderr = client.exec_command(f"cat > {REMOTE_APP}/docker-compose.standalone.yml << 'EOF'\n{compose}\nEOF")
    stdout.channel.recv_exit_status()
    print("✅ Created\n")
    
    # Start services
    print("🚀 Starting services...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && echo '{VPS_PASS}' | sudo -S docker compose -f docker-compose.standalone.yml up -d --build", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    print("\n⏳ Waiting 30 seconds...")
    time.sleep(30)
    
    # Run migrations
    print("\n📊 Running migrations...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Check status
    print("\n✅ Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    print("\n🎉 DONE! Containers running:")
    print(f"   - Database: localhost:5433")
    print(f"   - Backend: localhost:5000")
    print(f"\nNext: Configure Cloudflare DNS cintabuku.com → {VPS_IP}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
