#!/usr/bin/env python3
# strip_notes.py
#
# Description:
#   Recursively strips LaTeX macros like \FJHNote{...}, \NKNote{...}, \AGSNote{...}
#   from a .tex file, preserving their content.
#
# Usage:
#   ./strip_notes.py myfile.tex
#
#   or
#
#   python strip_notes.py <input_file.tex>
#
#   Example:
#     python strip_notes.py myfile.tex
#     → creates myfile_cleaned.tex
#
# Customization:
#   You can edit the `macros` list inside the script to remove different macros.
#
# Author: FJH and ChatGPT
# Date: 2025-08-04

import re
import sys
import os

def strip_macros_recursive(content, macros_to_strip):
    pattern = re.compile(
        r'\\(' + '|'.join(macros_to_strip) + r')\s*\{',
        re.DOTALL
    )

    def find_macro_at(text, start):
        match = pattern.match(text, start)
        if not match:
            return None
        i = match.end()
        depth = 1
        brace_content = []
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            if depth > 0:
                brace_content.append(text[i])
            i += 1
        return (match.start(), i, ''.join(brace_content))

    while True:
        i = 0
        found = False
        new_text = []
        while i < len(content):
            result = find_macro_at(content, i)
            if result:
                found = True
                start, end, inner = result
                new_text.append(content[i:start])
                new_text.append(inner)
                i = end
            else:
                new_text.append(content[i])
                i += 1
        updated_content = ''.join(new_text)
        if not found:
            break
        content = updated_content

    return content

def generate_output_filename(input_filename):
    base, ext = os.path.splitext(input_filename)
    return f"{base}_cleaned{ext}"

# === Entry Point ===

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python strip_notes.py <input_file.tex>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = generate_output_filename(input_file)

    macros = ['FJHNote', 'NKNote', 'AGSNote']  # Customize as needed

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        cleaned_content = strip_macros_recursive(original_content, macros)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"✅ Done. Cleaned file written to: {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)