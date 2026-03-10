import tomli
import tomli_w

with open("pixi.toml", "rb") as f:
    data = tomli.load(f)

# we do not use [pypi-options] because tomli_w doesn't handle all arbitrary new keys easily if we just append,
# actually wait, tomli_w dict mutation is easy:
if "pypi-options" not in data:
    data["pypi-options"] = {}
data["pypi-options"]["no-build-isolation"] = ["torch-cluster", "torch-scatter", "torch-sparse", "flash-attn"]
data["pypi-options"]["find-links"] = ["https://data.pyg.org/whl/torch-2.6.0+cu124.html"]

with open("pixi.toml", "wb") as f:
    tomli_w.dump(data, f)
