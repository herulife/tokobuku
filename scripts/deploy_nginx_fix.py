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
        
        # Upload Nginx Config
        local_nginx = "d:/uma/cintabuku/nginx/nginx.conf"
        remote_nginx_tmp = "/tmp/nginx.conf"
        
        if not upload_file_base64(ssh, local_nginx, remote_nginx_tmp):
            sys.exit(1)
            
        # Move Nginx config
        print("Moving Nginx config...")
        cmd_move = f"echo '{VPS_PASS}' | sudo -S mv /tmp/nginx.conf /home/ubuntu24/my-docker-apps/nginx/nginx.conf"
        ssh.exec_command(cmd_move)
        
        # Check uploads directory permissions and existence
        print("Checking uploads directory...")
        cmd_check = f"echo '{VPS_PASS}' | sudo -S ls -la /home/ubuntu24/my-docker-apps/apps/cintabuku"
        stdin, stdout, stderr = ssh.exec_command(cmd_check)
        print(stdout.read().decode())
        
        # Create uploads directory if missing
        cmd_mkdir = f"echo '{VPS_PASS}' | sudo -S mkdir -p /home/ubuntu24/my-docker-apps/apps/cintabuku/uploads"
        ssh.exec_command(cmd_mkdir)
        
        # Set permissions
        cmd_chmod = f"echo '{VPS_PASS}' | sudo -S chmod -R 777 /home/ubuntu24/my-docker-apps/apps/cintabuku/uploads"
        ssh.exec_command(cmd_chmod)
        
        # Restart Nginx
        print("Restarting Nginx...")
        cmd_restart = f"echo '{VPS_PASS}' | sudo -S docker restart nginx-proxy"
        stdin, stdout, stderr = ssh.exec_command(cmd_restart)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
