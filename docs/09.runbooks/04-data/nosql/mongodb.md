# MongoDB Recovery Runbook

Step-by-step procedures for resolving critical failures in the MongoDB infrastructure.

## Canonical References

-   **Incident Management**: [Global Incident Protocol](../../../00.governance/protocols/incident.md)
-   **Operations Policy**: [MongoDB Operations](./mongodb.md)

## Emergency Contact

-   **Primary**: Data Platform Team (@data-sre)
-   **Secondary**: Infrastructure Lead (@infra-lead)

## Incident Classification

-   **L1 (Information)**: High read latency on secondary.
-   **L2 (Warning)**: Single node failure (Replica set still has quorum).
-   **L3 (Critical)**: Majority loss or Primary unavailable (No quorum).

## Diagnostic Procedures

### 1. Check Replica Set Health

```bash
docker exec -it mongodb-rep1 mongosh -u root -p <password> --eval "rs.status()"
```

**What to look for:**
-   `members[].stateStr`: Look for `(not reachable/maybe down)` or `REMOVED`.
-   `members[].health`: Should be `1` for all nodes.

### 2. Verify KeyFile Synchronization

If nodes cannot communicate, check the key file:
```bash
docker exec mongodb-rep1 ls -l /data/configdb/mongodb.key
```

## Recovery Procedures

### Scenario A: Master Election Failure (No Primary)

1.  Check the Arbiter node: `docker logs mongodb-arbiter`.
2.  If the Arbiter is down, restart it: `docker-compose restart mongodb-arbiter`.
3.  If a Primary is not elected within 30 seconds, manually force a step down:
    ```bash
    rs.stepDown(60)
    ```

### Scenario B: Data Corruption on a Single Node

1.  Stop the corrupted node: `docker-compose stop mongodb-rep2`.
2.  Delete the corrupted volume: `docker volume rm mongodb_data2`.
3.  Restart the node: `docker-compose up -d mongodb-rep2`.
4.  The node will perform an **Initial Sync** from the current Primary.

### Scenario C: Full Cluster Re-initialization

1.  Bring down all services.
2.  Ensure volumes are cleared (if data is sacrificial).
3.  Start data nodes.
4.  Execute `mongo-init` or manual initiation:
    ```javascript
    rs.initiate({
      _id: "MyReplicaSet",
      members: [
        { _id: 0, host: "mongodb-rep1:27017" },
        { _id: 1, host: "mongodb-rep2:27017" },
        { _id: 2, host: "mongodb-arbiter:27017", arbiterOnly: true }
      ]
    })
    ```

## Post-Mortem and Evidence Capture

-   **Diagnostic Logs**: `docker-compose logs > diagnostic_logs_$(date +%s).txt`
-   **Metric Snapshots**: Capture Grafana dashboard screenshots.
-   **Final Status**: Record the output of `rs.conf()`.

## Validation Checklist

-   [ ] Primary node is identified via `db.isMaster().ismaster`.
-   [ ] `mongo-express` management UI is reachable.
-   [ ] `mongodb-exporter` shows all members as healthy.
