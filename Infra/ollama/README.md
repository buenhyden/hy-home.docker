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

## Traefik Configuration

- **Ollama API**: `ollama.${DEFAULT_URL}`
- **Web UI**: `chat.${DEFAULT_URL}`
- **Entrypoints**: `websecure` (TLS enabled)
