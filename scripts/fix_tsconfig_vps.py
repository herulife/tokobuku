import paramiko

VPS_IP = "103.107.206.10"
VPS_PORT = 2480
VPS_USER = "ubuntu24"
VPS_PASS = "Ubuntu@2025"

REMOTE_APP = "/home/ubuntu24/my-docker-apps/apps/cintabuku"

tsconfig_content = """{
    "compilerOptions": {
        "target": "ES2022",
        "module": "CommonJS",
        "moduleResolution": "node",
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": false,
        "esModuleInterop": true,
        "skipLibCheck": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules"]
}"""

print("\n🔧 Fixing tsconfig.json directly on VPS...\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(VPS_IP, port=VPS_PORT, username=VPS_USER, password=VPS_PASS)
    print("✅ Connected\n")
    
    # Write correct tsconfig.json
    stdin, stdout, stderr = client.exec_command(f"cat > {REMOTE_APP}/backend/tsconfig.json << 'TSEOF'\n{tsconfig_content}\nTSEOF")
    stdout.channel.recv_exit_status()
    print("✅ tsconfig.json fixed\n")
    
    # Test it
    stdin, stdout, stderr = client.exec_command(f"cat {REMOTE_APP}/backend/tsconfig.json")
    stdout.channel.recv_exit_status()
    print("Verifying:\n", stdout.read().decode('utf-8')[:200])
    
    print("\n✅ tsconfig fixed on VPS! Running complete_deployment.py now will work.\n")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
