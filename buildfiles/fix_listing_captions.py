#!/usr/bin/env python3
r"""
Fix code listing captions in generated LaTeX file.
Extracts caption text from notebook and injects into LaTeX \caption{} commands.
"""
import sys
import json
import re

def extract_captions_from_notebook(notebook_path):
    """Extract fig-cap text for each lst- label from notebook."""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    captions = {}
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            
            # Find label
            label_match = re.search(r'#\| label: (lst-[\w-]+)', source)
            if label_match:
                label = label_match.group(1)
                
                # Find fig-cap
                cap_match = re.search(r'#\| fig-cap: ["\']([^"\']+)["\']', source)
                if cap_match:
                    captions[label] = cap_match.group(1)
    
    return captions

def fix_latex_captions(tex_path, captions):
    r"""Inject caption text into empty \caption{} commands in LaTeX."""
    with open(tex_path, 'r') as f:
        content = f.read()
    
    # For each label, find and fix its caption
    for label, caption_text in captions.items():
        # Escape special LaTeX characters in caption
        escaped_caption = caption_text.replace('_', r'\_').replace('%', r'\%').replace('&', r'\&')
        
        # Find pattern: \caption{\label{lst-xxx}} and replace with: \caption{Text\label{lst-xxx}}
        # Use literal string matching, not regex
        old_pattern = '\\caption{\\label{' + label + '}}'
        new_pattern = '\\caption{' + escaped_caption + '\\label{' + label + '}}'
        
        content = content.replace(old_pattern, new_pattern)
    
    with open(tex_path, 'w') as f:
        f.write(content)
    
    return len(captions)

if __name__ == '__main__':
    # Accept notebook path as command-line argument or use default
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    else:
        notebook_path = 'Modul_8_Derivate.ipynb'

    # Derive .tex path from .ipynb path
    tex_path = notebook_path.replace('.ipynb', '.tex')

    print("Extracting captions from notebook...")
    captions = extract_captions_from_notebook(notebook_path)
    print(f"Found {len(captions)} captions:")
    for label, text in captions.items():
        print(f"  {label}: {text}")

    print("\nFixing LaTeX captions...")
    count = fix_latex_captions(tex_path, captions)
    print(f"✓ Fixed {count} caption(s)")
