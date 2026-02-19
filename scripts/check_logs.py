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
        
        cmd = f"echo '{VPS_PASS}' | sudo -S docker logs cintabuku-frontend --tail 100"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print("--- Docker Logs ---")
        print(stdout.read().decode())
        print(stderr.read().decode())
        print("--- End Logs ---")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
