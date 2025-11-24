# fix_streamlit_deprecation.py
import os
import glob

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace width='stretch' with width='stretch'
    content = content.replace('width='stretch'', "width='stretch'")
    
    # Replace width='content' with width='content'
    content = content.replace('width='content'', "width='content'")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated: {file_path}")

# Update all Python files in the project
python_files = glob.glob('**/*.py', recursive=True)

for file in python_files:
    update_file(file)

print("All files updated successfully!")