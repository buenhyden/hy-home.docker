# AI Infrastructure Tier (08-ai)

> Local LLM inference engines, RAG interfaces, and vector-backed intelligence.

## Overview

The `08-ai` tier provides the platform's artificial intelligence capabilities, focusing on privacy-preserving local inference and Retrieval-Augmented Generation (RAG). It leverages NVIDIA GPU acceleration to serve Large Language Models (LLMs) via Ollama and provides a sophisticated user interface through Open WebUI.

## Audience

이 README의 주요 독자:

- AI Engineers (Model deployment & RAG tuning)
- Backend Developers (LLM API integration)
- SREs (GPU resource orchestration)

## Scope

### In Scope

- Ollama (LLM Inference engine)
- Open WebUI (User Interface & RAG Orchestration)
- NVIDIA CUDA integration
- Local Model Management

### Out of Scope

- Model training or fine-tuning (handled in external dedicated clusters)
- Vector DB hosting (managed in `04-data/qdrant`)
- Cloud-based LLM APIs (OpenAI, Claude, etc. - may be proxied but not hosted)

## Structure

```text
08-ai/
├── ollama/             # Inference engine (Go-based)
├── open-webui/         # Web interface and RAG logic
└── README.md           # This file
```

## How to Work in This Area

1. Read the [LLM Inference Guide](../../docs/07.guides/08-ai/01.llm-inference.md).
2. Follow the [RAG Workflow Guide](../../docs/07.guides/08-ai/02.rag-workflow.md).
3. Check the [Operations Policy](../../docs/08.operations/08-ai/README.md) for GPU resource management.
4. Consult the [AI Runbook](../../docs/09.runbooks/08-ai/README.md) for NVIDIA driver or OOM troubleshooting.

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Inference | Ollama | v0.18.2 (CUDA enabled) |
| Interface | Open WebUI | v0.8.5-cuda |
| Acceleration | NVIDIA CUDA | Requires NVIDIA Container Toolkit |
| Vector DB | Qdrant | External dependency in `04-data` |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `ollama` | HTTP | `ai` | 11434 |
| `open-webui` | HTTP | `ai` | 8080 (Mapped to chat domain) |
| `ollama-exporter` | HTTP | `ai` | 11435 (Metrics) |

## Configuration

- **GPU Access**: Services are configured with `reservations.devices` for NVIDIA GPU access.
- **SSO**: Accessible via `chat.${DEFAULT_URL}` and `ollama.${DEFAULT_URL}`, protected by Keycloak auth middleware.
- **Persistence**: Models are stored in `${DEFAULT_AI_MODEL_DIR}/ollama` to avoid repeated multi-GB downloads.

## Testing

```bash
# Verify GPU availability inside Ollama
docker exec -it ollama nvidia-smi

# List loaded models
docker exec -it ollama ollama list
```

## AI Agent Guidance

1. Always pull models explicitly via `ollama pull <model>` before referencing them in RAG.
2. Monitor VRAM usage via `ollama-exporter` to prevent OOM during concurrent inference.
3. For RAG tasks, ensure `qwen3-embedding:0.6b` (or current standard) is available for vectorization.
