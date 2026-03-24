---
layer: infra
---

# Data Tier Setup Guide

**Overview (KR):** 데이터 티어의 서비스별 초기화, 클러스터링 구성 및 환경 변수 검증 가이드입니다.

## 1. Prerequisites

Before starting the data tier, ensure secrets are initialized:

```bash
bash scripts/bootstrap-secrets.sh
```

Verification of Docker Compose profiles:
```bash
docker compose config | grep -E "pg-cluster|minio|valkey"
```

## 2. PostgreSQL HA (Patroni/Etcd)

The PostgreSQL cluster requires a 3-node etcd quorum for leadership election.

### Bootstrap Procedure
1.  **Bring up Etcd & PG Nodes**:
    ```bash
    docker compose up -d etcd-1 etcd-2 etcd-3 pg-0 pg-1 pg-2 pg-router
    ```
2.  **Verify Cluster Initiation**:
    Check the logs of the init container which handles initial user/DB creation:
    ```bash
    docker logs pg-cluster-init
    ```
3.  **Check Cluster Status**:
    ```bash
    docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml list
    ```

## 3. Object Storage (MinIO)

MinIO uses an automated tool (`mc`) to provision mandatory buckets on first boot.

### Managed Buckets Configuration
The `minio-create-buckets` container automatically creates:
- `loki-bucket` (Logs)
- `tempo-bucket` (Traces)
- `cdn-assets` (Public)

### Verification
```bash
docker logs minio-create-buckets
```

## 4. In-Memory Cache (Valkey Cluster)

Valkey requires an initial cluster meet command if not using a pre-configured image.

### Initialization
```bash
docker exec -it valkey-node-0 sh -c 'valkey-cli --cluster create \
  valkey-node-0:6379 valkey-node-1:6379 valkey-node-2:6379 \
  valkey-node-3:6379 valkey-node-4:6379 valkey-node-5:6379 \
  --cluster-replicas 1'
```

## 5. Search Engine (OpenSearch)

OpenSearch requires specific host-level `vm.max_map_count` settings:

```bash
sudo sysctl -w vm.max_map_count=262144
```

Add this to `/etc/sysctl.conf` for persistence.
