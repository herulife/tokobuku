import paramiko
import sys

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def execute(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    return stdout.read().decode('utf-8', errors='ignore')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {VPS_IP}...")
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    print("🔍 Checking docker-compose.yml structure...")
    
    # Check if volumes section exists
    result = execute(client, "grep -n '^volumes:' ~/my-docker-apps/docker-compose.yml")
    print(f"Volumes sections found at lines:\n{result}")
    
    # Check if cintabuku service exists
    result = execute(client, "grep -n 'cintabuku-db:' ~/my-docker-apps/docker-compose.yml")
    print(f"\nCintabuku service at:\n{result}")
    
    # Show tail of docker-compose to see what was added
    result = execute(client, "tail -30 ~/my-docker-apps/docker-compose.yml")
    print(f"\nLast 30 lines of docker-compose.yml:\n{result}")
    
    # Check .env file
    result = execute(client, "tail -5 ~/my-docker-apps/.env")
    print(f"\nLast 5 lines of .env:\n{result}")
    
finally:
    client.close()
