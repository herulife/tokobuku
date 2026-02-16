import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected to VPS\n")
    
    # Check if cintabuku folder exists
    stdin, stdout, stderr = client.exec_command("ls -la /home/ubuntu24/my-docker-apps/apps/cintabuku/ 2>/dev/null || echo 'Folder not found'")
    stdout.channel.recv_exit_status()
    print("📁 Cintabuku folder status:")
    print(stdout.read().decode('utf-8'))
    
    # Check if git clone is running
    stdin, stdout, stderr = client.exec_command("ps aux | grep git || echo 'No git process'")
    stdout.channel.recv_exit_status()
    print("\n🔍 Git processes:")
    print(stdout.read().decode('utf-8'))
    
    # Try manual clone test
    print("\n🧪 Testing manual git clone...")
    stdin, stdout, stderr = client.exec_command("cd /tmp && timeout 10 git clone https://github.com/herulife/tokobuku.git test_clone 2>&1 || echo 'Clone failed'")
    stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8')
    print(output)
    
    # Cleanup test
    stdin, stdout, stderr = client.exec_command("rm -rf /tmp/test_clone")
    stdout.channel.recv_exit_status()
    
finally:
    client.close()
