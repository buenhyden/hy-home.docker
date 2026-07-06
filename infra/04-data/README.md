# Data Tier (04-data)

> Central repository for databases, object storage, and persistence engines.

## 1. Context & Objective

The `04-data` tier provides a polyglot persistence layer for the `hy-home.docker` ecosystem. It manages all stateful data ranging from transactional SQL to high-velocity time-series and semantic vector data. It is engineered for high availability (HA) and durability, ensuring that platform state is preserved across restarts and failures.

### Target Personas

- **Storage Engineers**: Database performance and reliability.
- **Application Developers**: Selecting the right persistence engine.
- **AI Agents**: Automated backup, migration, and state management.

## 2. Requirements & Constraints

### Infrastructure Requirements

- **Data Path**: All services MUST store data in `${DEFAULT_DATA_DIR}`.
- **Secrets**: Passwords MUST be managed via Docker secrets.
- **Networking**: All data services are isolated within `infra_net`.

### Constraints

- Never perform `DROP` operations in production without manual gate verification.
- Policy changes (WAL levels, max connections) require full cluster re-validation.

## 3. Setup & Installation

### Core Stack Deployment

Deployment is handled via individual `docker-compose.yml` files in subdirectories.

| Category | Technology | Notes |
| :--- | :--- | :--- |
| SQL | PostgreSQL 17 (Spilo) | HA with Patroni/Etcd |
| NoSQL | MongoDB, CouchDB, Cassandra | Polyglot persistence |
| Cache | Valkey 8.0 | 6-node Distributed Clstr |
| Vector | Qdrant v1.12 | AI/RAG Support |
| Graph | Neo4j | Relationship data |
| Search | OpenSearch | Analytics & Dashboard |
| Object | MinIO / SeaweedFS | S3-Compatible |

### Verification

```bash
# Verify PostgreSQL HA status
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list

# Verify Valkey cluster
docker exec valkey-node-0 valkey-cli -p 6379 cluster nodes
```

## 4. Usage & Integration

### Service Matrix (Core)

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `pg-router` | PostgreSQL | `data` | 15432 (RW) / 15433 (RO) |
| `valkey-cluster` | Redis | `data` | 6379-6384 |
| `minio` | S3/HTTP | `storage` | 9000 (API) / 9001 (Console) |
| `qdrant` | HTTP/gRPC | `ai` | 6333 / 6334 |
| `opensearch` | HTTP | `analytics` | 9200 |

### Integration Guidelines

1. Read the [Relational Databases Guide](../../docs/05.operations/guides/04-data/relational/README.md) for cluster setup.
2. Follow the [Cache & KV Stores Guide](../../docs/05.operations/guides/04-data/cache-and-kv/README.md) for cache management.

## 5. Maintenance & Safety

### Health & Monitoring

- Check [Operations Policy](../../docs/05.operations/policies/04-data/README.md) for backup standards.
- Consult the [Data Runbook](../../docs/05.operations/runbooks/04-data/README.md) for recovery.

### Safety Protocols

1. Use the `pg-router` entrypoint for all database connections to ensure failover support.
2. Check `available_slots` before adding new nodes to the Valkey cluster.
3. Always verify snapshot integrity before initiating a restore runbook.

---

Copyright (c) 2026. Licensed under the MIT License.

---

## Overview

`infra/04-data`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/04-data/
├── analytics/  # 하위 구성 영역
├── cache-and-kv/  # 하위 구성 영역
├── lake-and-object/  # 하위 구성 영역
├── nosql/  # 하위 구성 영역
├── operational/  # 하위 구성 영역
├── relational/  # 하위 구성 영역
├── specialized/  # 하위 구성 영역
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related Documents

- [infra/README.md](../README.md)
- [docs/05.operations/README.md](../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../docs/05.operations/README.md)
