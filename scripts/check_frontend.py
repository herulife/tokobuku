import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_FRONTEND = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend"

print("\n🔍 FRONTEND READINESS CHECK\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check directory
    print("📋 Checking frontend directory...")
    stdin, stdout, stderr = client.exec_command(f"ls -la {REMOTE_FRONTEND}", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode())
    
    # Check .env files
    print("\n📋 Checking .env files...")
    stdin, stdout, stderr = client.exec_command(f"ls -la {REMOTE_FRONTEND}/.env*", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode())
    
    # Read .env if it exists
    print("\n📋 Current .env content:")
    stdin, stdout, stderr = client.exec_command(f"cat {REMOTE_FRONTEND}/.env 2>/dev/null || cat {REMOTE_FRONTEND}/.env.local 2>/dev/null", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode())
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
