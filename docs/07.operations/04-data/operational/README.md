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

- **Usages**: [Technical Usages](../../../07.operations/04-data/operational/README.md)
- **Procedures**: [Recovery Procedures](../../../07.operations/04-data/operational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.

## Usage

> Migrated from `docs/07.operations/04-data/operational/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Operational Usages: 04-data

> Usages for operational data services and management databases.

#### Overview

이 디렉토리는 `04-data` 티어 중 운영 및 관리 서비스(Management Database 등)와 관련된 가이드 문서를 포함한다. 각 문서는 시스템 구조 이해 및 사용자 가이드를 제공한다.

#### Audience

이 README의 주요 독자:

- 개발자, 운영자, AI 에이전트

- 데이터 서비스 연결이 필요한 **Developers**
- 인프라 상태를 점검하는 **Operators**
- 문서 간 추적성을 유지하는 **AI Agents**

#### Scope

##### In Scope

- `postgresql-cluster`(HA) 사용 및 구성 가이드
- `mng-db` 운영 관리 데이터베이스 가이드
- `supabase` 로컬 스택 및 외부 연동 가이드

##### Out of Scope

- 캐시 및 Key-Value 엔진 가이드 (-> `../cache-and-kv/`)
- 분석용 및 특수 데이터베이스 가이드 (-> `../specialized/`)

#### Structure

```text
operational/
├── mng-db.md                 # 운영 관리용 DB 기술 가이드
├── supabase.md               # Supabase 스택 기술 가이드
└── README.md                 # This file
```

#### How to Work in This Area

1. 새 가이드를 작성할 때는 `docs/99.templates/operation.template.md`를 사용한다.
2. 각 문서는 하위 구현인 `infra/04-data/relational/`과 1:1 대응 관계를 유지해야 한다.
3. 아키텍처 수준의 결정 사항은 `docs/03.adr/`을 먼저 참조한다.

#### Related References

- **# Operational Data Usages

> Technical guides for management and shared backend platforms.

#### Overview

이 디렉터리는 플랫폼 운영에 필수적인 핵심 데이터베이스 및 공통 백엔드 서비스에 대한 기술 가이드를 포함합니다.

#### Services

| Service | Category | Usage |
| :--- | :--- | :--- |
| **mng-db** | Management DB | [mng-db.md](./mng-db.md) |
| **supabase** | Backend Platform | [supabase.md](./supabase.md) |
| **postgresql-cluster** | Relational DB | [relational/README.md](../relational/README.md) |

---
Copyright (c) 2026. Licensed under the MIT License.

## Procedure

> Migrated from `docs/07.operations/04-data/operational/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Operational Procedures: 04-data

> Step-by-step procedures for shared data services.

#### Overview

이 디렉토리는 `04-data` 티어의 운영 계층 서비스(Management DB 등)에 대한 실행 절차 문서를 포함한다.

#### Audience

이 README의 주요 독자:

- 온콜 엔지니어, 플랫폼 관리자, AI 에이전트

- 장애 대응을 수행하는 **Operators / SRE**
- 복구 절차의 유효성을 검증하는 **QA Engineers**
- 실시간 장애 조치를 가이드하는 **AI Agents**

#### Scope

##### In Scope

- `postgresql-cluster`(HA) 노드 및 쿼럼 복구 절차
- `mng-db` 장애 시 서비스 복구 지침
- `supabase` 로컬/배포 스택의 긴급 복구 런북

##### Out of Scope

- 캐시 및 Key-Value 복구 런북 (-> `../cache-and-kv/`)
- 분석용 및 특수 데이터베이스 런북 (-> `../specialized/`)

#### Structure

```text
operational/
├── mng-db.md                 # 운영 관리용 DB 복구 런북
├── supabase.md               # Supabase 스택 복구 런북
└── README.md                 # This file
```

#### How to Work in This Area

이 디렉터리는 플랫폼 핵심 데이터 서비스의 장애 복구 및 트러블슈팅을 위한 단계별 절차서를 포함합니다.

#### Procedures

| Service | Category | Procedure |
| :--- | :--- | :--- |
| **mng-db** | Management DB | [mng-db.md](./mng-db.md) |
| **supabase** | Backend Platform | [supabase.md](./supabase.md) |
| **postgresql-cluster** | Relational DB | [relational/README.md](../relational/README.md) |

---
Copyright (c) 2026. Licensed under the MIT License.

---

#### Related References

- [docs/07.operations/README.md](../README.md)
- [docs/07.operations/README.md](../../../07.operations/README.md)
- [docs/10.incidents/README.md](../../../10.incidents/README.md)
