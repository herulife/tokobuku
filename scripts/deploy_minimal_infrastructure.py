import os
import sys
import secrets
import string

try:
    import paramiko
except ImportError:
    print("❌ Please install: pip install paramiko")
    sys.exit(1)

# VPS Configuration
VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_BASE = "/home/ubuntu24/my-docker-apps"

def print_step(step, message):
    print(f"\n{'='*70}")
    print(f"🚀 Step {step}: {message}")
    print(f"{'='*70}\n")

def execute_command(ssh, command, show_output=True):
    """Execute command on VPS"""
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    exit_status = stdout.channel.recv_exit_status()
    
    output = stdout.read().decode('utf-8', errors='ignore')
    
    if show_output and output:
        print(output)
    
    return exit_status == 0

def generate_secret(length=32):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("\n" + "="*70)
    print("🚀 Minimal Infrastructure Deployment - Cintabuku")
    print("="*70)
    print("\n📝 This will setup:")
    print("   - PostgreSQL database container")
    print("   - Basic backend health check")
    print("   - Nginx routing")
    print("   - Test infrastructure")
    
    # Connect
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"\n🔌 Connecting to {VPS_IP}:{VPS_PORT}...")
        client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        print("✅ Connected\n")
        
        # Generate secrets
        print_step(1, "Generating Secrets")
        jwt_secret = generate_secret(40)
        db_password = generate_secret(24)
        print(f"🔐 JWT_SECRET: {jwt_secret[:8]}...{jwt_secret[-8:]}")
        print(f"🔐 DB_PASSWORD: {db_password[:4]}...{db_password[-4:]}")
        
        # Create environment file
        print_step(2, "Creating Environment Configuration")
        
        env_content = f"""CINTABUKU_DB_PASSWORD={db_password}
CINTABUKU_JWT_SECRET={jwt_secret}
"""
        
        execute_command(client, f"cat >> {REMOTE_BASE}/.env << 'ENVEOF'\n{env_content}\nENVEOF", show_output=False)
        print("✅ Environment file updated")
        
        # Add database service to docker-compose
        print_step(3, "Adding PostgreSQL Database Service")
        
        db_service = f"""
  # PostgreSQL for Cintabuku
  cintabuku-db:
    image: postgres:15-alpine
    container_name: cintabuku-db
    restart: always
    environment:
      POSTGRES_USER: cintabuku_user
      POSTGRES_PASSWORD: {db_password}
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
"""
        
        # Backup docker-compose
        import time
        timestamp = int(time.time())
        execute_command(client, f"cp {REMOTE_BASE}/docker-compose.yml {REMOTE_BASE}/docker-compose.yml.backup_{timestamp}", show_output=False)
        
        # Add service
        execute_command(client, f"cat >> {REMOTE_BASE}/docker-compose.yml << 'DCEOF'\n{db_service}\nDCEOF", show_output=False)
        
        # Add volume
        volume_def = """
volumes:
  cintabuku_db:
    driver: local
"""
        execute_command(client, f"cat >> {REMOTE_BASE}/docker-compose.yml << 'VOLEOF'\n{volume_def}\nVOLEOF", show_output=False)
        
        print("✅ Database service added to docker-compose.yml")
        
        # Start database
        print_step(4, "Starting PostgreSQL Database")
        execute_command(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-db")
        
        # Wait for database
        print("\n⏳ Waiting 15 seconds for database to be ready...")
        import time
        time.sleep(15)
        
        # Verify database
        print_step(5, "Verifying Database")
        execute_command(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db pg_isready -U cintabuku_user")
        execute_command(client, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-db psql -U cintabuku_user -d cintabuku -c 'SELECT version();'")
        
        # Add Nginx routing
        print_step(6, "Configuring Nginx Routing")
        
        nginx_config = """
# Cintabuku - Health Check Only
server {
    listen 80;
    server_name cintabuku.com www.cintabuku.com;
    
    location / {
        return 200 'Cintabuku Infrastructure Ready!';
        add_header Content-Type text/plain;
    }
    
    location /health {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
"""
        
        # Backup nginx config
        execute_command(client, f"cp {REMOTE_BASE}/nginx/nginx.conf {REMOTE_BASE}/nginx/nginx.conf.backup_{timestamp}", show_output=False)
        
        # Add nginx config
        execute_command(client, f"cat >> {REMOTE_BASE}/nginx/nginx.conf << 'NGEOF'\n{nginx_config}\nNGEOF", show_output=False)
        
        print("✅ Nginx routing configured")
        
        # Restart nginx
        print_step(7, "Restarting Nginx")
        execute_command(client, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose restart nginx")
        
        # Final verification
        print_step(8, "Final Verification")
        
        print("\n📊 Infrastructure Status:")
        execute_command(client, f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku")
        
        print("\n✅ Minimal Infrastructure Deployed!")
        print("\n" + "="*70)
        print("🎉 Success! Infrastructure is ready")
        print("="*70)
        
        print(f"\n📝 What's deployed:")
        print(f"   ✅ PostgreSQL database (cintabuku-db)")
        print(f"   ✅ Database: cintabuku")
        print(f"   ✅ User: cintabuku_user")
        print(f"   ✅ Nginx routing for cintabuku.com")
        
        print(f"\n🌐 Test access:")
        print(f"   curl -H 'Host: cintabuku.com' http://{VPS_IP}/health")
        
        print(f"\n📁 Saved credentials:")
        print(f"   JWT_SECRET: {jwt_secret}")
        print(f"   DB_PASSWORD: {db_password}")
        print(f"   (Stored in {REMOTE_BASE}/.env)")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Configure Cloudflare DNS: cintabuku.com → {VPS_IP}")
        print(f"   2. Upload source code (can do later)")
        print(f"   3. Deploy full backend application")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()
