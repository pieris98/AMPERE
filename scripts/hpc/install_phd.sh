#!/bin/bash
# install_phd.sh - Bulletproof installation script for PhD Monorepo on HPC
# Designed for Leonardo HPC but should work on most Linux clusters.

set -e  # Exit on error

echo "--------------------------------------------------------"
echo "PHD Monorepo: Starting Bulletproof Installation"
echo "--------------------------------------------------------"

# 1. Pixi Installation
PIXI_DIR="$HOME/.pixi"
if ! command -v pixi &> /dev/null; then
    echo "[1/4] Pixi not found. Installing Pixi to $PIXI_DIR..."
    curl -fsSL https://pixi.sh/install.sh | bash
    # Export path for current session
    export PATH="$PIXI_DIR/bin:$PATH"
    echo "      Pixi installed successfully."
else
    echo "[1/4] Pixi is already installed."
    export PATH="$PIXI_DIR/bin:$PATH"
fi

# 2. Project Directory
PROJECT_ROOT=$(pwd)
echo "[2/4] Setting project root to $PROJECT_ROOT"

# 3. Environment Installation
echo "[3/4] Installing Pixi environments (dima-env)..."
# Using --frozen to ensure we match the lockfile exactly
pixi install -e dima-env --frozen

# 4. Post-installation (Git dependencies)
echo "[4/4] Running post-install git dependencies for DiMA..."
pixi run -e dima-env install-git-deps

echo "--------------------------------------------------------"
echo "Verification..."
pixi run -e dima-env python -c "import torch; print(f'PyTorch {torch.__version__} | CUDA available: {torch.cuda.is_available()}'); import openfold; print('OpenFold imported successfully.')"

echo "--------------------------------------------------------"
echo "INSTALLATION COMPLETE"
echo "To use pixi in your current shell, run: export PATH=\"\$HOME/.pixi/bin:\$PATH\""
echo "--------------------------------------------------------"
