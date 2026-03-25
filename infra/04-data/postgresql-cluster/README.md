<!-- [ID:04-data:postgresql-cluster] -->
# PostgreSQL HA Cluster

> High-availability PostgreSQL cluster managed by Patroni.

## 1. Context (SSoT)

The `postgresql-cluster` provides a resilient, production-grade SQL backend. It utilizes a leader-follower architecture with automated failover managed by Patroni and ETCD.

- **Status**: HA Enabled / Production
- **SSoT Documentation**: [docs/07.guides/04-data/01.core-dbs.md](../../../docs/07.guides/04-data/01.core-dbs.md)
- **Consensus**: ETCD Cluster (3 nodes)

## 2. Structure

```text
postgresql-cluster/
├── docker-compose.yml   # HA Stack definition
├── config/              # Patroni & HAProxy config
└── init-scripts/        # DB Initialization
```

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **pg-0..2** | Zalando Spilo (PG 17) | SQL Nodes (Patroni) |
| **etcd-1..3** | CoreOS ETCD | Consensus (DCS) |
| **pg-router** | HAProxy | Load Balancer |

## 4. Configuration (Secrets & Env)

- **Secrets**: `POSTGRES_PASSWORD_FILE`, `PATRONI_SUPERUSER_PASSWORD_FILE`.
- **DCS**: Custom ETCD cluster on `infra_net`.
- **Cluster Status**: `docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml list`

## 5. Persistence

- **Volumes**: `pg0-data`, `pg1-data`, `pg2-data`.
- **Path**: `${DEFAULT_DATA_DIR}/pg/...`

## 6. Operational Status

| Purpose | Address | Description |
| :--- | :--- | :--- |
| **R/W Master** | `pg-router:5432` | Primary write endpoint. |
| **Read Only** | `pg-router:5433` | Distributed read replicas. |
| **Stats UI** | `pg-router:1936` | HAProxy dashboard. |

---
Copyright (c) 2026. Licensed under the MIT License.
