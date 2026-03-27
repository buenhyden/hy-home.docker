# Operational Data Tier (04-data/operational)

> Shared core databases and management platforms for the hy-home.docker ecosystem.

## Overview

이 디렉터리는 `hy-home.docker` 플랫폼의 운영 및 관리를 지원하는 공통 데이터 서비스를 포함합니다. 여기에는 ID 관리, 자동화, 워크플로우를 위한 핵심 데이터베이스(`mng-db`)와 통합 백엔드 플랫폼(`supabase`)이 포함됩니다.

## Audience

이 README의 주요 독자:

- **Platform Ops**: 플랫폼 부트스트랩 및 서비스 관리
- **Backend Developers**: 공통 DB 및 Supabase 연동 개발
- **SREs**: 가용성 모니터링 및 장애 대응
- **AI Agents**: 시스템 의존성 분석 및 하위 가이드 제공

## Scope

### In Scope

- **Management Database (mng-db)**: Keycloak, n8n, Airflow 등을 위한 전용 PostgreSQL/Valkey.
- **Supabase Stack**: Auth, Realtime, Storage를 포함한 로컬 Firebase 대체 플랫폼.
- **Operational Alignment**: 관리 서비스 간의 데이터 격리 및 공유 정책 준수.
- **HA PostgreSQL Cluster (Reference)**: 비관리형 고가용성 DB는 [relational](../relational/README.md) 참조.

### Out of Scope

- **High-Availability Production Data**: 플랫폼 핵심 메타데이터 외의 서비스 데이터는 [relational](../relational/README.md) 활용.
- **Specialized Analytics**: 벡터 검색이나 그래프 데이터는 [specialized](../specialized/README.md) 참조.

## Structure

```text
operational/
├── mng-db/             # Shared management PostgreSQL & Valkey
├── postgresql-cluster/  # HA Cluster Infrastructure (Patroni based)
├── supabase/           # Self-hosted Supabase platform
└── README.md           # This file
```

## How to Work in This Area

1. **서비스 기동 순서**: `mng-db`가 먼저 실행되어야 하며, 이후 `supabase` 및 다른 관리 서비스가 실행됩니다.
2. **권한 관리**: 모든 비밀번호는 `/run/secrets/` 하위의 파일로 관리되어야 합니다.
3. **문서 동기화**: 인프라 변경 시 `docs/0x.*` 하위의 관련 문서(Guide, Operation, Runbook)를 함께 갱신합니다.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **mng-pg** | PostgreSQL 17 | Platform Metadata Storage |
| **mng-valkey** | Valkey 9 | Platform Shared Cache |
| **Supabase** | Multi-stack | Integrated Backend Platform |

## Related References

- **Guide**: [Operational Guides](../../docs/07.guides/04-data/operational/README.md)
- **Operation**: [Operational Policies](../../docs/08.operations/04-data/operational/README.md)
- **Runbook**: [Operational Runbooks](../../docs/09.runbooks/04-data/operational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
