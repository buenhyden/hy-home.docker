<!-- [ID:04-data:cassandra] -->
# Apache Cassandra

> Distributed wide-column NoSQL database for high-throughput workloads.

## 1. Context & Objective

Apache Cassandra is a highly available, linearly scalable NoSQL database designed for large-scale data sets and fast write performance. In `hy-home.docker`, it serves as the storage layer for time-series data and real-time processing requirements that demand zero downtime.

## 2. Requirements & Constraints

* **Resources**: Uses `template-stateful-high` for dedicated high-performance resources.
* **Security**: Requires `cassandra_password` Docker secret for authentication.
* **Storage**: Persistent data is stored in `${DEFAULT_DATA_DIR}/cassandra/node1`.
* **Network**: Runs on `infra_net` to isolate data traffic.

## 3. Setup & Installation

The deployment consists of a Cassandra 5.0 node and a JMX-based metrics exporter.

```bash
# Deploy Cassandra stack
docker compose up -d
```

| Service | Image | Role |
| :--- | :--- | :--- |
| `cassandra-node1` | `cassandra:5.0.6` | Main Data Node |
| `cassandra-exporter` | `bitnami/cassandra-exporter:2.3.11` | Metrics Collection |

## 4. Usage & Integration

* **Client Port**: `9042` (CQL binary protocol).
* **Metrics Port**: `8080/8081` (Prometheus scraping via exporter).
* **Inter-node Port**: `7000` (Intra-cluster communication).

Integration Example:

```yaml
environment:
  - CASSANDRA_HOST=cassandra-node1
  - CASSANDRA_PORT=9042
```

## 5. Maintenance & Safety

* **Health Checks**: Monitored via `nodetool status`.
* **Operational Tools**: Use `docker exec -it cassandra-node1 nodetool <command>` for snapshots or repairs.
* **Data Integrity**: Ensure `${DEFAULT_DATA_DIR}/cassandra` is included in host backup routines.
* **Security**: Always rotate `cassandra_password` via secrets management if compromised.

---

## Documentation References

* [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
* [Backup Operations](../../../docs/08.operations/04-data/README.md)
* [Disaster Recovery](../../../docs/09.runbooks/04-data/README.md)
