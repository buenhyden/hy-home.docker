# Ollama Inference Engine

> Local LLM inference server with NVIDIA GPU acceleration.

## Overview

Ollama is the core inference engine for the platform, providing a simple API to run various open-source LLMs (Llama 3, Mistral, Gemma, etc.). It is optimized for NVIDIA GPUs using the CUDA toolkit.

## Audience

- AI Engineers (Model lifecycle)
- Developers (LLM API consumption)

## Structure

```text
ollama/
├── docker-compose.yml  # Container orchestration for Ollama & Exporter
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Inference Management Guide](../../../docs/07.guides/08-ai/01.llm-inference.md).
2. API Access: `http://ollama:11434/api`.
3. Metrics: `http://ollama-exporter:11435/metrics`.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Inference | Ollama | v0.18.2 |
| Monitoring | Ollama Exporter | v1.0.1 |
| Drivers | NVIDIA CUDA | Host-dependent |

## Testing

```bash
# Test inference API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

## AI Agent Guidance

1. Models are persisted in `/root/.ollama` (mapped to host). Do not delete this volume unless wiping the model cache is intended.
2. Use the `ollama-exporter` to track tokens-per-second and VRAM saturation.
3. Pre-pulling heavy models (70B+) should be done during low-traffic maintenance windows.
