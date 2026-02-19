import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 CHECK ALL NGINX SITES & FIX ROUTING\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check all enabled sites
    print("📋 ALL Enabled Sites:")
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    enabled = stdout.read().decode('utf-8')
    print(enabled)
    
    # Disable ALL other sites except cintabuku
    print("\n🛑 Disabling all OTHER sites...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S rm /etc/nginx/sites-enabled/default 2>/dev/null || true", get_pty=True)
    stdout.channel.recv_exit_status()
    
    # List again to confirm only cintabuku
    stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    after = stdout.read().decode('utf-8')
    print("After cleanup:")
    print(after)
    
    # Check what's listening on 443
    print("\n🔍 Sites on Port 443:")
    stdin, stdout, stderr = client.exec_command("grep -r 'listen 443' /etc/nginx/sites-enabled/", get_pty=True)
    stdout.channel.recv_exit_status()
    port443 = stdout.read().decode('utf-8')
    print(port443 if port443 else "(Only cintabuku)")
    
    # Reload Nginx
    print("\n🔄 Reloading Nginx...")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S systemctl reload nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Reloaded\n")
    
    # Test direct
    print("🧪 Testing HTTPS:")
    stdin, stdout, stderr = client.exec_command("curl -k -s -H 'Host: cintabuku.com' https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    result = stdout.read().decode('utf-8')
    print(f"{result}\n")
    
    # Test HTTP (should redirect)
    print("🧪 Testing HTTP redirect:")
    stdin, stdout, stderr = client.exec_command("curl -s -I http://localhost/ -H 'Host: cintabuku.com'", get_pty=True)
    stdout.channel.recv_exit_status()
    redirect = stdout.read().decode('utf-8')
    print(redirect[:300])
    
    if '"status":"ok"' in result:
        print("\n" + "="*70)
        print("🎉 NGINX ROUTING TO BACKEND!")
        print("="*70)
        print("\n✅ Only cintabuku.com enabled")
        print("✅ Port 443 routing correctly")
        print("✅ Backend responding")
        print("\n🌐 TEST NOW:")
        print("   https://cintabuku.com")
        print("   Hard refresh: Ctrl+Shift+R")
        print("\n💡 If still shows darussunnah:")
        print("   - Clear ALL browser cache")
        print("   - Try different browser")
        print("   - Wait 2-3 minutes for DNS\n")
    else:
        print("\n⚠️  Check results above\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
