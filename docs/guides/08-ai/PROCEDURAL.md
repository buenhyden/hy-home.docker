---
layer: infra
---
# AI Tier: Maintenance & Procedures

This guide covers routine operations, upgrades, and troubleshooting for the AI stack.

## 1. Daily Operations

### Health Checks

```bash
# Ollama API
curl http://localhost:11434/api/tags

# Open WebUI API
curl http://localhost:8080/health
```

### Model Management

```bash
# List all downloaded models
docker exec ollama ollama list

# Remove a model
docker exec ollama ollama rm <model-name>
```

## 2. Upgrading Images

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
| System context | [CONTEXT.md](CONTEXT.md) |
| Setup and installation | [SETUP.md](SETUP.md) |
| Operational usage | [USAGE.md](USAGE.md) |
| LGTM monitoring setup | [../06-observability/README.md](../06-observability/README.md) |
