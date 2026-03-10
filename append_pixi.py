import tomli
import tomli_w
import json

with open("pixi.toml", "rb") as f:
    config = tomli.load(f)

# FastPLMs
config.setdefault("feature", {})
config["feature"]["fastplms"] = {
    "dependencies": {
        "python": "3.12.*",
        "gxx_linux-64": ">=11,<=13",
        "cuda-nvcc": ">=12.1",
        "cuda-cudart-dev": ">=12.1",
        "cuda-libraries-dev": ">=12.1",
        "ninja": "*",
        "pytorch": "2.5.1.*",
        "torchvision": "0.20.1.*",
        "matplotlib": "*",
        "numpy": "1.26.4.*",
        "scikit-learn": "*",
        "scipy": "*",
        "seaborn": "*"
    },
    "pypi-dependencies": {
        "einops": "*",
        "tensorflow": "==2.20.0",
        "transformers": "==4.57.6",
        "accelerate": "==1.12.0",
        "datasets": "==4.5.0",
        "hf_transfer": "==0.1.9",
        "hf-xet": "*",
        "peft": "*",
        "networkx": "*",
        "omegaconf": "*",
        "rich": "*",
        "trifast": "*",
        "kernels": "*"
    }
}
config["environments"]["fastplms-env"] = {"features": ["fastplms"]}

# ProTrek
config["feature"]["protrek"] = {
    "dependencies": {
        "python": "3.10.*",
        "pytorch": "2.0.1.*",
        "torchvision": "0.15.2.*",
        "torchaudio": "2.0.2.*",
        "torchmetrics": "0.9.3.*",
        "pytorch-lightning": "2.1.3.*",
        "scikit-learn": "1.4.0.*",
        "biopython": "1.83.*"
    },
    "pypi-dependencies": {
        "gradio": "==4.43",
        "transformers": "==4.28.0",
        "tabulate": "==0.9.0",
        "easydict": "==1.13",
        "lmdb": "==1.4.1",
        "multiprocess": "*",
        "pyspellchecker": "==0.8.2"
    }
}
config["environments"]["protrek-env"] = {"features": ["protrek"]}

# ProteinDT
config["feature"]["proteindt"] = {
    "dependencies": {
        "python": "3.7.*",
        "mkl": "2024.0.*",
        "numpy": "*",
        "networkx": "*",
        "scikit-learn": "*",
        "pytorch": "1.10.*",
        "transformers": "*",
        "lxml": "*",
        "h5py": "*",
        "biopython": "*",
        "omegaconf": "*",
        "scipy": "*"
    },
    "pypi-dependencies": {
        "lmdb": "*",
        "seqeval": "*",
        "openai": "*",
        "accelerate": "*",
        "matplotlib": "*",
        "torch-scatter": "*",
        "torch-sparse": "*",
        "torch-cluster": "*",
        "dm-tree": "*",
        "ml-collections": "*",
        "einops": "*",
        "mdtraj": "*",
        "torch-geometric": "==2.0.*",
        "dllogger": {"git": "https://github.com/NVIDIA/dllogger", "rev": "0540a43971f4a8a16693a9de9de73c1072020769"}
    }
}
config["environments"]["proteindt-env"] = {"features": ["proteindt"]}

# ProtoMech
config["feature"]["protomech"] = {
    "dependencies": {
        "python": "3.10.8",
        "pip": "25.1.*",
        "sqlite": "3.45.3.*",
        "zlib": "1.2.13.*"
    },
    "pypi-dependencies": {
        "absl-py": "==2.2.2",
        "numpy": "==2.2.6",
        "pandas": "==2.2.3",
        "safetensors": "==0.5.3",
        "scikit-learn": "==1.6.1",
        "torch": "==2.7.1",
        "tqdm": "==4.67.1",
        "transformers": "==4.52.0",
        "matplotlib": "==3.10.3",
        "peft": "==0.15.2",
        "pytorch-lightning": "==2.5.1.post0",
        "torchvision": "==0.22.1",
        "fair-esm": "==2.0.0"
    }
}
config["environments"]["protomech-env"] = {"features": ["protomech"]}

# SaProt
config["feature"]["saprot"] = {
    "dependencies": {
        "python": "3.10.*",
        "pytorch": "1.13.1.*",
        "torchvision": "0.14.1.*",
        "torchaudio": "0.13.1.*",
        "pytorch-lightning": "1.8.3.*",
        "pandas": "2.1.1.*",
        "numpy": "1.25.2.*",
        "scipy": "1.14.1.*",
        "torchmetrics": "0.9.3.*",
        "biopython": "1.81.*"
    },
    "pypi-dependencies": {
        "wandb": "==0.12.10",
        "transformers": "==4.28.0",
        "easydict": "==1.10",
        "peft": "==0.10.0",
        "lmdb": "==1.4.1",
        "fair-esm": "==2.0.0",
        "protobuf": "<4,>=3.20.0"
    }
}
config["environments"]["saprot-env"] = {"features": ["saprot"]}

# magneton
config["feature"]["magneton"] = {
    "dependencies": {
        "python": "3.11.*",
        "ninja": ">=1.13.0"
    },
    "pypi-dependencies": {
        "biotite": "<1.0.0",
        "certifi": ">=2025.4.26",
        "easydict": ">=1.13",
        "esm": ">=3.1.2",
        "fire": ">=0.7.1",
        "gpustat": ">=1.1.1",
        "h5py": ">=3.13.0",
        "hydra-colorlog": ">=1.2.0",
        "hydra-core": ">=1.3.2",
        "ipykernel": ">=6.29.5",
        "jupyter": ">=1.1.1",
        "lightning": ">=2.5.0.post0",
        "matplotlib": ">=3.10.0",
        "numpy": "<2.0.0",
        "pandas": ">=2.2.3",
        "pathos": ">=0.3.4",
        "pdbecif": ">=1.5",
        "pysam": ">=0.22.1",
        "scikit-learn": ">=1.6.0",
        "seaborn": ">=0.13.2",
        "torch": "==2.6.0",
        "torch-geometric": ">=2.6.1",
        "torch-scatter": ">=2.1.2",
        "torchdata": "*",
        "torchvision": ">=0.21.0",
        "tqdm": ">=4.67.1",
        "umap-learn": ">=0.5.7",
        "wandb": ">=0.19.6",
        "pytest": ">=8.4.2",
        "lmdb": ">=1.7.3",
        "flash-attn": ">=2.7.4-post1"
    }
}
config["environments"]["magneton-env"] = {"features": ["magneton"]}

with open("pixi.toml", "wb") as f:
    tomli_w.dump(config, f)

