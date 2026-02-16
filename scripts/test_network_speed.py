import paramiko
import time
import sys
from pathlib import Path

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def test_upload_speed(sftp, size_kb=500):
    """Test upload speed to VPS"""
    # Create test file
    test_file = Path(f"test_{size_kb}kb.dat")
    with open(test_file, 'wb') as f:
        f.write(b'0' * (size_kb * 1024))
    
    # Upload test
    remote_path = f"/tmp/{test_file.name}"
    try:
        start = time.time()
        sftp.put(str(test_file), remote_path)
        duration = time.time() - start
        speed_kbps = (size_kb * 8) / duration  # Convert to Kbps
        
        # Cleanup
        sftp.remove(remote_path)
        test_file.unlink()
        
        return duration, speed_kbps, True
    except Exception as e:
        if test_file.exists():
            test_file.unlink()
        return 0, 0, False

def test_download_speed(sftp, ssh, size_kb=500):
    """Test download speed from VPS"""
    remote_file = f"/tmp/test_download_{size_kb}kb.dat"
    local_file = Path(f"downloaded_{size_kb}kb.dat")
    
    # Create file on VPS
    stdin, stdout, stderr = ssh.exec_command(f"dd if=/dev/zero of={remote_file} bs=1024 count={size_kb} 2>/dev/null")
    stdout.channel.recv_exit_status()
    
    try:
        start = time.time()
        sftp.get(remote_file, str(local_file))
        duration = time.time() - start
        speed_kbps = (size_kb * 8) / duration
        
        # Cleanup
        sftp.remove(remote_file)
        local_file.unlink()
        
        return duration, speed_kbps, True
    except Exception as e:
        if local_file.exists():
            local_file.unlink()
        return 0, 0, False

def execute(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.recv_exit_status()
    return stdout.read().decode('utf-8', errors='ignore')

print("="*70)
print("🔍 Network Diagnostic: VPS vs Your Internet")
print("="*70)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"\n📡 Connecting to {VPS_IP}...")
    start = time.time()
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=10)
    connect_time = time.time() - start
    print(f"✅ Connected in {connect_time:.2f}s")
    
    sftp = client.open_sftp()
    
    # Test 1: Upload speed tests
    print("\n" + "="*70)
    print("📤 UPLOAD Speed Tests (Your Internet → VPS)")
    print("="*70)
    
    sizes = [100, 300, 500]  # KB
    upload_speeds = []
    
    for size in sizes:
        print(f"\n  Testing {size}KB upload...")
        duration, speed, success = test_upload_speed(sftp, size)
        if success:
            print(f"    ✅ {duration:.2f}s ({speed:.0f} Kbps)")
            upload_speeds.append(speed)
        else:
            print(f"    ❌ Failed")
    
    # Test 2: Download speed tests
    print("\n" + "="*70)
    print("📥 DOWNLOAD Speed Tests (VPS → Your Internet)")
    print("="*70)
    
    download_speeds = []
    
    for size in sizes:
        print(f"\n  Testing {size}KB download...")
        duration, speed, success = test_download_speed(sftp, client, size)
        if success:
            print(f"    ✅ {duration:.2f}s ({speed:.0f} Kbps)")
            download_speeds.append(speed)
        else:
            print(f"    ❌ Failed")
    
    # Test 3: Latency test
    print("\n" + "="*70)
    print("⏱️  LATENCY Test (Round-trip time)")
    print("="*70)
    
    latencies = []
    for i in range(5):
        start = time.time()
        execute(client, "echo test")
        latency = (time.time() - start) * 1000
        latencies.append(latency)
        print(f"  Attempt {i+1}: {latency:.0f}ms")
    
    avg_latency = sum(latencies) / len(latencies)
    
    # Test 4: VPS Network Speed (baseline)
    print("\n" + "="*70)
    print("🌐 VPS Network Quality")
    print("="*70)
    
    print("\n  Testing VPS → Internet speed...")
    result = execute(client, "curl -s -w '%{speed_download}' -o /dev/null http://speedtest.tele2.net/1MB.zip 2>/dev/null || echo 'Test failed'")
    print(f"  VPS download speed: {result.strip()}")
    
    # Test 5: VPS Resources
    print("\n" + "="*70)
    print("💻 VPS Resources")
    print("="*70)
    
    print("\n  CPU Load:")
    result = execute(client, "uptime")
    print(f"  {result.strip()}")
    
    print("\n  Memory:")
    result = execute(client, "free -h | grep Mem")
    print(f"  {result.strip()}")
    
    print("\n  Network interfaces:")
    result = execute(client, "ip -s link | grep -E '(eth0|ens|UP)'")
    print(f"  {result.strip()}")
    
    # Analysis
    print("\n" + "="*70)
    print("📊 ANALYSIS & DIAGNOSIS")
    print("="*70)
    
    avg_upload = sum(upload_speeds) / len(upload_speeds) if upload_speeds else 0
    avg_download = sum(download_speeds) / len(download_speeds) if download_speeds else 0
    
    print(f"\n📈 Summary:")
    print(f"  Average Upload Speed:   {avg_upload:.0f} Kbps ({avg_upload/1024:.2f} Mbps)")
    print(f"  Average Download Speed: {avg_download:.0f} Kbps ({avg_download/1024:.2f} Mbps)")
    print(f"  Average Latency:        {avg_latency:.0f}ms")
    print(f"  Connection Time:        {connect_time:.2f}s")
    
    print(f"\n🔍 Diagnosis:")
    
    # Analyzelatency
    if avg_latency > 300:
        print(f"  ❌ HIGH LATENCY ({avg_latency:.0f}ms) - Koneksi internet Bapak lambat")
        verdict_latency = "YOUR_INTERNET"
    elif avg_latency > 150:
        print(f"  ⚠️  MODERATE LATENCY ({avg_latency:.0f}ms) - Koneksi lumayan")
        verdict_latency = "MODERATE"
    else:
        print(f"  ✅ Good latency ({avg_latency:.0f}ms)")
        verdict_latency = "GOOD"
    
    # Analyze upload speed
    if avg_upload < 100:  # < 100 Kbps
        print(f"  ❌ VERY SLOW UPLOAD ({avg_upload:.0f} Kbps) - Upload file besar pasti timeout")
        print(f"     → Masalah: KONEKSI INTERNET BAPAK (upload speed terlalu lambat)")
        verdict_upload = "YOUR_INTERNET"
    elif avg_upload < 500:
        print(f"  ⚠️  SLOW UPLOAD ({avg_upload:.0f} Kbps) - File >1MB akan lama/timeout")
        verdict_upload = "YOUR_INTERNET"
    else:
        print(f"  ✅ Upload speed acceptable ({avg_upload:.0f} Kbps)")
        verdict_upload = "GOOD"
    
    # Analyze download
    if avg_download < 100:
        print(f"  ❌ VERY SLOW DOWNLOAD ({avg_download:.0f} Kbps)")
        verdict_download = "YOUR_INTERNET"
    elif avg_download < 500:
        print(f"  ⚠️  SLOW DOWNLOAD ({avg_download:.0f} Kbps)")
        verdict_download = "YOUR_INTERNET"
    else:
        print(f"  ✅ Download speed acceptable ({avg_download:.0f} Kbps)")
        verdict_download = "GOOD"
    
    # Final verdict
    print(f"\n" + "="*70)
    print("🎯 FINAL VERDICT")
    print("="*70)
    
    if verdict_upload == "YOUR_INTERNET" or verdict_latency == "YOUR_INTERNET":
        print(f"\n❌ Masalah utama: KONEKSI INTERNET BAPAK")
        print(f"\nPenyebab:")
        print(f"  - Upload speed terlalu lambat ({avg_upload:.0f} Kbps)")
        print(f"  - {avg_upload/1024:.2f} Mbps tidak cukup untuk upload file 1MB+ dengan stabil")
        print(f"  - Timeout terjadi karena transfer terlalu lama")
        print(f"\nSolusi:")
        print(f"  1. Pakai WiFi/koneksi lebih cepat")
        print(f"  2. Upload di jam sepi (malam/pagi)")
        print(f"  3. Pakai chunked upload (split file kecil)")
        print(f"  4. ATAU: Pakai Git (push code, clone di VPS)")
    else:
        print(f"\n✅ Koneksi internet Bapak OK")
        print(f"\n⚠️  Kemungkinan masalah:")
        print(f"  - SSH timeout settings di VPS")
        print(f"  - Firewall blocking")
        print(f"  - SCP protocol issue (pakai SFTP instead)")
    
    sftp.close()
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()

print(f"\n" + "="*70)
