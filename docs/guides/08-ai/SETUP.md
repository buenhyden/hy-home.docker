---
layer: infra
---

# AI Tier: Setup & Initialization

This guide covers the initial configuration and prerequisites for Ollama and Open WebUI.

## 1. Prerequisites

### Hardware Requirements
- **GPU**: NVIDIA GPU (Pascal or newer) with at least 8GB VRAM recommended.
- **RAM**: 16GB+ System RAM.
- **Storage**: 100GB+ free space for model weights in `${DEFAULT_AI_MODEL_DIR}`.

### Software Requirements
1. **NVIDIA Container Toolkit**: Must be installed and configured on the host.
   ```bash
   nvidia-smi
   ```
2. **Docker Engine**: 24.x+ with GPU support.

## 2. Environment Configuration

Ensure the following variables are set in your `.env` file:

```bash
DEFAULT_AI_MODEL_DIR=/path/to/ai/data
DEFAULT_URL=yourdomain.com
```

## 3. Profile Activation

The AI tier is **opt-in**.

```bash
# Start the AI stack
COMPOSE_PROFILES=ai docker compose up -d
```

## 4. First-Run Tasks

### Pulling Base Models
Ollama starts without any models. You must pull them manually:

```bash
# Chat model
docker exec ollama ollama pull llama3:8b

# Embedding model (for RAG)
docker exec ollama ollama pull qwen3-embedding:0.6b
```

### Initial UI Setup
1. Access `https://chat.${DEFAULT_URL}`.
2. The first user to register becomes the **Admin**.
3. Go to **Settings -> Connections** and verify the Ollama URL is `http://ollama:11434`.
