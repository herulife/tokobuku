import paramiko
import sys

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Connecting to VPS...")
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Kill stuck git processes
    print("🔪 Killing stuck git clone processes...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S pkill -f 'git clone.*tokobuku'", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Processes killed\n")
    
    # Remove incomplete cintabuku folder
    print("🗑️  Removing incomplete cintabuku folder...")
    stdin, stdout, stderr = client.exec_command("rm -rf /home/ubuntu24/my-docker-apps/apps/cintabuku")
    stdout.channel.recv_exit_status()
    print("✅ Folder removed\n")
    
    # Recreate directory
    print("📁 Creating fresh directory...")
    stdin, stdout, stderr = client.exec_command("mkdir -p /home/ubuntu24/my-docker-apps/apps/cintabuku")
    stdout.channel.recv_exit_status()
    print("✅ Directory ready\n")
    
    print("=" * 60)
    print("✅ VPS Cleaned Successfully!")
    print("=" * 60)
    print("\nReady to deploy from public repo!")
    
finally:
    client.close()
