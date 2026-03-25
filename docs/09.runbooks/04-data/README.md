# Data Recovery Runbook (04-data)

> Incident Response & Emergency Restoration Procedures (04-data)

## 1. Context & Objective

This runbook provides step-by-step instructions for responding to critical data infrastructure failures in the `hy-home.docker` ecosystem. Our objective is to minimize Downtime (RTO) and Data Loss (RPO) through structured recovery protocols.

- **Primary Engine**: PostgreSQL, Valkey, MongoDB, Cassandra
- **Recovery Level**: Node-level, Cluster-level, and Site-level

## 2. Requirements & Constraints

- **Access**: Requires root/sudo access to the cluster hosts and Docker management.
- **Backups**: Verified daily backups must be available in `${DEFAULT_DATA_DIR}/backups`.
- **Quorum**: Most HA clusters require a majority of nodes to be online for automatic recovery.

## 3. Setup & Initial Triage

Before attempting deep recovery, perform initial triage:

1. **Check Service Status**: `docker compose ps`
2. **Review Logs**: `docker compose logs --tail=100 [service]`
3. **Verify Disk Space**: `df -h`

## 4. Recovery Procedures

### 4.1 PostgreSQL Cluster (Patroni)

**Issue**: No leader elected or split-brain detected.

1. **Status**: `docker exec pg-0 patronictl list`
2. **Manual Failover**:

   ```bash
   docker exec -it pg-0 patronictl failover --candidate pg-1 --force
   ```

3. **Re-initialize Node**: If a node is out of sync:

   ```bash
   docker exec -it pg-2 patronictl reinit [cluster-name] pg-2
   ```

### 4.2 Valkey Cluster Recovery

**Issue**: Cluster slots in "fail" state.

1. **Check Slots**: `docker exec valkey-node-0 valkey-cli --cluster check localhost:6379`
2. **Fix Clusters**:

   ```bash
   docker exec -it valkey-node-0 valkey-cli --cluster fix localhost:6379
   ```

### 4.3 Full Restoration from Backup
For full restoration, refer to the storage-specific sections in the core guides.
**Issue**: Data corruption or accidental deletion.
1. **Stop Services**: `docker compose stop [service]`
2. **Restore Path**: Replace corrupted data in `${DEFAULT_DATA_DIR}/[service]` with the latest verified backup.
3. **Restart**: `docker compose up -d [service]`
4. **Validation**: Check service logs for consistent database state.

## 5. Related Documentation

- [Technical Guides](../../07.guides/04-data/README.md)
- [Operations Policy](../../08.operations/04-data/README.md)

## 6. Maintenance & Safety

- **Vacuuming**: Maintain PostgreSQL performance via periodic `VACUUM ANALYZE`.
- **Scrubbing**: Perform periodic data integrity checks on MinIO and SeaweedFS volumes.
- **Failover Testing**: Conduct quarterly simulated failovers to verify cluster resilience.

---
Copyright (c) 2026. Licensed under the MIT License.
