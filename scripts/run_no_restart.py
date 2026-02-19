import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

print("\n🔧 Running backend WITHOUT restart to see full error\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Stop and remove old container
    print("🛑 Stopping old container...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker stop cintabuku-backend 2>/dev/null && echo '{VPS_PASS}' | sudo -S docker rm cintabuku-backend 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Removed\n")
    
    # Start WITHOUT restart policy to see full error
    print("🚀 Starting backend WITHOUT auto-restart...")
    start_cmd = f"""echo '{VPS_PASS}' | sudo -S docker run \\
  --name cintabuku-backend \\
  --env-file {REMOTE_APP}/backend/.env \\
  -v {REMOTE_APP}/uploads:/app/uploads \\
  -v {REMOTE_APP}/logs:/app/logs \\
  -p 5000:5000 \\
  --link cintabuku-db:db \\
  cintabuku-backend"""
    
    # Run in foreground to see output
    print("Watching output... (will show full crash if it happens)\n")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(start_cmd, get_pty=True)
    
    # Read output in real-time for 15 seconds
    import time
    start_time = time.time()
    output_lines = []
    
    while time.time() - start_time < 15:
        if stdout.channel.recv_ready():
            data = stdout.read(1024).decode('utf-8', errors='ignore')
            print(data, end='', flush=True)
            output_lines.append(data)
        time.sleep(0.1)
    
    print("\n" + "="*70)
    
    # Check exit code
    exit_status = stdout.channel.recv_exit_status()
    print(f"\n📊 Container Exit Code: {exit_status}")
    
    if exit_status == 0:
        print("\n✅ SUCCESS! Container ran without error!")
        print("Issue was the restart policy detection timing.\n")
    else:
        print(f"\n❌ Container crashed with exit code {exit_status}")
        print("Check output above for error details.\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
