---
layer: infra
---
# Qdrant Vector DB Operations Tracking

**Overview (KR):** RAG 플랫폼에 사용되는 Qdrant 벡터 데이터베이스의 인덱싱 및 운영 최적화 기록입니다.

> This document records operational anomalies, indexing scaling results, and recovery processes specific to the `qdrant` vector database engine used for the RAG platform.

## Golden Rules

> [!NOTE]
> Qdrant is deployed in `infra/04-data/qdrant/`, not in `infra/08-ai/`. Open WebUI connects to it via the internal `qdrant:${QDRANT_PORT}` DNS name.

- **Memory consumption**: Qdrant uses significant RAM for HNSW index algorithms. If OOM kills occur, document the observed limits and adjust resource limits in `infra/04-data/qdrant/docker-compose.yml`.
- **Snapshot integrity**: Record every instance of snapshot corruption or restoration tests.

## Operations History

### 2026-02-23: Initial Initialization

**Status**: Stable
**Context**: Qdrant integrated into the local AI stack, connecting natively with Open WebUI for knowledge retrieval. Storage paths routed cleanly to `qdrant-data` volume.

---
*End of current logs*
