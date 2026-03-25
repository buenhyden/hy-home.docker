<!-- [ID:04-data:qdrant] -->
# Qdrant Vector Database

> High-performance vector similarity search engine.

## 1. Context (SSoT)

The `qdrant` service provides the vector database layer for AI/ML applications, enabling fast semantic search for high-dimensional embeddings.

- **Status**: Production / AI
- **Role**: RAG Persistence
- **SSoT Documentation**: [docs/07.guides/04-data/03.specialized-dbs.md](../../../docs/07.guides/04-data/03.specialized-dbs.md)

## 2. Structure

```text
qdrant/
├── docker-compose.yml   # Service definition
└── config/              # Engine settings
```

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **qdrant** | Qdrant latest | Vector Search Engine |

## 4. Configuration (Secrets & Env)

- **API Key**: Managed via `QDRANT_API_KEY_FILE` secret.
- **Snapshots**: Automated snapshots enabled via configuration.
- **Memory**: Optimized for high-throughput vector indexing.

## 5. Persistence

- **Data**: `qdrant-data` volume mapped to `${DEFAULT_DATA_DIR}/qdrant`.

## 6. Operational Status

| Port | Protocol | Purpose |
| :--- | :--- | :--- |
| `6333` | HTTP | REST API |
| `6334` | gRPC | High-performance API |

---
Copyright (c) 2026. Licensed under the MIT License.
