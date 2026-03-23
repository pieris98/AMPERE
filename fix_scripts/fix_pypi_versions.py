import re

with open("pixi.toml", "r") as f:
    text = f.read()

# fix anything inside [feature.X.pypi-dependencies]
parts = re.split(r'(\[feature\..*?\.pypi-dependencies\])', text)

new_text = parts[0]
for i in range(1, len(parts), 2):
    header = parts[i]
    content = parts[i+1]
    
    # replace "1.83.*" with "==1.83"
    content = re.sub(r'"(\d+\.\d+(?:\.\d+)?)\.\*"', r'"==\1"', content)
    # replace "1.83" with "==1.83" if it doesn't have operator
    def fix_bare(match):
        val = match.group(1)
        if val == '*' or val.startswith('=') or val.startswith('>') or val.startswith('<'):
            return f'"{val}"'
        return f'"=={val}"'
    
    content = re.sub(r'"([^"]+)"', fix_bare, content)
    
    new_text += header + content

with open("pixi.toml", "w") as f:
    f.write(new_text)

