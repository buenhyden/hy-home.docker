# Management Database (mng-db)

> Shared core database and cache for platform management services.

## Overview

A lightweight, shared persistence layer for management tier services (e.g., identity, monitoring metadata). It provides a standalone PostgreSQL instance and a single-node Valkey cache for non-HA critical management data during the initial bootstrap and operational phases.

## Audience

이 README의 주요 독자:

- **Platform Ops**: 시스템 부트스트랩 및 관리
- **SREs**: 메타데이타 유지보수 및 트러블슈팅
- **AI Agents**: 서비스 건강 상태 확인 및 하위 시스템 가이드 제공

## Scope

### In Scope

- **Shared PostgreSQL 17**: n8n, Keycloak, Airflow 등 플랫폼 서비스용 DB
- **Shared Valkey 9**: 플랫폼 서비스용 임시 캐시
- **Initialization Job**: `mng-pg-init`을 통한 사용자 및 DB 초기화
- **Monitoring**: PostgreSQL 및 Valkey Exporter를 통한 메트릭 노출

### Out of Scope

- **HA Production Data**: 고가용성이 필요한 운영 데이타는 [postgresql-cluster](../postgresql-cluster/README.md) 사용 권장
- **Large Datasets**: 분석용 대용량 데이타는 [lake-and-object](../lake-and-object/README.md) 사용

## Structure

```text
mng-db/
├── pg/                 # PostgreSQL init scripts (init_users_dbs.sql)
├── valkey/             # Valkey data storage
├── docker-compose.yml  # Service orchestration
└── README.md          # This file
```

## How to Work in This Area

1. **초기화 확인**: `pg/init-scripts/init_users_dbs.sql`에서 초기 사용자 및 DB 생성 스크립트를 확인한다.
2. **서비스 가이드**: [Management DB 가이드](../../../docs/07.guides/04-data/operational/mng-db.md)를 통해 접근 방법을 익힌다.
3. **운영 정책**: [운영 정책](../../../docs/08.operations/04-data/operational/mng-db.md)에 따라 백업 및 모니터링 기준을 준수한다.
4. **장애 대응**: 긴급 복구가 필요한 경우 [복구 런북](../../../docs/09.runbooks/04-data/operational/mng-db.md)을 수행한다.

## Configuration

| Variable | Target | Description |
| :--- | :--- | :--- |
| `POSTGRES_DB` | mng-pg | Management root DB name |
| `VALKEY_PORT` | mng-valkey | Shared cache exposition port (Default: 6379) |

## Testing

```bash
# Test PostgreSQL connectivity
docker exec mng-pg pg_isready -U ${POSTGRES_DEFAULT_USER}

# Test Valkey connectivity
docker exec mng-valkey valkey-cli -a ${VALKEY_PASSWORD} ping
```

## Change Impact

- **Restart Impact**: `mng-db` 재시작 시 이를 공유하는 모든 관리 계층 서비스의 일시적인 순단이 발생한다.
- **Dependency**: `02-auth` 및 `08-automation` 서비스는 이 DB에 의존하므로 우선 실행되어야 한다.

## AI Agent Guidance

1. 이 영역은 플랫폼 메타데이타 전용이므로 대규모 비즈니스 데이타 저장을 피한다.
2. `mng-pg-init` 잡이 정상 완료되었는지 로그를 통해 확인 후 상위 서비스를 배포한다.
3. 문서 갱신 시 `docs/0x.*` 경로의 관련 문서를 동기화한다.

---

## Related References

- **ARD**: [0004-data-architecture.md](../../../docs/02.ard/0004-data-architecture.md)
- **Spec**: [spec.md](../../../docs/04.specs/04-data/spec.md)
- **Guide**: [mng-db.md](../../../docs/07.guides/04-data/operational/mng-db.md)
- **Operation**: [mng-db.md](../../../docs/08.operations/04-data/operational/mng-db.md)
- **Runbook**: [mng-db.md](../../../docs/09.runbooks/04-data/operational/mng-db.md)
