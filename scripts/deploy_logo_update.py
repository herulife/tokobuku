import paramiko
import sys
import base64
import time
import os

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

BASE_REMOTE_DIR = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

def upload_file_base64(ssh, local_path, remote_temp_path):
    print(f"Uploading {local_path} to {remote_temp_path} via base64...")
    try:
        if not os.path.exists(local_path):
             print(f"Error: Local file not found: {local_path}")
             return False

        with open(local_path, "rb") as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode('utf-8')
        
        # Split into chunks to avoid command line length limits
        chunk_size = 32000 # Increased chunk size slightly
        chunks = [b64_content[i:i+chunk_size] for i in range(0, len(b64_content), chunk_size)]
        
        # Create/Clear the file
        ssh.exec_command(f"echo -n '' > {remote_temp_path}.b64")
        
        for i, chunk in enumerate(chunks):
            # Escape single quotes if necessary, though base64 shouldn't have them usually
            # But just to be safe, stick to simple echo
            cmd = f"echo '{chunk}' >> {remote_temp_path}.b64"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                print(f"Error uploading chunk {i}: {stderr.read().decode()}")
                return False
                
        cmd_decode = f"base64 -d {remote_temp_path}.b64 > {remote_temp_path}"
        stdin, stdout, stderr = ssh.exec_command(cmd_decode)
        if stdout.channel.recv_exit_status() != 0:
            print(f"Error decoding: {stderr.read().decode()}")
            return False
            
        print(f"Successfully uploaded {local_path}")
        return True
    except Exception as e:
        print(f"Exception uploading {local_path}: {e}")
        return False

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {VPS_IP}...")
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        print("Connected to VPS")
        
        files_to_deploy = [
            # (Local Path, Remote Temp Path, Final Remote Path)
            (
                r"d:\uma\cintabuku\frontend\public\images\logo.webp", 
                "/tmp/logo.webp", 
                f"{BASE_REMOTE_DIR}/frontend/public/images/logo.webp"
            ),
            (
                r"d:\uma\cintabuku\frontend\public\favicon.ico", 
                "/tmp/favicon.ico", 
                f"{BASE_REMOTE_DIR}/frontend/public/favicon.ico"
            ),
            (
                r"d:\uma\cintabuku\frontend\src\components\Navbar.tsx", 
                "/tmp/Navbar.tsx", 
                f"{BASE_REMOTE_DIR}/frontend/src/components/Navbar.tsx"
            ),
            (
                r"d:\uma\cintabuku\frontend\src\app\layout.tsx", 
                "/tmp/layout.tsx", 
                f"{BASE_REMOTE_DIR}/frontend/src/app/layout.tsx"
            )
        ]
        
        # 1. Upload files to /tmp
        for local, remote_temp, _ in files_to_deploy:
            if not upload_file_base64(ssh, local, remote_temp):
                print(f"Failed to upload {local}")
                sys.exit(1)
        
        print("\nAll files uploaded to /tmp. Moving to final destination...")

        # 2. Move files to final destination using sudo
        for _, remote_temp, remote_final in files_to_deploy:
            # Ensure directory exists (just in case)
            remote_dir = os.path.dirname(remote_final).replace('\\', '/')
            cmd_mkdir = f"echo '{VPS_PASS}' | sudo -S mkdir -p {remote_dir}"
            ssh.exec_command(cmd_mkdir)

            cmd_move = f"echo '{VPS_PASS}' | sudo -S mv {remote_temp} {remote_final}"
            # Set permissions to ensure ubuntu24 can read/write if needed, though docker might run as root
            cmd_chown = f"echo '{VPS_PASS}' | sudo -S chown {VPS_USER}:{VPS_USER} {remote_final}"
            
            print(f"Moving {remote_temp} -> {remote_final}")
            stdin, stdout, stderr = ssh.exec_command(f"{cmd_move} && {cmd_chown}")
            if stdout.channel.recv_exit_status() != 0:
                print(f"Error moving file: {stderr.read().decode()}")
                sys.exit(1)

        print("\nFiles in place. Starting rebuild process...")
        
        # 3. Rebuild frontend container
        # Note: We use 'cintabuku-frontend' if that is the service name in the active compose file.
        # Based on previous file reads, it seems 'cintabuku-frontend' is the service name in 'docker-compose.cintabuku.yml' (Not exactly seen, but inferred from redeploy_clean.py line 78)
        # Wait, let's double check redeploy_clean.py: 
        # cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'cd /home/ubuntu24/my-docker-apps && docker compose up -d --build --force-recreate cintabuku-frontend'"
        # It assumes the service name is 'cintabuku-frontend'.
        
        cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'cd /home/ubuntu24/my-docker-apps && docker compose up -d --build --force-recreate cintabuku-frontend'"
        
        print("Rebuilding frontend (timeout 10 mins)...")
        stdin, stdout, stderr = ssh.exec_command(cmd_rebuild)
        
        # Stream output
        start_time = time.time()
        while not stdout.channel.exit_status_ready():
            if time.time() - start_time > 600: # 10 minutes timeout
                print("Command timed out!")
                break
                
            if stdout.channel.recv_ready():
                 sys.stdout.write(stdout.channel.recv(1024).decode())
                 sys.stdout.flush()
            if stderr.channel.recv_ready():
                 sys.stderr.write(stderr.channel.recv(1024).decode())
                 sys.stderr.flush()
            time.sleep(0.1)
            
        print("\nBuild command finished.")
        
        # 4. Verify
        print("\nVerifying deployment...")
        cmd_verify = f"echo '{VPS_PASS}' | sudo -S docker ps --format '{{{{.Names}}}} {{{{.Status}}}}' | grep cintabuku-frontend"
        stdin, stdout, stderr = ssh.exec_command(cmd_verify)
        print("Container Status:", stdout.read().decode().strip())
        
        ssh.close()
        print("\n✅ Deployment Script Completed.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
