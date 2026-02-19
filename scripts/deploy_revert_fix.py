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
            if stdout.channel.recv_exit_status() != 0:
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

def run_cmd(ssh, cmd, desc, ignore_error=False):
    print(f"\n--- {desc} ---")
    print(f"Executing: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print(stdout.channel.recv(1024).decode(), end='')
        if stderr.channel.recv_ready():
            print(stderr.channel.recv(1024).decode(), end='')
            
    exit_code = stdout.channel.recv_exit_status()
    if exit_code == 0:
        print(f"\nSUCCESS: {desc}")
        return True
    else:
        print(f"\n{'WARNING' if ignore_error else 'FAILURE'}: {desc} failed with exit code {exit_code}")
        if not ignore_error: print(stderr.read().decode())
        return ignore_error

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {VPS_IP}...")
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        
        # 1. Upload
        local = "d:/uma/cintabuku/frontend/src/components/Footer.tsx"
        remote_tmp = "/tmp/Footer.tsx"
        if not upload_file_base64(ssh, local, remote_tmp):
            sys.exit(1)
            
        repo_path = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/components/Footer.tsx"
        cmd_mv = f"echo '{VPS_PASS}' | sudo -S mv {remote_tmp} {repo_path}"
        if not run_cmd(ssh, cmd_mv, "Move File to Repo"):
            sys.exit(1)
            
        base_cmd = f"echo '{VPS_PASS}' | sudo -S bash -c"
        
        # 2. Build
        cmd_build = f"{base_cmd} 'cd /home/ubuntu24/my-docker-apps && docker compose build --no-cache cintabuku-frontend'"
        if not run_cmd(ssh, cmd_build, "Build Image"):
            sys.exit(1)
            
        # 3. Stop & Remove
        run_cmd(ssh, f"{base_cmd} 'docker stop cintabuku-frontend'", "Stop Old Container", ignore_error=True)
        run_cmd(ssh, f"{base_cmd} 'docker rm cintabuku-frontend'", "Remove Old Container", ignore_error=True)
        
        # 4. Up
        cmd_up = f"{base_cmd} 'cd /home/ubuntu24/my-docker-apps && docker compose up -d cintabuku-frontend'"
        if not run_cmd(ssh, cmd_up, "Start New Container"):
            sys.exit(1)
            
        # 5. Verify
        print("\nWaiting for container...")
        time.sleep(10)
        cmd_grep = f"{base_cmd} 'docker exec cintabuku-frontend grep \"Developed by\" /app/src/components/Footer.tsx'"
        if run_cmd(ssh, cmd_grep, "Verify Content"):
            print("FULL DEPLOYMENT SUCCESSFUL!")
        else:
            print("VERIFICATION FAILED! Content might still be old.")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
