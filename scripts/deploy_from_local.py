import paramiko
import subprocess
import os

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku/backend"
LOCAL_BACKEND = "d:/uma/cintabuku/backend"

print("\n🚀 FAST DEPLOY - Using TAR Method\n")

# Check dist exists
if not os.path.exists(f'{LOCAL_BACKEND}/dist'):
    print("❌ No dist folder. Run: npm run build")
    exit(1)

print("✅ Local build found\n")

# Create tar of dist
print("📦 Compressing dist folder...")
os.chdir(LOCAL_BACKEND)
subprocess.run(['tar', '-czf', 'dist.tar.gz', 'dist'], shell=True, check=True)
print("✅ Compressed to dist.tar.gz\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Upload using pscp (faster for large files)
    print("📤 Uploading tar file (faster)...")
    upload_cmd = f'pscp -P {VPS_PORT} -pw {VPS_PASS} "{LOCAL_BACKEND}/dist.tar.gz" {VPS_USER}@{VPS_IP}:{REMOTE_APP}/'
    result = subprocess.run(upload_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Uploaded\n")
    else:
        # Fallback to scp
        print("Using fallback scp...")
        scp_cmd = f'scp -P {VPS_PORT} "{LOCAL_BACKEND}/dist.tar.gz" {VPS_USER}@{VPS_IP}:{REMOTE_APP}/'
        subprocess.run(scp_cmd, shell=True, check=True)
        print("✅ Uploaded via scp\n")
    
    # Extract on VPS
    print("📦 Extracting on VPS...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_APP} && rm -rf dist && tar -xzf dist.tar.gz", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Extracted\n")
    
    # Install PM2
    print("📦 Setting up PM2...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S npm install -g pm2 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ PM2 ready\n")
    
    # Stop Docker
    print("🛑 Stopping Docker backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Docker stopped\n")
    
    # Start with PM2
    print("🚀 Starting backend with PM2...")
    start_cmd = f"cd {REMOTE_APP} && pm2 delete cintabuku-backend 2>/dev/null || true && pm2 start dist/index.js --name cintabuku-backend"
    stdin, stdout, stderr = client.exec_command(start_cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Started\n")
    
    # Wait
    import time
    print("⏳ Waiting 10 seconds...")
    time.sleep(10)
    
    # Check
    print("\n📊 PM2 Status:")
    stdin, stdout, stderr = client.exec_command("pm2 list", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    
    # Test
    print("\n🧪 Testing:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(f"Health: {health}\n")
    
    if '"status"' in health and 'ok' in health:
        print("="*70)
        print("🎉🎉🎉 SUCCESS! BACKEND LIVE!")
        print("="*70)
        print("\n✅ Local build deployed")
        print("✅ PM2 managing process")
        print("✅ Backend responding\n")
        print("🌐 TEST: https://cintabuku.com\n")
    else:
        print("📋 Check logs: pm2 logs cintabuku-backend\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
    # Cleanup
    if os.path.exists(f'{LOCAL_BACKEND}/dist.tar.gz'):
        os.remove(f'{LOCAL_BACKEND}/dist.tar.gz')
