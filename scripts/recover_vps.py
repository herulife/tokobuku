import paramiko
from scp import SCPClient
import sys

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def main():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=30)
        
        print("Connected to VPS")
        
        # Upload updated frontend env
        # Upload updated frontend env
        with SCPClient(ssh.get_transport(), socket_timeout=120.0) as scp:
            print("Uploading updated frontend env...")
            scp.put("d:/uma/cintabuku/frontend/env.production", "/tmp/env.production")
            print("Uploading updated api-client.ts...")
            scp.put("d:/uma/cintabuku/frontend/src/lib/api-client.ts", "/tmp/api-client.ts")
            print("Uploading patched page.tsx files...")
            scp.put("d:/uma/cintabuku/frontend/src/app/page.tsx", "/tmp/page.tsx")
            scp.put("d:/uma/cintabuku/frontend/src/app/books/page.tsx", "/tmp/books_page.tsx")
            scp.put("d:/uma/cintabuku/frontend/src/app/books/[slug]/page.tsx", "/tmp/slug_page.tsx")
            
        # Move env, move files, and rebuild
        cmd_rebuild = f"echo '{VPS_PASS}' | sudo -S bash -c 'mv /tmp/env.production /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/.env.local && mv /tmp/api-client.ts /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/lib/api-client.ts && mv /tmp/page.tsx /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/app/page.tsx && mv /tmp/books_page.tsx /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/app/books/page.tsx && mv /tmp/slug_page.tsx /home/ubuntu24/my-docker-apps/apps/cintabuku/frontend/src/app/books/[slug]/page.tsx && cd /home/ubuntu24/my-docker-apps && docker compose down cintabuku-frontend && docker buildx prune -af || true && docker compose up -d --build --force-recreate cintabuku-frontend'"
        
        print("Rebuilding frontend with correct API URL...")
        stdin, stdout, stderr = ssh.exec_command(cmd_rebuild)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
