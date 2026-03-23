import re

with open("pixi.toml", "r") as f:
    text = f.read()

# Remove all problematic PyG packages from PyPI
for pkg in ["torch-scatter", "torch-sparse", "torch-cluster", "torch-geometric"]:
    text = re.sub(rf'^{pkg}\s*=.*?\n', '', text, flags=re.MULTILINE)

# Add them to Conda dependencies for proteindt
pdt_str = "pytorch-scatter = \"*\"\npyg = \"2.0.*\"\n"
if "pytorch-scatter" not in text:
    pdt_dep_idx = text.find("[feature.proteindt.dependencies]")
    pdt_pypi_idx = text.find("[feature.proteindt.pypi-dependencies]")
    if pdt_dep_idx != -1 and pdt_pypi_idx != -1:
        text = text[:pdt_pypi_idx] + pdt_str + text[pdt_pypi_idx:]

# Add them to Conda dependencies for magneton
mag_str = "pytorch-scatter = \"*\"\npyg = \"*\"\n"
if "pytorch-scatter" not in text[text.find("[feature.magneton.dependencies]"):]:
    mag_dep_idx = text.find("[feature.magneton.dependencies]")
    mag_pypi_idx = text.find("[feature.magneton.pypi-dependencies]")
    if mag_dep_idx != -1 and mag_pypi_idx != -1:
        text = text[:mag_pypi_idx] + mag_str + text[mag_pypi_idx:]

# Remove [pypi-options] if it exists to prevent 403
if "[pypi-options]" in text:
    text = text.split("[pypi-options]")[0]

with open("pixi.toml", "w") as f:
    f.write(text)

