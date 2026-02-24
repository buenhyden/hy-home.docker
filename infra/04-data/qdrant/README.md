# Qdrant Vector Database

Qdrant is a high-performance vector search engine designed for RAG (Retrieval-Augmented Generation) applications.

## Services

| Service  | Image                     | Role            | Resources       |
| :------- | :------------------------ | :-------------- | :-------------- |
| `qdrant` | `qdrant/qdrant:v1.12.1`   | Vector Search   | 0.5 CPU / 2GB RAM |

## Networking

| Endpoint             | Port | Purpose             |
| :------------------- | :--- | :------------------ |
| `vector.${DEFAULT_URL}`| 6333 | REST / Web Console  |
| `qdrant:6334`        | 6334 | gRPC API            |

## Persistence

- **Data**: `/qdrant/storage` (mounted to `qdrant-data` volume).

## Configuration

- **API Key**: Protected via the `QDRANT__SERVICE__API_KEY` environment variable.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and RAG integration docs. |
