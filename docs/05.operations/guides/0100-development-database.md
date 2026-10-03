---
title: "Development Database Usage Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "GDE-0100"
parent_ids:
- "POL-0100"
implementation_services:
  infra/04-data/dev-db/docker-compose.yml:
  - "dev-pg"
  - "dev-platform-provision"
  - "dev-perf-provision"
  - "dev-valkey"
created: "2026-10-03"
---

# Development Database Usage Guide

## Usage

`dev-db`는 미래 외부 프로젝트의 업무 데이터를 위한 선택형 개발 엔진이다.
관리 서비스 metadata·세션·관리 queue는 `mng-db`에 계속 남는다. `app_db`는 신규
프로젝트의 공용 DB가 아니며, 현재 source integration은 그 DB의 삭제·이관·전환을
승인하지 않는다.

[`infra/04-data/dev-db/docker-compose.yml`](../../../infra/04-data/dev-db/docker-compose.yml)은
TimescaleDB Community 기반 `dev-pg`, 승인된 내부 fixture의 계정·DB를 만드는
`dev-platform-provision`, 공용 시험 결과의 `dev-perf-provision`, project ACL을 적용하는
`dev-valkey`를 소유한다. 서비스는 `dev_data_net`과 독립 bind-backed state를 사용한다. `dev-pg`와 `dev-valkey`의 실제
image, profile, host exposure, resource limit, mount 및 secret reference는 Compose와
각 엔진 README가 권위다.

현재 외부 프로젝트에는 DB, role, Valkey ACL을 만들지 않는다. 승인된 project manifest가
명시적 `project_id`, DB 이름, owner/migrator/runtime/reader, Valkey user/prefix를 제공할
때만 infra provision을 확장한다. 앱 migration, 업무 schema, fixture와 E2E는 외부
Project-Template-derived workspace의 소유다.

`dev-perf-provision`은 명시적 `quality-results` profile에서 `perf_db`와 `quality`
schema를 준비한다. 해당 job의 실행과 프로젝트별 결과 writer/reader/verdict LOGIN
발급은 별도 운영 승인 범위다. `quality-results`를 `testing`에 암묵적으로 포함하지 않는다.

`dev-platform-provision`은 `analytics-engineering` 또는 `cdc` profile에서만 내부
`platform_dev` fixture를 만들 수 있다. 이는 dbt/CDC source contract 확인용이며 외부
앱 provision이나 HOME cutover가 아니다. runtime과 reader는 schema/database owner가
아니며 migration 계정도 아니다.

### 시간 데이터 계약

현재 `platform_dev`에는 승인된 hypertable이 없고 provision은 Timescale 확장만 준비한다. 외부 앱 migration이 시간 이력 테이블을 소유할 때 다음 항목을 프로젝트 계약에 명시한다. 사용자·권한·구독·outbox는 필요가 입증되지 않으면 일반 관계형 테이블로 유지한다.

- 저장 시각은 UTC `timestamptz`로 정규화하고 입력 timezone·단위(`ns/us/ms/s`)를 명시한다. PostgreSQL의 microsecond 정밀도를 넘는 원본 `ns` 값은 별도 원본 열/객체에 보존한다.
- 이력의 event time은 `NOT NULL`로 검증하고, 선택 속성의 NULL 의미와 중복 식별자·재적재 시 upsert 기준을 계약으로 정한다. 늦게 온 이벤트의 허용 창, 재집계·재처리·백필 책임도 정의한다.
- hypertable을 승인하는 경우 시간 partition column을 모든 unique/primary key에 포함하고, chunk interval·인덱스·compression·continuous aggregate refresh window를 함께 시험한다. raw retention은 refresh window보다 짧게 줄이지 않으며 데이터 삭제 정책 활성화는 별도 승인한다.
- 실제 표본량·쿼리·디스크·WAL을 관측해 chunk와 retention을 조정한다. 현재 수치는 실측 성능 순위나 보존 승인으로 사용하지 않는다.

pgBackRest repository mount와 secret reference는 소스에 선언되어 있다.
SPEC-0202-TSK-0002의 합성 격리 환경에서는 오프라인 전체 백업과 별도 볼륨 복원을
확인했고, `archive_mode=off` 상태의 온라인 백업은 의도대로 거절됐다. HOME 백업,
WAL 연속 보관·PITR, 관리 DB 복구, HOME 서비스 기동·정지·재시작, 실제 데이터 이관,
기존 자격 증명 회전은 실행하지 않았으며 별도 승인 범위다.

## Common Checks

저장소 root에서 정적 Compose와 permission contract만 확인한다. 이 명령은 컨테이너를
시작하거나 private environment를 출력하지 않는다.

```bash
docker compose --env-file .env.example --profile dev-data config --quiet
python3 -m unittest tests.validation.test_dev_pg_provision tests.validation.test_dev_valkey_acl tests.validation.test_dev_data_boundary
```

`dev-data`는 HOME의 기존 `dev` profile과 별도다. 현재 root candidate 선택에 새 엔진을
포함하거나 profile을 변경하지 않는다. `dev-pg` readiness는 연결 수락만 확인하며 extension,
project grant, 백업 또는 application readiness를 증명하지 않는다.

## Runbook Handoff

정적 소스 사전 검사와 HOME 실행 경계는 [RUN-0100](../runbooks/0100-development-database.md)이
소유한다. 합성 격리 검사 증거는 SPEC-0202-TSK-0002에 있다. HOME 기동·실제 프로젝트
provision·운영 백업/복원·이관·전환은 각각 `NOT_RUN`이며 별도 승인이 필요하다.

## Traceability

- Artifact: `GDE-0100`; governing policy: `POL-0100`.
- Source contract: `SPEC-0202`; architecture context: `AD-0031`.
- Runtime authority: `infra/04-data/dev-db/docker-compose.yml`.

## Related Documents

- [Development database policy](../policies/0100-development-database.md)
- [Development database source preflight](../runbooks/0100-development-database.md)
- [Management database guide](0028-management-database.md)
- [Development database package](../../../infra/04-data/dev-db/README.md)
