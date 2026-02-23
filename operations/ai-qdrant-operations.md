# Qdrant Vector DB Operations Tracking

> This document records operational anomalies, indexing scaling results, and recovery processes specific to the `qdrant` vector database engine used for the RAG platform.

## Golden Rules

- **Memory Consumption**: Qdrant utilizes significant RAM for HNSW algorithms. If OOM Kills occur, document the limits and adjust `infra/04-data/qdrant/docker-compose.yml`.
- **Snapshot Integrity**: Record every instance of snapshot corruption or restoration tests.

## Operations History

### 2026-02-23: Initial Initialization

**Status**: Stable
**Context**: Qdrant integrated into the local AI stack, connecting natively with Open WebUI for knowledge retrieval. Storage paths routed cleanly to `qdrant-data` volume.

---
*End of current logs*
