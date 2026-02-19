import paramiko
import sys
import time

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def run_command(ssh, cmd, description):
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
        print(f"\nFAILURE: {description} failed with exit code {exit_code}")
        # Print remaining stderr if any
        print(stderr.read().decode())
        return False

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {VPS_IP}...")
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        
        base_cmd = f"echo '{VPS_PASS}' | sudo -S bash -c"
        
        # Step 1: navigate and build
        # We combine cd and build because cd is session-local
        cmd_build = f"{base_cmd} 'cd /home/ubuntu24/my-docker-apps && docker compose build --no-cache cintabuku-frontend'"
        if not run_command(ssh, cmd_build, "Build Container (No Cache)"):
            sys.exit(1)
            
        # Step 2: Up
        cmd_up = f"{base_cmd} 'cd /home/ubuntu24/my-docker-apps && docker compose up -d --force-recreate cintabuku-frontend'"
        if not run_command(ssh, cmd_up, "Restart Container"):
            sys.exit(1)
            
        # Step 3: Verify
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
