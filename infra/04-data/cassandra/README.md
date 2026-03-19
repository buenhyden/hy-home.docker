# Apache Cassandra

Apache Cassandra is a distributed wide-column NoSQL database optimized for write-heavy workloads and high-throughput key-value access.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `cassandra-node1` | `bitnami/cassandra:4` | Database node | 1.0 CPU / 2GB RAM |
| `cassandra-exporter` | `bitnami/cassandra-exporter` | Prometheus metrics | 256MB RAM |

## Networking

- **Internal DNS**: `cassandra-node1:9042` (CQL, within `infra_net`)
- **Exporter**: `${CASSANDRA_EXPORTER_PORT}` (host-mapped, Prometheus scrape target)
- **Note**: The Cassandra host port is commented out by default. Access is internal-only.

## Persistence

- **Data**: `cassandra-node1-volume` → `/bitnami/cassandra`
- **Exporter Config**: `cassandra-exporter-volume`

## Configuration

| Variable / Secret | Description |
| :--- | :--- |
| `CASSANDRA_USERNAME` | CQL client username |
| `cassandra_password` | Secret at `secrets/db/cassandra/cassandra_password.txt` |
| `CASSANDRA_EXPORTER_PORT` | Prometheus exporter port |

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Single-node Cassandra + exporter stack. |
| `README.md` | Service overview and access notes. |

## Documentation References

- **Cassandra Context Guide**: [docs/guides/04-data/cassandra-context.md](../../../docs/guides/04-data/cassandra-context.md)
