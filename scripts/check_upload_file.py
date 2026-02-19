import paramiko
import sys

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {VPS_IP}...")
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        print("Connected to VPS")
        
        target_file = "book-1771287984998-333126110.webp"
        upload_dir = "/home/ubuntu24/my-docker-apps/apps/cintabuku/uploads"
        
        print(f"Checking for {target_file} in {upload_dir}...")
        
        # Check specific file
        cmd = f"ls -la {upload_dir}/{target_file}"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        
        if out:
            print(f"File FOUND: {out}")
        else:
            print(f"File NOT FOUND. Error: {err}")
            
        print("-" * 20)
        print("Listing directory contents (first 10 files):")
        cmd_ls = f"ls -la {upload_dir} | head -n 15"
        stdin, stdout, stderr = ssh.exec_command(cmd_ls)
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
