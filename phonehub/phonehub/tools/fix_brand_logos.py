#!/usr/bin/env python3
"""
Update data.js to use local brand logo files
"""
import re

DATA_FILE = r'c:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\phonehub\js\data.js'

# Read the data file
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all logo URLs with local paths
# Pattern to match any logo URL and replace with local path
pattern = r'("logo":\s*")https?://[^"]+(")'
replacement = r'\1img/brands/\1\2'

# This won't work directly, we need to do it per brand
# Let's use a different approach

# Find all brand IDs and their current logo URLs
brand_pattern = r'("id":\s*"([^"]+)"[^}]*?"logo":\s*")([^"]+)(")'

replacements = 0
for match in re.finditer(brand_pattern, content):
    brand_id = match.group(2)
    old_logo = match.group(3)
    
    # Skip if already using local path
    if old_logo.startswith('img/brands/'):
        continue
    
    # Create new local path
    new_logo = f"img/brands/{brand_id}.svg"
    
    # Replace in content
    old_text = match.group(1) + old_logo + match.group(4)
    new_text = match.group(1) + new_logo + match.group(4)
    
    content = content.replace(old_text, new_text, 1)
    replacements += 1
    print(f"Updated {brand_id}: {old_logo} -> {new_logo}")

print(f"\nTotal replacements: {replacements}")

# Write back
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")