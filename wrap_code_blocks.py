#!/usr/bin/env python3
import os
import re

def wrap_code_blocks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all code blocks and wrap them
    pattern = r'(```[^\n]*\n.*?^```)'
    
    def replace_func(match):
        code_block = match.group(1)
        # Check if already wrapped
        if '{% raw %}' in code_block:
            return code_block
        return '{% raw %}\n' + code_block + '\n{% endraw %}'
    
    new_content = re.sub(pattern, replace_func, content, flags=re.MULTILINE | re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Process all Rust files
rust_dir = '_posts/rust'
for filename in os.listdir(rust_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(rust_dir, filename)
        wrap_code_blocks(filepath)
        print(f'Processed: {filepath}')

# Process all Tauri files
tauri_dir = '_posts/tauri'
for filename in os.listdir(tauri_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(tauri_dir, filename)
        wrap_code_blocks(filepath)
        print(f'Processed: {filepath}')

print('Done!')
