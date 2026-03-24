---
layer: infra
---

# Data Tier Usage Guide

**Overview (KR):** 데이터 티어 서비스별 연결 방식(Connection Strings), CLI 도구 사용법 및 UI 관리 엔드포인트 가이드입니다.

## 1. Connection Reference (Internal)

Applications on the same Docker network should use the following endpoints:

| Service | Protocol | Host | Port | Credentials |
| --- | --- | --- | --- | --- |
| **PostgreSQL (Write)** | `postgres` | `pg-router` | `5000` | `${POSTGRES_USER}:${POSTGRES_PASSWORD}`|
| **PostgreSQL (Read)** | `postgres` | `pg-router` | `5001` | Read-only replica access |
| **MinIO (S3)** | `s3` | `minio` | `9000` | `${MINIO_ROOT_USER}:${MINIO_ROOT_PASSWORD}`|
| **Valkey (Cache)** | `redis` | `valkey-node-0..5`| `6379` | Cluster-aware client required |
| **OpenSearch** | `http` | `opensearch` | `9200` | Basic Auth |

## 2. CLI Tooling

### PostgreSQL (psql)
Access the cluster via the router for automatic node selection:
```bash
docker compose exec pg-router psql -h pg-router -p 5000 -U postgres
```

### MinIO (mc)
Setup local alias to interact with the S3 API:
```bash
mc alias set local-minio http://localhost:9000 admin pass123
mc ls local-minio/
```

### Valkey (valkey-cli)
Interact with the cluster (use `-c` for cluster mode):
```bash
docker exec -it valkey-node-0 valkey-cli -c
```

## 3. Web Management UIs

| Service | External URL | Purpose |
| --- | --- | --- |
| **MinIO Console** | `https://minio-console.${DEFAULT_URL}` | Bucket/IAM management |
| **Valkey Insight** | `https://valkey-insight.${DEFAULT_URL}` | Visual cache explorer |
| **OpenSearch Dashboards** | `https://logs.${DEFAULT_URL}` | Log analysis & dev tools |
| **Postgres Stats** | `http://pg-router:8404` | HAProxy cluster status |

## 4. Resource Limitations
By default, the following memory limits are applied to ensure host stability:
- **PostgreSQL**: 2GB (Shared Buffers)
- **OpenSearch**: 4GB (JVM Heap)
- **Valkey**: 1GB (maxmemory)
