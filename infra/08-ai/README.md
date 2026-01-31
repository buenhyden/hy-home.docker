# AI (08-ai)

## Overview

Local AI/LLM services. The stack is **optional** and enabled via the `ollama` profile. It provides model inference with **Ollama** and a web UI via **Open WebUI**.

## Services

| Service | Profile | Path | Notes |
| --- | --- | --- | --- |
| Ollama | `ollama` | `./ollama` | LLM inference server |
| Open WebUI | `ollama` | `./open-webui` | Chat UI + RAG orchestration |

## Run

```bash
docker compose --profile ollama up -d ollama open-webui
```

## Notes

- Open WebUI expects Qdrant (`infra/04-data/qdrant`) for vector storage.
- GPU usage requires NVIDIA container tooling on the host.

## File Map

| Path | Description |
| --- | --- |
| `ollama/` | Ollama inference + exporter. |
| `open-webui/` | Open WebUI service. |
| `README.md` | Category overview. |
