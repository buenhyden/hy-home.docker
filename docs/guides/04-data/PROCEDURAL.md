---
layer: infra
---

# Data Tier Procedural Guide

**Overview (KR):** 데이터 티어 서비스별 정기 점검, 백업 및 복구, 장애 조치(Failover) 및 스케일링 절차 가이드입니다.

## 1. Maintenance & Health Checks

### PostgreSQL (Patroni)
Check cluster health and leader status:
```bash
docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml list
```

### MinIO (mc admin)
Check storage utilization and disk health:
```bash
mc admin info local-minio
```

### Valkey Cluster
Verify slot distribution and node connectivity:
```bash
docker exec -it valkey-node-0 sh -c 'valkey-cli --cluster info'
```

## 2. Backup & Restore Operations

### PostgreSQL (Logical Backup)
```bash
## Backup
docker exec pg-router pg_dumpall -h pg-router -p 5000 -U postgres > full_backup_$(date +%F).sql

## Restore
cat full_backup.sql | docker exec -i pg-router psql -h pg-router -p 5000 -U postgres
```

### MinIO (S3 Mirroring)
To sync data to a secondary site or local disk:
```bash
mc mirror local-minio/my-bucket /path/to/backup/
```

### Qdrant (Snapshotting)
Qdrant supports hot snapshots via API:
```bash
curl -X POST "http://localhost:6333/collections/{collection_name}/snapshots"
```

## 3. Failover & Recovery

### PostgreSQL (Graceful Switchover)
To perform a leader rotation for maintenance without downtime:
```bash
docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml switchover
```

### Valkey Cluster (Node Replacement)
If a master node fails, it should failover to its replica automatically. To resync a new node:
```bash
docker exec -it valkey-node-new valkey-cli --cluster add-node valkey-node-new:6379 valkey-node-0:6379 --cluster-slave
```

## 4. Scaling
- **Vertical**: Adjust `deploy.resources.limits.memory` in `docker-compose.yml`.
- **Horizontal**: PostgreSQL and Valkey are pre-configured for a fixed number of nodes. To scale out, update the number of replicas and perform a cluster rebalance.
