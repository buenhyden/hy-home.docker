---
title: "Analytics dbt Transformation Job"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
created: "2026-09-21"
---

# Analytics dbt Transformation Job

> PostgreSQL 어댑터를 사용하는 커맨드라인 dbt Core로, 애플리케이션 데이터베이스를 전용 스키마로 변환합니다.

## Overview

dbt는 웹 서비스가 아니라 1회성 작업으로 실행되므로 라우트, OIDC 클라이언트,
장기 실행 컨테이너가 없습니다. 자체 `dbt` 역할로 `dev-pg`의 `platform_dev`에 연결해
애플리케이션 소스 스키마를 읽고 대상 스키마(기본값 `analytics`)에만
기록합니다. Lifecycle: **OPTIONAL**, `analytics-engineering`에서만 선택되며
HOME에는 포함되지 않습니다.

## Audience

- **Analytics engineers**: 모델을 작성하고 실행합니다.
- **Operators**: 역할을 프로비저닝하고 `run`/`build`의 부작용을 검토합니다.
- **AI agents**: 소유 Guide, Policy, Runbook 아래에서 이 패키지를 변경합니다.

## Scope

- **Included**: dbt 이미지, 프로필, 프로젝트 스켈레톤, 기능 전용 역할/권한 프로비저닝.
- **Excluded**: 애플리케이션 스키마 소유권, 스케줄링(오케스트레이션은 Airflow가 담당), BI 서빙.

## Structure

```text
.
├── Dockerfile                  # python slim + pinned dbt-core and dbt-postgres
├── docker-entrypoint.sh        # Reads dbt_db_password into DBT_PASSWORD, then runs dbt
├── docker-compose.yml          # dbt job and dbt-db-provision
├── profiles/profiles.yml       # hyhome profile; every connection value comes from env
├── projects/
│   ├── dbt_project.yml         # target/log/packages paths on the job's /tmp tmpfs
│   └── models/platform/        # hyhome_dbt_connectivity smoke model and test
├── provisioning/dev-pg.sql     # Role, source read grants, target schema (feature-owned)
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `dbt` | [Dockerfile](Dockerfile) (dbt-core, dbt-postgres) | 변환 CLI |
| `dbt-db-provision` | [Compose](docker-compose.yml), PostgreSQL 클라이언트 이미지 | 공유 [프로비저닝 러너](../../04-data/mng-db/pg/provision/run-feature-provision.sh)를 통해 [dev-pg.sql](provisioning/dev-pg.sql)을 실행 |

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증을 제공합니다.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `analytics-engineering` (`dev-pg`, `dev-platform-provision`도 함께 선택) |
| Default command | `debug` — 프로필과 연결을 검증하며 `/tmp`에만 기록 |
| Side effects | `compile`은 SQL만 렌더링(데이터베이스 기록 없음); `run`/`build`는 `DBT_SCHEMA`에 뷰/테이블을 생성 또는 교체; `--full-refresh`는 증분 모델을 재구성; `test`는 읽기 쿼리만 실행 |
| Environment keys | `DBT_DB_HOST`와 `DBT_DB_NAME`(필수), `DBT_DB_USER`, `DBT_SCHEMA`, `DBT_THREADS`, `POSTGRES_PORT`; 대상 DB는 `platform_dev`, source schema는 `app`, source owner는 `platform_owner` |
| Secret | `dbt_db_password` (PG-023); 프로비저닝은 `dev_pg_admin_password`도 읽음 |
| Grants | 데이터베이스에 대한 `CONNECT`, 소스 스키마에 대한 `USAGE`와 `SELECT`(애플리케이션 소유자가 나중에 생성하는 테이블에 대한 기본 권한 포함), 대상 스키마의 소유권; 데이터베이스에 대한 `CREATE`는 없음 |
| Writable paths | tmpfs의 `/tmp/dbt/{target,logs,packages}`; 프로젝트와 프로필은 읽기 전용 마운트 |
| Network | `dev_data_net` |

## Validation

- `HYHOME_COMPOSE_PROFILES=analytics-engineering bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests`

`dbt --version`이나 `debug` 성공은 어떤 모델이 실행되었다는 근거가 되지 않습니다.

## How to Work in This Area

1. 등록된 시크릿 워크플로우를 통해 `secrets/db/postgres/dbt_password.txt`를 프로비저닝합니다.
2. 승인된 환경에서 `docker compose --profile core --profile analytics-engineering run --rm dbt debug`를
   실행한 뒤 `... run --rm dbt compile`을 실행합니다.
3. 대상 스키마를 검토한 후에만 `... run --rm dbt build --select <models>`를 실행합니다.
4. 비즈니스 소스는 자체 `sources.yml`과 함께 `projects/models/`에 선언하고 권한은
   `provisioning/dev-pg.sql`에 유지합니다.

## Related Documents

- **Guide**: dbt usage guide (`docs/05.operations/guides/0090-dbt.md`)
- **Policy**: dbt operations policy (`docs/05.operations/policies/0090-dbt.md`)
- **Runbook**: dbt recovery runbook (`docs/05.operations/runbooks/0090-dbt.md`)
- [Documentation index](../../../docs/README.md)
