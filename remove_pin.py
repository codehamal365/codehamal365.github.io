#!/usr/bin/env python3
"""
Remove 'pin: true' from all markdown files in _posts/ directory.
"""

import os
import re
from pathlib import Path

def remove_pin_from_file(filepath):
    """Remove 'pin: true' from a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match 'pin: true' followed by optional trailing spaces and newline
    # This handles both with and without leading spaces
    content = re.sub(r'\n\s*pin:\s*true\s*\n', '\n', content)
    
    # Also handle case where pin: true might be the last thing in front matter (before ---)
    content = re.sub(r'\n\s*pin:\s*true\s*\n\s*---', '\n---', content)
    
    # Also handle case where pin: true might be right after tags:
    content = re.sub(r'tags:\s*\n.*pin:\s*true', 'tags:', content, flags=re.MULTILINE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed pin: true from: {filepath}")

def main():
    posts_dir = Path('_posts')
    
    # Process all markdown files recursively
    for md_file in posts_dir.glob('**/*.md'):
        remove_pin_from_file(md_file)

if __name__ == '__main__':
    main()
