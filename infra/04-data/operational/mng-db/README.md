# Management Database (mng-db)

> Shared core database and cache for platform management services.

## Overview

`mng-db`는 플랫폼 핵심 서비스(Identity, Automation, Workflow 등)의 메타데이터를 관리하는 PostgreSQL 및 Valkey 인스턴스로 구성된 전용 퍼시스턴스 계층입니다. 초기 부트스트랩 및 일상적인 플랫폼 운영에 필요한 비 HA(High Availability)성 메타데이터를 안정적으로 관리하는 것을 목표로 합니다.

## Audience

이 README의 주요 독자:

- **Platform Ops**: 시스템 부트스트랩 및 관리
- **SREs**: 메타데이타 유지보수 및 트러블슈팅
- **AI Agents**: 서비스 건강 상태 확인 및 하위 시스템 가이드 제공

## Scope

### In Scope

- **Shared PostgreSQL 17**: n8n, Keycloak, Airflow 등 플랫폼 서비스용 DB.
- **Shared Valkey 9**: 플랫폼 서비스용 임시 캐시 및 세션 저장소.
- **Initialization Job**: `mng-pg-init`을 통한 사용자 및 DB 자동 생성.
- **Monitoring**: 전용 Exporter를 통한 메트릭 노출(PostgreSQL, Valkey).

### Out of Scope

- **HA Production Data**: 고가용성이 필요한 서비스 데이터는 [postgresql-cluster](../postgresql-cluster/README.md) 사용.
- **Large Volumetric Data**: 분석용 대용량 데이터는 [lake-and-object](../lake-and-object/README.md) 참조.

## Structure

```text
mng-db/
├── pg/                 # PostgreSQL init scripts & data
├── valkey/             # Valkey data storage
├── docker-compose.yml  # Service orchestration
└── README.md           # This file
```

## How to Work in This Area

1. **초기화 확인**: 신규 플랫폼 서비스 추가 시 `pg/init-scripts/init_users_dbs.sql`을 업데이트합니다.
2. **환경 설정**: 사용 중인 비밀번호는 `/run/secrets/`에 안전하게 저장되어 있는지 확인합니다.
3. **변경 영향**: 이 서비스의 재시작은 전체 관리 서비스의 순단을 초래하므로 주의가 필요합니다.

## Available Scripts

| Category | Command | Description |
| :--- | :--- | :--- |
| **Execution** | `docker compose up -d` | 전체 서비스 배포 |
| **Initialization** | `docker compose run --rm mng-pg-init` | DB 초기화 재실행 |
| **Health Check** | `docker exec mng-pg pg_isready` | PostgreSQL 상태 점검 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `POSTGRES_DEFAULT_USER` | Yes | 루트 유저 (secrets 연동 권장) |
| `POSTGRES_DEFAULT_DB` | Yes | 기본 관리용 DB 이름 (mng-pg) |
| `VALKEY_PORT` | No | 노출 포트 (Default: 6379) |

## Related References

- **ARD**: [0004-data-architecture.md](../../../docs/02.ard/0004-data-architecture.md)
- **Spec**: [spec.md](../../../docs/04.specs/04-data/spec.md)
- **Guide**: [mng-db.md](../../../docs/07.guides/04-data/operational/mng-db.md)
- **Operation**: [mng-db.md](../../../docs/08.operations/04-data/operational/mng-db.md)
- **Runbook**: [mng-db.md](../../../docs/09.runbooks/04-data/operational/mng-db.md)

---
Copyright (c) 2026. Licensed under the MIT License.
