# Qdrant Vector Database

Qdrant is a high-performance vector search engine designed for RAG (Retrieval-Augmented Generation) applications.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `qdrant` | `qdrant/qdrant:v1.17` | Vector Database | 1.0 CPU / 1GB RAM |

## Networking

- **Internal DNS**: `qdrant:${QDRANT_PORT:-6333}` (within `infra_net`)
- **External URL**: `https://qdrant.${DEFAULT_URL}` (via Traefik)

## Persistence

- **Data**: `qdrant-data` volume mapped to `${DEFAULT_DATA_DIR}/qdrant/data`.

## Configuration

- **Auth**: Not enabled in the current Compose definition.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and RAG integration docs. |
