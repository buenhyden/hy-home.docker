# MongoDB Operations Policy

Operational standards and maintenance procedures for the MongoDB persistence layer.

## Canonical References

-   **Policy**: [04-data Operations Policy](../../../00.governance/policies/data-ops.md)
-   **System Guide**: [MongoDB Guide](../../07.guides/04-data/nosql/mongodb.md)

## Lifecycle Management

### Bootstrap Sequence

1.  `mongo-key-generator` runs once to ensure `mongodb.key` exists.
2.  Data nodes (`rep1`, `rep2`) and arbiter start.
3.  `mongo-init` executes `rs.initiate()` and creates management users.

### Maintenance Windows

-   **Non-disruptive**: Upgrades can be performed via rolling restarts (Secondary first, then step down Primary).
-   **Disruptive**: Changes to `replicaSet` name or major version upgrades.

## Security Standard

-   **Authentication**: SCRAM-SHA-256 mandatory.
-   **Authorization**: RBAC (Role-Based Access Control) must be enforced.
-   **Network**: MongoDB ports (27017) are NOT exposed to the public internet; access via internal network or jump host only.

## Backup and Recovery

### Backup Strategy (mongodump)

-   **Frequency**: Daily logical backups.
-   **Retention**: 7 days local, 30 days off-site.

```bash
# Example Manual Backup
docker exec mongodb-rep1 mongodump --archive --gzip -u root -p <password> > /backups/mongo_$(date +%F).gz
```

## Performance & Monitoring

### Health Indicators

| Metric | Threshold | Action |
| :--- | :--- | :--- |
| `mongodb_rs_members_state` | != 1 (Primary) or 2 (Secondary) | Investigate election lag |
| `mongodb_op_counters_total` | Spikes > 200% baseline | Check for unindexed queries |
| `mongodb_memory_resident` | > 80% RAM | Scale horizontal or vertical |

## Capacity Planning

-   **Vertical**: Increase memory to fit the working set (indexes + hot data).
-   **Horizontal**: Add more secondary nodes to scale read capacity.

## Audit and Compliance

-   **Logs**: Audit logs are captured at `/var/log/mongodb/audit.log`.
-   **Access Review**: Quarterly review of `mongo-express` users.

## Change Management

-   Configuration changes must be applied via Docker environment variables or custom `mongod.conf`.
-   Always verify `rs.status()` after any infrastructure change.

## Decommissioning

1.  Export final data via `mongodump`.
2.  Remove DNS entries for `mongo-express`.
3.  Purge persistent volumes `mongodb_data*`.
