#!/usr/bin/env python3
"""
Quick verification script to check VPS deployment status
"""

import sys
try:
    import paramiko
except ImportError:
    print("Please install: pip install paramiko")
    sys.exit(1)

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

def check_vps():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to {VPS_IP}...")
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    checks = [
        ("Container Status", "sudo docker ps | grep cintabuku"),
        ("Database Ready", "sudo docker exec cintabuku-db pg_isready -U cintabuku_user || echo 'Not running'"),
        ("Backend Health", "sudo docker exec cintabuku-backend wget -q -O- http://localhost:5000/health 2>/dev/null || echo 'Not accessible'"),
        ("Nginx Config", "sudo docker exec nginx-proxy nginx -t 2>&1 | tail -1"),
        ("Disk Space", "df -h / | tail -1 | awk '{print $5 \" used\"}'"),
    ]
    
    for name, cmd in checks:
        print(f"🔍 {name}:")
        stdin, stdout, stderr = client.exec_command(f"echo '{VPS_PASS}' | {cmd}", get_pty=True)
        output = stdout.read().decode('utf-8', errors='ignore').strip()
        if output:
            print(f"   {output}\n")
    
    client.close()
    print("✅ Verification complete")

if __name__ == "__main__":
    try:
        check_vps()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
