#!/bin/bash
# SBATCH --job-name=dima_experiments
# SBATCH --partition=boost_usr_prod         # Leonardo Boost partition (A100)
# SBATCH --nodes=1
# SBATCH --ntasks-per-node=1
# SBATCH --cpus-per-task=16
# SBATCH --gres=gpu:1                       # Use 1 GPU
# SBATCH --time=04:00:00                    # 4 hours
# SBATCH --output=%x_%j.out
# SBATCH --error=%x_%j.err

# Ensure Pixi is in the path
export PATH="$HOME/.pixi/bin:$PATH"

echo "Running DiMA comprehensive experiments on $(hostname)"
echo "Start time: $(date)"

# Mode: all (unconditional + family generation)
# num_samples: 512 for a reasonably fast run on HPC
pixi run -e dima-env python DiMA/auto-scripts/run_experiments.py \
    --mode all \
    --num_samples 512 \
    --output_dir results_hpc \
    --encoder esm2

echo "End time: $(date)"
