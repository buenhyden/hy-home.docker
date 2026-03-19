---
layer: infra
---
# AI Stack Lifecycle Guide (08-ai)

**Overview (KR):** Ollama와 Open WebUI 스택의 초기화, 모델 관리, 업그레이드, 백업, 장애 대응 절차입니다.

> **Profile**: `ai`
> **Services**: `ollama`, `ollama-exporter`, `open-webui`
> **System context**: [ai-context.md](ai-context.md)

---

## 1. First-run initialization

### Prerequisites

1. Verify `nvidia-container-toolkit` is installed on the host:

   ```bash
   nvidia-smi
   docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
   ```

2. Ensure `.env` defines `DEFAULT_AI_MODEL_DIR` pointing to a directory with sufficient disk space (100 GB+ recommended for multiple models).
3. Ensure `infra/04-data/qdrant` is running before starting Open WebUI if RAG is needed.

### Starting the stack

```bash
# From project root
docker compose --profile ai up -d
```

Services start in this order: `ollama` → (health check passes) → `ollama-exporter` and `open-webui`.

### Pulling the first model

The Ollama container starts empty. Pull a model to make inference available:

```bash
# Interactive — model runs immediately after download
docker exec -it ollama ollama run llama3:8b

# Non-interactive pull only
docker exec ollama ollama pull llama3:8b
```

Check available models:

```bash
docker exec ollama ollama list
```

### Pulling the embedding model for RAG

Open WebUI is configured to use `qwen3-embedding:0.6b` for RAG. Pull it before creating knowledge bases:

```bash
docker exec ollama ollama pull qwen3-embedding:0.6b
```

---

## 2. Daily operations

### Checking service health

```bash
# Ollama API readiness
curl http://localhost:11434/api/tags

# Open WebUI health
curl http://localhost:8080/health

# Exporter metrics sample
curl http://localhost:11435/metrics | head -20
```

### Listing and removing models

```bash
# List all downloaded models
docker exec ollama ollama list

# Remove a model to free disk space
docker exec ollama ollama rm <model-name>
```

### Viewing inference logs

```bash
docker logs ollama --follow
docker logs open-webui --follow
```

---

## 3. Upgrading images

### Ollama

1. Update the `image:` tag in `infra/08-ai/ollama/docker-compose.yml`.
2. Validate: `docker compose -f infra/08-ai/ollama/docker-compose.yml config --quiet`
3. Roll the container: `docker compose --profile ai up -d --no-deps ollama`
4. Confirm health: `docker inspect ollama --format '{{.State.Health.Status}}'`

> [!NOTE]
> Model weights in `ollama-data` persist across upgrades. No re-pull is needed unless the model format changes between major Ollama versions.

### Open WebUI

1. Update the `image:` tag in `infra/08-ai/open-webui/docker-compose.yml`.
2. Validate: `docker compose -f infra/08-ai/open-webui/docker-compose.yml config --quiet`
3. Roll: `docker compose --profile ai up -d --no-deps open-webui`
4. Check the UI at `https://chat.${DEFAULT_URL}` and verify settings are intact.

> [!IMPORTANT]
> Open WebUI stores user accounts, conversation history, and RAG collections in the `open-webui` volume. Always back up before a major version upgrade.

---

## 4. Backup and restore

### Ollama models

Models are stored in `${DEFAULT_AI_MODEL_DIR}/ollama`. Back up the manifests and blobs directories:

```bash
# Backup
tar -czf ollama-models-$(date +%Y%m%d).tar.gz -C "${DEFAULT_AI_MODEL_DIR}" ollama/

# Restore
tar -xzf ollama-models-<date>.tar.gz -C "${DEFAULT_AI_MODEL_DIR}"
```

Alternatively, simply re-pull lost models — `ollama pull` is idempotent.

### Open WebUI data

```bash
# Stop the container first to avoid data corruption
docker compose --profile ai stop open-webui

# Backup
tar -czf open-webui-data-$(date +%Y%m%d).tar.gz -C "${DEFAULT_AI_MODEL_DIR}" open-webui/

# Restore
tar -xzf open-webui-data-<date>.tar.gz -C "${DEFAULT_AI_MODEL_DIR}"

# Restart
docker compose --profile ai up -d open-webui
```

---

## 5. Troubleshooting

### Ollama stuck in unhealthy state

```bash
docker inspect ollama --format '{{json .State.Health}}'
docker logs ollama --tail 50
```

Common causes:

- GPU not detected: check `nvidia-smi` on the host and reinstall `nvidia-container-toolkit` if needed.
- Insufficient memory: reduce model size or increase the memory reservation in the compose file.

### Open WebUI cannot reach Ollama

1. Check Ollama health: `docker inspect ollama --format '{{.State.Health.Status}}'`
2. Verify network connectivity: `docker exec open-webui curl -s http://ollama:11434/api/tags`
3. In Open WebUI, go to **Settings → Connections** and confirm the URL is `http://ollama:11434`.

> [!NOTE]
> `open-webui` will not start until `ollama` passes its health check, due to `depends_on: {ollama: {condition: service_healthy}}`. If the startup is slow, increase `start_period` in the Ollama healthcheck.

### RAG embeddings not working

1. Confirm the embedding model is available: `docker exec ollama ollama list | grep qwen3-embedding`
2. Pull it if missing: `docker exec ollama ollama pull qwen3-embedding:0.6b`
3. Verify Qdrant is running: `docker inspect qdrant --format '{{.State.Health.Status}}'`
4. In Open WebUI, go to **Settings → Documents** and verify **Embedding Model** points to `qwen3-embedding:0.6b`.

### High memory / OOM kills

LLMs require contiguous memory. If the host OOM killer terminates Ollama:

1. Note the model that was running and its parameter count.
2. Switch to a smaller quantized variant (e.g., `q4_0` instead of `q8_0`).
3. If persistent, raise the memory limit in `infra/08-ai/ollama/docker-compose.yml` and document the change.

---

## 6. References

| Document | Link |
| --- | --- |
| System context | [ai-context.md](ai-context.md) |
| Inference & UI guide | [ai-inference-guide.md](ai-inference-guide.md) |
| Qdrant operations log | [ai-qdrant-operations.md](ai-qdrant-operations.md) |
| LGTM monitoring setup | [../06-observability/lgtm-stack-blueprint.md](../06-observability/lgtm-stack-blueprint.md) |
