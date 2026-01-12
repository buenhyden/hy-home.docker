# Ollama & Open WebUI

## Overview

Local LLM runner with a ChatGPT-style web interface.

## Services

- **ollama**: LLM Runner.
  - Port: `${OLLAMA_PORT}` (11434)
  - URL: `https://ollama.${DEFAULT_URL}` (API)
- **open-webui**: Web Interface for Ollama.
  - URL: `https://chat.${DEFAULT_URL}`
- **ollama-exporter**: Prometheus metrics.

## Configuration

### Environment Variables

- `OLLAMA_HOST`: `0.0.0.0:${OLLAMA_PORT}`
- `NVIDIA_VISIBLE_DEVICES`: `all` (GPU support).
- `OLLAMA_BASE_URL`: Connection from WebUI to Ollama.
- `VECTOR_DB_URL`: Connection to Qdrant (for RAG).

### Volumes

- `ollama-data`: `/root/.ollama` (Model storage)
- `ollama-webui`: `/app/backend/data` (User data)

## Networks

- `infra_net`
  - ollama: `172.19.0.40`
  - open-webui: `172.19.0.42`

## Traefik Routing

- **Ollama API**: `ollama.${DEFAULT_URL}`
- **Chat UI**: `chat.${DEFAULT_URL}`
