import os

projects = {
    "ProTrek": "protrek-env",
    "ProteinDT": "proteindt-env",
    "ProtoMech": "protomech-env",
    "SaProt": "saprot-env",
    "magneton": "magneton-env",
    "FastPLMs": "fastplms-env",
}

dockerfile_template = """# Built as part of the PhD Monorepo (unified pixi manifest)

FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \\
    TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \\
        wget git curl ca-certificates \\
        build-essential gcc g++ \\
        libssl-dev zlib1g-dev \\
        ninja-build \\
    && rm -rf /var/lib/apt/lists/*

# ── pixi installation ─────────────────────────────────────────────────────────
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/root/.pixi/bin:${{PATH}}"

# ── workspace preparation ───────────────────────────────────────────────────
WORKDIR /workspace/phd

COPY pixi.toml pixi.lock ./

RUN pixi install -e {env_name} --frozen

# ── environment variables ──────────────────────────────────────────────────────
ENV CONDA_PREFIX=/workspace/phd/.pixi/envs/{env_name} \\
    PATH="/workspace/phd/.pixi/envs/{env_name}/bin:${{PATH}}" \\
    CUDA_HOME="/workspace/phd/.pixi/envs/{env_name}" \\
    LD_LIBRARY_PATH="/workspace/phd/.pixi/envs/{env_name}/lib:${{LD_LIBRARY_PATH}}" \\
    TORCH_CUDA_ARCH_LIST="7.0;7.5;8.0;8.6;8.9;9.0"

# ── project source ─────────────────────────────────────────────────────────────
COPY . .

ENV PYTHONPATH=/workspace/phd/{project_name}
ENV PROJECT_ROOT=/workspace/phd/{project_name}

WORKDIR /workspace/phd/{project_name}

ENTRYPOINT ["pixi", "run", "-e", "{env_name}"]
CMD ["bash"]
"""

docker_compose_template = """services:
  {low_project_name}:
    build:
      context: ..
      dockerfile: {project_name}/Dockerfile
    image: {low_project_name}:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ~/.cache/huggingface:/workspace/phd/{project_name}/.cache/huggingface
      - ./checkpoints:/workspace/phd/{project_name}/checkpoints
      - ./data:/workspace/phd/{project_name}/data
      - ./src:/workspace/phd/{project_name}/src
    working_dir: /workspace/phd/{project_name}
    environment:
      - WANDB_MODE=offline
      - HF_HOME=/workspace/phd/{project_name}/.cache/huggingface
      - PROJECT_ROOT=/workspace/phd/{project_name}
    stdin_open: true
    tty: true
    command: ["bash"]
"""

for project, env in projects.items():
    if project == "FastPLMs":
        # FastPLMs has its own Dockerfile already adapted, let's just make sure it has docker-compose.yml
        dc_path = os.path.join(project, "docker-compose.yml")
        with open(dc_path, "w") as f:
            f.write(docker_compose_template.format(project_name=project, low_project_name=project.lower(), env_name=env))
        continue
        
    df_path = os.path.join(project, "Dockerfile")
    dc_path = os.path.join(project, "docker-compose.yml")
    
    if not os.path.exists(df_path):
        with open(df_path, "w") as f:
            f.write(dockerfile_template.format(project_name=project, env_name=env))
            
    if not os.path.exists(dc_path):
        with open(dc_path, "w") as f:
            f.write(docker_compose_template.format(project_name=project, low_project_name=project.lower(), env_name=env))

