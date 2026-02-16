import os
import sys
import time
import secrets
import string
import zipfile
from pathlib import Path

try:
    import paramiko
    from scp import SCPClient
except ImportError:
    print("❌ Required modules not installed!")
    print("Please run: pip install paramiko scp")
    sys.exit(1)

# VPS Configuration
VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

# Deployment paths
REMOTE_BASE = "/home/ubuntu24/my-docker-apps"
REMOTE_APPS = f"{REMOTE_BASE}/apps/cintabuku"
TEMP_DIR = "/tmp/cintabuku_deploy"

def print_step(step, message):
    print(f"\n{'='*70}")
    print(f"🚀 Step {step}: {message}")
    print(f"{'='*70}\n")

def generate_secure_secret(length=32):
    """Generate cryptographically secure random string"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_ssh_client():
    """Create SSH connection to VPS"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"🔌 Connecting to {VPS_IP}:{VPS_PORT}...")
        client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        print("✅ Connected successfully\n")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

def execute_command(ssh, command, show_output=True, check_error=True):
    """Execute command on VPS"""
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    exit_status = stdout.channel.recv_exit_status()
    
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    if show_output and output:
        print(output)
    
    if check_error and exit_status != 0:
        print(f"⚠️  Command exited with status {exit_status}")
        if error:
            print(f"Error: {error}")
        return False
    
    return True

def create_source_archive():
    """Create ZIP archive of source code"""
    print_step(1, "Creating Source Code Archive")
    
    project_root = Path(__file__).parent.parent
    
    archive_name = f"cintabuku_source_{int(time.time())}.zip"
    archive_path = project_root / archive_name
    
    print(f"📦 Creating {archive_name}...")
    
    # Files and directories to include
    frontend_files = [
        'frontend/src',
        'frontend/public',
        'frontend/package.json',
        'frontend/package-lock.json',
        'frontend/next.config.ts',
        'frontend/tsconfig.json',
        'frontend/tailwind.config.ts',
        'frontend/postcss.config.mjs',
        'frontend/eslint.config.mjs',
        'frontend/.env.local',
    ]
    
    backend_files = [
        'backend/src',
        'backend/prisma',
        'backend/package.json',
        'backend/package-lock.json',
        'backend/tsconfig.json',
        'backend/.env',
    ]
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add frontend files
        for item in frontend_files:
            full_path = project_root / item
            if full_path.exists():
                if full_path.is_file():
                    zipf.write(full_path, item)
                else:
                    for root, dirs, files in os.walk(full_path):
                        # Skip node_modules, .next, .git
                        dirs[:] = [d for d in dirs if d not in ['.next', 'node_modules', '.git', 'dist']]
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(project_root)
                            zipf.write(file_path, arcname)
        
        # Add backend files
        for item in backend_files:
            full_path = project_root / item
            if full_path.exists():
                if full_path.is_file():
                    zipf.write(full_path, item)
                else:
                    for root, dirs, files in os.walk(full_path):
                        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist']]
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(project_root)
                            zipf.write(file_path, arcname)
    
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    print(f"✅ Archive created: {archive_name} ({size_mb:.2f} MB)")
    
    return archive_path

def upload_files(ssh, archive_path):
    """Upload source archive to VPS"""
    print_step(2, "Uploading Source Code to VPS")
    
    remote_archive = f"/tmp/{archive_path.name}"
    
    print(f"📤 Uploading {archive_path.name}...")
    start_time = time.time()
    
    with SCPClient(ssh.get_transport(), progress=lambda x, y, z: None) as scp:
        scp.put(str(archive_path), remote_archive)
    
    duration = time.time() - start_time
    print(f"✅ Upload complete ({duration:.1f}s)")
    return remote_archive

def upload_configs(ssh):
    """Upload Docker and Nginx configs"""
    print_step(3, "Uploading Configuration Files")
    
    project_root = Path(__file__).parent.parent
    
    # Create temp directory on VPS
    execute_command(ssh, f"mkdir -p {TEMP_DIR}", show_output=False)
    
    configs = {
        'docker-compose.cintabuku.yml': f'{TEMP_DIR}/docker-compose.cintabuku.yml',
        'nginx-cintabuku.conf': f'{TEMP_DIR}/nginx-cintabuku.conf',
        'backend/Dockerfile.production': f'{TEMP_DIR}/Dockerfile.production'
    }
    
    with SCPClient(ssh.get_transport()) as scp:
        for local_file, remote_file in configs.items():
            local_path = project_root / local_file
            if local_path.exists():
                print(f"📤 {local_file} → {remote_file}")
                scp.put(str(local_path), remote_file)
    
    print("✅ Configs uploaded")

def setup_vps_structure(ssh):
    """Create directory structure on VPS"""
    print_step(4, "Setting Up VPS Directory Structure")
    
    commands = [
        f"mkdir -p {REMOTE_APPS}/frontend",
        f"mkdir -p {REMOTE_APPS}/backend",
        f"mkdir -p {REMOTE_APPS}/uploads",
        f"mkdir -p {REMOTE_APPS}/logs",
        f"chmod 755 {REMOTE_APPS}",
        f"chmod 777 {REMOTE_APPS}/uploads {REMOTE_APPS}/logs"
    ]
    
    for cmd in commands:
        execute_command(ssh, cmd, show_output=False)
    
    print("✅ Directory structure created")

def extract_source(ssh, remote_archive):
    """Extract source code on VPS"""
    print_step(5, "Extracting Source Code")
    
    commands = [
        f"cd {TEMP_DIR} && unzip -o {remote_archive}",
        f"cp -r {TEMP_DIR}/frontend/* {REMOTE_APPS}/frontend/ 2>/dev/null || true",
        f"cp -r {TEMP_DIR}/backend/* {REMOTE_APPS}/backend/ 2>/dev/null || true",
        f"cp {TEMP_DIR}/Dockerfile.production {REMOTE_APPS}/backend/",
        f"rm {remote_archive}"
    ]
    
    for cmd in commands:
        execute_command(ssh, cmd, show_output=False)
    
    print("✅ Source code extracted")

def configure_environment(ssh):
    """Generate and configure production environment variables"""
    print_step(6, "Configuring Production Environment")
    
    # Generate secrets
    jwt_secret = generate_secure_secret(40)
    db_password = generate_secure_secret(24)
    
    print(f"🔐 Generated JWT_SECRET: {jwt_secret[:8]}...{jwt_secret[-8:]}")
    print(f"🔐 Generated DB_PASSWORD: {db_password[:4]}...{db_password[-4:]}")
    
    # Read Komship API keys from local .env
    project_root = Path(__file__).parent.parent
    local_env = project_root / 'backend' / '.env'
    
    komship_key = ""
    komship_seller = ""
    
    if local_env.exists():
        with open(local_env, 'r') as f:
            for line in f:
                if line.startswith('KOMSHIP_API_KEY='):
                    komship_key = line.split('=', 1)[1].strip()
                elif line.startswith('KOMSHIP_SELLER_CODE='):
                    komship_seller = line.split('=', 1)[1].strip()
    
    # Create backend .env for Docker build
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
    
    # Create docker-compose .env
    docker_env = f"""CINTABUKU_DB_PASSWORD={db_password}
CINTABUKU_JWT_SECRET={jwt_secret}
KOMSHIP_API_KEY={komship_key}
KOMSHIP_SELLER_CODE={komship_seller}
"""
    
    # Write to VPS
    execute_command(ssh, f"cat > {REMOTE_APPS}/backend/.env << 'ENVEOF'\n{backend_env}\nENVEOF", show_output=False)
    execute_command(ssh, f"cat >> {REMOTE_BASE}/.env << 'ENVEOF'\n{docker_env}\nENVEOF", show_output=False)
    
    print("✅ Environment configured")
    
    return db_password

def merge_docker_compose(ssh):
    """Merge Cintabuku services into existing docker-compose.yml"""
    print_step(7, "Updating Docker Compose Configuration")
    
    # Backup existing
    timestamp = int(time.time())
    execute_command(ssh, f"cp {REMOTE_BASE}/docker-compose.yml {REMOTE_BASE}/docker-compose.yml.backup_{timestamp}", show_output=False)
    
    # Append cintabuku services
    execute_command(ssh, f"cat {TEMP_DIR}/docker-compose.cintabuku.yml >> {REMOTE_BASE}/docker-compose.yml", show_output=False)
    
    print("✅ Docker Compose updated")

def update_nginx_config(ssh):
    """Append Cintabuku server block to nginx.conf"""
    print_step(8, "Updating Nginx Configuration")
    
    timestamp = int(time.time())
    
    commands = [
        f"cp {REMOTE_BASE}/nginx/nginx.conf {REMOTE_BASE}/nginx/nginx.conf.backup_{timestamp}",
        f"cat {TEMP_DIR}/nginx-cintabuku.conf >> {REMOTE_BASE}/nginx/nginx.conf"
    ]
    
    for cmd in commands:
        execute_command(ssh, cmd, show_output=False)
    
    # Update nginx volume mounts in docker-compose.yml
    print("Adding nginx volume mounts for cintabuku...")
    
    volume_adds = f"""
# Add cintabuku frontend volume mount to nginx service
sed -i '/nginx:/,/networks:/{{
  /volumes:/a\\      - ./apps/cintabuku/frontend/.next/static:/usr/share/nginx/html/cintabuku/_next/static:ro\\n      - ./apps/cintabuku/uploads:/usr/share/nginx/html/cintabuku-uploads:ro
}}' {REMOTE_BASE}/docker-compose.yml
"""
    
    execute_command(ssh, volume_adds, show_output=False, check_error=False)
    
    print("✅ Nginx config updated")

def build_and_deploy(ssh):
    """Build Docker image and start containers"""
    print_step(9, "Building and Deploying Containers")
    
    print("📦 Building backend Docker image (this may take 3-5 minutes)...")
    execute_command(ssh, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose build cintabuku-backend", check_error=False)
    
    print("\n🚀 Starting database container...")
    execute_command(ssh, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-db", check_error=False)
    
    print("\n⏳ Waiting 10 seconds for database to be ready...")
    time.sleep(10)
    
    print("\n🚀 Starting backend container...")
    execute_command(ssh, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose up -d cintabuku-backend", check_error=False)
    
    print("\n✅ Containers deployed")

def run_migrations(ssh):
    """Run database migrations"""
    print_step(10, "Running Database Migrations")
    
    print("⏳ Waiting 15 seconds for backend to be fully ready...")
    time.sleep(15)
    
    print("\n🗄️ Running Prisma migrations...")
    execute_command(ssh, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma migrate deploy", check_error=False)
    
    print("\n🌱 Seeding database...")
    execute_command(ssh, f"echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend npx prisma db seed || echo 'Seed script not found or failed'", check_error=False)
    
    print("✅ Migrations completed")

def restart_nginx(ssh):
    """Restart nginx to load new config"""
    print_step(11, "Restarting Nginx")
    
    execute_command(ssh, f"cd {REMOTE_BASE} && echo '{VPS_PASS}' | sudo -S docker compose restart nginx", show_output=False)
    
    print("✅ Nginx restarted")

def verify_deployment(ssh):
    """Verify deployment success"""
    print_step(12, "Verifying Deployment")
    
    checks = [
        ("Container status", f"echo '{VPS_PASS}' | sudo -S docker ps | grep cintabuku"),
        ("Backend health (may take a moment)", f"sleep 5 && echo '{VPS_PASS}' | sudo -S docker exec cintabuku-backend wget -q -O- http://localhost:5000/health 2>&1 || echo 'Health check pending...'"),
    ]
    
    for name, cmd in checks:
        print(f"\n🔍 {name}:")
        execute_command(ssh, cmd, check_error=False)
    
    print("\n✅ Verification complete")

def cleanup(ssh, archive_path):
    """Cleanup temp files"""
    print_step(13, "Cleanup")
    
    # Remove local archive
    if archive_path.exists():
        archive_path.unlink()
        print(f"🗑️  Removed local archive: {archive_path.name}")
    
    # Remove temp dir on VPS
    execute_command(ssh, f"rm -rf {TEMP_DIR}", show_output=False)
    print("🗑️  Removed temp files on VPS")
    
    print("✅ Cleanup complete")

def main():
    print("\n" + "="*70)
    print("🚀 Cintabuku Docker Build Deployment")
    print("="*70)
    print("\n📝 Source code will be uploaded and built on VPS using Docker")
    
    # Confirm deployment
    print(f"\n📡 Target VPS: {VPS_IP}")
    print(f"📁 Deployment path: {REMOTE_APPS}")
    
    response = input("\n⚠️  Continue with deployment? [y/N]: ")
    if response.lower() != 'y':
        print("❌ Deployment cancelled")
        sys.exit(0)
    
    archive_path = None
    ssh = None
    
    try:
        # Create source archive
        archive_path = create_source_archive()
        
        # Connect to VPS
        ssh = create_ssh_client()
        
        # Execute deployment steps
        setup_vps_structure(ssh)
        upload_configs(ssh)
        remote_archive = upload_files(ssh, archive_path)
        extract_source(ssh, remote_archive)
        configure_environment(ssh)
        merge_docker_compose(ssh)
        update_nginx_config(ssh)
        build_and_deploy(ssh)
        run_migrations(ssh)
        restart_nginx(ssh)
        verify_deployment(ssh)
        cleanup(ssh, archive_path)
        
        print("\n" + "="*70)
        print("✅ Deployment Completed Successfully!")
        print("="*70)
        print(f"\n🌐 Next steps:")
        print(f"   1. Configure Cloudflare DNS A record: cintabuku.com → {VPS_IP}")
        print(f"   2. Wait 5-10 minutes for DNS propagation")
        print(f"   3. Visit https://cintabuku.com")
        print(f"   4. Monitor: docker logs cintabuku-backend -f")
        
    except KeyboardInterrupt:
        print("\n\n❌ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    main()
