import re

with open("pixi.toml", "r") as f:
    text = f.read()

# remove pypi-options
text = text.replace("""[pypi-options]
no-build-isolation = ["torch-cluster", "torch-scatter", "torch-sparse", "flash-attn"]""", "")

# magneton
# move pyg packages to conda dependencies
magneton_adds = """
pytorch-scatter = ">=2.1.2"
pyg = ">=2.6.1"
"""

mag_dep_idx = text.find("[feature.magneton.dependencies]")
if mag_dep_idx != -1:
    mag_pypi_idx = text.find("[feature.magneton.pypi-dependencies]", mag_dep_idx)
    insert_idx = text.find("\n\n", mag_dep_idx) if text.find("\n\n", mag_dep_idx) < mag_pypi_idx else mag_pypi_idx
    text = text[:insert_idx] + "\n" + magneton_adds.strip() + "\n" + text[insert_idx:]

text = re.sub(r'^torch-scatter\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^torch-geometric\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)

# Also flash-attn needs build isolation off, but let's see if we can just remove it or build it. Actually let's keep flash-attn out of pypi-options, it will build or we can just specify flash-attn in conda forge! conda-forge has flash-attn!
text = re.sub(r'^flash-attn\s*=\s*".*?"\n', '', text, flags=re.MULTILINE)

# Add flash-attn to magneton conda
text = text.replace('pyg = ">=2.6.1"\n', 'pyg = ">=2.6.1"\nflash-attn = "*"\n')


with open("pixi.toml", "w") as f:
    f.write(text)

