# Ollama & Open WebUI

## Overview

A local **LLM (Large Language Model)** inference stack with a ChatGPT-like web interface. It supports **RAG (Retrieval-Augmented Generation)** via Qdrant/Chroma and uses **GPU acceleration** if available.

## Services

- **Service Name**: `ollama`
- **Image**: `ollama/ollama:0.13.5`
- **Role**: Inference Engine
- **Hardware**: NVIDIA GPU Configured (Driver: `nvidia`)

- **Service Name**: `open-webui`
- **Image**: `ghcr.io/open-webui/open-webui:main`
- **Role**: Web Interface & RAG Orchestrator

- **Service Name**: `ollama-exporter`
- **Image**: `lucabecker42/ollama-exporter:latest`
- **Role**: Prometheus Metrics Exporter

## Networking

Services run on `infra_net` with static IPs (172.19.0.4X).

| Service | Static IP | Internal Port | Host Port | Traefik Domain |
| :--- | :--- | :--- | :--- | :--- |
| `ollama` | `172.19.0.40` | `${OLLAMA_PORT}` | - | `ollama.${DEFAULT_URL}` |
| `open-webui` | `172.19.0.42` | `8080` | - | `chat.${DEFAULT_URL}` |
| `ollama-exporter` | `172.19.0.43` | `${OLLAMA_EXPORTER_PORT}` | `${OLLAMA_EXPORTER_HOST_PORT}` | - |

## Persistence

- **Models**: `ollama-data` → `/root/.ollama` (Large model files)
- **User Data**: `ollama-webui` → `/app/backend/data` (Chats, preferences)

## Configuration

### Ollama Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OLLAMA_HOST` | Binding Address | `0.0.0.0:${OLLAMA_PORT}` |
| `NVIDIA_VISIBLE_DEVICES` | GPU Isolation | `all` |

### Open WebUI Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OLLAMA_BASE_URL` | Connection to Ollama | `http://ollama:${OLLAMA_PORT}` |
| `VECTOR_DB_URL` | Connection to Qdrant | `http://qdrant:${QDRANT_PORT}` |
| `RAG_EMBEDDING_ENGINE` | Embedding Provider | `ollama` |
| `RAG_EMBEDDING_MODEL` | Embedding Model | `qwen3-embedding:0.6b` |

## Traefik Integration

Services are exposed via Traefik with TLS enabled (`websecure`).

- **Ollama API**: `ollama.${DEFAULT_URL}`
- **Web Interface**: `chat.${DEFAULT_URL}`

## Usage

1. **Web Interface**: Access `https://chat.${DEFAULT_URL}`.
2. **API**: Access `https://ollama.${DEFAULT_URL}`.

### GPU Check

Verify GPU usage inside the container:

```bash
docker exec -it ollama nvidia-smi
```
