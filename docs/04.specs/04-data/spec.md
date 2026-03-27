<!-- Target: docs/04.specs/04-data/spec.md -->

# Data Tier (04-data) Technical Specification (Spec)

## Overview (KR)

이 문서는 `04-data` 티어의 기술 설계와 구현 계약을 정의하는 명세서다. PRD 요구를 기술적으로 구체화하고, PostgreSQL Patroni 클러스터, Valkey 분산 클러스터, MinIO 오브젝트 스토리지의 구체적인 설정값과 검증 방법을 정의한다.

## Strategic Boundaries & Non-goals

- **Owns**: 데이터베이스 엔진 설정, 스토리지 토폴로지, 클러스터링 로직, `infra_net` 내 포트 매핑.
- **Does Not Own**: 애플리케이션 레벨의 SQL 쿼리 최적화, 비즈니스 엔티티 정의.

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-26-04-data.md]`
- **ARD**: `[../../02.ard/0004-data-architecture.md]`
- **Related ADRs**: `[../../03.adr/0004-postgresql-ha-patroni.md]`

## Contracts

- **Config Contract**: `${DEFAULT_DATA_DIR}` 환경 변수 필수, Docker Secrets를 통한 시크릿 주입.
- **Data / Interface Contract**: S3 API (MinIO), PostgreSQL Wire Protocol, Valkey Cluster Protocol.
- **Governance Contract**: 모든 데이터 서비스는 `infra_net` 외부로의 직접 노출을 금지함.

## Core Design

### 1. Relational Database: PostgreSQL HA

- **Image**: `ghcr.io/zalando/spilo-17:4.0-p3`
- **Orchestration**: Patroni v4.0 / Etcd v3.6.7
- **Routing (pg-router)**:
  - **Write (15432)** -> Primary 노드
  - **Read (15433)** -> Replica 노드들

### 2. Distributed Cache: Valkey Cluster

- **Image**: `valkey/valkey:9.0.2-alpine`
- **Topology**: 6-node (3 Master, 3 Slave)
- **Ports**: 6379 (Client), 16379 (Bus)

### 3. Object Storage: MinIO

- **API Port**: 9000
- **Console Port**: 9001
- **Buckets**: `tempo-bucket`, `loki-bucket`, `cdn-bucket`.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: 각 서비스는 독립된 `/data` 서브 디렉토리를 사용함.
- **Migration / Transition Plan**: `infra/04-data/` 하위의 개별 Compose 파일을 통한 점진적 배포.

## Resource & Security

- **Secrets List**:
  - `patroni_superuser_password`
  - `service_valkey_password`
  - `minio_root_password`

## Verification

### PostgreSQL HA Check
```bash
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list
```

### Valkey Cluster Check
```bash
docker exec valkey-node-0 valkey-cli -p 6379 cluster nodes
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 모든 DB 컨테이너가 `infra_net`에 정상적으로 연결되어야 함.
- **VAL-SPC-002**: `pg-router`를 통한 Primary 노드로의 쓰기 작업이 성공해야 함.

## Related Documents

- **Plan**: `[../../05.plans/2026-03-26-04-data-standardization.md]`
- **Tasks**: `[../../06.tasks/04-data-tasks.md]`
- **Runbook**: `[../../09.runbooks/04-data/README.md]`
