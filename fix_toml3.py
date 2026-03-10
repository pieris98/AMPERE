import re

with open("pixi.toml", "r") as f:
    text = f.read()

# Fix cmd
text = text.replace('cmd = "==ln', 'cmd = "ln')

with open("pixi.toml", "w") as f:
    f.write(text)
