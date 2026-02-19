import paramiko
import subprocess

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 COMPLETE DIAGNOSTIC - Why Site Not Accessible\n")

# Test DNS first
print("1️⃣ DNS Resolution Test:")
try:
    result = subprocess.run(['nslookup', 'cintabuku.com'], capture_output=True, text=True, timeout=5)
    output = result.stdout
    if VPS_IP in output:
        print(f"✅ DNS resolves to {VPS_IP}")
    else:
        print(f"⚠️  DNS NOT resolving to {VPS_IP}")
        print(output)
except Exception as e:
    print(f"DNS check failed: {e}")

print("\n2️⃣ VPS Services Check:")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ SSH Connected\n")
    
    # Check Nginx
    print("📋 Nginx Status:")
    stdin, stdout, stderr = client.exec_command("systemctl is-active nginx", get_pty=True)
    stdout.channel.recv_exit_status()
    nginx_status = stdout.read().decode('utf-8').strip()
    print(f"   {nginx_status}")
    
    # Check PM2
    print("\n📋 PM2 Backend Status:")
    stdin, stdout, stderr = client.exec_command("pm2 jlist", get_pty=True)
    stdout.channel.recv_exit_status()
    pm2_status = stdout.read().decode('utf-8')
    if '"status":"online"' in pm2_status:
        print("   ✅ Backend ONLINE")
    else:
        print(f"   ⚠️  Backend status: {pm2_status[:200]}")
    
    # Check what's listening on ports
    print("\n📋 Ports Check:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S netstat -tlnp | grep ':80\\|:443\\|:5000' 2>/dev/null || sudo ss -tlnp | grep ':80\\|:443\\|:5000'", get_pty=True)
    stdout.channel.recv_exit_status()
    ports = stdout.read().decode('utf-8')
    print(ports if ports else "   ⚠️  No services on ports 80, 443, 5000")
    
    # Test localhost
    print("\n📋 Localhost Tests:")
    print("   Testing HTTP...")
    stdin, stdout, stderr = client.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    http_code = stdout.read().decode('utf-8').strip()
    print(f"   HTTP: {http_code}")
    
    print("   Testing HTTPS...")
    stdin, stdout, stderr = client.exec_command("curl -k -s -o /dev/null -w '%{http_code}' https://localhost/health", get_pty=True)
    stdout.channel.recv_exit_status()
    https_code = stdout.read().decode('utf-8').strip()
    print(f"   HTTPS: {https_code}")
    
    # Check Nginx error logs
    print("\n📋 Nginx Error Log (last 10 lines):")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S tail -n 10 /var/log/nginx/error.log", get_pty=True)
    stdout.channel.recv_exit_status()
    errors = stdout.read().decode('utf-8')
    print(errors if errors.strip() else "   (No errors)")
    
    # Test external access
    print("\n3️⃣ External Access Test:")
    print(f"   Testing http://{VPS_IP} ...")
    test_cmd = f"curl -s -o /dev/null -w '%{{http_code}}' http://{VPS_IP}/"
    external_result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True, timeout=10)
    print(f"   Result: {external_result.stdout.strip()}")
    
    print("\n" + "="*70)
    print("📊 SUMMARY:")
    print("="*70)
    
    issues = []
    if VPS_IP not in output:
        issues.append("❌ DNS not resolving to VPS IP")
    if nginx_status != "active":
        issues.append(f"❌ Nginx not active: {nginx_status}")
    if '"status":"online"' not in pm2_status:
        issues.append("❌ Backend not online")
    if not ports or '5000' not in ports:
        issues.append("❌ Backend not listening on port 5000")
    if http_code != "200" and http_code != "301":
        issues.append(f"❌ HTTP test failed: {http_code}")
    
    if issues:
        print("\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 SOLUTION NEEDED:")
        if VPS_IP not in output:
            print("   → Update Cloudflare DNS A record to 103.107.206.10")
        if not ports or '5000' not in ports:
            print("   → Restart PM2: pm2 restart cintabuku-backend")
        if nginx_status != "active":
            print("   → Start Nginx: sudo systemctl start nginx")
    else:
        print("\n✅ ALL SYSTEMS OPERATIONAL!")
        print("\n⚠️  If site still not accessible:")
        print("   → Wait 5 minutes for DNS propagation")
        print("   → Try: http://103.107.206.10 directly")
        print("   → Check Cloudflare SSL mode: should be 'Full'")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
