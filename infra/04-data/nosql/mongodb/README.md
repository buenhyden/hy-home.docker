# MongoDB infrastructure

MongoDB NoSQL Infrastructure for the `hy-home.docker` ecosystem.

## Audience

-   **System Architects**: For understanding the data persistence layer.
-   **DevOps/SRE**: For cluster lifecycle management and scaling.
-   **Developers**: For connection string patterns and data modeling.

## Scope

-   **Primary/Secondary/Arbiter Replica Set**: Core persistence cluster.
-   **Mongo Express**: Administrative GUI.
-   **MongoDB Exporter**: Performance metrics for Prometheus.
-   **Key Generator**: Automated internal authentication management.

## Tech Stack

| Component | Technology | Version | Description |
| :--- | :--- | :--- | :--- |
| Database | MongoDB | 8.0-rc | Core NoSQL engine |
| Management | Mongo Express | 1.0.0 | Web-based GUI |
| Monitoring | MongoDB Exporter | 0.40 | Prometheus metrics |
| Security | SCRAM-SHA-256 | Default | Standard internal auth |

## How to Work in This Area

### Available Scripts

| Script | description |
| :--- | :--- |
| `docker-compose up -d` | Start the full MongoDB stack |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs -f` | Follow service logs |
| `docker exec -it mongodb-rep1 mongosh -u root -p <password>` | Access MongoDB shell |

### Common Operations

```bash
# Verify Replica Set Status
docker exec -it mongodb-rep1 mongosh --eval "rs.status()"

# Check Arbiter Connectivity
docker exec -it mongodb-arbiter mongosh --eval "db.hello()"
```

## Related Documents

### Guides

-   [MongoDB Guide](../../../../docs/07.guides/04-data/nosql/mongodb.md): System architecture and usage guide.

### Operations

-   [MongoDB Operations](../../../../docs/08.operations/04-data/nosql/mongodb.md): Maintenance policies and backup standards.

### Runbooks

-   [MongoDB Runbook](../../../../docs/09.runbooks/04-data/nosql/mongodb.md): Recovery procedures and troubleshooting.

## Deployment Details

### Networking

-   **Mongo Express**: Accessible via `mongo-express.local.hy-home.tech` (Auth: `admin:mongodb`).
-   **Internal Communication**: Uses a dedicated `mongodb.key` file for replica set authentication.

### Storage

-   Persistent data is stored in Docker volumes: `mongodb_data1`, `mongodb_data2`.
-   Arbiter node uses `mongodb_arbiter_data`.

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
