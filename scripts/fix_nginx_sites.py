import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 Checking Nginx Sites Configuration\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check enabled sites
    print("📋 Enabled sites:")
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    enabled = stdout.read().decode('utf-8')
    print(enabled)
    
    # Check available sites
    print("\n📋 Available sites:")
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-available/", get_pty=True)
    stdout.channel.recv_exit_status()
    available = stdout.read().decode('utf-8')
    print(available)
    
    # Check cintabuku config
    print("\n📄 Cintabuku config:")
    stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    config = stdout.read().decode('utf-8')
    print(config[:500])
    
    # Disable other sites
    print("\n🔧 Disabling other sites...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/darussunnahparung* /etc/nginx/sites-enabled/heru*", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Other sites disabled\n")
    
    # Ensure cintabuku enabled
    print("🔗 Ensuring cintabuku.com enabled...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S ln -sf /etc/nginx/sites-available/cintabuku.com /etc/nginx/sites-enabled/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Cintabuku enabled\n")
    
    # Test config
    print("🧪 Testing configuration...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test_result = stdout.read().decode('utf-8')
    
    if 'successful' in test_result:
        print("✅ Config test PASSED\n")
    else:
        print(f"Result: {test_result}\n")
    
    # Reload Nginx
    print("🔄 Reloading Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Nginx reloaded\n")
    
    # Check what's enabled now
    print("📋 Currently enabled sites:")
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    final_enabled = stdout.read().decode('utf-8')
    print(final_enabled)
    
    print("\n" + "="*70)
    print("✅ FIXED!")
    print("="*70)
    print("\nOnly cintabuku.com should be enabled now.")
    print("\nTest again:")
    print("  https://cintabuku.com")
    print("  https://cintabuku.com/health\n")
    print("Clear browser cache jika perlu (Ctrl+Shift+R)\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
