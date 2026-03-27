# Operational Policies: 04-data

> Operational policies for shared data management services.

## Overview

이 디렉토리는 `04-data` 티어의 운영 계층 서비스(Management DB 등)에 대한 거버넌스 및 정책 문서를 포함한다. 각 문서는 통제 기준과 검증 방법을 정의한다.

## Audience

이 README의 주요 독자:
- 플랫폼 운영팀, SRE, AI 에이전트

- 운영 정책을 수립하고 모니터링하는 **Operators**
- 데이터 보안 및 규정 준수를 검토하는 **Security Engineers**
- 정책 준수 자동화를 수행하는 **AI Agents**

## Scope

### In Scope

- `postgresql-cluster`(HA) 가용성 및 쿼럼 정책
- `mng-db` 운영 데이터 보호 및 백업 표준
- `supabase` 서비스 거버넌스 및 접근 제어

### Out of Scope

- 캐시 및 Key-Value 운영 정책 (-> `../cache-and-kv/`)
- 분석용 및 특수 데이터베이스 정책 (-> `../specialized/`)

## Structure

```text
operational/
├── mng-db.md                 # 운영 관리용 DB 운영 정책
├── supabase.md               # Supabase 스택 운영 정책
└── README.md                 # This file
```

## How to Work in This Area

1. 정책 문서를 작성하거나 수정할 때는 `docs/99.templates/operation.template.md`를 준수한다.
2. 모든 정책은 `docs/02.ard/`에 정의된 아키텍처 원칙과 일치해야 한다.
3. 중요 정책 변경 시에는 영향도 평가 및 승인 절차를 거쳐야 한다.

## Operational Data Policies

> Governance and operational standards for management data services.

## Overview

이 디렉터리는 플랫폼 데이터 계층의 운영 가용성, 보안 및 백업에 대한 정책 문서를 포함합니다.

## Policies

| Service | Category | Policy |
| :--- | :--- | :--- |
| **mng-db** | Management DB | [mng-db.md](./mng-db.md) |
| **supabase** | Backend Platform | [supabase.md](./supabase.md) |
| **postgresql-cluster** | Relational DB | [relational/README.md](../relational/README.md) |

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/operational/README.md)
- **Runbooks**: [Recovery Runbooks](../../09.runbooks/04-data/operational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
