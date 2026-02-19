import paramiko
import os

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

LOCAL_FILE = "d:/uma/cintabuku/frontend/frontend.tar.gz"
REMOTE_DIR = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend"
REMOTE_FILE = f"{REMOTE_DIR}/frontend.tar.gz"

print(f"\n📤 UPLOADING FRONTEND TARBALL via SFTP\n")

if not os.path.exists(LOCAL_FILE):
    print(f"❌ Local file not found: {LOCAL_FILE}")
    exit(1)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Ensure remote directory exists
    stdin, stdout, stderr = client.exec_command(f"mkdir -p {REMOTE_DIR}")
    stdout.channel.recv_exit_status()
    
    # SFTP Upload
    sftp = client.open_sftp()
    print(f"📦 Uploading {LOCAL_FILE} to {REMOTE_FILE}...")
    
    def progress_callback(transferred, total):
        pct = (transferred / total) * 100
        print(f"⏳ Progress: {pct:.1f}% ({transferred}/{total})", end='\r')

    sftp.put(LOCAL_FILE, REMOTE_FILE, callback=progress_callback)
    sftp.close()
    print("\n✅ Upload Complete\n")
    
    # Extract
    print("📦 Extracting tarball...")
    stdin, stdout, stderr = client.exec_command(f"cd {REMOTE_DIR} && tar -xzf frontend.tar.gz && rm frontend.tar.gz", get_pty=True)
    stdout.channel.recv_exit_status()
    print("✅ Extracted\n")
    
    # Verification
    print("📋 Verifying extraction:")
    stdin, stdout, stderr = client.exec_command(f"ls -la {REMOTE_DIR}", get_pty=True)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode())
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    client.close()
