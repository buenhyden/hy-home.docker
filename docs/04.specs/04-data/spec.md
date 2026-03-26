# Technical Spec: Data Tier (04-data)

## Overview (KR)

본 문서는 `04-data` 티어의 기술 구현 명세서이다. PostgreSQL Patroni 클러스터, Valkey 분산 클러스터, MinIO 오브젝트 스토리지의 구체적인 설정값, 포트 매핑, 볼륨 구조 및 보안 주입 방식을 기술한다.

## 1. Relational Database: PostgreSQL HA

### 1.1 Cluster Components

- **Primary Image**: `ghcr.io/zalando/spilo-17:4.0-p3`
- **Orchestration**: Patroni v4.0
- **Consensus**: Etcd v3.6.7 (3-node)
- **Routing**: HAProxy v3.3.1 (pg-router)

### 1.2 Configuration Details

- **Patroni Listener**: `0.0.0.0:8008`
- **Postgres Listener**: `0.0.0.0:5432`
- **Router Entrypoints**:
  - **Write (Primary)**: 15432
  - **Read (Replicas)**: 15433
- **Storage**: `${DEFAULT_DATA_DIR}/pg/pg[0-2]-data`

## 2. Distributed Cache: Valkey Cluster

### 2.1 Cluster Topology

- **Image**: `valkey/valkey:9.0.2-alpine`
- **Structure**: 6-node distributed cluster (3 Master, 3 Slave).
- **Communication**: Port 6379-6384 (Client) / 16379-16384 (Bus).

### 2.2 Initialization

- `valkey-cluster-init` 컨테이너가 부팅 시 `valkey-cli --cluster create` 명령을 통해 샤딩 구성을 수행함.

## 3. Object Storage: MinIO

### 3.1 Server Config

- **Console Port**: 9001
- **API Port**: 9000
- **Buckets**: `tempo-bucket`, `loki-bucket`, `cdn-bucket`, `doc-intel-assets`.

## 4. Resource & Security

### 4.1 Secrets Management

- `/run/secrets/` 경로를 통해 비밀번호 주입:
  - `patroni_superuser_password`
  - `service_valkey_password`
  - `minio_root_password`

### 4.2 Network Mapping

| Service | Internal Host | External Port | Network |
| --- | --- | --- | --- |
| pg-router | pg-router | 15432, 15433 | infra_net |
| valkey | valkey-node-0 | 6379 | infra_net |
| minio | minio | 9000 | infra_net |

## Related Documents

- **PRD**: [2026-03-26-04-data.md](../../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../../02.ard/0004-data-architecture.md)
- **ADR**: [0004-postgresql-ha-patroni.md](../../03.adr/0004-postgresql-ha-patroni.md)
- **Plan**: [2026-03-26-04-data-standardization.md](../../05.plans/2026-03-26-04-data-standardization.md)
