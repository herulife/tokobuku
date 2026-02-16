import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    
    print("\n📊 Deployment Status Check\n")
    print("="*60)
    
    # Check containers
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps -a | grep cintabuku", get_pty=True)
    stdout.channel.recv_exit_status()
    print("Containers:")
    print(stdout.read().decode('utf-8'))
    
    # Check backend logs
    print("\n" + "="*60)
    print("Backend Logs (last 30 lines):")
    print("="*60)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 30", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
finally:
    client.close()
