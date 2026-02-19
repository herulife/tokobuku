import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 Backend Environment & Database Check\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Check .env file exists
    print("📄 Checking .env file:")
    stdin, stdout, stderr = client.exec_command("ls -la /home/ubuntu24/my-docker-apps/apps/cintabuku/backend/.env", get_pty=True)
    stdout.channel.recv_exit_status()
    env_check = stdout.read().decode('utf-8')
    print(env_check)
    
    # Check DATABASE_URL (masked)
    print("\n🔍 Checking DATABASE_URL:")
    stdin, stdout, stderr = client.exec_command("grep DATABASE_URL /home/ubuntu24/my-docker-apps/apps/cintabuku/backend/.env | head -c 50", get_pty=True)
    stdout.channel.recv_exit_status()
    db_url = stdout.read().decode('utf-8')
    print(f"DATABASE_URL={db_url}... (masked)")
    
    # Check database container
    print("\n📊 Database Container:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps | grep db", get_pty=True)
    stdout.channel.recv_exit_status()
    db_status = stdout.read().decode('utf-8')
    print(db_status if db_status else "(Database not running!)")
    
    # Get FULL backend logs to see actual crash
    print("\n📋 Full Backend Logs (last 50 lines):")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 50", get_pty=True)
    stdout.channel.recv_exit_status()
    full_logs = stdout.read().decode('utf-8')
    print(full_logs)
    print("="*70)
    
    # Check for crash patterns
    if "Error" in full_logs or "ERROR" in full_logs:
        print("\n⚠️  ERRORS FOUND IN LOGS!")
    elif "ECONNREFUSED" in full_logs:
        print("\n⚠️  DATABASE CONNECTION REFUSED!")
    elif full_logs.count("Server running") > 3:
        print("\n⚠️  Server starts multiple times = crash loop!")
        print("    Possible causes:")
        print("    1. Database connection issue")
        print("    2. Unhandled promise rejection")  
        print("    3. Process exiting unexpectedly")
    
    # Suggest solution
    print("\n💡 SOLUTION:")
    print("   1. Check if backend can connect to database")
    print("   2. Run backend without restart to see full error")
    print("   3. Fix runtime issue or env variables\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
