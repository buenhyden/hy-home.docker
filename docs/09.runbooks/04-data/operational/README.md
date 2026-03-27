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

이 디렉터리는 플랫폼 핵심 데이터 서비스의 장애 복구 및 트러블슈팅을 위한 단계별 절차서를 포함합니다.

## Runbooks

| Service | Category | Runbook |
| :--- | :--- | :--- |
| **mng-db** | Management DB | [mng-db.md](./mng-db.md) |
| **supabase** | Backend Platform | [supabase.md](./supabase.md) |
| **postgresql-cluster** | Relational DB | [relational/README.md](../relational/README.md) |

---
Copyright (c) 2026. Licensed under the MIT License.
