import re

with open("pixi.toml", "r") as f:
    text = f.read()

# Specifically replace the lines in the exact features to avoid breaking dima
sections_to_patch = [
    "[feature.fastplms.dependencies]",
    "[feature.protrek.dependencies]",
    "[feature.proteindt.dependencies]",
    "[feature.protomech.dependencies]",
    "[feature.saprot.dependencies]",
    "[feature.magneton.dependencies]",
]

def clean_section(text, sec):
    parts = text.split(sec)
    if len(parts) > 1:
        # split after next section or end
        next_sec_idx = parts[1].find("\n[")
        if next_sec_idx == -1:
            next_sec_idx = len(parts[1])
            
        sec_content = parts[1][:next_sec_idx]
        
        # remove torch related from this chunk
        sec_content = re.sub(r'^pytorch\s*=.*?\n', '', sec_content, flags=re.MULTILINE)
        sec_content = re.sub(r'^torchvision\s*=.*?\n', '', sec_content, flags=re.MULTILINE)
        sec_content = re.sub(r'^torchaudio\s*=.*?\n', '', sec_content, flags=re.MULTILINE)
        sec_content = re.sub(r'^pytorch-lightning\s*=.*?\n', '', sec_content, flags=re.MULTILINE)
        sec_content = re.sub(r'^torchmetrics\s*=.*?\n', '', sec_content, flags=re.MULTILINE)
        
        parts[1] = sec_content + parts[1][next_sec_idx:]
        return parts[0] + sec + parts[1]
    return text

for sec in sections_to_patch:
    text = clean_section(text, sec)
    
# Add pip dependencies
for feat in ["fastplms", "protrek", "proteindt", "saprot", "protomech", "magneton"]:
    if "fastplms" in feat:
        text = text.replace(f"[feature.{feat}.pypi-dependencies]\n", f"[feature.{feat}.pypi-dependencies]\ntorch = \"*\"\ntorchvision = \"*\"\n")
    if "protrek" in feat or "saprot" in feat:
        text = text.replace(f"[feature.{feat}.pypi-dependencies]\n", f"[feature.{feat}.pypi-dependencies]\ntorch = \"*\"\ntorchvision = \"*\"\ntorchaudio = \"*\"\ntorchmetrics = \"*\"\nlightning = \"*\"\n")
    if "proteindt" in feat:
        text = text.replace(f"[feature.{feat}.pypi-dependencies]\n", f"[feature.{feat}.pypi-dependencies]\ntorch = \"*\"\n")

with open("pixi.toml", "w") as f:
    f.write(text)
