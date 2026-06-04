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

1. Read the [Ollama Usage Guide](../../docs/05.operations/guides/08-ai/ollama.md).
2. Follow the [Open WebUI Usage Guide](../../docs/05.operations/guides/08-ai/open-webui.md) and [RAG Workflow Guide](../../docs/05.operations/guides/08-ai/02.rag-workflow.md).
3. Check the [Operations Policy](../../docs/05.operations/policies/08-ai/README.md) for GPU, model, access, and logging controls.
4. Consult the [AI Runbooks](../../docs/05.operations/runbooks/08-ai/README.md) for NVIDIA driver, OOM, or Open WebUI troubleshooting.

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Inference | Ollama | `ollama/ollama:0.30.2` |
| Interface | Open WebUI | `ghcr.io/open-webui/open-webui:v0.9.6-cuda` |
| Acceleration | NVIDIA CUDA | Requires NVIDIA Container Toolkit |
| Vector DB | Qdrant | External dependency in `04-data` |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `ollama` | HTTP | `ai`, `dev` | `${OLLAMA_HOST_PORT}:${OLLAMA_PORT}` and `ollama.${DEFAULT_URL}` |
| `open-webui` | HTTP | `ai` | `chat.${DEFAULT_URL}` via Traefik; no host port is declared |
| `ollama-exporter` | HTTP metrics | `ai`, `dev` | exposed on `${OLLAMA_EXPORTER_PORT}` inside `infra_net` |

## Configuration

- **GPU Access**: Services are configured with `reservations.devices` for NVIDIA GPU access.
- **SSO**: Accessible via `chat.${DEFAULT_URL}` and `ollama.${DEFAULT_URL}`, protected by Keycloak auth middleware.
- **Persistence**: Models are stored in `${DEFAULT_AI_MODEL_DIR}/ollama` to avoid repeated multi-GB downloads.

## Testing

```bash
# Verify GPU availability inside Ollama
docker compose exec ollama nvidia-smi

# List loaded models
docker compose exec ollama ollama list
```

## AI Agent Guidance

1. Always pull models explicitly via `ollama pull <model>` before referencing them in RAG.
2. Monitor VRAM usage via `ollama-exporter` to prevent OOM during concurrent inference.
3. For RAG tasks, ensure `qwen3-embedding:0.6b` (or current standard) is available for vectorization.

---

## Related Documents

- [infra/README.md](../README.md)
- [Operations guides - 08-ai](../../docs/05.operations/guides/08-ai/README.md)
- [Operations policies - 08-ai](../../docs/05.operations/policies/08-ai/README.md)
- [Operations runbooks - 08-ai](../../docs/05.operations/runbooks/08-ai/README.md)
