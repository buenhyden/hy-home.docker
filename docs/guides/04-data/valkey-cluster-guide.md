---
layer: infra
---
# Valkey In-Memory Storage Cluster Guide

**Overview (KR):** Valkey(인메모리 저장소) 클러스터 모드 설정 및 데이터 샤딩 구성 가이드입니다.

> **Component**: `valkey-cluster`
> **Nodes**: 6 (3 Masters + 3 Replicas)
> **Protocols**: Redis 7.2+ compatible

## 1. Cluster Topology

The cluster is partitioned into 16,384 slots across 3 masters. Replication ensures data availability during node failures.

- **Ports**: `6379` through `6384` (External/Internal mapping)
- **Persistence**: AOF (Append Only File) is enabled by default for durability.

## 2. Operational Health Check

To verify cluster status and slot distribution:

```bash
docker exec -it valkey-node-0 sh -c 'valkey-cli -v cluster nodes'
```

## 3. Client Requirements

Applications connecting to the cluster MUST use a "Cluster-Aware" client library (e.g., `redis-py` with Cluster support or `node-redis` cluster mode). Single-node Redis clients will fail on redirection commands.

## 4. Management Console

Visual management and key searching are available via RedisInsight (branded as Valkey Insight):

- **URL**: `https://valkey-insight.${DEFAULT_URL}`
