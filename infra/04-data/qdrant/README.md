<!-- [ID:04-data:qdrant] -->
# Qdrant Vector Database

> High-performance vector similarity search engine.

## Overview (KR)

Qdrant는 고성능 벡터 유사도 검색 엔진입니다. AI 기반 애플리케이션의 벡터 임베딩 저장 및 검색에 사용됩니다.

## Overview

The `qdrant` service provides the vector database layer for AI and ML applications in `hy-home.docker`. It enables fast nearest-neighbor search for high-dimensional embeddings.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **qdrant** | Qdrant latest | Vector Engine |

## Networking

| Port | Protocol | Purpose |
| :--- | :--- | :--- |
| `6333` | HTTP | REST API |
| `6334` | gRPC | High-performance API |

## Persistence

- **Data Volume**: `qdrant-data` volume mounted to `/qdrant/storage`.
- **Storage Path**: `${DEFAULT_DATA_DIR}/qdrant` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Service definition. |
| `config/` | Engine settings. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Recovery Runbook](../../../docs/09.runbooks/04-data/README.md)
