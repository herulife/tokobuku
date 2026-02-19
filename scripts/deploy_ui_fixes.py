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
            print(f"Uploading chunk {i+1}/{len(chunks)}...")
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
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        print("Connected to VPS")
        
        files = [
            ("d:/uma/cintabuku/frontend/src/components/Navbar.tsx", "/tmp/Navbar.tsx"),
            ("d:/uma/cintabuku/frontend/src/components/ClientToaster.tsx", "/tmp/ClientToaster.tsx")
        ]
        
        for local, remote in files:
            if not upload_file_base64(ssh, local, remote):
                print(f"Failed to upload {local}")
                sys.exit(1)
            time.sleep(1)
            
        print("All files uploaded successfully via base64.")
            
        # Move files and rebuild
        cmd_move = f"echo '{VPS_PASS}' | sudo -S bash -c 'mv /tmp/Navbar.tsx /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/components/Navbar.tsx && mv /tmp/ClientToaster.tsx /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/components/ClientToaster.tsx'"
        
        print("Moving files interactively...")
        stdin, stdout, stderr = ssh.exec_command(cmd_move)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Rebuild frontend
        cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'cd /home/ubuntu24/my-docker-apps && docker compose down cintabuku-frontend && docker buildx prune -af || true && docker compose up -d --build --force-recreate cintabuku-frontend'"
        
        print("Rebuilding frontend...")
        stdin, stdout, stderr = ssh.exec_command(cmd_rebuild)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end='')
            if stderr.channel.recv_ready():
                 print(stderr.channel.recv(1024).decode(), end='')
                 
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
