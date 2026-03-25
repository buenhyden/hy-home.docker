# Open WebUI

Enterprise-grade chat interface and RAG orchestration layer.

## 0. Context & SSoT

- **Parent Tier**: [infra/08-ai/](../README.md)
- **Public URL**: `chat.${DEFAULT_URL}`
- **Backend API**: `open-webui:8080`

## 1. Structure

| Component | Image | Role |
| :--- | :--- | :--- |
| `open-webui` | `ghcr.io/open-webui/open-webui:v0.8.5-cuda` | Web application & Backend |

## 2. Tech Stack

- **Frontend**: SvelteKit
- **Backend**: Python (FastAPI)
- **Vector DB**: Qdrant (RAG Storage)
- **Inference**: Ollama (Primary Engine)

## 3. Configuration

- `OLLAMA_BASE_URL`: `http://ollama:11434`
- `VECTOR_DB_URL`: `http://qdrant:6333`
- `RAG_EMBEDDING_MODEL`: `qwen3-embedding:0.6b`

## 4. Persistence

- **User Data**: `${DEFAULT_AI_MODEL_DIR}/open-webui`
- **Mount Point**: `/app/backend/data` (RW)

## 5. Operational Status

> [!NOTE]
> Initial startup may be slow while the system prepares the internal SQLite database and RAG indices.

> [!IMPORTANT]
> Ensure Ollama is healthy and models are pulled before attempting to use the UI.
