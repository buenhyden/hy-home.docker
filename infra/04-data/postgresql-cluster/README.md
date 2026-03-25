<!-- [ID:04-data:postgresql-cluster] -->
# PostgreSQL HA Cluster

> High-availability PostgreSQL cluster managed by Patroni.

## Overview (KR)

이 스택은 Patroni에 의해 관리되는 고가용성 PostgreSQL 클러스터를 제공합니다. 데이터 합의를 위해 ETCD를 사용하며, 트래픽 부하 분산을 위해 HAProxy를 사용합니다.

## Overview

The `postgresql-cluster` provides a resilient, production-grade SQL backend for the `hy-home.docker` ecosystem. It utilizes a leader-follower architecture with automated failover and health monitoring, ensuring 24/7 data availability for critical applications.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **pg-0, 1, 2** | Zalando Spilo (PG 17) | SQL Nodes (Patroni) |
| **etcd-1, 2, 3** | CoreOS ETCD | Consensus (DCS) |
| **pg-router** | HAProxy | Load Balancer |

## Networking

| Purpose | Address | Description |
| :--- | :--- | :--- |
| **R/W Master** | `pg-router:5432` | Primary write and consistent read traffic. |
| **Read Only** | `pg-router:5433` | Distributed read traffic across replicas. |
| **Stats UI** | `pg-router:1936` | HAProxy monitoring dashboard. |

## Persistence

- **DB Data**: Mounted to `pg0-data`, `pg1-data`, `pg2-data` volumes.
- **Storage Path**: `${DEFAULT_DATA_DIR}/pg/...` on the host system.

## Operations

### Checking Cluster Status

```bash
docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml list
```

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | HA stack definition. |
| `config/` | Patroni and HAProxy configurations. |
| `init-scripts/` | Database initialization scripts. |

---

## Documentation References

- [Core DB Guide](../../../docs/07.guides/04-data/01.core-dbs.md)
- [Recovery Runbook](../../../docs/09.runbooks/04-data/README.md)
