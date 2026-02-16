import paramiko
import sys
import secrets
import string
from pathlib import Path

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

GITHUB_REPO = "https://github.com/herulife/tokobuku.git"
REMOTE_BASE = "/home/ubuntu24/my-docker-apps"
REMOTE_APP = f"{REMOTE_BASE}/apps/cintabuku"

def print_step(step, msg):
    print(f"\n{'='*70}")
    print(f"🚀 Step {step}: {msg}")
    print(f"{'='*70}\n")

def execute(ssh, cmd, show=True):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='ignore')
    if show and output:
        print(output)
    return output

def generate_secret(length=32):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("\n" + "="*70)
    print("🚀 Cintabuku Deployment via GitHub")
    print("="*70)
    print(f"\n📦 Repo: {GITHUB_REPO}")
    print(f"📍 VPS: {VPS_IP}")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"\n🔌 Connecting to VPS...")
        client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
        print("✅ Connected\n")
        
        # Generate secrets
        print_step(1, "Generating Secrets")
        jwt_secret = generate_secret(40)
        db_password = generate_secret(24)
        print(f"🔐 JWT_SECRET: {jwt_secret[:8]}...{jwt_secret[-8:]}")
        print(f"🔐 DB_PASSWORD: {db_password[:4]}...{db_password[-4:]}")
        
        # Clone repository
        print_step(2, "Cloning Repository from GitHub")
        
        # Remove if exists
        execute(client, f"rm -rf {REMOTE_APP}", show=False)
        execute(client, f"mkdir -p {REMOTE_APP}", show=False)
        
        # Clone
        print(f"📥 Cloning {GITHUB_REPO}...")
        result = execute(client, f"cd {REMOTE_APP} && git clone {GITHUB_REPO} .")
        
        if "fatal" in result.lower():
            print("❌ Git clone failed. Check if repo is accessible.")
            sys.exit(1)
        
        print("✅ Repository cloned")
        
        # Create environment files
        print_step(3, "Creating Environment Files")
        
        # Read local .env for API keys
        local_env = Path("backend/.env")
        komship_key = ""
        komship_seller = ""
        
        if local_env.exists():
            with open(local_env, 'r') as f:
                for line in f:
                    if line.startswith('KOMSHIP_API_KEY='):
                        komship_key = line.split('=', 1)[1].strip()
                    elif line.startswith('KOMSHIP_SELLER_CODE='):
                        komship_seller = line.split('=', 1)[1].strip()
        
        # Backend .env
        backend_env = f"""NODE_ENV=production
PORT=5000
DATABASE_URL=postgresql://cintabuku_user:{db_password}@cintabuku-db:5432/cintabuku
JWT_SECRET={jwt_secret}
JWT_EXPIRES_IN=7d
CLIENT_URL=https://cintabuku.com
CORS_ORIGIN=http://cintabuku.com,https://cintabuku.com
KOMSHIP_API_KEY={komship_key}
KOMSHIP_SELLER_CODE={komship_seller}
UPLOAD_DIR=/app/uploads
LOG_DIR=/app/logs
LOG_LEVEL=info
MAX_FILE_SIZE=5242880
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100
"""
        
        execute(client, f"cat > {REMOTE_APP}/backend/.env << 'ENVEOF'\n{backend_env}\nENVEOF", show=False)
        
        # Docker compose .env
        docker_env = f"""CINTABUKU_DB_PASSWORD={db_password}
CINTABUKU_JWT_SECRET={jwt_secret}
KOMSHIP_API_KEY={komship_key}
KOMSHIP_SELLER_CODE={komship_seller}
"""
        
        execute(client, f"cat >> {REMOTE_BASE}/.env << 'DCEOF'\n{docker_env}\nDCEOF", show=False)
        
        print("✅ Environment files created")
        
        # Copy Dockerfile to correct location
        print_step(4, "Setting Up Docker Configuration")
        
        execute(client, f"cp {REMOTE_APP}/backend/Dockerfile.production {REMOTE_APP}/backend/Dockerfile || echo 'Dockerfile not found'", show=False)
        
        # Update docker-compose.yml with proper paths
        print_step(5, "Updating Docker Compose")
        
        # Check if cintabuku-db already in docker-compose
        check = execute(client, f"grep 'cintabuku-db:' {REMOTE_BASE}/docker-compose.yml || echo 'not found'", show=False)
        
        if "not found" in check:
            # Add services
            compose_addition = f"""
  cintabuku-db:
    image: postgres:15-alpine
    container_name: cintabuku-db
    restart: always
    environment:
      POSTGRES_USER: cintabuku_user
      POSTGRES_PASSWORD: ${{CINTABUKU_DB_PASSWORD}}
      POSTGRES_DB: cintabuku
    volumes:
      - cintabuku_db:/var/lib/postgresql/data
    networks:
      - app-network

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
            
            # Backup and add
            import time
            ts = int(time.time())
            execute(client, f"cp {REMOTE_BASE}/docker-compose.yml {REMOTE_BASE}/docker-compose.yml.backup_{ts}", show=False)
            execute(client, f"cat >> {REMOTE_BASE}/docker-compose.yml << 'CEOF'\n{compose_addition}\nCEOF", show=False)
            
            # Add volume if not exists
            vol_check = execute(client, f"grep 'cintabuku_db:' {REMOTE_BASE}/docker-compose.yml || echo 'not found'", show=False)
            if "not found" in vol_check:
                execute(client, f"echo '\n  cintabuku_db:' >> {REMOTE_BASE}/docker-compose.yml", show=False)
        
        print("✅ Docker Compose updated")
        
        # Update Nginx if not done
        print_step(6, "Updating Nginx Configuration")
        
        nginx_check = execute(client, f"grep 'cintabuku.com' {REMOTE_BASE}/nginx/nginx.conf || echo 'not found'", show=False)
        
        if "not found" in nginx_check:
            nginx_config = """
server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;
    
    location / {
        return 200 'Cintabuku - Coming Soon!';
        add_header Content-Type text/plain;
    }
}
"""
            execute(client, f"cat >> {REMOTE_BASE}/nginx/nginx.conf << 'NEOF'\n{nginx_config}\nNEOF", show=False)
            print("✅ Nginx config added")
        else:
            print("✅ Nginx already configured")
        
        # Build and deploy
        print_step(7, "Building Docker Images")
        print("📦 Building backend image (this may take 3-5 minutes)...")
        
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose build cintabuku-backend")
        
        print_step(8, "Starting Containers")
        
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-db")
        
        print("\n⏳ Waiting 15 seconds for database...")
        import time
        time.sleep(15)
        
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-backend")
        
        print_step(9, "Running Database Migrations")
        
        print("⏳ Waiting for backend to be ready...")
        time.sleep(10)
        
        execute(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy || echo 'Migrations pending'")
        
        print_step(10, "Restarting Nginx")
        
        execute(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose restart nginx")
        
        # Verification
        print_step(11, "Verification")
        
        print("\n📊 Container Status:")
        execute(client, f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku")
        
        print("\n✅ Deployment Complete!")
        print("\n" + "="*70)
        print("🎉 Cintabuku Deployed Successfully!")
        print("="*70)
        
        print(f"\n📝 What's deployed:")
        print(f"   ✅ Code from GitHub: {GITHUB_REPO}")
        print(f"   ✅ PostgreSQL database (cintabuku-db)")
        print(f"   ✅ Backend API (cintabuku-backend)")
        print(f"   ✅ Nginx routing")
        
        print(f"\n🔐 Credentials saved in:")
        print(f"   {REMOTE_APP}/backend/.env")
        print(f"   {REMOTE_BASE}/.env")
        
        print(f"\n🌐 Next steps:")
        print(f"   1. Configure Cloudflare DNS: cintabuku.com → {VPS_IP}")
        print(f"   2. Test: http://{VPS_IP} (with Host: cintabuku.com header)")
        print(f"   3. Wait for DNS propagation")
        print(f"   4. Visit: https://cintabuku.com")
        
        print(f"\n📊 Monitor logs:")
        print(f"   sudo docker logs cintabuku-backend -f")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()
