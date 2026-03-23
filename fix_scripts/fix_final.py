import re

with open("pixi.toml", "r") as f:
    text = f.read()

# restore pypi-options
if "[pypi-options]" not in text:
    text += '\n[pypi-options]\nno-build-isolation = ["torch-cluster", "torch-scatter", "torch-sparse", "flash-attn"]\n'

# Add setuptools and wheel to magneton and proteindt
text = text.replace('[feature.magneton.dependencies]', '[feature.magneton.dependencies]\nsetuptools = "*"\nwheel = "*"')
text = text.replace('[feature.proteindt.dependencies]', '[feature.proteindt.dependencies]\nsetuptools = "*"\nwheel = "*"')

# Move pytorch-scatter to torch-scatter in pypi
text = re.sub(r'^pytorch-scatter\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^pytorch-sparse\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^pytorch-cluster\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^pyg\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)

# Add them to pypi
mag_pypi = "[feature.magneton.pypi-dependencies]"
if mag_pypi in text:
    text = text.replace(mag_pypi, mag_pypi + '\ntorch-scatter = ">=2.1.2"\ntorch-geometric = ">=2.6.1"')

pdt_pypi = "[feature.proteindt.pypi-dependencies]"
if pdt_pypi in text:
    text = text.replace(pdt_pypi, pdt_pypi + '\ntorch-scatter = "*"\ntorch-sparse = "*"\ntorch-cluster = "*"\ntorch-geometric = "==2.0.*"')

with open("pixi.toml", "w") as f:
    f.write(text)
