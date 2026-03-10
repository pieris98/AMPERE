# Built as part of the PhD Monorepo (unified pixi manifest)
ARG BASE_IMAGE=nvidia/cuda:12.1.1-devel-ubuntu22.04
FROM ${BASE_IMAGE}

# Provide the subproject directory and its mapped pixi environment
ARG PROJECT_DIR
ARG PIXI_ENV

RUN test -n "$PROJECT_DIR" || (echo "PROJECT_DIR not set. Please pass --build-arg PROJECT_DIR=<dir>" && false)
RUN test -n "$PIXI_ENV" || (echo "PIXI_ENV not set. Please pass --build-arg PIXI_ENV=<env>" && false)

# System packages
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
        wget git curl ca-certificates \
        build-essential gcc g++ \
        libssl-dev zlib1g-dev \
        ninja-build \
    && rm -rf /var/lib/apt/lists/*

# ── pixi installation ─────────────────────────────────────────────────────────
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/root/.pixi/bin:${PATH}"

# ── workspace preparation ───────────────────────────────────────────────────
WORKDIR /workspace/phd

# Only copy manifest files to cache the long-running dependency installation steps
COPY pixi.toml pixi.lock ./

RUN pixi install -e ${PIXI_ENV} --frozen

# ── environment variables ──────────────────────────────────────────────────────
ENV CONDA_PREFIX=/workspace/phd/.pixi/envs/${PIXI_ENV} \
    PATH="/workspace/phd/.pixi/envs/${PIXI_ENV}/bin:${PATH}" \
    CUDA_HOME="/workspace/phd/.pixi/envs/${PIXI_ENV}" \
    LD_LIBRARY_PATH="/workspace/phd/.pixi/envs/${PIXI_ENV}/lib:${LD_LIBRARY_PATH}" \
    TORCH_CUDA_ARCH_LIST="7.0;7.5;8.0;8.6;8.9;9.0"

# Optional: run any post-install setup tasks isolated to a project
RUN if /root/.pixi/bin/pixi task list -e ${PIXI_ENV} | grep -q 'install-git-deps'; then \
      /root/.pixi/bin/pixi run -e ${PIXI_ENV} install-git-deps; \
    fi

# ── project source ─────────────────────────────────────────────────────────────
COPY . .

# Environment routing to the active subproject
ENV PYTHONPATH=/workspace/phd/${PROJECT_DIR} \
    PROJECT_ROOT=/workspace/phd/${PROJECT_DIR} \
    HF_HOME=/workspace/phd/${PROJECT_DIR}/.cache/huggingface \
    TRANSFORMERS_CACHE=/workspace/phd/${PROJECT_DIR}/.cache/huggingface/hub \
    WANDB_MODE=offline

RUN mkdir -p /workspace/phd/${PROJECT_DIR}/.cache/huggingface /workspace/phd/${PROJECT_DIR}/checkpoints

WORKDIR /workspace/phd/${PROJECT_DIR}

# Provide an entrypoint script that automatically hooks into the Pixi environment dynamically
RUN echo "#!/bin/bash\nexec /root/.pixi/bin/pixi run -e ${PIXI_ENV} \"\$@\"" > /workspace/phd/entrypoint.sh \
    && chmod +x /workspace/phd/entrypoint.sh

ENTRYPOINT ["/workspace/phd/entrypoint.sh"]
CMD ["bash"]
