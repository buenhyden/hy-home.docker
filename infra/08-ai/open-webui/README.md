# Open WebUI

> Full-featured web interface for LLM interaction and RAG orchestration.

## Overview

Open WebUI (formerly Ollama WebUI) provides a ChatGPT-like interface for local LLMs. Beyond simple chat, it acts as a RAG (Retrieval-Augmented Generation) orchestrator, integrating with Qdrant for vector document search and Ollama for embedding generation.

## Audience

이 README의 주요 독자:

- End Users (Chat interface)
- AI Engineers (RAG & Prompt Engineering)
- Developers (Service integration)
- Operators (Resource management)
- AI Agents

## Scope

### In Scope

- `docker-compose.yml`: Interface & RAG backend orchestration.
- RAG configuration: Embedding model and Vector DB connectivity.
- Traefik routing and SSO integration labels.

### Out of Scope

- Model weights: Managed in [ollama](../ollama/README.md).
- Vector persistence: Managed in [qdrant](../../04-data/specialized/qdrant/README.md).

## Structure

```text
open-webui/
├── docker-compose.yml  # Svelte-based interface & RAG backend
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Open WebUI service leaf in `08-ai`; services: `open-webui`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-webui/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `OLLAMA_BASE_URL`, `VECTOR_DB_URL`, `RAG_EMBEDDING_ENGINE`, `RAG_EMBEDDING_MODEL`; profiles: `ai` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-webui/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `open-webui:/app/backend/data:rw`, `open-webui` |
| Ports | Not declared |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.open-webui.rule`, `traefik.http.routers.open-webui.entrypoints`, `traefik.http.routers.open-webui.tls`, `traefik.http.services.open-webui.loadbalancer.server.port`, `traefik.http.routers.open-webui.middlewares` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `open-webui` |
| Operations | [Guide](../../../docs/05.operations/guides/08-ai/open-webui.md), [Policy](../../../docs/05.operations/policies/08-ai/open-webui.md), [Runbook](../../../docs/05.operations/runbooks/08-ai/open-webui.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `bash scripts/hardening/check-all-hardening.sh 08-ai`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Read the [Open WebUI Interface & RAG Guide](../../../docs/05.operations/guides/08-ai/open-webui.md).
2. Access the UI at `https://chat.${DEFAULT_URL}` with SSO.
3. Verify connection to Ollama and Qdrant before document indexing.

## Troubleshooting

- Start with `bash scripts/hardening/check-all-hardening.sh 08-ai` to confirm Open WebUI hardening contracts.
- Do not run this service-local compose file as a standalone config check; it depends on root `infra_net` context.
- Check Open WebUI logs and the linked runbook before changing RAG, auth, or model endpoint settings.

## Related Documents

- [Ollama Implementation](../ollama/README.md)
- [Qdrant Implementation](../../04-data/specialized/qdrant/README.md)
- [Open WebUI System Guide](../../../docs/05.operations/guides/08-ai/open-webui.md)
- [Open WebUI Operations Policy](../../../docs/05.operations/policies/08-ai/open-webui.md)
- [Open WebUI Runbook](../../../docs/05.operations/runbooks/08-ai/open-webui.md)

---

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `OLLAMA_BASE_URL` | Yes | Endpoint for Ollama API. |
| `VECTOR_DB_URL` | Yes | Endpoint for Qdrant vector store. |
| `RAG_EMBEDDING_MODEL` | Yes | Model used for document indexing; current compose value is `qwen3-embedding:0.6b`. |

## Change Impact

- Changes to `docker-compose.yml` may affect SSO authentication flows.
- Updating `RAG_EMBEDDING_MODEL` requires re-indexing of existing documents.

---

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. 이 README를 먼저 읽는다.
2. Open WebUI stores chat history and RAG metadata in a local SQLite DB mapped to `${DEFAULT_AI_MODEL_DIR}/open-webui`.
3. RAG indexing performance depends on the `qwen3-embedding:0.6b` model speed in Ollama.
4. Ensure the `VECTOR_DB_URL` correctly points to the Qdrant instance in the `04-data` tier.

### Allowed Outputs

- `docker-compose.yml`: Update service configuration.
- `README.md`: Update documentation links.

### Guardrails

- Do not modify `${DEFAULT_AI_MODEL_DIR}` paths without architectural approval.
- Do not disable SSO middlewares unless explicitly requested for local debugging.

### Validation

- Verify Traefik host rules match `${DEFAULT_URL}`.
- Ensure dependency on `ollama` health is maintained.
