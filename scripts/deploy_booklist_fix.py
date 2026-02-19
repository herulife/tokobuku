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
        # 1. BookList.tsx
        
        files = [
            ("d:/uma/cintabuku/frontend/src/components/BookList.tsx", "/tmp/BookList.tsx"),
        ]
        
        for local, remote in files:
            if not upload_file_base64(ssh, local, remote):
                sys.exit(1)
        
        # Move files
        print("Moving frontend files...")
        cmd_mv = f"echo '{VPS_PASS}' | sudo -S mv /tmp/BookList.tsx /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/components/BookList.tsx"
        ssh.exec_command(cmd_mv)
        
        print("Rebuilding frontend...")
        # Rebuild frontend again
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
             
        print("Frontend update deployed.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
