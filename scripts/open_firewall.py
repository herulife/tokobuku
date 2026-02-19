import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔥 OPEN FIREWALL PORTS 80 & 443\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check if ufw is active
    print("🔍 Checking firewall status...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ufw status", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print(status)
    
    # Open ports
    print("\n🔓 Opening port 80 (HTTP)...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ufw allow 80/tcp", get_pty=True)
    stdout.channel.recv_exit_status()
    out80 = stdout.read().decode('utf-8')
    print(out80)
    
    print("🔓 Opening port 443 (HTTPS)...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ufw allow 443/tcp", get_pty=True)
    stdout.channel.recv_exit_status()
    out443 = stdout.read().decode('utf-8')
    print(out443)
    
    # Reload ufw
    print("\n🔄 Reloading firewall...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ufw reload", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Reloaded\n")
    
    # Check status again
    print("📋 Final firewall status:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ufw status", get_pty=True)
    stdout.channel.recv_exit_status()
    final = stdout.read().decode('utf-8')
    print(final)
    
    # Test from outside
    print("\n🧪 Testing external access...")
    stdin, stdout, stderr = client.exec_command("curl -s -I http://localhost/ -H 'Host: cintabuku.com' | head -n 5", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    print(test)
    
    print("\n" + "="*70)
    print("🎉 FIREWALL PORTS OPENED!")
    print("="*70)
    print("\n✅ Port 80 (HTTP): OPEN")
    print("✅ Port 443 (HTTPS): OPEN")
    print("\n🌐 TEST NOW:")
    print("   https://cintabuku.com")
    print("   (Should work now!)")
    print("\n💡 Wait 30 seconds for firewall to fully apply\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
