#!/bin/bash
#SBATCH --job-name=dima_simple
#SBATCH --partition=boost_usr_prod         # Leonardo Boost partition (A100)
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1                       # Use 1 GPU
#SBATCH --time=00:30:00                    # 30 mins
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Leonardo specific: ensure basic modules or environments if needed
# module load ... (Pixi usually handles everything, but you might need to load a driver context)

# Ensure Pixi is in the path
export PATH="$HOME/.pixi/bin:$PATH"

# Go to project root (assumed to be launched from there)
# cd /path/to/phd

echo "Running DiMA simple example on $(hostname)"
echo "Start time: $(date)"

# Run using pixi
pixi run -e dima-env python DiMA/example_simple.py

echo "End time: $(date)"
