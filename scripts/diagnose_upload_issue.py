import paramiko
import sys
import time
from pathlib import Path

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def print_test(name):
    print(f"\n{'='*60}")
    print(f"🔍 Test: {name}")
    print(f"{'='*60}")

def execute(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    return stdout.read().decode('utf-8', errors='ignore')

print("🔍 Diagnostic: VPS Upload Issues")
print("="*60)

# Test 1: Basic SSH connectivity
print_test("Basic SSH Connection")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    start = time.time()
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=10)
    duration = time.time() - start
    print(f"✅ SSH connection successful ({duration:.2f}s)")
    
    # Test 2: Check SSH server config
    print_test("SSH Server Configuration")
    result = execute(client, "sudo cat /etc/ssh/sshd_config | grep -E '(ClientAlive|MaxSessions|MaxStartups)'")
    print(result)
    
    # Test 3: Check available memory/resources
    print_test("VPS Resources")
    result = execute(client, "free -h")
    print(result)
    
    result = execute(client, "df -h /tmp /home")
    print(result)
    
    # Test 4: Check network/firewall
    print_test("Network & Firewall")
    result = execute(client, "sudo iptables -L INPUT -n | head -20 || echo 'No iptables'")
    print(result)
    
    result = execute(client, "sudo ufw status || echo 'UFW not active'")
    print(result)
    
    # Test 5: Check SSH limits
    print_test("SSH Connection Limits")
    result = execute(client, "ulimit -n")
    print(f"File descriptors limit: {result}")
    
    result = execute(client, "cat /proc/sys/fs/file-max")
    print(f"System-wide file max: {result}")
    
    # Test 6: Create small test file and try upload
    print_test("Small File Upload Test")
    
    # Create 100KB test file
    test_file = Path("test_upload.txt")
    with open(test_file, 'w') as f:
        f.write("test\n" * 10000)
    
    print(f"Created test file: {test_file.stat().st_size} bytes")
    
    # Try SFTP instead of SCP
    try:
        sftp = client.open_sftp()
        start = time.time()
        sftp.put(str(test_file), f"/tmp/{test_file.name}")
        duration = time.time() - start
        print(f"✅ SFTP upload successful ({duration:.2f}s)")
        
        # Verify
        result = execute(client, f"ls -lh /tmp/{test_file.name}")
        print(f"Uploaded file: {result}")
        
        # Cleanup
        sftp.remove(f"/tmp/{test_file.name}")
        sftp.close()
        test_file.unlink()
        
    except Exception as e:
        print(f"❌ SFTP upload failed: {e}")
    
    # Test 7: Network latency
    print_test("Network Latency")
    for i in range(3):
        start = time.time()
        execute(client, "echo test")
        latency = (time.time() - start) * 1000
        print(f"  Attempt {i+1}: {latency:.0f}ms")
    
    # Test 8: Check /tmp permissions
    print_test("/tmp Directory Permissions")
    result = execute(client, "ls -ld /tmp")
    print(result)
    
    result = execute(client, "df -h /tmp")
    print(result)
    
    # Test 9: Check if any rate limiting
    print_test("Connection Rate Limiting")
    result = execute(client, "sudo grep -i 'maxstartups\\|maxsessions' /etc/ssh/sshd_config")
    print(result if result.strip() else "No explicit rate limits found")
    
    print("\n" + "="*60)
    print("📊 Diagnostic Summary")
    print("="*60)
    print("\n✅ Tests completed. Check results above for issues.")
    print("\n💡 Common issues:")
    print("   - High network latency (>200ms)")
    print("   - SSH MaxSessions too low")
    print("   - /tmp disk full")
    print("   - Firewall blocking large transfers")
    print("   - Memory/resource constraints")
    
except Exception as e:
    print(f"\n❌ Diagnostic failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
