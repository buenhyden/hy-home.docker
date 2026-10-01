---
title: "Management Database Operations Policy"
version: "1.0.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0028"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Management Database Operations Policy

## Overview

이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한
운영 통제에 묶는다.

## Policy Scope

다섯 개의 `mng-db` 서비스는 HOME 대상이다. 공유 의존성이므로 database,
role, broker, credential 변경은 consumer를 인지하는 유지보수와 rollback을
요구한다.

## Controls

- `mng`, `core`, `dev`, `local` 중 하나와 함께 root project를 통해 운영한다.
  Leaf Compose 파일을 독립적으로 실행하지 않는다.
- PostgreSQL과 Valkey를 별도의 bind-backed volume에 유지하고 `mng_data_net`,
  health check, secret 파일, 공유 리소스 제한을 보존한다.
- `mng_postgres_password`, `mng_valkey_password`와 서비스 database credential을
  Docker secret 보관에 유지한다. Dump와 evidence는 plaintext 값을 포함해서는
  안 된다.
- `mng-pg-init`을 restore가 아니라 idempotent provisioning으로 취급한다. Rerun
  전에 완전한 role/database 목록을 검토한다. Optional-capability secret을
  읽거나 그 DDL을 실행해서는 안 된다. 이 둘은 feature provisioning job에 속하며
  이 job은 administrator role 이름과 타 소유 database나 schema를 거부한다.
- Init SQL이 읽는 모든 psql 변수는 그 실행자가 전달해야 하며,
  `tests/validation/test_compose_baseline_gates.py`의 contract test가 이를
  강제한다.
- Replication slot은 CDC 복구 state다. `POL-0036`의 CDC 재동기화 승인 없이
  공간을 회수하기 위해 삭제하지 않는다.
- Valkey를 폐기 가능한 cache가 아니라 workflow broker state로 취급한다. 오래된
  queue를 복원하면 작업이 중복되거나 순서가 바뀔 수 있다.

### Backup and restore

아래는 필수 보존 계약이다. 현 RUN-0021 automation은 physical pgBackRest/WAL+globals와RDB만 제공하며 database별 logical/AOF capture 및 앱 quiescence는 별도 구현·승인 작업이다. Restic30일 archive가 broker7일 업무 replay 승인을 대신하지 않는다.

PostgreSQL globals와 현재 각 database를 logical tool로 별도의 암호화된
destination에 capture한다. Valkey의 완전한 AOF 세트와 manifest, 그리고
문서화된 quiesced 시점의 RDB checkpoint를 capture한다. PostgreSQL 일일 세트는
30일, 주간 세트는 90일 보관한다. Valkey broker 세트는 일일로 7일 보관한다.
계획 목표는 RPO 24시간과 RTO 4시간이며, 이를 증명하는 HOME rehearsal은 없다.
공유 resource-template 제한은 계속 필수다. Removal이나 통합을 하려면 모든 consumer,
schema, credential, queue가 마이그레이션되고 rollback-tested 상태여야 한다.

새 isolated compatible cluster에서 database 이전에 PostgreSQL globals를
복원한다. 모든 dump를 신뢰할 수 없는 실행 가능 SQL로 취급하고, restore 권한을
제한하며, role, schema, row count, 지명된 consumer의 health를 검증한다. Valkey는
workflow owner가 queue replay semantics를 승인한 뒤에만 복원한다. Production
cutover나 data 교체는 별도 승인이 필요하다.

### Upgrade policy

모든 pin 변경에 대해 공식 release note, extension/client 호환성, rollback을
검토한다. PostgreSQL major upgrade는 isolated logical restore/rehearsal을
요구한다. `PGDATA`를 직접 재사용하는 것은 금지한다. Acceptance와 rollback
만료 시점까지 이전 volume을 보존한다.


### Accountable lifecycle boundary

적용 identity: `mng-pg`, `mng-pg-exporter`, `mng-pg-init`, `mng-valkey`, `mng-valkey-exporter`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

Workflow queue state에는 cache-only 예외가 적용되지 않는다. 예외는 runtime
mutation, plaintext secret, raw active storage 복사, 동일 host 가용성 주장을
허용하지 않는다.

## Verification

Root 구성과 범위가 지정된 static policy check를 검증한 뒤, 승격이나 cutover
전에 application 수준 acceptance를 갖춘 isolated compatible restore를
요구한다. 검증되지 않은 runtime 속성은 명시적으로 기록한다.

## Review Cadence

Profile, image, volume, credential, consumer, retention 또는 upstream
lifecycle 변경 후, 그리고 보관되는 동안 최소 연 1회 검토한다.

## Traceability

- Artifact: `POL-0028`; parent: `AD-0004`.
- Runtime 권한은 연결된 Compose/소스 파일에 남아 있으며, 정확한 pin도 그곳에 있다.

### References

- [PostgreSQL backup](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore security and options](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Runbook](../runbooks/0028-management-database.md)

## Related Documents

- [Domain catalog](../README.md)
