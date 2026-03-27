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

- 캐시 및 NoSQL 운영 정책 (-> `docs/08.operations/04-data/cache-and-kv/` 등)
- 데이터베이스 쿼리 튜닝 가이드 (-> `docs/07.guides/04-data/relational/` 참조)
- 서비스 애플리케이션의 비즈니스 로직 운영

## Structure

```text
relational/
├── postgresql-cluster.md # PostgreSQL HA Operations Policy
└── README.md             # This file
```

## How to Work in This Area

1. 전반적인 운영 계획은 [Data Optimization Plan](../../../../docs/05.plans/2026-03-26-04-data-standardization.md)을 참조합니다.
2. 모든 운영 정책은 [Data Specification](../../../../docs/04.specs/04-data/spec.md)의 기술 제약 사항을 준수해야 합니다.
3. 새로운 정책 정의 시 `docs/99.templates/operation.template.md`를 사용합니다.

## Usage Instructions

- 이 영역의 정책 문서는 정기적으로 검토되어야 하며, 인프라 변경 시 실시간으로 갱신되어야 합니다.
- 정책 위반 사례 발생 시 [Incident Records](../../../10.incidents/README.md)와 연계하여 원인을 분석합니다.
- 상세 실행 절차는 [Relational Runbooks](../../../../docs/09.runbooks/04-data/relational/README.md)를 참조하십시오.

## Incident and Recovery Links

- **Guides**: [Relational Guides](../../../../docs/07.guides/04-data/relational/README.md)
- **Runbooks**: [Relational Runbooks](../../../../docs/09.runbooks/04-data/relational/README.md)
- **Source**: [Infrastructure README](../../../../infra/04-data/relational/postgresql-cluster/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
