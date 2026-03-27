# Relational Data Runbooks

> 관계형 데이터베이스(RDB) 시스템 긴급 복구 및 운영 실행 지침

## Overview

이 디렉터리는 `hy-home.docker` 플랫폼의 관계형 데이터베이스 서비스 장애 시 신속한 복구 및 유지보수 작업을 수행하기 위한 단계별 실행 절차(Runbook)를 포함한다. 운영자가 복잡한 상황에서도 감정에 치우치지 않고 표준화된 절차에 따라 안전하게 대응할 수 있도록 가이드하는 것을 목적으로 한다.

## Audience

이 README의 주요 독자:

- 장애 대응 및 온콜 업무를 수행하는 **Operators / SRE**
- 복구 절차의 유효성을 테스트하는 **QA Engineers**
- 실시간으로 복구 동작을 실행하거나 가이드하는 **AI Agents**

## Scope

### In Scope

- `postgresql-cluster` 장애 시 수동 페일오버 및 쿼럼 복구 절차
- 데이터베이스 초기화 및 스키마 마이그레이션 실행 단계
- 리더 노드 교체(Switchover) 등 계획된 유지보수 절차

### Out of Scope

- 캐시 및 NoSQL 복구 런북 (-> `../cache-and-kv/`, `../nosql/`)
- 근본적인 기술 원리 설명 (-> `docs/07.guides/04-data/relational/`)
- 운영 정책 및 거버넌스 정의 (-> `docs/08.operations/04-data/relational/`)

## Structure

```text
relational/
├── postgresql-cluster.md     # HA PostgreSQL 클러스터 복구 런북
└── README.md                 # This file
```

## How to Work in This Area

1. 새 런북을 작성할 때는 `docs/99.templates/runbook.template.md`를 사용한다.
2. 모든 실행 단계는 실제 환경에서 검증되어야 하며, 데이터 손실 위험이 있는 단계는 명확히 경고해야 한다.
3. 복구 완료 후에는 `docs/10.incidents/`에 대응 기록을 남기는 것을 권장한다.

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/relational/README.md)
- **Operations**: [Operations Policy](../../08.operations/04-data/relational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
