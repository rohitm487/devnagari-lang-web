import os
import re

def fix_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace src. imports with relative imports
    content = re.sub(r'from src\.', 'from .', content)
    content = re.sub(r'import src\.', 'import .', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    package_dir = 'devnagari_lang'
    for filename in os.listdir(package_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(package_dir, filename)
            print(f"Fixing imports in {file_path}")
            fix_imports(file_path)

if __name__ == '__main__':
    main() 