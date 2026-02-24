# Qdrant Vector Database

Qdrant is a high-performance vector search engine designed for RAG (Retrieval-Augmented Generation) applications.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `qdrant` | `qdrant/qdrant:v1.17` | Vector Database | 1.0 CPU / 1GB RAM |

## Networking

- **Static IP**: `172.19.0.41`
- **URL**: `qdrant.${DEFAULT_URL}` via Traefik.
- **Internal Port**: `6333` (HTTP API).

## Persistence

- **Data**: `qdrant-data` volume mapped to `${DEFAULT_DATA_DIR}/qdrant/data`.

## Configuration

- **API Key**: Protected via the `QDRANT__SERVICE__API_KEY` environment variable.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and RAG integration docs. |
