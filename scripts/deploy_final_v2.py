import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def run_command(ssh, cmd, description, ignore_error=False):
    print(f"\n--- {description} ---")
    print(f"Executing: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    # Stream output
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print(stdout.channel.recv(1024).decode(), end='')
        if stderr.channel.recv_ready():
            print(stderr.channel.recv(1024).decode(), end='')
            
    exit_code = stdout.channel.recv_exit_status()
    if exit_code == 0:
        print(f"\nSUCCESS: {description}")
        return True
    else:
        print(f"\n{'WARNING' if ignore_error else 'FAILURE'}: {description} failed with exit code {exit_code}")
        print(stderr.read().decode())
        return ignore_error

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {VPS_IP}...")
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        
        base_cmd = f"echo '{VPS_PASS}' | sudo -S bash -c"
        
        # We already built the image successfully in the previous step, so we can skip build.
        # But let's build again just to be sure if users want a complete script. 
        # Actually, let's just do the stop/rm/up part since build took 4 minutes.
        
        # Stop container
        cmd_stop = f"{base_cmd} 'docker stop cintabuku-frontend'"
        run_command(ssh, cmd_stop, "Stop Container", ignore_error=True)
        
        # Remove container
        cmd_rm = f"{base_cmd} 'docker rm cintabuku-frontend'"
        run_command(ssh, cmd_rm, "Remove Container", ignore_error=True)
        
        # Up
        cmd_up = f"{base_cmd} 'cd /home/ubuntu24/my-docker-apps && docker compose up -d cintabuku-frontend'"
        if not run_command(ssh, cmd_up, "Start Container"):
            sys.exit(1)
            
        # Verify
        print("\nWaiting for container to initialize...")
        time.sleep(10)
        
        cmd_verify = f"{base_cmd} 'docker exec cintabuku-frontend grep \"Dikembangkan oleh\" /app/src/components/Footer.tsx'"
        if run_command(ssh, cmd_verify, "Verify Content"):
            print("DEPLOYMENT SUCCESSFUL!")
        else:
            print("DEPLOYMENT FAILED VERIFICATION!")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
