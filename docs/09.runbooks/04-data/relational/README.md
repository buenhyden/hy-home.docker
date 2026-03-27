# Relational Database Runbooks (04-data/relational)

> High-Availability Relational Database (PostgreSQL) 긴급 대응 및 일상 운영 실행 지침

## Overview

이 디렉터리는 `hy-home.docker` 데이터 티어의 관계형 데이터베이스(RDBMS) 운영 작업의 실행 지침을 포함합니다. 클러스터 장애 복구, 노드 교체, 백업 복원 등 반복적이고 중요한 유지보수 작업을 단계별로 정의하여 운영 실수를 방지하고 빠른 복구를 돕습니다.

## Audience

이 README의 주요 독자:

- 긴급 장애 대응을 수행하는 **On-call Engineers**
- 데이터베이스 유지보수를 담당하는 **Ops Engineers**
- 복구 절차를 검증하고 실행하는 **AI Agents**

## Scope

### In Scope

- PostgreSQL HA 클러스터 페일오버 및 리더 복구 절차
- 데이터베이스 스냅샷 백업 및 시점 복구(PITR) 단계
- 클러스터 확장 및 노드 교체 가이드
- etcd 분산 락(DCS) 상태 점검 및 초기화 절차

### Out of Scope

- 캐시 및 NoSQL 복구 절차 (-> `docs/09.runbooks/04-data/nosql/` 등)
- 데이터 아키텍처 및 상세 설계 명세 (-> `docs/04.specs/04-data/spec.md` 참조)
- 수동 쿼리 실행을 통한 데이터 수정 (반드시 운영 정책 준수)

## Structure

```text
relational/
├── postgresql-cluster.md # PostgreSQL HA Recovery Runbook
└── README.md             # This file
```

## How to Work in This Area

1. 장애 복구 시 [Operational Policy](../../../../docs/08.operations/04-data/relational/postgresql-cluster.md)를 먼저 확인하여 통제 및 승인 기준을 준수합니다.
2. 모든 실행 결과는 [Incident/Postmortem](../../../../docs/11.postmortems/README.md) 문서화를 통해 학습 자산으로 남깁니다.
3. 새로운 실행 지침 추가 시 `docs/99.templates/runbook.template.md`를 사용합니다.

## Usage Instructions

- 실행 전 반드시 백업 여부를 확인하고, 스테이징 환경에서 절차를 사전 검증할 것을 권장합니다.
- 런북의 각 단계(Procedure)는 `Checklist`와 병행하여 누락 없이 수행되어야 합니다.
- 실행 중 예상치 못한 오류 발생 시 상위 엔지니어에게 보고하고 즉시 중단합니다.

## Incident and Recovery Links

- **Guides**: [Relational Guides](../../../../docs/07.guides/04-data/relational/README.md)
- **Operations**: [Relational Operations](../../../../docs/08.operations/04-data/relational/README.md)
- **Source**: [Infrastructure README](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
