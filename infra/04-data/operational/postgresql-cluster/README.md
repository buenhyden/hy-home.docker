# postgresql-cluster

> [!NOTE]
> **Base Structure**: Relational Database Cluster (HA)
> **Tier**: 04-data (Operational)
> **Engine**: PostgreSQL 17 (Spilo)

---

## Overview (개요)

`postgresql-cluster`는 Patroni와 etcd를 사용하여 고가용성(High Availability)을 보장하는 관계형 데이타베이스 클러스터이다. 3개 노드(Leader/Replica)와 DCS(Distributed Configuration Store)용 etcd 클러스터로 구성되어 있으며, HAProxy(`pg-router`)를 통해 읽기/쓰기 부하 분산 및 자동 페일오버를 지원한다.

---

## Implementation Snippet

### Architecture Info
- **Type**: High-Availability Cluster (Patroni)
- **Consensus**: etcd (3-node Quorum)
- **Routing**: HAProxy (Read/Write Splitting)
- **Storage**: Bind mounts to `${DEFAULT_DATA_DIR}/pg` and `/etcd`

### System Links
- **Guide**: [docs/07.guides/04-data/operational/postgresql-cluster.md](../../../../docs/07.guides/04-data/operational/postgresql-cluster.md)
- **Operations**: [docs/08.operations/04-data/operational/postgresql-cluster.md](../../../../docs/08.operations/04-data/operational/postgresql-cluster.md)
- **Runbook**: [docs/09.runbooks/04-data/operational/postgresql-cluster.md](../../../../docs/09.runbooks/04-data/operational/postgresql-cluster.md)

### Key Configuration
- `SCOPE`: `pg-ha`
- `pg-router`: Port `15432` (Master/Write), `15433` (Replica/Read)
- `postgres-exporter`: Node-level metrics on port `9187`

---

## Quick Start

```bash
# Start cluster
docker compose up -d

# Check cluster status
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list
```

---

## Canonical References
- [ARD: 0004-data-architecture.md](../../../../docs/02.ard/0004-data-architecture.md)
- [Spec: 04-data/spec.md](../../../../docs/04.specs/04-data/spec.md)

---

Copyright (c) 2026. Licensed under the MIT License.

