# Ollama Service

Local LLM inference server providing standardized API for language models.

## 0. Context & SSoT

- **Parent Tier**: [infra/08-ai/](../README.md)
- **Internal API**: `ollama:11434`
- **Metrics**: `ollama-exporter:11435`
- **SSO Access**: `ollama.${DEFAULT_URL}`

## 1. Structure

| Component | Image | Role |
| :--- | :--- | :--- |
| `ollama` | `ollama/ollama:0.18.2` | Core inference engine |
| `exporter` | `lucabecker42/ollama-exporter:1.0.1` | Prometheus metrics |

## 2. Tech Stack

- **Runtimes**: C++ (llama.cpp based)
- **Acceleration**: NVIDIA CUDA
- **Observability**: Prometheus Metrics via Exporter

## 3. Configuration

Key environment variables and settings:
- `OLLAMA_HOST`: Set to `0.0.0.0` within the container.
- `OLLAMA_ORIGINS`: Restricted to internal network.
- `GPU Reservation`: 1 NVIDIA GPU reserved via Docker Compose `reservations`.

## 4. Persistence

- **Model Storage**: `${DEFAULT_AI_MODEL_DIR}/ollama`
- **Mount Point**: `/root/.ollama` (RW)

## 5. Operational Status

> [!WARNING]
> High resource usage. GPU memory (VRAM) is the primary bottleneck. Monitor via `nvidia-smi`.

> [!TIP]
> Use `ollama pull <model>` to download new models. Models are persisted in the host's AI model directory.
