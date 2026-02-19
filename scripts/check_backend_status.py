import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 Backend & Port 5000 Check\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check backend container
    print("📊 Backend Container Status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps -a | grep backend", get_pty=True)
    stdout.channel.recv_exit_status()
    backend_status = stdout.read().decode('utf-8')
    print(backend_status)
    
    # Check port 5000
    print("\n🔍 What's listening on port 5000:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S netstat -tlnp | grep 5000", get_pty=True)
    stdout.channel.recv_exit_status()
    port_check = stdout.read().decode('utf-8')
    print(port_check if port_check else "(Nothing on port 5000!)")
    
    # Test direct connection to port 5000
    print("\n🧪 Testing http://localhost:5000:")
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:5000/health", get_pty=True)
    stdout.channel.recv_exit_status()
    health = stdout.read().decode('utf-8')
    print(health[:300] if health else "(No response)")
    
    # Check recent backend logs
    print("\n📋 Backend Logs (last 15 lines):")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 15", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    
    print("\n" + "="*70)
    if "Server running" in logs:
        print("✅ Backend IS starting!")
        print("   Issue: May be restarting quickly or timing issue")
    else:
        print("⚠️  Backend may not be running properly")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
