# Ollama & Open WebUI

## Overview

A local LLM (Large Language Model) inference stack with a ChatGPT-like web interface. Supports RAG (Retrieval-Augmented Generation) via Qdrant.

## Service Details

### 1. Ollama (`ollama`)

- **Image**: `ollama/ollama:0.13.5`
- **Purpose**: LLM Inference Engine.
- **Hardware**: configured for NVIDIA GPU (`metrics` mapped to `nvidia`).
- **Dependencies**: None.

### 2. Open WebUI (`open-webui`)

- **Image**: `ghcr.io/open-webui/open-webui:main`
- **Purpose**: Web interface for Ollama.
- **RAG Integration**:
  - Connected to `qdrant` (Vector DB).
  - Embedding Engine: `ollama` (using `qwen3-embedding:0.6b`).

### 3. Exporter

- **Image**: `lucabecker42/ollama-exporter`
- **Port**: `${OLLAMA_EXPORTER_PORT}`

## Environment Variables

| Service | Variable | Description | Default |
| :--- | :--- | :--- | :--- |
| **Ollama** | `OLLAMA_HOST` | Binding Address | `0.0.0.0:${OLLAMA_PORT}` |
| **Ollama** | `NVIDIA_VISIBLE_DEVICES` | GPU Isolation | `all` |
| **WebUI** | `OLLAMA_BASE_URL` | Connection to Ollama | `http://ollama:${OLLAMA_PORT}` |
| **WebUI** | `VECTOR_DB_URL` | Connection to Qdrant | `http://qdrant:${QDRANT_PORT}` |
| **WebUI** | `RAG_EMBEDDING_ENGINE` | Embedding Provider | `ollama` |
| **WebUI** | `RAG_EMBEDDING_MODEL` | Embedding Model | `qwen3-embedding:0.6b` |
| **Exporter** | `OLLAMA_HOST` | Target to scrape | `ollama:${OLLAMA_PORT}` |

## Network

Services are assigned static IPs in the `172.19.0.4X` range on `infra_net`.

| Service | IP Address |
| :--- | :--- |
| `ollama` | `172.19.0.40` |
| `open-webui` | `172.19.0.42` |
| `ollama-exporter` | `172.19.0.43` |

## Traefik Configuration

- **Ollama API**: `ollama.${DEFAULT_URL}`
- **Web UI**: `chat.${DEFAULT_URL}`
- **Entrypoints**: `websecure` (TLS enabled)
