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
        
        # Check Dockerfile
        dockerfile_path = "/home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/Dockerfile"
        print(f"\nReading Dockerfile at {dockerfile_path}...")
        cmd_df = f"cat {dockerfile_path}"
        stdin, stdout, stderr = ssh.exec_command(cmd_df)
        print(stdout.read().decode())
        
        # Check Docker container status
        print("\nChecking container status...")
        cmd_ps = "echo 'Ubuntu@2025' | sudo -S docker ps | grep cintabuku-frontend"
        stdin, stdout, stderr = ssh.exec_command(cmd_ps)
        print(stdout.read().decode())
        
        # Check if the file exists INSIDE the container
        print("\nChecking file content INSIDE the container...")
        cmd_exec = "echo 'Ubuntu@2025' | sudo -S docker exec cintabuku-frontend grep 'Dikembangkan oleh' /app/src/components/Footer.tsx"
        stdin, stdout, stderr = ssh.exec_command(cmd_exec)
        out = stdout.read().decode()
        if out:
            print(f"Found match inside container: {out}")
        else:
            print("Match NOT found inside container!")
            print(f"Error/Stderr: {stderr.read().decode()}")

             # Check .next/static chunks if possible? No that's too complex.
            
            # Try to list the file in container to confirm path
            print("Listing file in container:")
            cmd_ls = "echo 'Ubuntu@2025' | sudo -S docker exec cintabuku-frontend ls -l /app/src/components/Footer.tsx"
            stdin, stdout, stderr = ssh.exec_command(cmd_ls)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
