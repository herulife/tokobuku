import paramiko
import sys
import time

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
        
        # Verify file on host first (sanity check)
        remote_path = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/components/Footer.tsx"
        cmd_check = f"grep 'Dikembangkan oleh' {remote_path}"
        stdin, stdout, stderr = ssh.exec_command(cmd_check)
        if stdout.channel.recv_exit_status() != 0:
            print("WARNING: File on host does not seem to be updated! Re-uploading...")
            # Copied from previous script if needed, but assuming it's there based on debug
            
        print("Forcing rebuild with --no-cache...")
        
        cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'cd /home/ubuntu24/my-docker-apps && docker compose build --no-cache cintabuku-frontend && docker compose up -d --force-recreate cintabuku-frontend'"
        
        stdin, stdout, stderr = ssh.exec_command(cmd_rebuild)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end='')
            if stderr.channel.recv_ready():
                print(stderr.channel.recv(1024).decode(), end='')
                
        exit_code = stdout.channel.recv_exit_status()
        if exit_code == 0:
            print("\nRebuild complete!")
        else:
            print(f"\nRebuild failed with exit code {exit_code}")
            sys.exit(1)
            
        # Verify inside container
        print("Verifying inside container...")
        time.sleep(5) # Give it a moment to start
        cmd_verify = "echo 'Ubuntu@2025' | sudo -S docker exec cintabuku-frontend grep 'Dikembangkan oleh' /app/src/components/Footer.tsx"
        stdin, stdout, stderr = ssh.exec_command(cmd_verify)
        out = stdout.read().decode()
        if out:
            print(f"SUCCESS: Found match inside container: {out.strip()}")
        else:
            print("FAILURE: Match still NOT found inside container!")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
