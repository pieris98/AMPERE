# HPC Deployment: Leonardo

This directory contains automation scripts to deploy the `phd` monorepo on the Leonardo HPC (or any Slurm cluster).

## 1. Quick Start (Installation)

Run the bulletproof installer from the root of the monorepo:

```bash
bash scripts/hpc/install_phd.sh
```

This script:
1. Installs **Pixi** in `$HOME/.pixi` (if not present).
2. Uses `pixi.lock` to install the **exact** dependency versions (`dima-env`).
3. Compiles the specialized **git dependencies** (OpenFold, ESM, etc.).
4. Verifies GPU availability.

## 2. Running Jobs

### Simple Generation Example
To verify everything is working with a short generation job:

```bash
sbatch scripts/hpc/dima_simple.slurm
```

### Full Experiments Pipeline
To run the full evaluation suite including unconditional generation and family-specific conditional generation:

```bash
sbatch scripts/hpc/dima_experiments.slurm
```

## Troubleshooting

- **Memory/Disk Space**: If your home directory (`~`) is small, Pixi can store environments in a different location. Run `export PIXI_HOME=/path/to/scratch/.pixi` before installing.
- **Proxy**: If the compute nodes don't have internet access, ensure you run the `install_phd.sh` on a **login node** with internet access first. The compute nodes will then use the cached environments.
- **CUDA Errors**: The scripts assume the `boost_usr_prod` partition (A100 GPUs). If using a different partition, update the `--partition` line in the `.slurm` files.
