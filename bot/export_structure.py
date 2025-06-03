import os

def print_structure(startpath, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                if not file.endswith(('.pyc', '__pycache__', '.env')):
                    f.write(f"{subindent}{file}\n")

print_structure('.', 'project_structure.txt')