# PostgreSQL HA Cluster

This stack provides a high-availability PostgreSQL cluster managed by **Patroni**, using **ETCD** for consensus and **HAProxy** for load balancing.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `pg-0, 1, 2` | `ghcr.io/zalando/spilo-17:4.0-p3` | SQL Nodes (Patroni) | 1 CPU / 2GB RAM ea |
| `etcd-1, 2, 3`| `quay.io/coreos/etcd:v3.6.7` | Consensus (DCS) | 256MB RAM ea |
| `pg-router` | `haproxy:3.3.1` | Load Balancer | 0.5 CPU / 256MB |
| `pg-exporter` | `postgres-exporter:v0.18.1` | Metrics | 0.1 CPU / 128MB |

## Networking

| Service | Port (Int) | Host Port | Purpose |
| :--- | :--- | :--- | :--- |
| `pg-router` | `5432` | `${POSTGRES_WRITE_HOST_PORT}` | R/W Master Traffic |
| `pg-router` | `5433` | `${POSTGRES_READ_HOST_PORT}` | RO Replica Traffic |
| `pg-router` | `${HAPROXY_PORT}` | - | Stats UI (Internal) |
| `etcd-*` | `2379` | - | Client API |

## Persistence

- **DB Data**: `/home/postgres/pgdata` (mounted to `pg0-data`, `pg1-data`, `pg2-data`).
- **Storage**: `${DEFAULT_DATA_DIR}/pg/...` on host.

## Configuration

### Key Variables

| Variable | Description | Value |
| :--- | :--- | :--- |
| `SCOPE` | Patroni Cluster Name | `pg-ha` |
| `POSTGRES_PORT` | DB Internal Port | `5432` |
| `PATRONI_RESTAPI_PORT` | Patroni internal API | `8008` |

## Operations

### Checking Cluster Status

```bash
docker compose exec postgres-cluster patronictl list
```

## File Map

| Path                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `docker-compose.yml` | Patroni + ETCD + HAProxy stack definition.     |
| `config/`            | Custom Patroni and HAProxy configurations.     |
| `README.md`          | HA docs and operational commands.              |

> **Note**: This component's local documentation has been migrated to the global repository standards to enforce Spec-Driven Development boundaries.

Please refer to the following global documentation directories for information regarding this service:

- **Architecture & Topology**: [docs/architecture](../../../docs/architecture)
- **Configuration & Setup Guides**: [docs/guides](../../../docs/guides)
- **Routine Operations**: [operations/](../../../operations)
- **Troubleshooting & Recovery**: [runbooks/](../../../runbooks)
