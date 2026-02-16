import paramiko
import sys

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_BASE = "/home/ubuntu24/my-docker-apps"
REMOTE_APP = f"{REMOTE_BASE}/apps/cintabuku"

def execute(ssh, cmd, show=True):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='ignore')
    if show and output:
        print(output)
    return output

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Connecting...")
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Read .env to get password
    print("📖 Reading credentials...")
    env_content = execute(client, f"cat {REMOTE_BASE}/.env | grep CINTABUKU", show=False)
    
    db_pass = ""
    for line in env_content.split('\n'):
        if 'CINTABUKU_DB_PASSWORD=' in line:
            db_pass = line.split('=')[1].strip()
            break
    
    print(f"DB Password: {db_pass[:4]}...{db_pass[-4:]}\n")
    
    # Add services to docker-compose.yml
    print("📝 Adding Cintabuku services...")
    
    services_block = f"""
  # Cintabuku Services
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
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cintabuku_user -d cintabuku"]
      interval: 10s
      timeout: 5s
      retries: 5

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
    depends_on:
      - cintabuku-db
    expose:
      - "5000"
    networks:
      - app-network
"""
    
    execute(client, f"cat >> {REMOTE_BASE}/docker-compose.yml << 'SVCEOF'\n{services_block}\nSVCEOF", show=False)
    
    # Add volume
    volume_line = "  cintabuku_db:"
    execute(client, f"echo '{volume_line}' >> {REMOTE_BASE}/docker-compose.yml", show=False)
    
    print("✅ Services added\n")
    
    # Validate
    result = execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose config > /dev/null 2>&1 && echo 'OK' || echo 'ERROR'", show=False)
    
    if 'OK' in result:
        print("✅ docker-compose.yml valid!\n")
    else:
        print("❌ Validation failed. Showing errors:")
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose config")
        sys.exit(1)
    
    # Start containers
    print("🚀 Starting containers...\n")
    
    print("1️⃣ Starting database...")
    execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-db")
    
    print("\n⏳ Waiting 20 seconds for database...")
    import time
    time.sleep(20)
    
    print("\n2️⃣ Building & starting backend...")
    execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d --build cintabuku-backend")
    
    print("\n⏳ Waiting 15 seconds for backend...")
    time.sleep(15)
    
    print("\n3️⃣ Running migrations...")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy || echo 'Migration may need manual run'")
    
    print("\n✅ Checking status...")
    execute(client, f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku")
    
    print("\n🎉 Deployment Complete!")
    
finally:
    client.close()
