import paramiko
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🔍 CAPTURE BACKEND CRASH ERROR\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Stop current backend
    print("🛑 Stopping current backend...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Stopped & removed\n")
    
    # Check and fix volume permissions
    print("🔒 Checking/fixing volume permissions...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S mkdir -p {REMOTE_APP}/uploads {REMOTE_APP}/logs && echo '{VPS_PASS}' | sudo -S chmod -R 777 {REMOTE_APP}/uploads {REMOTE_APP}/logs", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Permissions fixed\n")
    
    # Run backend WITHOUT restart policy in foreground
    print("🚀 Running backend WITHOUT restart (foreground)...")
    print("Watching for 20 seconds...\n")
    print("="*70)
    
    run_cmd = f"""echo '{VPS_PASS}' | sudo -S docker run --rm \
  --name cintabuku-backend-debug \
  --env-file {REMOTE_APP}/backend/.env \
  -v {REMOTE_APP}/uploads:/app/uploads \
  -v {REMOTE_APP}/logs:/app/logs \
  -p 5000:5000 \
  --link cintabuku-db:db \
  cintabuku-backend"""
    
    stdin, stdout, stderr = client.exec_command(run_cmd, get_pty=True)
    
    # Read output for 20 seconds
    start_time = time.time()
    output_buffer = []
    
    while time.time() - start_time < 20:
        if stdout.channel.recv_ready():
            data = stdout.read(1024).decode('utf-8', errors='ignore')
            print(data, end='', flush=True)
            output_buffer.append(data)
        time.sleep(0.1)
    
    print("\n" + "="*70)
    
    # Get exit code
    exit_code = stdout.channel.recv_exit_status()
    
    print(f"\n📊 Exit Code: {exit_code}")
    
    full_output = ''.join(output_buffer)
    
    # Analyze output
    if exit_code == 0:
        print("\n✅ SUCCESS! Backend ran without crashing!")
        print("   Issue was likely the restart policy or timing.\n")
    else:
        print(f"\n❌ Backend crashed with exit code {exit_code}")
        
        if "ECONNREFUSED" in full_output:
            print("   ⚠️  DATABASE CONNECTION REFUSED")
            print("   Fix: Check DATABASE_URL in .env\n")
        elif "ENOENT" in full_output or "permission denied" in full_output.lower():
            print("   ⚠️  FILE/PERMISSION ERROR")
            print("   Fix: Check volume mounts and permissions\n")
        elif "Cannot find module" in full_output:
            print("   ⚠️  MODULE NOT FOUND")
            print("   Fix: Rebuild Docker image\n")
        else:
            print("   Error details captured above.\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
