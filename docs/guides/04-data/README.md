---
layer: infra
---

# Data Tier Guides (04-data)

**Overview (KR):** 관계형 데이터베이스(PostgreSQL), NoSQL, 인메모리 캐시(Valkey), 오브젝트 스토리지(MinIO) 및 검색 엔진(OpenSearch)을 포함하는 인프라 데이터 계층 가이드입니다.

## Navigation Map

| Marker | Entry Point | Use when |
| :--- | :--- | :--- |
| `[LOAD:CONTEXT]` | [CONTEXT.md](./CONTEXT.md) | Understanding data architecture, topology, and host paths |
| `[LOAD:SETUP]` | [SETUP.md](./SETUP.md) | First boot, cluster initialization, and environment validation |
| `[LOAD:USAGE]` | [USAGE.md](./USAGE.md) | Daily connection strings, CLI tools, and management UIs |
| `[LOAD:PROC]` | [PROCEDURAL.md](./PROCEDURAL.md) | Maintenance, backups, failover recovery, and scaling |

---

## 🛠️ Integrated Service Reference

The following services are documented in the unified guides above:
- **Relational**: PostgreSQL (Patroni HA), SQL Server (Optional)
- **Object Storage**: MinIO (S3 API)
- **In-Memory**: Valkey (Cluster Mode)
- **Search & Analytics**: OpenSearch
- **Vector DB**: Qdrant (AI Memory)
- **Extended**: MongoDB, Cassandra, CouchDB, Neo4j, SeaweedFS, Supabase

For technical configuration details (Docker Compose, Config files), see [infra/04-data/](../../infra/04-data/README.md).
