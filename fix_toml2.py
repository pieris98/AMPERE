import re

with open("pixi.toml", "r") as f:
    text = f.read()

sections = [
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
        next_sec_idx = parts[1].find("\n[")
        if next_sec_idx == -1:
            next_sec_idx = len(parts[1])
            
        sec_content = parts[1][:next_sec_idx]
        
        packages_to_move = []
        lines = sec_content.split("\n")
        new_sec_content = []
        for line in lines:
            if not line.strip() or line.strip().startswith("[") or "=" not in line:
                new_sec_content.append(line)
                continue
                
            pkg_name = line.split("=")[0].strip()
            if pkg_name not in ["python", "pip", "cuda-nvcc", "cuda-cudart-dev", "cuda-libraries-dev", "gxx_linux-64", "ninja", "sqlite", "zlib", "mkl"]:
                packages_to_move.append(line.strip())
            else:
                new_sec_content.append(line)
        
        parts[1] = "\n".join(new_sec_content) + parts[1][next_sec_idx:]
        new_text = parts[0] + sec + parts[1]
        
        feat = sec.split(".")[1]
        pypi_sec = f"[feature.{feat}.pypi-dependencies]"
        
        if pypi_sec in new_text:
            pypi_additions = []
            for line in packages_to_move:
                # e.g., numpy = "1.26.4.*" -> numpy = "==1.26.4"
                parts = line.split("=")
                pkg = parts[0].strip()
                val = "=".join(parts[1:]).strip().strip('"')
                
                if val == "*":
                    pypi_additions.append(f'{pkg} = "*"')
                else:
                    val = val.replace(".*", "")
                    if not (val.startswith(">") or val.startswith("<") or val.startswith("=")):
                        val = f"=={val}"
                    pypi_additions.append(f'{pkg} = "{val}"')
            
            pypi_block = pypi_sec + "\n" + "\n".join(pypi_additions)
            new_text = new_text.replace(pypi_sec, pypi_block)
                
        return new_text
    return text

for sec in sections:
    text = clean_section(text, sec)
    
# also fix protomech python versions that complained
text = text.replace('python = "3.10.8"', 'python = "3.10.8.*"')

with open("pixi.toml", "w") as f:
    f.write(text)

