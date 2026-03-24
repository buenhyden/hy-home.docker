---
layer: infra
---

# Data Tier Guides (04-data)

Databases (PostgreSQL, Valkey), object storage (MinIO), and search (OpenSearch).

- [Procedural & Lifecycle Guide](./postgresql-operations.md): General data lifecycle and maintenance.
- [System & Service Context](./minio-s3-guide.md): Data storage architecture.
- [Database Specifics](./postgres-patroni-ha-guide.md): Deep dives into specific data technologies.

## Service Deep Dives

- [PostgreSQL HA with Patroni](./postgres-patroni-ha-guide.md)
- [Valkey Cluster Guide](./valkey-cluster-guide.md)
- [MinIO S3 Integration](./minio-s3-guide.md)
- [OpenSearch Log Analysis](./opensearch-log-search-guide.md)
- [Qdrant Vector DB](./qdrant-vector-db-context.md)

For technical configuration details (Docker Compose, Config files), see [infra/04-data/](../../infra/04-data/README.md).
