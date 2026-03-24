---
layer: infra
---
# AI Stack System Context (08-ai)

**Overview (KR):** 08-ai 스택 전체 — Ollama, Open WebUI, Qdrant 연동, 메트릭, 볼륨, 네트워크 구성을 포함한 시스템 컨텍스트입니다.

> **Stack**: `ollama`, `ollama-exporter`, `open-webui`
> **Profile**: `ai`
> **Qdrant dependency**: `infra/04-data/qdrant` (separate stack, same `infra_net`)

## 1. Service overview

| Service | Container | Image | Role |
| --- | --- | --- | --- |
| `ollama` | `ollama` | `ollama/ollama:0.18.2` | LLM inference engine |
| `ollama-exporter` | `ollama-exporter` | `lucabecker42/ollama-exporter:1.0.1` | Prometheus metrics sidecar |
| `open-webui` | `open-webui` | `ghcr.io/open-webui/open-webui:v0.8.5-cuda` | Chat UI and RAG front-end |

## 2. Networking

| Endpoint | URL / Address | Notes |
| --- | --- | --- |
| Ollama API (internal) | `http://ollama:${OLLAMA_PORT:-11434}` | Consumed by Open WebUI and other services on `infra_net` |
| Ollama UI (external) | `https://ollama.${DEFAULT_URL}` | Protected by SSO (`sso-errors@file,sso-auth@file`) |
| Open WebUI (external) | `https://chat.${DEFAULT_URL}` | Protected by SSO |
| Exporter metrics | `http://ollama-exporter:${OLLAMA_EXPORTER_PORT:-11435}/metrics` | Internal only, scraped by Prometheus |

All services attach to the shared `infra_net` bridge network.

## 3. Volumes and bind mounts

| Volume name | Host path | Container path | Contents |
| --- | --- | --- | --- |
| `ollama-data` | `${DEFAULT_AI_MODEL_DIR}/ollama` | `/root/.ollama` | Downloaded model weights |
| `open-webui` | `${DEFAULT_AI_MODEL_DIR}/open-webui` | `/app/backend/data` | WebUI settings, conversation history, user accounts |

> [!IMPORTANT]
> `DEFAULT_AI_MODEL_DIR` must be set in `.env`. Model weights can be tens of gigabytes per model; ensure the target directory has adequate disk space.

## 4. Environment variables

### Ollama

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_PORT` | `11434` | Ollama HTTP API port |
| `OLLAMA_EXPORTER_PORT` | `11435` | Prometheus exporter scrape port |

### Open WebUI

| Variable | Value | Purpose |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://ollama:${OLLAMA_PORT:-11434}` | Ollama API endpoint for inference |
| `VECTOR_DB_URL` | `http://qdrant:${QDRANT_PORT:-6333}` | Qdrant connection for RAG retrieval |
| `RAG_EMBEDDING_ENGINE` | `ollama` | Use Ollama to generate embeddings |
| `RAG_EMBEDDING_MODEL` | `qwen3-embedding:0.6b` | Embedding model pulled from Ollama |
| `OLLAMA_WEBUI_PORT` | `8080` | Open WebUI HTTP port |

## 5. Secrets

The 08-ai stack currently has **no Docker secrets**. All credentials are passed via environment variables or resolved internally through Traefik SSO middleware. If API keys for external providers (OpenAI, Anthropic) are added, introduce them as Docker secrets following the project's secrets-first policy.

## 6. Resource allocation

| Service | CPU | Memory | Notes |
| --- | --- | --- | --- |
| `ollama` | 4.0 (limit) | 8 GB limit / 4 GB reserved | GPU reservation active when NVIDIA toolkit is present |
| `ollama-exporter` | 0.5 (limit) | 256 MB | Lightweight sidecar |
| `open-webui` | 1.0 (limit) | 512 MB | CUDA image; GPU not directly used by WebUI |

## 7. GPU configuration

GPU passthrough is configured via the `deploy.resources.reservations.devices` block in `infra/08-ai/ollama/docker-compose.yml`:

```yaml
devices:
  - driver: nvidia
    count: 1
    capabilities: [gpu]
```

The host must have `nvidia-container-toolkit` installed. Without it, containers start but Ollama falls back to CPU inference, which is an order of magnitude slower for large models.

## 8. Metrics

`ollama-exporter` exposes Prometheus metrics derived from the Ollama `/api/tags` and stats endpoints. Typical scrape target configuration in `infra/06-observability/prometheus/`:

```yaml
- job_name: ollama
  static_configs:
    - targets: ['ollama-exporter:11435']
```

## 9. Qdrant integration

Qdrant runs in `infra/04-data/qdrant/` under the `data` profile. Open WebUI reaches it via `http://qdrant:${QDRANT_PORT:-6333}` on `infra_net`. The embedding model (`qwen3-embedding:0.6b`) must be pulled into Ollama before RAG collections can be created in Open WebUI.

## 10. Security baseline

All services inherit the project's security defaults via `common-optimizations.yml`:

- `security_opt: [no-new-privileges:true]`
- `cap_drop: [ALL]`
- `init: true`
- Traefik SSO middleware on both external-facing routers

## 11. References

| Document | Link |
| --- | --- |
| Inference & UI guide | [ai-inference-guide.md](ai-inference-guide.md) |
| Qdrant operations log | [ai-qdrant-operations.md](ai-qdrant-operations.md) |
| Lifecycle procedures | [ai-lifecycle.md](ai-lifecycle.md) |
| LGTM monitoring context | [../06-observability/lgtm-stack-blueprint.md](../06-observability/lgtm-stack-blueprint.md) |
| Qdrant data-tier context | [../04-data/](../04-data/) |
