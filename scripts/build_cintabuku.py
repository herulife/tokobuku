import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"📦 Step {step}: {message}")
    print(f"{'='*60}\n")

def run_command(cmd, cwd=None):
    """Run command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def clean_dir(path):
    """Remove directory handling permission errors"""
    if path.exists():
        try:
            shutil.rmtree(path)
            return True
        except PermissionError:
            print(f"⚠️  Cannot remove {path} (files in use, skipping...)")
            return False
        except Exception as e:
            print(f"⚠️  Error removing {path}: {e}")
            return False
    return True

def main():
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🏗️  Cintabuku Production Build Script")
    print(f"📁 Project root: {project_root}\n")
    
    # Step 1: Clean previous builds
    print_step(1, "Cleaning previous builds")
    
    dirs_to_clean = [
        'frontend/dist',
        'frontend/.next',
        'backend/dist',
        'build_output'
    ]
    
    for dir_path in dirs_to_clean:
        full_path = project_root / dir_path
        print(f"🗑️  Removing {dir_path}...")
        clean_dir(full_path)
    
    # Step 2: Build Frontend
    print_step(2, "Building Frontend (Next.js)")
    
    frontend_dir = project_root / 'frontend'
    print("📦 Installing frontend dependencies...")
    run_command("npm ci", cwd=frontend_dir)
    
    print("🔨 Building production bundle...")
    run_command("npm run build", cwd=frontend_dir)
    
    # Check if build output exists
    frontend_dist = frontend_dir / 'out'  # Next.js static export
    if not frontend_dist.exists():
        frontend_dist = frontend_dir / '.next'  # Standard Next.js build
    
    if not frontend_dist.exists():
        print("❌ Frontend build output not found!")
        sys.exit(1)
    
    print("✅ Frontend build complete")
    
    # Step 3: Build Backend
    print_step(3, "Building Backend (TypeScript)")
    
    backend_dir = project_root / 'backend'
    print("📦 Installing backend dependencies...")
    run_command("npm ci", cwd=backend_dir)
    
    print("🔨 Compiling TypeScript...")
    run_command("npm run build", cwd=backend_dir)
    
    backend_dist = backend_dir / 'dist'
    if not backend_dist.exists():
        print("❌ Backend build output not found!")
        sys.exit(1)
    
    print("✅ Backend build complete")
    
    # Step 4: Generate Prisma Client
    print_step(4, "Generating Prisma Client")
    run_command("npx prisma generate", cwd=backend_dir)
    print("✅ Prisma client generated")
    
    # Step 5: Create deployment package
    print_step(5, "Creating deployment package")
    
    build_output = project_root / 'build_output'
    build_output.mkdir(exist_ok=True)
    
    # Copy frontend
    frontend_output = build_output / 'frontend'
    frontend_output.mkdir(exist_ok=True)
    
    if (frontend_dir / 'out').exists():
        # Static export
        shutil.copytree(frontend_dir / 'out', frontend_output / 'dist', dirs_exist_ok=True)
    else:
        # Next.js standalone or regular build
        shutil.copytree(frontend_dir / '.next', frontend_output / '.next', dirs_exist_ok=True)
        shutil.copy(frontend_dir / 'package.json', frontend_output)
        if (frontend_dir / 'public').exists():
            shutil.copytree(frontend_dir / 'public', frontend_output / 'public', dirs_exist_ok=True)
    
    print("✅ Frontend copied to build_output")
    
    # Copy backend
    backend_output = build_output / 'backend'
    backend_output.mkdir(exist_ok=True)
    
    # Copy essential backend files
    shutil.copytree(backend_dist, backend_output / 'dist', dirs_exist_ok=True)
    shutil.copytree(backend_dir / 'prisma', backend_output / 'prisma', dirs_exist_ok=True)
    shutil.copy(backend_dir / 'package.json', backend_output)
    shutil.copy(backend_dir / 'package-lock.json', backend_output)
    
    # Copy Dockerfile
    if (backend_dir / 'Dockerfile.production').exists():
        shutil.copy(backend_dir / 'Dockerfile.production', backend_output)
    
    print("✅ Backend copied to build_output")
    
    # Step 6: Create .env.example for production
    print_step(6, "Creating environment template")
    
    env_template = """# Production Environment Variables
# Fill in actual values before deployment

NODE_ENV=production
PORT=5000

# Database (will be auto-configured by deployment script)
DATABASE_URL=postgresql://cintabuku_user:PASSWORD@cintabuku-db:5432/cintabuku

# JWT Secret (will be auto-generated)
JWT_SECRET=REPLACE_WITH_32_CHAR_SECRET
JWT_EXPIRES_IN=7d

# Client URL
CLIENT_URL=https://cintabuku.com
CORS_ORIGIN=http://cintabuku.com,https://cintabuku.com

# Komship API (copy from .env)
KOMSHIP_API_KEY=
KOMSHIP_SELLER_CODE=

# Upload & Logging
UPLOAD_DIR=/app/uploads
LOG_DIR=/app/logs
LOG_LEVEL=info
MAX_FILE_SIZE=5242880

# Rate Limiting
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100
"""
    
    with open(build_output / '.env.production.example', 'w') as f:
        f.write(env_template)
    
    print("✅ Environment template created")
    
    # Step 7: Build verification
    print_step(7, "Verifying build")
    
    required_files = [
        'frontend/dist',
        'backend/dist',
        'backend/package.json',
        'backend/prisma',
    ]
    
    all_ok = True
    for file_path in required_files:
        full_path = build_output / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_ok = False
    
    if not all_ok:
        print("\n❌ Build verification failed!")
        sys.exit(1)
    
    # Calculate sizes
    def get_dir_size(path):
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
        return total / (1024 * 1024)  # MB
    
    frontend_size = get_dir_size(build_output / 'frontend')
    backend_size = get_dir_size(build_output / 'backend')
    total_size = frontend_size + backend_size
    
    print(f"\n📊 Build Sizes:")
    print(f"   Frontend: {frontend_size:.2f} MB")
    print(f"   Backend:  {backend_size:.2f} MB")
    print(f"   Total:    {total_size:.2f} MB")
    
    print(f"\n{'='*60}")
    print("✅ Build Complete!")
    print(f"{'='*60}")
    print(f"\n📦 Build output location: {build_output}")
    print("\n🚀 Ready for deployment!")
    print("\nNext step: Run 'python scripts/deploy_cintabuku_docker.py' to deploy to VPS")

if __name__ == "__main__":
    main()
