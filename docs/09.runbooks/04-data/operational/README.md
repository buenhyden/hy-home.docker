# Operational Runbooks: 04-data

> Step-by-step procedures for shared data services.

## Overview

이 디렉토리는 `04-data` 티어의 운영 계층 서비스(Management DB 등)에 대한 실행 절차 문서를 포함한다. 

## Audience

이 README의 주요 독자:
- 온콜 엔지니어, 플랫폼 관리자, AI 에이전트

- 장애 대응을 수행하는 **Operators / SRE**
- 복구 절차의 유효성을 검증하는 **QA Engineers**
- 실시간 장애 조치를 가이드하는 **AI Agents**

## Scope

### In Scope

- `postgresql-cluster`(HA) 노드 및 쿼럼 복구 절차
- `mng-db` 장애 시 서비스 복구 지침
- `supabase` 로컬/배포 스택의 긴급 복구 런북

### Out of Scope

- 캐시 및 Key-Value 복구 런북 (-> `../cache-and-kv/`)
- 분석용 및 특수 데이터베이스 런북 (-> `../specialized/`)

## Structure

```text
operational/
├── mng-db.md                 # 운영 관리용 DB 복구 런북
├── supabase.md               # Supabase 스택 복구 런북
└── README.md                 # This file
```

## How to Work in This Area

1. 새 런북을 작성할 때는 `docs/99.templates/runbook.template.md`를 사용한다.
2. 모든 절차는 실제 환경에서 검증되어야 하며, 위험한 단계에는 반드시 경고 문구를 포함한다.
3. 복구 완료 후에는 `docs/10.incidents/`에 기록을 남기는 것을 원칙으로 한다.

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/operational/README.md)
- **Operations**: [Operations Policy](../../08.operations/04-data/operational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
