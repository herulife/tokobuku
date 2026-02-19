import paramiko
import sys
import base64
import os
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

LOCAL_DIR = "d:/uma/cintabuku/darussunnah2"
REMOTE_DIR_BASE = "/home/ubuntu24/my-docker-apps/apps"
REMOTE_APP_DIR = f"{REMOTE_DIR_BASE}/web-sekolah"

def upload_file_base64_chunked(ssh, local_path, remote_path):
    print(f"Uploading {local_path} -> {remote_path}")
    try:
        with open(local_path, "rb") as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode('utf-8')
        
        chunk_size = 16384 # 16KB chunks
        chunks = [b64_content[i:i+chunk_size] for i in range(0, len(b64_content), chunk_size)]
        
        # Create dir if not exists (dirname)
        remote_dir = os.path.dirname(remote_path).replace("\\", "/")
        ssh.exec_command(f"mkdir -p {remote_dir}")
        
        # Init file
        ssh.exec_command(f"echo -n '' > {remote_path}.b64")
        
        for i, chunk in enumerate(chunks):
            cmd = f"echo '{chunk}' >> {remote_path}.b64"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                print(f"Error uploading chunk {i}: {stderr.read().decode()}")
                return False
                
        cmd_decode = f"base64 -d {remote_path}.b64 > {remote_path} && rm {remote_path}.b64"
        stdin, stdout, stderr = ssh.exec_command(cmd_decode)
        if stdout.channel.recv_exit_status() != 0:
            print(f"Error decoding: {stderr.read().decode()}")
            return False
            
        return True
    except Exception as e:
        print(f"Exception uploading {local_path}: {e}")
        return False

def sync_directory(ssh, local_base, remote_base):
    print(f"Syncing directory {local_base} to {remote_base}...")
    
    # 1. Clean remote directory via sudo (faster than individual deletes if many files)
    # BE CAREFUL: Verify path is correct!
    if remote_base == "/" or remote_base == "/home":
        print("Safety Catch: Remote base is too root!")
        return False
        
    print("Pre-cleaning remote directory...")
    cmd_clean = f"echo '{VPS_PASS}' | sudo -S rm -rf {remote_base}/*"
    ssh.exec_command(cmd_clean)
    
    # 2. Walk local directory
    files_to_upload = []
    for root, dirs, files in os.walk(local_base):
        # Exclude node_modules, .git, etc
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
        if '.next' in dirs:
            dirs.remove('.next')
            
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, local_base)
            remote_path = f"{remote_base}/{rel_path}".replace("\\", "/")
            files_to_upload.append((local_path, remote_path))
            
    print(f"Found {len(files_to_upload)} files to upload.")
    
    # Upload one by one (slow but reliable with paramiko/base64 without rsync)
    for local, remote in files_to_upload:
        if not upload_file_base64_chunked(ssh, local, remote):
            print(f"Failed to upload {local}")
            # continue anyway?
            
    return True

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {VPS_IP}...")
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        print("Connected to VPS")
        
        # 1. Sync Darussunnah2
        sync_directory(ssh, LOCAL_DIR, REMOTE_APP_DIR)
        
        # 2. Ensure Dockerfile is named correctly (Dockerfile.deploy -> Dockerfile)
        print("Configuring Dockerfile...")
        cmd_rename = f"mv {REMOTE_APP_DIR}/Dockerfile.deploy {REMOTE_APP_DIR}/Dockerfile"
        ssh.exec_command(cmd_rename)
        
        # 3. Update docker-compose.yml on VPS
        print("Updating docker-compose.yml...")
        local_compose = "d:/uma/cintabuku/docker-compose.corrected.yml"
        remote_compose = "/home/ubuntu24/my-docker-apps/docker-compose.yml"
        
        # Send via base64, careful with size
        if not upload_file_base64_chunked(ssh, local_compose, remote_compose):
            print("Failed to upload docker-compose.")
            sys.exit(1)
            
        # 4. Rebuild web-sekolah
        print("Rebuilding web-sekolah container...")
        cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'cd /home/ubuntu24/my-docker-apps && docker compose up -d --build --force-recreate web-sekolah'"
        stdin, stdout, stderr = ssh.exec_command(cmd_rebuild)
        
        start_time = time.time()
        while not stdout.channel.exit_status_ready():
             if time.time() - start_time > 600:
                  print("Timeout waiting for build.")
                  break
             if stdout.channel.recv_ready():
                  sys.stdout.write(stdout.channel.recv(1024).decode())
             if stderr.channel.recv_ready():
                  sys.stderr.write(stderr.channel.recv(1024).decode())
             time.sleep(0.5)
             
        print("Deployment finished.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
