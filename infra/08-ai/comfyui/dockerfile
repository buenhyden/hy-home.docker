# syntax=docker/dockerfile:1.7

FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG COMFYUI_REF=v0.36.0
ARG PUID=1000
ARG PGID=1000

LABEL org.opencontainers.image.title="hy-home ComfyUI"
LABEL org.opencontainers.image.description="ComfyUI for NVIDIA Pascal / GTX 10-series"
LABEL org.opencontainers.image.source="https://github.com/Comfy-Org/ComfyUI"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    HOME=/home/comfyui \
    HF_HOME=/home/comfyui/.cache/huggingface \
    TORCH_HOME=/home/comfyui/.cache/torch \
    TORCH_CUDA_ARCH_LIST=6.1 \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    COMFYUI_PORT=8188 \
    COMFYUI_PREVIEW_METHOD=none \
    COMFYUI_RESERVE_VRAM=0.5 \
    COMFYUI_ARGS=""

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    ffmpeg \
    git \
    git-lfs \
    libgl1 \
    libglib2.0-0t64 \
    libgomp1 \
    python3 \
    python3-venv \
    build-essential \
    tini \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid "${PGID}" comfyui \
    && useradd \
    --uid "${PUID}" \
    --gid "${PGID}" \
    --create-home \
    --home-dir /home/comfyui \
    --shell /bin/bash \
    comfyui

RUN python3 -m venv "${VIRTUAL_ENV}" \
    && python -m pip install --upgrade pip setuptools wheel

# GTX 1060(Pascal)은 CUDA 13 계열 대신 cu126 사용.
RUN python -m pip install \
    torch==2.10.0 \
    torchvision==0.25.0 \
    torchaudio==2.10.0 \
    --index-url https://download.pytorch.org/whl/cu126

WORKDIR /opt

RUN git clone \
    --depth 1 \
    --branch "${COMFYUI_REF}" \
    https://github.com/Comfy-Org/ComfyUI.git \
    /opt/comfyui

WORKDIR /opt/comfyui

# requirements.txt의 torch/torchvision/torchaudio는 위에서 설치한
# cu126 버전으로 이미 충족된다.
RUN python -m pip install -r requirements.txt

# 빌드 시 버전 고정 여부 확인.
# GPU 자체는 build 단계에서 보이지 않을 수 있으므로 런타임 검증은 Compose 기동 후 수행한다.
RUN python - <<'PY'
import torch

assert torch.__version__.startswith("2.10.0"), torch.__version__
assert torch.version.cuda == "12.6", torch.version.cuda

print("PyTorch:", torch.__version__)
print("CUDA runtime:", torch.version.cuda)
PY

RUN mkdir -p \
    /opt/comfyui/models \
    /opt/comfyui/custom_nodes \
    /opt/comfyui/input \
    /opt/comfyui/output \
    /opt/comfyui/user \
    /home/comfyui/.cache/huggingface \
    /home/comfyui/.cache/torch \
    && chown -R comfyui:comfyui \
    /opt/comfyui \
    /opt/venv \
    /home/comfyui

USER comfyui:comfyui

EXPOSE 8188

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/bin/bash", "-lc", "exec python main.py --listen 0.0.0.0 --port \"${COMFYUI_PORT}\" --preview-method \"${COMFYUI_PREVIEW_METHOD}\" --reserve-vram \"${COMFYUI_RESERVE_VRAM}\" ${COMFYUI_ARGS}"]