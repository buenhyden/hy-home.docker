---
title: "Development Database Operations Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "POL-0100"
parent_ids:
- "AD-0031"
- "SPEC-0202"
created: "2026-10-03"
---

# Development Database Operations Policy

## Overview

이 정책은 source-only `dev-pg`와 `dev-valkey`의 관리 데이터 분리, 최소 권한
provision, 그리고 승인 전 실행 금지 경계를 정한다.

## Policy Scope

적용 대상은 `dev-pg`, `dev-platform-provision`, `dev-valkey`와 그 선언된 state,
network, secret reference다. `mng-pg`와 `mng-valkey`의 metadata, session, management
queue, 기존 PGDATA와 backup chain은 이 정책으로 변경하지 않는다. LAB entrypoint와
외부 업무 앱도 범위 밖이다.

## Controls

- `dev-data`와 목적별 `analytics-engineering`/`cdc` profile만 새 개발 엔진을 선택한다.
  HOME root profile 또는 기존 `dev` selector를 확대하지 않는다.
- 프로젝트 provision은 승인된 manifest의 명시적 DB·role·ACL 이름만 수용한다. shell
  문자열 조합, DB-number 격리, 공유 runtime password, PUBLIC privilege 확대를 허용하지 않는다.
- 프로젝트마다 NOLOGIN owner, migrator, runtime, reader를 분리한다. runtime은 DDL/소유권을
  가지지 않고 reader는 write/DDL을 가지지 않는다. default privilege, sequence, future object와
  `search_path` 검증을 함께 유지한다.
- `dev-valkey`는 project ACL과 key prefix를 보안 경계로 사용한다. TTL, persistence,
  maxmemory와 eviction의 업무 의미는 프로젝트 계약에서 명시한다. queue의 `noeviction`과
  cache LRU를 같은 instance에 혼합하는 변경은 별도 sizing decision을 요구한다.
- pgBackRest source declaration은 backup/PITR 보장이 아니다. archive activation, retention
  변경, restore, storage 삭제와 기존 `app_db` migration은 별도 승인과 격리 검증이 필요하다.
- secret은 Docker secret reference로만 소비한다. 값, rendered private configuration, raw
  database payload를 source evidence나 문서에 기록하지 않는다.

## Exceptions

내부 `platform_dev` fixture는 dbt/CDC contract 확인에 한정된다. 외부 project DB·schema·계정
생성 또는 writer 전환의 근거가 되지 않는다. 예외는 @buenhyden의 승인, 대상 manifest,
rollback 보존 기간과 검증 결과를 기록할 때만 종료한다.

## Verification

source change는 Compose render와 permission regression test를 통과해야 한다. fresh PGDATA,
repeat provision, app A/B isolation, reader write/DDL rejection, Timescale behavior, Valkey ACL,
backup/restore, CDC replay와 external consumer switching은 runtime task에서 별도로 증명한다.
SPEC-0202-TSK-0002는 합성 격리 엔진의 백업/복원과 일부 권한 거절만 증명한다.
정적 통과나 격리 시험을 HOME deployment, 운영 recovery 또는 data migration 증거로 사용하지 않는다.

## Review Cadence

Compose image/profile/network/mount/secret reference, project provision schema, 권한 계약,
backup declaration 또는 external consumer가 바뀔 때 검토한다. runtime acceptance 전에는
각 실행 요청에서 Docker context, resource, port, network, volume과 cleanup 범위를 재확인한다.

## Traceability

- Artifact: `POL-0100`; parents: `AD-0031`, `SPEC-0202`.
- Runtime declaration: `infra/04-data/dev-db/docker-compose.yml`.

## Related Documents

- [Development database guide](../guides/0100-development-database.md)
- [Development database source preflight](../runbooks/0100-development-database.md)
- [Backup and restore policy](0021-backup-and-restore.md)
- [Management database policy](0028-management-database.md)
