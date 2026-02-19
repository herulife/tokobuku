import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 DEEP NGINX INVESTIGATION\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check ALL sites in sites-available
    print("="*70)
    print("📋 ALL AVAILABLE SITES:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-available/", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Check what's ACTUALLY enabled
    print("="*70)
    print("📋 ALL ENABLED SITES:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode('utf-8'))
    
    # Check cintabuku config
    print("="*70)
    print("📄 CINTABUKU CONFIG:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    cintabuku = stdout.read().decode('utf-8')
    print(f"Length: {len(cintabuku)} bytes")
    print(cintabuku)
    
    # Check if there are OTHER configs with server_name for cintabuku
    print("\n" + "="*70)
    print("🔍 SEARCHING FOR 'cintabuku' IN ALL CONFIGS:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("grep -r 'cintabuku' /etc/nginx/sites-available/ /etc/nginx/sites-enabled/ 2>/dev/null", get_pty=True)
    stdout.channel.recv_exit_status()
    search = stdout.read().decode('utf-8')
    print(search if search else "(Not found in any config)")
    
    # Check if there are configs for darussunnah
    print("\n" + "="*70)
    print("🔍 SEARCHING FOR 'darussunnah' IN CONFIGS:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("grep -r 'darussunnah' /etc/nginx/sites-enabled/ 2>/dev/null", get_pty=True)
    stdout.channel.recv_exit_status()
    darus_search = stdout.read().decode('utf-8')
    print(darus_search if darus_search else "(None in sites-enabled - GOOD!)")
    
    # Test what localhost HTTPS returns
    print("\n" + "="*70)
    print("🧪 TESTING HTTPS://LOCALHOST:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("curl -k -s -H 'Host: cintabuku.com' https://localhost/ | head -n 30", get_pty=True)
    stdout.channel.recv_exit_status()
    test_cintabuku = stdout.read().decode('utf-8')
    print("With Host: cintabuku.com header:")
    print(test_cintabuku[:500])
    
    if 'darussunnah' in test_cintabuku.lower():
        print("\n⚠️  PROBLEM: Even with Host header, returns darussunnah!\n")
    elif 'cintabuku' in test_cintabuku.lower() or 'koalisi' in test_cintabuku.lower():
        print("\n✅ GOOD: Returns cintabuku content!\n")
    
    # Check nginx error log
    print("="*70)
    print("📋 NGINX ERROR LOG (last 20 lines):")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("sudo tail -n 20 /var/log/nginx/error.log", get_pty=True)
    stdout.channel.recv_exit_status()
    error_log = stdout.read().decode('utf-8')
    print(error_log if error_log else "(No errors)")
    
    # Check which config files nginx is actually loading
    print("\n" + "="*70)
    print("🔍 WHICH CONFIGS NGINX IS LOADING:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -T 2>&1 | grep 'server_name' | head -n 20", get_pty=True)
    stdout.channel.recv_exit_status()
    loaded = stdout.read().decode('utf-8')
    print(loaded)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
