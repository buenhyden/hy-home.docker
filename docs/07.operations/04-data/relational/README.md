# Relational Database Operations (04-data/relational)

> High-Availability Relational Database (PostgreSQL) 운영 정책 및 거버넌스

## Overview

이 디렉터리는 `hy-home.docker` 데이터 티어의 관계형 데이터베이스(RDBMS) 운영 정책을 정의합니다. 데이터 무결성, 가용성 보장을 위한 쿼럼 관리, 백업 정책, 그리고 모니터링 기준을 규정하여 안정적인 시스템 운영을 지원합니다.

## Audience

이 README의 주요 독자:

- 인프라 가용성을 관리하는 **Ops Engineers**
- 데이터 백업 및 복구 프로세스를 담당하는 **DBAs**
- 운영 현황을 점검하는 **AI Agents**

## Scope

### In Scope

- PostgreSQL HA 클러스터 가용성 정책 (Quorum, Failover)
- 데이터베이스 백업 시점 및 보관 주기 (Backup Policy)
- 모니터링 메트릭 임계값 및 알림 설정 기준
- 운영 계정 관리 및 접근 제어 통제 기준

### Out of Scope

- 캐시 및 NoSQL 운영 정책 (-> `docs/07.operations/04-data/cache-and-kv/` 등)
- 데이터베이스 쿼리 튜닝 가이드 (-> `docs/07.operations/04-data/relational/` 참조)
- 서비스 애플리케이션의 비즈니스 로직 운영

## Structure

```text
relational/
├── postgresql-cluster.md # PostgreSQL HA Operations Policy
└── README.md             # This file
```

## How to Work in This Area

1. 전반적인 운영 계획은 [Data Optimization Plan](../../../05.plans/2026-03-26-04-data-standardization.md)을 참조합니다.
2. 모든 운영 정책은 [Data Specification](../../../04.specs/04-data/spec.md)의 기술 제약 사항을 준수해야 합니다.
3. 새로운 정책 정의 시 `docs/99.templates/operation.template.md`를 사용합니다.

## Usage Instructions

- 이 영역의 정책 문서는 정기적으로 검토되어야 하며, 인프라 변경 시 실시간으로 갱신되어야 합니다.
- 정책 위반 사례 발생 시 [Incident Records](../../../10.incidents/README.md)와 연계하여 원인을 분석합니다.
- 상세 실행 절차는 [Relational Procedures](../../../07.operations/04-data/relational/README.md)를 참조하십시오.

## Incident and Recovery Links

- **Usages**: [Relational Usages](../../../07.operations/04-data/relational/README.md)
- **Procedures**: [Relational Procedures](../../../07.operations/04-data/relational/README.md)
- **Source**: [Infrastructure README](../../../../infra/04-data/relational/postgresql-cluster/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

---

## Related References

- [docs/07.operations/README.md](../README.md)
- [docs/07.operations/README.md](../../../07.operations/README.md)
- [docs/07.operations/README.md](../../../07.operations/README.md)

## Usage

> Migrated from `docs/07.operations/04-data/relational/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Relational Database Usages (04-data/relational)

> High-Availability Relational Database (PostgreSQL) 사용 및 최적화 가이드

#### Overview

이 디렉터리는 `hy-home.docker` 데이터 티어의 관계형 데이터베이스(RDBMS) 기술 가이드를 포함합니다. Patroni 기반의 고가용성 PostgreSQL 클러스터 연결 방법, 쿼리 최적화, 그리고 클러스터 관리 지침을 제공합니다.

#### Audience

이 README의 주요 독자:

- 데이터베이스 연결이 필요한 **Backend Developers**
- 클러스터 아키텍처를 관리하는 **Ops Engineers**
- 문서 구조를 학습하는 **AI Agents**

#### Scope

##### In Scope

- PostgreSQL HA 클러스터 접속 및 인증 방법
- 읽기/쓰기 분리를 위한 HAProxy 엔드포인트 활용
- 데이터베이스 초기화 및 사용자 계정 관리 절차
- 주요 성능 메트릭 및 모니터링 대시보드 사용법

##### Out of Scope

- NoSQL 및 캐시 서비스 가이드 (-> `docs/07.operations/04-data/nosql/` 등)
- 애플리케이션 프레임워크별 ORM 최적화 (별도 가이드 참조)
- 개별 도메인별 ERD 설계 및 비즈니스 모델 정의

#### Structure

```text
relational/
├── postgresql-cluster.md # PostgreSQL HA Cluster Usage
└── README.md             # This file
```

#### How to Work in This Area

1. 전반적인 데이터 아키텍처는 [Data Spec](../../../04.specs/04-data/spec.md) 문서를 먼저 확인합니다.
2. 각 서비스의 배포 및 실행 방법은 `infra/04-data/relational/postgresql-cluster/` 경로를 참조합니다.
3. 새로운 가이드 추가 시 `docs/99.templates/operation.template.md`를 사용합니다.

#### Documentation Standards

- 모든 기술 문서는 `docs/99.templates/`의 표준 스켈레톤을 준수해야 함
- Overview 섹션은 반드시 한글(KR)과 영문(EN)을 병기함 (Bilingual Policy)
- Single Source of Truth(SSoT) 유지 및 중복 방지

#### Related References

- **Operations**: [Relational Operations](../../../07.operations/04-data/relational/README.md)
- **Procedures**: [Relational Procedures](../../../07.operations/04-data/relational/README.md)
- **Source**: [Infrastructure README](../../../../infra/04-data/relational/postgresql-cluster/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

## Procedure

> Migrated from `docs/07.operations/04-data/relational/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Relational Database Procedures (04-data/relational)

> High-Availability Relational Database (PostgreSQL) 긴급 대응 및 일상 운영 실행 지침

#### Overview

이 디렉터리는 `hy-home.docker` 데이터 티어의 관계형 데이터베이스(RDBMS) 운영 작업의 실행 지침을 포함합니다. 클러스터 장애 복구, 노드 교체, 백업 복원 등 반복적이고 중요한 유지보수 작업을 단계별로 정의하여 운영 실수를 방지하고 빠른 복구를 돕습니다.

#### Audience

이 README의 주요 독자:

- 긴급 장애 대응을 수행하는 **On-call Engineers**
- 데이터베이스 유지보수를 담당하는 **Ops Engineers**
- 복구 절차를 검증하고 실행하는 **AI Agents**

#### Scope

##### In Scope

- PostgreSQL HA 클러스터 페일오버 및 리더 복구 절차
- 데이터베이스 스냅샷 백업 및 시점 복구(PITR) 단계
- 클러스터 확장 및 노드 교체 가이드
- etcd 분산 락(DCS) 상태 점검 및 초기화 절차

##### Out of Scope

- 캐시 및 NoSQL 복구 절차 (-> `docs/07.operations/04-data/nosql/` 등)
- 데이터 아키텍처 및 상세 설계 명세 (-> `docs/04.specs/04-data/spec.md` 참조)
- 수동 쿼리 실행을 통한 데이터 수정 (반드시 운영 정책 준수)

#### Structure

```text
relational/
├── postgresql-cluster.md # PostgreSQL HA Recovery Procedure
└── README.md             # This file
```

#### How to Work in This Area

1. 장애 복구 시 [Operational Policy](../../../07.operations/04-data/relational/postgresql-cluster.md)를 먼저 확인하여 통제 및 승인 기준을 준수합니다.
2. 모든 실행 결과는 [Incident/Postmortem](../../../10.incidents/README.md) 문서화를 통해 학습 자산으로 남깁니다.
3. 새로운 실행 지침 추가 시 `docs/99.templates/operation.template.md`를 사용합니다.

#### Usage Instructions

- 실행 전 반드시 백업 여부를 확인하고, 스테이징 환경에서 절차를 사전 검증할 것을 권장합니다.
- 런북의 각 단계(Procedure)는 `Checklist`와 병행하여 누락 없이 수행되어야 합니다.
- 실행 중 예상치 못한 오류 발생 시 상위 엔지니어에게 보고하고 즉시 중단합니다.

#### Incident and Recovery Links

- **Usages**: [Relational Usages](../../../07.operations/04-data/relational/README.md)
- **Operations**: [Relational Operations](../../../07.operations/04-data/relational/README.md)
- **Source**: [Infrastructure README](../../../../infra/04-data/relational/postgresql-cluster/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

---

#### Related References

- [docs/07.operations/README.md](../README.md)
- [docs/07.operations/README.md](../../../07.operations/README.md)
- [docs/10.incidents/README.md](../../../10.incidents/README.md)
