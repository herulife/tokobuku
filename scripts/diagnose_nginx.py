import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 FULL NGINX DIAGNOSTIC\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check ALL enabled sites
    print("="*70)
    print("📋 ALL ENABLED SITES:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    enabled = stdout.read().decode('utf-8')
    print(enabled)
    
    # Check cintabuku config content
    print("\n" + "="*70)
    print("📄 CINTABUKU CONFIG CONTENT:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("cat /etc/nginx/sites-available/cintabuku.com", get_pty=True)
    stdout.channel.recv_exit_status()
    cintabuku_config = stdout.read().decode('utf-8')
    print(f"Length: {len(cintabuku_config)} bytes")
    print(cintabuku_config if cintabuku_config else "(EMPTY!)")
    
    # Check if there are OTHER sites listening on 443
    print("\n" + "="*70)
    print("🔍 SITES LISTENING ON PORT 443:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("grep -r 'listen.*443' /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    port_443 = stdout.read().decode('utf-8')
    print(port_443 if port_443 else "(None found)")
    
    # Check nginx main config for includes
    print("\n" + "="*70)
    print("📋 NGINX MAIN CONFIG INCLUDES:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("grep -E 'include.*sites-enabled' /etc/nginx/nginx.conf", get_pty=True)
    stdout.channel.recv_exit_status()
    includes = stdout.read().decode('utf-8')
    print(includes)
    
    # Test current nginx config
    print("\n" + "="*70)
    print("🧪 NGINX CONFIG TEST:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S nginx -t", get_pty=True)
    stdout.channel.recv_exit_status()
    test = stdout.read().decode('utf-8')
    print(test)
    
    # Check what's actually serving
    print("\n" + "="*70)
    print("🌐 TEST LOCAL HTTPS:")
    print("="*70)
    stdin, stdout, stderr = client.exec_command("curl -k -s https://localhost/ | head -n 20", get_pty=True)
    stdout.channel.recv_exit_status()
    local_https = stdout.read().decode('utf-8')
    print(local_https[:500])
    
    if 'darussunnah' in local_https.lower():
        print("\n⚠️  CONFIRMED: Server returns darussunnah content!")
        print("    Issue: Wrong site is default or cintabuku config not working\n")
    
    print("\n" + "="*70)
    print("💡 DIAGNOSIS COMPLETE")
    print("="*70)
    print("\nIssue identified. Preparing fix...\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
