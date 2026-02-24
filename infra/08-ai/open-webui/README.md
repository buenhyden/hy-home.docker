# Open WebUI

Open WebUI is an extensible, self-hosted AI interface that operates entirely offline.

## Services

| Service       | Image                                 | Role           | Resources       |
| :------------ | :------------------------------------ | :------------- | :-------------- |
| `open-webui`  | `ghcr.io/open-webui/open-webui:main`  | Chat Interface | 1 CPU / 1GB RAM |

## Dependencies

- **Inference**: Connects to Ollama (`infra/08-ai/ollama`).
- **Vector DB**: Connects to Qdrant (`infra/04-data/qdrant`) for RAG.

## Networking

Exposed via Traefik at `chat.${DEFAULT_URL}`.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and user guides.   |
