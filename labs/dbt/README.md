---
title: "분석 dbt 변환 작업"
version: "1.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
created: "2026-09-21"
---

# 분석 dbt 변환 작업

> PostgreSQL 어댑터를 사용하는 커맨드라인 dbt Core LAB으로, 애플리케이션 데이터베이스를 전용 스키마로 변환합니다.

## Overview

dbt는 웹 서비스가 아니라 1회성 작업으로 실행되므로 라우트, OIDC 클라이언트,
장기 실행 컨테이너가 없습니다. 독립 Compose project인 [dbt LAB](../dbt.yml)
(`lab-dbt` profile)이며 root Compose에 포함되지 않고 HOME network에 연결되지
않습니다. 자체 `dbt` 역할로 `LAB_DBT_DB_HOST`가 가리키는 dev-pg의 `platform_dev`에
연결해 애플리케이션 소스 스키마를 읽고 대상 스키마(기본값 `analytics`)에만
기록합니다. HOME은 dev-pg를 LAB network에 게시하지 않으므로 owner가 도달 가능한
endpoint를 승인하기 전(미결정)까지는 render 검증만 합니다.

## Audience

- **Analytics engineers**: 모델을 작성하고 실행합니다.
- **Operators**: 역할을 프로비저닝하고 `run`/`build`의 부작용을 검토합니다.

## Scope

- **Included**: dbt 이미지, 프로필, 프로젝트 스켈레톤, 기능 전용 역할/권한 프로비저닝.
- **Excluded**: 애플리케이션 스키마 소유권, 스케줄링(오케스트레이션은 Airflow가 담당), BI 서빙.

## Structure

```text
.
├── Dockerfile                  # python slim + pinned dbt-core and dbt-postgres
├── docker-entrypoint.sh        # Reads dbt_db_password into DBT_PASSWORD, then runs dbt
├── profiles/profiles.yml       # hyhome profile; every connection value comes from env
├── projects/
│   ├── dbt_project.yml         # target/log/packages paths on the job's /tmp tmpfs
│   └── models/platform/        # hyhome_dbt_connectivity smoke model and test
├── provisioning/dev-pg.sql     # Role, source read grants, target schema (feature-owned)
└── README.md
```

서비스 정의(`dbt`, `dbt-db-provision`)는 [labs/dbt.yml](../dbt.yml)이 소유합니다.

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `dbt` | [Dockerfile](Dockerfile) (dbt-core, dbt-postgres) | 변환 CLI |
| `dbt-db-provision` | [Compose](../dbt.yml), PostgreSQL 클라이언트 이미지 | 공유 [프로비저닝 러너](../../infra/04-data/mng-db/pg/provision/run-feature-provision.sh)를 통해 [dev-pg.sql](provisioning/dev-pg.sql)을 실행 |

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며
[파생된 Compose 이미지 프로젝션](../../infra/tech-stack.versions.json)은 드리프트 검증을 제공합니다.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `lab-dbt` / `labs/dbt.yml` |
| Default command | `debug` — 프로필과 연결을 검증하며 `/tmp`에만 기록 |
| Side effects | `compile`은 SQL만 렌더링(데이터베이스 기록 없음); `run`/`build`는 `DBT_SCHEMA`에 뷰/테이블을 생성 또는 교체; `--full-refresh`는 증분 모델을 재구성; `test`는 읽기 쿼리만 실행 |
| Environment keys | `LAB_DBT_DB_HOST`(필수, 승인된 dev-pg endpoint), `LAB_DBT_DB_PORT`, `LAB_DBT_DB_ADMIN_USER`, `LAB_DBT_DB_USER`, `LAB_DBT_SCHEMA`, `LAB_DBT_THREADS`; 대상 DB는 `platform_dev`, source schema는 `app`, source owner는 `platform_owner` |
| Secret | `${LAB_SECRET_DIR}/dbt/`의 LAB 전용 `lab_dbt_db_password` -> `/run/secrets/dbt_db_password`; 프로비저닝은 `lab_dbt_dev_pg_admin_password` -> `dev_pg_admin_password`도 읽음. HOME 값 복사는 별도 승인 |
| Grants | 데이터베이스에 대한 `CONNECT`, 소스 스키마에 대한 `USAGE`와 `SELECT`(애플리케이션 소유자가 나중에 생성하는 테이블에 대한 기본 권한 포함), 대상 스키마의 소유권; 데이터베이스에 대한 `CREATE`는 없음 |
| Writable paths | tmpfs의 `/tmp/dbt/{target,logs,packages}`; 프로젝트와 프로필은 읽기 전용 마운트 |
| Network | `lab_dbt_net`(`hy-home-lab-dbt`); HOME network 없음 |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |

## Validation

- `docker compose --env-file labs/.env -f labs/dbt.yml --profile lab-dbt config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`

`dbt --version`이나 `debug` 성공은 어떤 모델이 실행되었다는 근거가 되지 않습니다.

## Usage

명령은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/dbt.yml --profile lab-dbt` 접두사로 실행합니다.
`config`는 render만 하며, 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down dbt`의 lease 규칙
([LAB 안내](../README.md#usage))을 따릅니다.

1. 승인된 dev-pg endpoint와 HOME `dev-platform-provision`이 만든 `platform_dev` fixture를 확인합니다.
2. `${LAB_SECRET_DIR}/dbt/db_password.txt`와 `dev_pg_admin_password.txt`를 별도 승인 아래 준비합니다.
3. 활성 lease 안에서 `... run --rm dbt debug`를 실행한 뒤 `... run --rm --no-deps dbt compile`을 실행합니다.
4. 대상 스키마를 검토한 후에만 `... run --rm --no-deps dbt build --select <models>`를 실행합니다.
5. 비즈니스 소스는 자체 `sources.yml`과 함께 `projects/models/`에 선언하고 권한은
   `provisioning/dev-pg.sql`에 유지합니다.

## Related Documents

- **Guide**: dbt usage guide (`docs/05.operations/guides/15-labs/0090-dbt.md`)
- **Policy**: dbt operations policy (`docs/05.operations/policies/15-labs/0090-dbt.md`)
- **Runbook**: dbt recovery runbook (`docs/05.operations/runbooks/15-labs/0090-dbt.md`)
- [LAB 탐색](../README.md)
- [Documentation index](../../docs/README.md)
