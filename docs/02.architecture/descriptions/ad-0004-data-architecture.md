---
status: active
artifact_id: ad-0004
artifact_type: architecture-description
parent_ids:
  - prd-004
created: 2026-03-26
updated: 2026-08-10
---
# Data Tier (04-data) Architecture Description

## Overview and Context

이 문서는 `04-data` 티어의 참조 아키텍처와 품질 속성을 정의한다. 시스템 경계, 책임, 데이터 흐름, 운영 관점을 정리하는 기준 문서다. 본 아키텍처는 다중 모델 영속성 계층을 지향하며, 고가용성(HA)과 보안 격리를 핵심 설계 원칙으로 한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`04-data` 티어는 플랫폼의 모든 영속성 데이터를 소유하며, 관계형, NoSQL, 캐시, 오브젝트, 벡터 등 다양한 데이터 요구사항을 충족하는 인프라를 제공한다.

## Boundaries and Constraints

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**: 데이터베이스 인스턴스, 스토리지 볼륨, 백업 데이터, 데이터 전용 네트워크(`infra_net`).
- **Consumes**: Docker Secrets, Vault 시크릿, 시스템 리소스(CPU/RAM/Storage).
- **Does Not Own**: 애플리케이션 비즈니스 코드, 사용자 UI, 네트워크 외부 노출(Gateway 담당).
- **Non-goals**: 실시간 대시보드 시각화 (Observability 티어에서 담당).

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: Valkey 클러스터를 통한 밀리초 단위 응답 보장.
- **Security**: `infra_net` 격리 및 Docker Secrets 기반 인증.
- **Reliability**: Patroni/Etcd 기반의 자동 장애 조치(Failover).
- **Scalability**: 데이터 샤딩 및 노드 확장이 용이한 마이크로서비스 친화적 구성.
- **Observability**: Prometheus Exporter를 통한 실시간 상태 모니터링.
- **Operability**: 표준화된 백업/복구 런북 제공.

## Architecture Views

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

`04-data` 티어는 `hy-home.docker`의 기초 계층으로, 모든 상위 티어(Auth, AI, App 등)에 데이터 저장소를 공급한다.

```mermaid
graph TD
    subgraph "External/App Layer"
        APP[Applications]
    end

    subgraph "04-data Tier (infra_net)"
        ROUTER[pg-router HAProxy]
        V_CLSTR[Valkey Cluster 6-nodes]
        MINIO[MinIO S3]
        QDRANT[Qdrant Vector]

        subgraph "PostgreSQL HA Cluster"
            PG0[PostgreSQL Primary]
            PG1[PostgreSQL Replica]
            PG2[PostgreSQL Replica]
            ETCD[Etcd Quorum 3-nodes]
        end
    end

    APP --> ROUTER
    APP --> V_CLSTR
    APP --> MINIO
    APP --> QDRANT

    ROUTER --> PG0
    ROUTER --> PG1
    ROUTER --> PG2

    PG0 --- ETCD
    PG1 --- ETCD
    PG2 --- ETCD
```

## Data and Infrastructure

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**: 트랜잭션 데이터(SQL), 비정형 자산(S3), 검색 인덱스(Vector).
- **Storage Strategy**: 호스트 볼륨 바인드 마운트(`${DEFAULT_DATA_DIR}`).
- **Data Boundaries**: 각 서비스는 독립된 볼륨과 물리적 격리를 유지함.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose / Linux.
- **Deployment Model**: Multi-node Cluster (HA).
- **Operational Evidence**: `docker ps`, `patronictl list`, `valkey-cli cluster nodes`.

## Decision and Requirement Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../../01.requirements/prd-004-data.md](../../01.requirements/prd-004-data.md)
- **Spec**: [../../03.specs/004-data/spec.md](../../03.specs/spec-0004-data/spec.md)
- **Plan**: ../../04.execution/plans/2026-03-26-04-data-standardization.md
- **ADR**: [../decisions/adr-0004-postgresql-ha-patroni.md](../decisions/adr-0004-postgresql-ha-patroni.md)
