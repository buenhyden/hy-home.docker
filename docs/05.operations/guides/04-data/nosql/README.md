# NoSQL Database Operations (04-data/nosql)

> Operational policies and maintenance standards for Cassandra, CouchDB, and MongoDB.

## Overview

이 디렉터리는 `hy-home.docker` NoSQL 데이터 플랫폼의 안정적인 운영을 위한 정책, 백업 전략, 보안 표준 및 모니터링 가이드라인을 포함한다.

## Audience

이 README의 주요 독자:

- **Operators (SRE/DBA)**: 정기 점검 및 운영 자동화 수행
- **Security Officers**: 데이터 보호 정책 및 접근 제어 검토
- **AI Agents**: 장애 감지 및 자동 복구 로직 구현

## Scope

### In Scope

- Service Level Objectives (SLO) 정의
- Backup & Retention 정책
- Cluster Scaling 가이드라인
- 정기 패치 및 업데이트 절차

### Out of Scope

- 기술적 시스템 구조 (05.operations/04-data/nosql 참조)
- 긴급 장애 복구 (05.operations/04-data/nosql 참조)
- 인프라 배포 코드 (infra/04-data/nosql 참조)

## Structure

```text
nosql/
├── README.md             # This file
├── cassandra.md          # Cassandra Operation Policy
├── couchdb.md            # CouchDB Operation Policy
└── mongodb.md            # MongoDB Operation Policy
```

## How to Work in This Area

1. **Templates**: 새 운영 정책 추가 시 `docs/99.templates/operation.template.md`를 사용한다. (현재 template.md 부재 시 Usage 형식을 준용하되 운영 관점에 집중)
2. **Review**: 모든 정책 변경은 인프라 팀의 승인을 거쳐야 한다.
3. **Traceability**: 정책 위반 발생 시 대응할 수 있는 `Procedure` 링크를 반드시 포함한다.

## Related References

- **Infrastructure**: [NoSQL Infrastructure](../../../../../infra/04-data/nosql/README.md)
- **Usages**: [NoSQL Technical Usages](./README.md)
- **Procedures**: [NoSQL Procedures](./README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

## Usage

> Migrated from `docs/05.operations/04-data/nosql/README.md` during the 2026-05-10 operations taxonomy consolidation.

### NoSQL Data Tier Usages (04-data/nosql)

> NoSQL 데이터베이스(Cassandra 등) 기술 가이드.

#### Resource Catalog

- [Apache Cassandra](./cassandra.md): Wide-column distributed store.
- [MongoDB](./mongodb.md): Document-based replica set cluster.
- [README.md](./README.md): This file

#### Overview

이 디렉터리는 `hy-home.docker` NoSQL 데이터 계층의 각 엔진별 사용 가이드와 시스템 아키텍처 설명을 포함한다. 개발자와 운영자가 각 데이터베이스의 특성을 이해하고 효율적으로 활용할 수 있도록 돕는다.

#### Audience

이 README의 주요 독자:

- **Developers**: 데이터 모델링 및 쿼리 최적화 가이드 참조
- **Operators**: 시스템 구성 이해 및 성능 튜닝 참조
- **AI Agents**: 시스템 도메인 지식 습득 및 기술 지원 수행

#### Scope

##### In Scope

- Apache Cassandra System Usage
- CouchDB Cluster Usage
- MongoDB Replica Set Usage
- NoSQL 엔진별 연결 패턴 및 베스트 프랙티스

##### Out of Scope

- 운영 정책 (05.operations/04-data/nosql 참조)
- 긴급 복구 런북 (05.operations/04-data/nosql 참조)
- 인프라 배포 코드 (infra/04-data/nosql 참조)

#### Structure

```text
nosql/
├── README.md             # This file
├── cassandra.md          # Cassandra System Usage
├── couchdb.md            # CouchDB Cluster Usage
└── mongodb.md            # MongoDB Replica Set Usage
```

#### How to Work in This Area

1. **Templates**: 새 가이드 추가 시 `docs/99.templates/operation.template.md`를 사용한다.
2. **SSoT**: 인프라 변경 사항이 가이드에 즉시 반영되도록 유지한다.
3. **Traceability**: 각 가이드는 관련 `Spec`, `Operation`, `Procedure` 문서와 연결되어야 한다.

#### Related References

- **Infrastructure**: [NoSQL Infrastructure](../../../../../infra/04-data/nosql/README.md)
- **Operations**: [NoSQL Operations](./README.md)
- **Procedures**: [NoSQL Procedures](./README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

## Procedure

> Migrated from `docs/05.operations/04-data/nosql/README.md` during the 2026-05-10 operations taxonomy consolidation.

### NoSQL Database Procedures (04-data/nosql)

> Step-by-step recovery procedures and troubleshooting guides for NoSQL infrastructure.

#### Overview

이 디렉터리는 `hy-home.docker` NoSQL 데이터 계층에서 발생할 수 있는 주요 장애 상황(데이터 유실, 노드 다운, 성능 저하 등)에 대한 구체적인 대응 절차(Procedures)를 포함한다.

#### Audience

이 README의 주요 독자:

- **On-call Engineers**: 장애 발생 시 긴급 복구 수행
- **SRE**: 장애 대응 프로세스 자동화 및 개선
- **AI Agents**: 장애 상황 감지 후 초기 대응 및 복구 보조

#### Scope

##### In Scope

- Service Down 복구 절차
- Backup 데이터 기반 Restoration (복원) 가이드
- Cluster Quorum 장애 해결
- Replication Lag 해소 방법

##### Out of Scope

- 일상적 운영 정책 (05.operations/04-data/nosql 참조)
- 기술적 상세 구조 (05.operations/04-data/nosql 참조)
- 인프라 초기 배포 (infra/04-data/nosql 참조)

#### Structure

```text
nosql/
├── README.md             # This file
├── cassandra.md          # Cassandra Recovery Procedure
├── couchdb.md            # CouchDB Recovery Procedure
└── mongodb.md            # MongoDB Recovery Procedure
```

#### How to Work in This Area

1. **Templates**: 새 런북 추가 시 `docs/99.templates/operation.template.md`를 사용한다. (현재 template.md 부재 시 Step-by-step 형식을 준용하여 행동 위주로 작성)
2. **Actionable**: 런북은 생각할 필요 없이 바로 명령어를 복사/붙여넣기 할 수 있을 정도로 구체적이어야 한다.
3. **Traceability**: 장애 원인 분석을 위해 관련 `Usage`와 `Operation` 문서를 링크한다.

#### Related References

- **Infrastructure**: [NoSQL Infrastructure](../../../../../infra/04-data/nosql/README.md)
- **Usages**: [NoSQL Technical Usages](./README.md)
- **Operations**: [NoSQL Operations](./README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
