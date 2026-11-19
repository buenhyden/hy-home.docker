---
title: "Development Database Operations Policy"
version: "0.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0100"
parent_ids:
- "AD-0031"
- "SPEC-0204"
created: "2026-10-03"
next_review_at: "2027-05-13"
---

# Development Database Operations Policy

## Purpose and Scope

### Objective

현재 source 인계 소유자는 [SPEC-0204](../../../03.specs/0204-service-integration-security-and-operations/spec.md)이며, SPEC-0202의 합성 검증은 삭제된 Spec의 역사적 근거이며 본문은 버전 이력에 있다.

이 정책은 source-only `dev-pg`와 `dev-valkey`의 관리 데이터 분리, 최소 권한
provision, 그리고 승인 전 실행 금지 경계를 정한다.

#### Authority

- Artifact: `POL-0100`; parents: `AD-0031`, `SPEC-0204`.
- Runtime declaration: `infra/04-data/dev-db/docker-compose.yml`.

### Applies To

적용 대상은 `dev-pg`, `dev-platform-provision`, `dev-perf-provision`, `dev-valkey`, 지표용 `dev-pg-monitor-provision`·`dev-pg-exporter`·`dev-valkey-exporter`와 그 선언된 state,
network, secret reference다.

#### Exclusions

`mng-pg`와 `mng-valkey`의 metadata, session, management
queue, 기존 PGDATA와 backup chain은 이 정책으로 변경하지 않는다. LAB entrypoint와
외부 업무 앱도 범위 밖이다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0100-R1 | 새 개발 엔진 선택 | 필수: `dev-data`와 목적별 `analytics-engineering`/`cdc`/`quality-results` profile만 사용한다 | none | none |
| POL-0100-R2 | 항상 | 금지: HOME root profile 또는 기존 `dev` selector 확대 | none | none |
| POL-0100-R3 | 프로젝트 provision | 필수: 승인된 manifest의 명시적 DB·role·ACL 이름만 수용한다 | none | none |
| POL-0100-R4 | 항상 | 금지: shell 문자열 조합/DB-number 격리/공유 runtime password/PUBLIC privilege 확대 | none | none |
| POL-0100-R5 | 프로젝트마다 | 필수: NOLOGIN owner/migrator/runtime/reader를 분리한다 | none | none |
| POL-0100-R6 | 항상 | 금지: runtime에 DDL/소유권 부여 | none | none |
| POL-0100-R7 | 항상 | 금지: reader에 write/DDL 부여 | none | none |
| POL-0100-R8 | 항상 | 필수: default privilege/sequence/future object/`search_path` 검증을 함께 유지한다 | none | none |
| POL-0100-R9 | `quality-results`의 `dev-perf-provision` | 필수: 공용 `perf_db` schema만 준비한다 | none | none |
| POL-0100-R10 | 시험 | 필수: `testing` profile과 분리한다 | none | none |
| POL-0100-R11 | 프로젝트별 LOGIN/실트래픽 | 필수: 별도 승인을 받는다 | 수동 | none |
| POL-0100-R12 | `dev-valkey` | 필수: project ACL과 key prefix를 보안 경계로 사용한다 | none | none |
| POL-0100-R13 | TTL/persistence/maxmemory/eviction | 필수: 업무 의미를 프로젝트 계약에서 명시한다 | none | none |
| POL-0100-R14 | queue `noeviction`과 cache LRU를 같은 instance에 혼합하는 변경 | 필수: 별도 sizing decision을 거친다 | none | none |
| POL-0100-R15 | pgBackRest source declaration | 금지: `archive_mode=on`/`dev` stanza/`${BACKUP_STATE_REPO_DIR}/dev-pgbackrest`/`dev_pgbackrest_cipher_pass` 선언을 backup/PITR 보장으로 취급 | none | none |
| POL-0100-R16 | HOME archive 활성화(stanza 생성)/retention 변경/restore/storage 삭제/기존 `app_db` migration | 필수: 별도 승인과 격리 검증을 받는다 | 수동 | none |
| POL-0100-R17 | 지표 수집 | 필수: `dev_pg_monitor`(통계·설정 읽기 전용 role)와 `devmonitor`(읽기 전용 ACL 사용자)만 쓴다 | none | none |
| POL-0100-R18 | 항상 | 금지: DEV exporter에 관리자 비밀 제공 | none | none |
| POL-0100-R19 | secret 소비 | 필수: Docker secret reference로만 소비한다 | none | none |
| POL-0100-R20 | source evidence/문서 | 금지: 값/rendered private configuration/raw database payload 기록 | none | none |
| POL-0100-R21 | source change | 필수: Compose render(`docker compose --env-file .env.example --profile dev-data config --quiet`)와 permission regression test를 통과한다 | `docker compose --env-file .env.example --profile dev-data config --quiet`/permission regression test | none |
| POL-0100-R22 | fresh PGDATA/repeat provision/app A/B isolation/reader write·DDL rejection/Timescale behavior/Valkey ACL/backup·restore/CDC replay/external consumer switching | 필수: runtime task에서 별도로 증명한다 | none | none |
| POL-0100-R23 | 항상 | 금지: 정적 통과나 격리 시험을 HOME deployment/운영 recovery/data migration 증거로 사용 | none | none |

- `dev-data`와 목적별 `analytics-engineering`/`cdc`/`quality-results` profile만 새 개발 엔진을 선택한다.
  HOME root profile 또는 기존 `dev` selector를 확대하지 않는다.
- 프로젝트 provision은 승인된 manifest의 명시적 DB·role·ACL 이름만 수용한다. shell
  문자열 조합, DB-number 격리, 공유 runtime password, PUBLIC privilege 확대를 허용하지 않는다.
- 프로젝트마다 NOLOGIN owner, migrator, runtime, reader를 분리한다. runtime은 DDL/소유권을
  가지지 않고 reader는 write/DDL을 가지지 않는다. default privilege, sequence, future object와
  `search_path` 검증을 함께 유지한다.
- `quality-results`의 `dev-perf-provision`은 공용 `perf_db` schema만 준비한다.
  시험의 `testing` profile과 분리하고 프로젝트별 LOGIN·실트래픽은 별도 승인한다.
- `dev-valkey`는 project ACL과 key prefix를 보안 경계로 사용한다. TTL, persistence,
  maxmemory와 eviction의 업무 의미는 프로젝트 계약에서 명시한다. queue의 `noeviction`과
  cache LRU를 같은 instance에 혼합하는 변경은 별도 sizing decision을 요구한다.
- pgBackRest source declaration(`archive_mode=on`, `dev` stanza, `${BACKUP_STATE_REPO_DIR}/dev-pgbackrest`, `dev_pgbackrest_cipher_pass`)은 backup/PITR 보장이 아니다. HOME archive 활성화(stanza 생성), retention
  변경, restore, storage 삭제와 기존 `app_db` migration은 별도 승인과 격리 검증이 필요하다.
- 지표 수집은 `dev_pg_monitor`(통계·설정 읽기 전용 role)와 `devmonitor`(읽기 전용 ACL 사용자)만 쓴다. DEV exporter에 관리자 비밀을 주지 않는다.
- secret은 Docker secret reference로만 소비한다. 값, rendered private configuration, raw
  database payload를 source evidence나 문서에 기록하지 않는다.

### Exceptions

#### Exception Conditions

내부 `platform_dev` fixture는 dbt/CDC contract 확인에 한정된다. 외부 project DB·schema·계정
생성 또는 writer 전환의 근거가 되지 않는다. 예외는 @buenhyden의 승인, 대상 manifest,
rollback 보존 기간과 검증 결과를 기록할 때만 종료한다.

#### Approval and Review

Compose image/profile/network/mount/secret reference, project provision schema, 권한 계약,
backup declaration 또는 external consumer가 바뀔 때 검토한다. runtime acceptance 전에는
각 실행 요청에서 Docker context, resource, port, network, volume과 cleanup 범위를 재확인한다.

## Enforcement

### Mechanisms

source change는 Compose render(`docker compose --env-file .env.example --profile dev-data config --quiet`)와 permission regression test를 통과해야 한다([RUN-0100](../../03.runbooks/05.databases-and-storage/0100-development-database.md#steps)). fresh PGDATA,
repeat provision, app A/B isolation, reader write/DDL rejection, Timescale behavior, Valkey ACL,
backup/restore, CDC replay와 external consumer switching은 runtime task에서 별도로 증명한다.
SPEC-0202-TSK-0002는 합성 격리 엔진의 백업/복원과 일부 권한 거절만 증명한다.
정적 통과나 격리 시험을 HOME deployment, 운영 recovery 또는 data migration 증거로 사용하지 않는다.

### Limits

이 정책에서 이름 붙은 검사는 Compose render와 permission regression test뿐이며(검증 행에만 연결), 아래 규칙은 자동 검사 없이 검토·승인에 의존합니다.

- profile: 자동 검사 없음(none) `POL-0100-R1`, `POL-0100-R2`
- provision: 자동 검사 없음(none) `POL-0100-R3`, `POL-0100-R4`, `POL-0100-R5`, `POL-0100-R6`, `POL-0100-R7`, `POL-0100-R8`
- perf: 자동 검사 없음(none) `POL-0100-R9`, `POL-0100-R10`; 수동 검토/승인 `POL-0100-R11`
- Valkey: 자동 검사 없음(none) `POL-0100-R12`, `POL-0100-R13`, `POL-0100-R14`
- backup: 자동 검사 없음(none) `POL-0100-R15`; 수동 검토/승인 `POL-0100-R16`
- 지표/secret: 자동 검사 없음(none) `POL-0100-R17`, `POL-0100-R18`, `POL-0100-R19`, `POL-0100-R20`
- 검증: 자동 검사 없음(none) `POL-0100-R22`, `POL-0100-R23`
- 정책이 밝힌 공백: fresh PGDATA/repeat provision/app A/B isolation/reader write·DDL rejection/Timescale behavior/Valkey ACL/backup·restore/CDC replay/external consumer switching은 runtime task에서 별도 증명 전까지 미검증이다.
- 정책이 밝힌 공백: SPEC-0202-TSK-0002는 합성 격리 엔진의 백업/복원과 일부 권한 거절만 증명한다.

## Ownership

### Owner

정책 소유자는 @buenhyden이다.

### Review Triggers

- [Development database guide](../../01.guides/05.databases-and-storage/0100-development-database.md)
- [Development database source preflight](../../03.runbooks/05.databases-and-storage/0100-development-database.md)
- [Backup and restore policy](../10.platform-and-backup/0021-backup-and-restore.md)
- [Management database policy](0028-management-database.md)
