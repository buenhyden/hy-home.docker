# MongoDB Replica Set

> Document-based NoSQL database for unstructured data.

## 1. Context & Objective

The `mongodb` stack provides a resilient document storage layer for the `hy-home.docker` ecosystem. It is optimized for high-volume unstructured data and features a 3-node replica set for automated failover and high availability.

### Key Components

- **Primary/Secondary Nodes**: Data persistence and replication.
- **Arbiter**: Voting node for leader election (no data storage).
- **Mongo Express**: Management Web UI.

## 2. Requirements & Constraints

- **Storage**: Requires persistent volumes for each data node.
- **Secrets**: Root credentials MUST be managed via the `mongodb_root_password` secret.
- **Network**: Standard port `27017` must be reachable within the `infra_net`.

## 3. Setup & Installation

### Deployment

```bash
# Start the replica set
docker compose up -d
```

### Verification

```bash
# Check cluster status
docker exec -it mongodb-rep1 mongosh -u admin -p <password> --eval "rs.status()"
```

## 4. Usage & Integration

### Operational Endpoints

- **DB Port**: `27017`
- **Management UI**: `mongo-express.${DEFAULT_URL}` (Port `8081`)
- **Metrics**: `mongodb-exporter:9216`

### Integration Pointers

- Consult the [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md) for connection examples.
- Use the provided exporter for Prometheus-based monitoring.

## 5. Maintenance & Safety

### Backup & Recovery

1. Automated backups are governed by the [Data Persistence Policy](../../../docs/08.operations/04-data/README.md).
2. Use the [Recovery Runbook](../../../docs/09.runbooks/04-data/README.md) for replica set re-initialization.

### Safety Warnings

- Never manually delete `configdb/` files as they contain the replica set's security keys.
- Ensure the Arbiter is always running to maintain quorum during node failures.

---

Copyright (c) 2026. Licensed under the MIT License.
