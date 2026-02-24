# PostgreSQL HA Cluster

This stack provides a high-availability PostgreSQL cluster managed by **Patroni**, using **ETCD** for consensus and **HAProxy** for load balancing.

## Services

| Service            | Image                                    | Role                        | Resources       |
| :----------------- | :--------------------------------------- | :-------------------------- | :-------------- |
| `postgres-cluster`| `bitnami/postgresql-repmgr:latest` (Ref) | Database Node (Patroni)     | 1 CPU / 2GB RAM |
| `etcd`             | `bitnami/etcd:latest`                    | Consensus / State Store     | 0.5 CPU / 512MB |
| `haproxy`          | `haproxy:latest`                         | SQL Load Balancer (R/W/RO)  | 0.2 CPU / 256MB |

## Networking

| Service    | Port (Int) | Purpose                       |
| :--------- | :--------- | :---------------------------- |
| `haproxy`  | `5432`     | Read/Write endpoint (Master)  |
| `haproxy`  | `5433`     | Read-Only endpoint (Slaves)   |
| `etcd`     | `2379`     | Client communication          |

## Persistence

- **Data**: `/bitnami/postgresql` (mounted to `pg-data` volumes).
- **Backups**: Automated via Barman or simple dump scripts (Check `operations/`).

## Configuration

### Key Variables

| Variable             | Description               | Value                     |
| :------------------- | :------------------------ | :------------------------ |
| `POSTGRES_PASSWORD`  | Admin Password            | `${POSTGRES_PASSWORD}`    |
| `PATRONI_SCOPE`      | Cluster Name              | `hy-home-db`              |
| `PATRONI_ETCD_HOSTS` | Consensus Cluster         | `etcd:2379`               |

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
