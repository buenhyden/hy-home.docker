# Open WebUI

Open WebUI is an extensible, self-hosted AI interface that operates entirely offline.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `open-webui` | `open-webui:v0.8.5-cuda`| ChatGPT-like UI | 1.0 CPU / 1GB RAM |

## Networking

- **Internal DNS**: `open-webui:8080` (within `infra_net`)
- **External URL**: `https://chat.${DEFAULT_URL}` (via Traefik)

## Dependencies

- **Ollama**: `http://ollama:${OLLAMA_PORT}`
- **Qdrant**: `http://qdrant:${QDRANT_PORT}` (Used for RAG).

## Persistence

- **Data**: `ollama-webui` volume mapped to `/app/backend/data`.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and user guides.   |
