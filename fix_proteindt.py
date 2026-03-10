import re

with open("pixi.toml", "r") as f:
    text = f.read()

# Add pyg to channels
text = text.replace('channels = ["pytorch", "nvidia", "conda-forge", "bioconda", "salilab"]', 'channels = ["pytorch", "nvidia", "pyg", "conda-forge", "bioconda", "salilab"]')

# Proteindt dependencies
proteindt_dep = """[feature.proteindt.dependencies]
python = "3.7.*"
mkl = "2024.0.*"
lxml = "*"
h5py = "*"
biopython = "*"
omegaconf = "*"
pytorch = "*"
pytorch-scatter = "*"
pytorch-sparse = "*"
pytorch-cluster = "*"
pyg = "2.0.*"
"""

pdt_start = text.find("[feature.proteindt.dependencies]")
pdt_end = text.find("[feature.proteindt.pypi-dependencies]")
text = text[:pdt_start] + proteindt_dep + text[pdt_end:]

# Remove them from pypi dependencies
text = re.sub(r'^torch-scatter\s*=\s*"\*"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^torch-sparse\s*=\s*"\*"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^torch-cluster\s*=\s*"\*"\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^torch-geometric\s*=.*?\n', '', text, flags=re.MULTILINE)

with open("pixi.toml", "w") as f:
    f.write(text)
