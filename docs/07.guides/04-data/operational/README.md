# Operational Guides: 04-data

> Guides for operational data services and management databases.

## Overview

이 디렉토리는 `04-data` 티어 중 운영 및 관리 서비스(Management Database 등)와 관련된 가이드 문서를 포함한다. 각 문서는 시스템 구조 이해 및 사용자 가이드를 제공한다.

## Audience

이 README의 주요 독자:
- 개발자, 운영자, AI 에이전트

- 데이터 서비스 연결이 필요한 **Developers**
- 인프라 상태를 점검하는 **Operators**
- 문서 간 추적성을 유지하는 **AI Agents**

## Scope

### In Scope

- `postgresql-cluster`(HA) 사용 및 구성 가이드
- `mng-db` 운영 관리 데이터베이스 가이드
- `supabase` 로컬 스택 및 외부 연동 가이드

### Out of Scope

- 캐시 및 Key-Value 엔진 가이드 (-> `../cache-and-kv/`)
- 분석용 및 특수 데이터베이스 가이드 (-> `../specialized/`)

## Structure

```text
operational/
├── mng-db.md                 # 운영 관리용 DB 기술 가이드
├── supabase.md               # Supabase 스택 기술 가이드
└── README.md                 # This file
```

## How to Work in This Area

1. 새 가이드를 작성할 때는 `docs/99.templates/guide.template.md`를 사용한다.
2. 각 문서는 하위 구현인 `infra/04-data/relational/`과 1:1 대응 관계를 유지해야 한다.
3. 아키텍처 수준의 결정 사항은 `docs/03.adr/`을 먼저 참조한다.

## Related References

- **Operations**: [Data Operations Policy](../../08.operations/04-data/operational/README.md)
- **Runbooks**: [Data Recovery Runbooks](../../09.runbooks/04-data/operational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
