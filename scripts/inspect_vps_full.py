import paramiko
import sys
from scp import SCPClient

# VPS Configuration
VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def create_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {VPS_IP}:{VPS_PORT}...")
        client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
        print("✅ Connected successfully\n")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

def execute_command(ssh, command, label=""):
    if label:
        print(f"\n{'='*60}")
        print(f"🔍 {label}")
        print(f"{'='*60}")
    print(f"$ {command}\n")
    
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    if output:
        print(output)
    if error and "WARNING" not in error:
        print(f"⚠️  {error}")
    
    return output

def main():
    ssh = create_ssh_client()
    
    try:
        # 1. Check Docker Compose structure
        execute_command(ssh, 
            "cat ~/my-docker-apps/docker-compose.yml",
            "Current Docker Compose Configuration")
        
        # 2. Check folder structure
        execute_command(ssh, 
            "ls -lah ~/my-docker-apps/",
            "Main Docker Apps Directory")
        
        execute_command(ssh, 
            "ls -lah ~/my-docker-apps/apps/",
            "Apps Subdirectory")
        
        # 3. Check Nginx configuration
        execute_command(ssh, 
            "cat ~/my-docker-apps/nginx/nginx.conf",
            "Current Nginx Configuration")
        
        execute_command(ssh, 
            "ls -lah ~/my-docker-apps/nginx/",
            "Nginx Directory")
        
        # 4. Check running containers
        execute_command(ssh, 
            "echo 'Ubuntu@2025' | sudo -S docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'",
            "Running Docker Containers")
        
        # 5. Check Docker networks
        execute_command(ssh, 
            "echo 'Ubuntu@2025' | sudo -S docker network ls",
            "Docker Networks")
        
        # 6. Check Docker volumes
        execute_command(ssh, 
            "echo 'Ubuntu@2025' | sudo -S docker volume ls",
            "Docker Volumes")
        
        # 7. Check database containers
        execute_command(ssh, 
            "echo 'Ubuntu@2025' | sudo -S docker exec wordpress-db mariadb -u root -pyestina_root_pass -e 'SHOW DATABASES;'",
            "MariaDB Databases")
        
        # 8. Check if PostgreSQL is installed on host
        execute_command(ssh, 
            "which psql || echo 'PostgreSQL not installed on host'",
            "PostgreSQL on Host")
        
        # 9. Check available ports
        execute_command(ssh, 
            "ss -tlnp | grep LISTEN | awk '{print $4}' | sort -u",
            "Listening Ports")
        
        # 10. Check disk space
        execute_command(ssh, 
            "df -h / /home",
            "Disk Space")
        
        # 11. Check if PM2 is installed
        execute_command(ssh, 
            "pm2 list || echo 'PM2 not installed or no processes'",
            "PM2 Processes")
        
        # 12. Check home directory structure
        execute_command(ssh, 
            "ls -lah ~/",
            "Home Directory Structure")
        
        # 13. Check certbot/SSL setup
        execute_command(ssh, 
            "ls -lah ~/my-docker-apps/certbot/conf/ 2>/dev/null || echo 'No certbot config'",
            "Certbot/SSL Configuration")
        
        print("\n" + "="*60)
        print("✅ VPS Inspection Complete!")
        print("="*60)
        
    finally:
        ssh.close()

if __name__ == "__main__":
    main()
