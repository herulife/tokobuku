import paramiko
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

print("\n🔍 DETAILED BACKEND LOG ANALYSIS\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Get FULL backend logs (last 100 lines)
    print("📋 Backend Logs (last 100 lines):")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 100", get_pty=True)
    stdout.channel.recv_exit_status()
    logs = stdout.read().decode('utf-8')
    print(logs)
    print("="*70)
    
    # Check container inspect for restart info
    print("\n🔍 Container Restart Info:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker inspect cintabuku-backend --format='{{{{json .State}}}}'", get_pty=True)
    stdout.channel.recv_exit_status()
    state = stdout.read().decode('utf-8')
    print(state)
    
    # Check if there's an exit code
    print("\n🔍 Exit Code & Error:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker inspect cintabuku-backend --format='ExitCode: {{{{.State.ExitCode}}}} | Error: {{{{.State.Error}}}}'", get_pty=True)
    stdout.channel.recv_exit_status()
    exit_info = stdout.read().decode('utf-8')
    print(exit_info)
    
    # Check last restart time
    print("\n🕐 Last Started:")
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker inspect cintabuku-backend --format='{{{{.State.StartedAt}}}}'", get_pty=True)
    stdout.channel.recv_exit_status()
    started = stdout.read().decode('utf-8')
    print(started)
    
    # Wait and check if still restarting
    print("\n⏳ Waiting 30 seconds to observe restart pattern...")
    time.sleep(30)
    
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker ps -a | grep cintabuku-backend", get_pty=True)
    stdout.channel.recv_exit_status()
    status = stdout.read().decode('utf-8')
    print("\n📊 Current Status:")
    print(status)
    
    # Get newest logs
    print("\n📋 Latest Logs (after 30s):")
    print("="*70)
    stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-backend --tail 20", get_pty=True)
    stdout.channel.recv_exit_status()
    new_logs = stdout.read().decode('utf-8')
    print(new_logs)
    print("="*70)
    
    print("\n✅ Analysis complete. Check logs above for crash reason.\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
