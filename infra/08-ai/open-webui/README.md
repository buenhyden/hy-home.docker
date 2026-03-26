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
- Vector persistence: Managed in [qdrant](../../04-data/qdrant/README.md).

## Structure

```text
open-webui/
├── docker-compose.yml  # Svelte-based interface & RAG backend
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Open WebUI Interface & RAG Guide](../../../docs/07.guides/08-ai/open-webui.md).
2. Access the UI at `https://chat.${DEFAULT_URL}` with SSO.
3. Verify connection to Ollama and Qdrant before document indexing.

## Related References

- [Ollama Implementation](../ollama/README.md)
- [Qdrant Implementation](../../04-data/qdrant/README.md)
- [Open WebUI System Guide](../../../docs/07.guides/08-ai/open-webui.md)
- [Open WebUI Operations Policy](../../../docs/08.operations/08-ai/open-webui.md)
- [Open WebUI Runbook](../../../docs/09.runbooks/08-ai/open-webui.md)

---

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `OLLAMA_BASE_URL` | Yes | Endpoint for Ollama API. |
| `VECTOR_DB_URL` | Yes | Endpoint for Qdrant vector store. |
| `RAG_EMBEDDING_MODEL` | Yes | Model used for document indexing. |

## Change Impact

- Changes to `docker-compose.yml` may affect SSO authentication flows.
- Updating `RAG_EMBEDDING_MODEL` requires re-indexing of existing documents.

---

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. 이 README를 먼저 읽는다.
2. Open WebUI stores chat history and RAG metadata in a local SQLite DB mapped to `${DEFAULT_AI_MODEL_DIR}/open-webui`.
3. RAG indexing performance depends on the `qwen3-embedding` model speed in Ollama.
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
