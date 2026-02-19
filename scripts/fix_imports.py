import os
import re

# Find all TypeScript files and remove .js from imports
backend_src = r"d:\uma\cintabuku\backend\src"

fixed_count = 0
files_processed = 0

for root, dirs, files in os.walk(backend_src):
    for file in files:
        if file.endswith('.ts'):
            filepath = os.path.join(root, file)
            files_processed += 1
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove .js from import statements
            new_content = re. sub(r"from\s+['\"](.+?)\.js['\"]", r"from '\1'", content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"✅ Fixed: {os.path.relpath(filepath, backend_src)}")

print(f"\n📊 Summary:")
print(f"   Files processed: {files_processed}")
print(f"   Files fixed: {fixed_count}")
print(f"\n✅ All .js extensions removed from imports!")
