# PostgreSQL HA Cluster

## Overview

A robust **High Availability (HA) PostgreSQL Cluster** designed for mission-critical data. It utilizes **Patroni** for automated failover, **etcd** as the distributed consensus store, and **HAProxy** for intelligent read/write routing.

```mermaid
graph TB
    subgraph "Clients"
        App[Application]
        Init[Init Service]
    end
    
    subgraph "Routing Layer"
        LB[HAProxy<br/>Write: 5432 / Read: 5433]
    end
    
    subgraph "Data Layer (Patroni Cluster)"
        P1[PG-0<br/>(Leader?)]
        P2[PG-1<br/>(Replica?)]
        P3[PG-2<br/>(Replica?)]
    end
    
    subgraph "Consensus (DCS)"
        E1[etcd-1]
        E2[etcd-2]
        E3[etcd-3]
    end

    App --> LB
    Init --> LB
    
    LB -->|Write| P1
    LB -->|Read Round-Robin| P2
    LB -->|Read Round-Robin| P3
    
    P1 <--> E1
    P1 <--> E2
    P1 <--> E3
    P2 <--> E1
    P3 <--> E1
    
    P1 -.->|Replication| P2
    P1 -.->|Replication| P3
```

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `etcd-{1,2,3}` | `coreos/etcd:v3.6.7` | DCS (Distributed Config Store) | 256MB RAM |
| `pg-{0,1,2}` | `zalando/spilo-17:4.0-p3` | PostgreSQL 17 + Patroni Agent | 1 CPU / 2GB |
| `pg-router` | `haproxy:3.3.1` | SQL Traffic Router | 0.5 CPU / 256MB |
| `pg-cluster-init` | `postgres:17-alpine` | Schema Initializer (One-off) | 0.5 CPU / 128MB |
| `pg-*-exporter` | `postgres-exporter` | Metrics Sidecar | 0.1 CPU / 128MB |

## Networking

Services run on `infra_net` with static IPs (`172.19.0.5X`).

| Service | Static IP | Port (Internal) | Host Port | Traefik Domain |
| :--- | :--- | :--- | :--- | :--- |
| `etcd-1` | `172.19.0.50` | `2379` | `${ETCD_CLIENT_PORT}` | - |
| `etcd-2` | `172.19.0.51` | `2379` | `${ETCD_CLIENT_PORT}` | - |
| `etcd-3` | `172.19.0.52` | `2379` | `${ETCD_CLIENT_PORT}` | - |
| `pg-0` | `172.19.0.53` | `5432` | `${POSTGRES_PORT}` | - |
| `pg-1` | `172.19.0.54` | `5432` | `${POSTGRES_PORT}` | - |
| `pg-2` | `172.19.0.55` | `5432` | `${POSTGRES_PORT}` | - |
| `pg-router` | `172.19.0.56` | W: `5432`, R: `5433` | W: `${POSTGRES_WRITE_HOST_PORT}`<br>R: `${POSTGRES_READ_HOST_PORT}` | `pg-haproxy.${DEFAULT_URL}` |

## Persistence

Data is isolated in named volumes for each node.

| Volume | Description |
| :--- | :--- |
| `etcd1-data`, `etcd2...` | Consensus state data |
| `pg0-data`, `pg1...` | PostgreSQL data files (mapped to `/home/postgres/pgdata`) |
| `haproxy.cfg` | Configuration bind mount |

## Configuration

### Patroni & Spilo

The `zalando/spilo` image encapsulates Postgres and Patroni. Key configuration via environment variables:

- `SCOPE`: Cluster name (`pg-ha`). All nodes with the same scope form a cluster.
- `ETCD3_HOSTS`: Connection string for the DCS.
- `PATRONI_NAME`: Unique identifier for the instance.

### Initialization (`pg-cluster-init`)

This container creates users and databases *after* the cluster is healthy.

- **Wait Logic**: Polls `pg_router` until it accepts connections.
- **Execution**: Runs `./init-scripts/init_users_dbs.sql`.
- **Target**: Connects to the **Cluster/Router**, not an individual node, ensuring metadata is replicated.

## Traefik Integration

The HAProxy Stats dashboard is exposed via Traefik.

- **URL**: `https://pg-haproxy.${DEFAULT_URL}`
- **Metrics**: Allows verifying which node is currently the Leader.

## Usage

### Connecting to the Cluster

Always connect via the **Router** to respect Leader/Replica roles.

**Write Operations (Leader):**

```bash
psql -h localhost -p ${POSTGRES_WRITE_HOST_PORT} -U postgres
```

**Read Operations (Replica):**

```bash
psql -h localhost -p ${POSTGRES_READ_HOST_PORT} -U postgres
```

### Checking Cluster Health

You can check the Patroni API on any node:

```bash
curl http://localhost:8008/cluster
```

## Troubleshooting

### Split Brain / No Leader

If `etcd` quorum is lost (e.g., 2 nodes down), the cluster becomes Read-Only.

- Check etcd health: `docker compose logs etcd-1`
- Ensure at least 2 etcd nodes are healthy.

### Node Flapping

If a PG node keeps restarting:

1. Check logs: `docker compose logs pg-0`
2. Look for "WalSender" or "Replication" errors.
3. Verify `etcd` connectivity from the PG container.

## File Map

| Path | Description |
| --- | --- |
| `docker-compose.yml` | Patroni + etcd + HAProxy cluster definition. |
| `.env.postgres` | Local env values for cluster bootstrap. |
| `.env.postgres.example` | Template env values. |
| `config/haproxy.cfg` | HAProxy routing for write/read split and stats. |
| `config/haproxy.cfg.example` | Template HAProxy config. |
| `init-scripts/init_users_dbs.sql` | Initial DB/user bootstrap (runs once). |
| `init-scripts/init_users_dbs.sql.example` | Template bootstrap SQL. |
| `README.md` | HA cluster usage and troubleshooting. |
