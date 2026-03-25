# Open WebUI

> Full-featured web interface for LLM interaction and RAG orchestration.

## Overview

Open WebUI (formerly Ollama WebUI) provides a ChatGPT-like interface for local LLMs. Beyond simple chat, it acts as a RAG (Retrieval-Augmented Generation) orchestrator, integrating with Qdrant for vector document search.

## Audience

- End Users (Chat interface)
- AI Engineers (RAG & Prompt Engineering)

## Structure

```text
open-webui/
├── docker-compose.yml  # Svelte-based interface & RAG backend
└── README.md           # This file
```

## How to Work in This Area

1. Read the [RAG Workflow Guide](../../../docs/07.guides/08-ai/02.rag-workflow.md).
2. Access: `https://chat.${DEFAULT_URL}`.
3. Admin Login: Managed via Keycloak/OIDC integration.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Interface | Open WebUI | v0.8.5-cuda |
| Embedding | Ollama (Local) | qwen3-embedding |
| Vector Store | Qdrant | v1.11.x (Remote) |

## AI Agent Guidance

1. Open WebUI stores chat history and RAG collections in a local SQLite DB (mapped to `${DEFAULT_AI_MODEL_DIR}/open-webui`).
2. RAG indexing performance depends on the `qwen3-embedding` model speed in Ollama.
3. Ensure the `VECTOR_DB_URL` correctly points to the Qdrant instance in the `04-data` tier.
