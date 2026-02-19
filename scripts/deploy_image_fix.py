import paramiko
import sys
import base64
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def upload_file_base64(ssh, local_path, remote_path):
    print(f"Uploading {local_path} to {remote_path} via base64...")
    try:
        with open(local_path, "rb") as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode('utf-8')
        
        chunk_size = 8192
        chunks = [b64_content[i:i+chunk_size] for i in range(0, len(b64_content), chunk_size)]
        
        ssh.exec_command(f"echo -n '' > {remote_path}.b64")
        
        for i, chunk in enumerate(chunks):
            cmd = f"echo '{chunk}' >> {remote_path}.b64"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                print(f"Error uploading chunk {i}: {stderr.read().decode()}")
                return False
                
        cmd_decode = f"base64 -d {remote_path}.b64 > {remote_path}"
        stdin, stdout, stderr = ssh.exec_command(cmd_decode)
        if stdout.channel.recv_exit_status() != 0:
            print(f"Error decoding: {stderr.read().decode()}")
            return False
            
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
        
        # Uploads:
        # 1. image-utils.ts
        # 2. docker-compose.corrected.yml
        
        files = [
            ("d:/uma/cintabuku/frontend/src/lib/image-utils.ts", "/tmp/image-utils.ts"),
            ("d:/uma/cintabuku/docker-compose.corrected.yml", "/tmp/docker-compose.yml")
        ]
        
        for local, remote in files:
            if not upload_file_base64(ssh, local, remote):
                sys.exit(1)
        
        # Move files
        print("Moving frontend files and docker-compose...")
        # Move image-utils
        cmd_mv_utils = f"echo '{VPS_PASS}' | sudo -S mv /tmp/image-utils.ts /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/lib/image-utils.ts"
        ssh.exec_command(cmd_mv_utils)
        
        # Move docker-compose.yml to overwrite existing one
        # Backup old one first just in case
        cmd_backup_compose = f"echo '{VPS_PASS}' | sudo -S cp /home/ubuntu24/my-docker-apps/docker-compose.yml /home/ubuntu24/my-docker-apps/docker-compose.yml.bak"
        ssh.exec_command(cmd_backup_compose)
        
        cmd_mv_compose = f"echo '{VPS_PASS}' | sudo -S mv /tmp/docker-compose.yml /home/ubuntu24/my-docker-apps/docker-compose.yml"
        ssh.exec_command(cmd_mv_compose)
        
        print("Rebuilding frontend and restarting affected services...")
        # Since docker-compose changed, we should use 'up -d' to recreate container with new volumes
        # And rebuild frontend to pick up code changes
        cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'cd /home/ubuntu24/my-docker-apps && docker compose up -d --build --force-recreate cintabuku-frontend'"
        stdin, stdout, stderr = ssh.exec_command(cmd_rebuild)
        
        # Stream logs
        start_time = time.time()
        while not stdout.channel.exit_status_ready():
             if time.time() - start_time > 900: # 15 mins for frontend build
                  print("Timeout waiting for build.")
                  break
             if stdout.channel.recv_ready():
                  sys.stdout.write(stdout.channel.recv(1024).decode())
             if stderr.channel.recv_ready():
                  sys.stderr.write(stderr.channel.recv(1024).decode())
             time.sleep(0.5)
             
        print("Frontend deployment finished.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
