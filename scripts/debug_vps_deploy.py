import paramiko
import sys

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
        
        # Check file content
        remote_path = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/components/Footer.tsx"
        print(f"Checking content of {remote_path}...")
        
        cmd = f"cat {remote_path} | grep 'Dikembangkan oleh'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        content = stdout.read().decode().strip()
        if content:
            print(f"Found match in file: {content}")
        else:
            print("Match NOT found in file! The file might not have been updated correctly.")
            
        # Check docker-compose.yml to see build context
        print("\nChecking docker-compose.yml for cintabuku-frontend service...")
        cmd_dc = "cat /home/ubuntu24/my-docker-apps/docker-compose.yml"
        stdin, stdout, stderr = ssh.exec_command(cmd_dc)
        dc_content = stdout.read().decode()
        
        # Simple parsing or printing relevant lines
        if "cintabuku-frontend" in dc_content:
            print("Found cintabuku-frontend in docker-compose.yml. Partial content:")
            # print surrounding lines
            lines = dc_content.split('\n')
            for i, line in enumerate(lines):
                if "cintabuku-frontend" in line:
                    print('\n'.join(lines[i:i+20]))
                    break
        else:
            print("cintabuku-frontend NOT found in base docker-compose.yml. Checking other files...")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
