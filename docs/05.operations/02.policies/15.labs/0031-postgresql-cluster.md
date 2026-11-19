---
title: "PostgreSQL Cluster Operations Policy"
version: "2.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0031"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# PostgreSQL Cluster Operations Policy

## Purpose and Scope

### Objective

이 정책은 `hy-home.docker`의 독립 LAB인 PostgreSQL HA 실습 cluster 운영 기준을 정의한다. 세 node가 한 host를 공유하므로 host HA가 아니며 HOME·DEV PostgreSQL은 단일 node다. 기준은 현재 tracked compose의 etcd 3노드 [quay.io/coreos/etcd image declaration](../../../../labs/postgresql-ha/docker-compose.yml) tag, HAProxy [haproxy image declaration](../../../../labs/postgresql-ha/docker-compose.yml), Spilo/Patroni [ghcr.io/zalando/spilo-17 image declaration](../../../../labs/postgresql-ha/docker-compose.yml), init job [postgres image declaration](../../../../labs/postgresql-ha/docker-compose.yml), postgres exporters [prometheuscommunity/postgres-exporter image declaration](../../../../labs/postgresql-ha/docker-compose.yml), Docker Secret 기반 credential 구성이다.

#### Authority

- Declared parent: [Data Tier (04-data) Architecture Description](../../../02.architecture/01.descriptions/0004-data-architecture.md) (`AD-0004`)

### Applies To

- `labs/postgresql-ha/docker-compose.yml`
- `etcd-1`, `etcd-2`, `etcd-3`
- `pg-router`, `pg-cluster-init`
- `pg-0`, `pg-1`, `pg-2`
- `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`
- `haproxy.cfg.tpl`, `init_users_dbs.sql`, `spilo-entrypoint-with-secrets.sh`
- `lab_pg_haproxy_stats_password`, `lab_pg_superuser_password`, `lab_pg_replication_password`, `lab_pg_exporter_password`, `lab_pg_service_password`
- Linked guide and runbook under `docs/05.operations`

#### Exclusions

root include와 `core` surface는 이 정책의 대상이 아니다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0031-R1 | 문서 작성/변경 시 | 필수: cluster를 정확한 `postgres-ha` profile 아래에서만 서비스가 해석되는 독립 `labs/postgresql-ha/docker-compose.yml` Compose로 식별한다 | none | none |
| POL-0031-R2 | 문서 작성/변경 시 | 금지: cluster를 root include 또는 `core` surface의 일부로 기술 | none | none |
| POL-0031-R3 | application 연결 가이드 작성 시 | 필수: `pg-router`의 write/read endpoint를 사용한다 | none | none |
| POL-0031-R4 | application 연결 가이드 작성 시 | 금지: `pg-0`/`pg-1`/`pg-2`에 직접 연결 | none | none |
| POL-0031-R5 | credential 가이드 작성 시 | 필수: Docker Secret mount와 secret-aware entrypoint를 참조한다 | none | none |
| POL-0031-R6 | 항상 | 금지: secret 값을 문서나 evidence에 복사 | none | none |
| POL-0031-R7 | 항상 | 필수: HAProxy stats를 `127.0.0.1:${LAB_PG_HAPROXY_STATS_HOST_PORT:-37000}` loopback port로만 게시한다 | none | none |
| POL-0031-R8 | 항상 | 금지: HAProxy stats에 HOME Traefik label 부여 | none | none |
| POL-0031-R9 | stats 접근 시 | 필수: `lab_pg_haproxy_stats_password`로 인증한다 | none | none |
| POL-0031-R10 | 서비스/init 가이드 작성 시 | 필수: `pg-cluster-init`을 `init_users_dbs.sql`로 exporter role/service role/service database를 동기화하는 compose job으로 기술한다 | none | none |
| POL-0031-R11 | logical backup 시 | 필수: cluster globals/role/privilege와 범위에 속한 모든 database schema/data dump, extension/ownership evidence, version, checksum, retention, 검증된 restore 기록을 포함한다 | 수동 | none |
| POL-0031-R12 | logical backup 시 | 필수: password는 별도로 보호하는 secret으로 유지한다 | 수동 | none |
| POL-0031-R13 | restore rehearsal 시 | 필수: 빈 isolated compatible cluster를 쓰고 database 이전에 globals를 복원한다 | 수동 | none |
| POL-0031-R14 | restore rehearsal 시 | 필수: owner/ACL/extension/sequence/data를 검증하고 test를 `pg-router`를 통해 라우팅한다 | 수동 | none |
| POL-0031-R15 | restore rehearsal 시 | 필수: Patroni/etcd state는 재구축한다 | 수동 | none |
| POL-0031-R16 | restore rehearsal 시 | 금지: Patroni/etcd state를 logical data로 복원 | 수동 | none |
| POL-0031-R17 | upgrade/removal 전 | 필수: 용량, WAL/dump 공간, 호환성, rollback evidence를 검토한다 | 수동 | none |
| POL-0031-R18 | upgrade/removal 전 | 금지: physical restore를 즉석에서 구성 | 수동 | none |
| POL-0031-R19 | 실제 HA 복원 구현/독립 검토가 없는 동안 | 필수: 운영 복원을 중단한다 | none | none |
| POL-0031-R20 | evidence 수집 시 | 허용: read-only `patronictl list`, `pg_isready`, HAProxy config 검증, compose config 렌더링, 로그, exporter metrics 확인 | none | none |
| POL-0031-R21 | 문서 수정 시 | 허용: image tag/서비스 이름/profile/port/network/secret/링크를 compose와 일치시키는 문서 전용 수정 | none | none |
| POL-0031-R22 | 항상 | 금지: 별도 owner 승인과 검증된 runbook evidence 없이 DCS data 삭제, 강제 cluster bootstrap, leadership mutation, backup restore, volume 교체, credential rotation, database mutation 단계를 승인된 policy로 제시 | 수동 | none |
| POL-0031-R23 | 추적된 구현 evidence가 없을 때 | 금지: WAL archiving, 일일 backup, DR drill을 활성 통제라고 주장 | none | none |
| POL-0031-R24 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0031-R25 | 항상 | 필수: `@buenhyden`이 named consumer/target/중단 영향/보존 기간/예외를 소유한다 | none | none |
| POL-0031-R26 | service image/profile/port/secret/mount, DDL/init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0031-R27 | engine secret/certificate 적용 시 | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0031-R28 | 앱 인증 연동 시 | 필수: 적용되는 `POL-0079` 통제를 따른다 | none | none |
| POL-0031-R29 | source 반영/재기동 시 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0031-R30 | 보존/삭제 시 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0031-R31 | exporter/stateless job 적용 시 | 필수: database restore가 없더라도 설정/credential과 그 작업이 변경하는 upstream state를 통제 범위에 포함한다 | none | none |
| POL-0031-R32 | 소유 artifact/복구 지점/expiry가 불명확할 때 | 금지: 삭제/재생성 | none | none |
| POL-0031-R33 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- **Required**: 문서는 cluster를 정확한 `postgres-ha` profile 아래에서만
  서비스가 해석되는 독립 `labs/postgresql-ha/docker-compose.yml` Compose로 식별해야 하며 root include 또는 `core` surface의 일부로 기술해서는 안 된다.
- **Required**: Application 연결 가이드는 `pg-0`, `pg-1`, `pg-2`에 직접 쓰지
  않고 `pg-router`의 write/read endpoint를 사용해야 한다.
- **Required**: Credential 가이드는 Docker Secret mount와 secret-aware
  entrypoint를 참조해야 한다. Secret 값은 문서나 evidence에 절대 복사해서는
  안 된다.
- **Required**: HAProxy stats는 `127.0.0.1:${LAB_PG_HAPROXY_STATS_HOST_PORT:-37000}` loopback port로만 게시하고 HOME Traefik label을 두지 않는다. stats 접근은 `lab_pg_haproxy_stats_password`로 인증한다.
- **Required**: 서비스/init 가이드는 `pg-cluster-init`을 `init_users_dbs.sql`을
  통해 exporter role, service role, service database를 동기화하는 compose
  job으로 기술해야 한다.
- **Required**: Logical backup은 cluster globals/role/privilege와 범위에 속한
  모든 database schema/data dump, extension/ownership evidence, version,
  checksum, retention, 검증된 restore 기록을 포함한다. Password는 별도로
  보호하는 secret으로 유지한다.
- **Required**: Restore rehearsal은 빈 isolated compatible cluster를 사용하며,
  database 이전에 globals를 복원하고, owner/ACL/extension/sequence/data를
  검증하며, test를 `pg-router`를 통해 라우팅한다. Patroni/etcd state는
  logical data로 복원하지 않고 재구축한다.
- **Required**: Upgrade나 removal 전에 용량, WAL/dump 공간, 호환성, rollback
  evidence를 검토한다. Physical restore를 즉석에서 만들지 않는다. 실제 HA 복원 구현·독립 검토가 없으므로 운영 복원은 중단한다.
- **Allowed**: Evidence 수집을 위한 read-only `patronictl list`,
  `pg_isready`, HAProxy config 검증, compose config 렌더링, 로그, exporter
  metrics 확인.
- **Allowed**: Image tag, 서비스 이름, profile, port, network, secret, 링크를
  compose와 일치시키는 문서 전용 수정.
- **Disallowed**: 별도의 owner 승인과 검증된 runbook evidence 없이 승인된
  policy로 제시되는 DCS data 삭제, 강제 cluster bootstrap, leadership
  mutation, backup restore, volume 교체, credential rotation, database
  mutation 단계.
- **Disallowed**: 추적된 구현 evidence가 추가되지 않는 한 WAL archiving, 일일
  backup, DR drill이 활성 통제라고 주장하는 것.

#### Accountable lifecycle boundary

적용 identity: `etcd-1`, `etcd-2`, `etcd-3`, `pg-0`, `pg-0-exporter`, `pg-1`, `pg-1-exporter`, `pg-2`, `pg-2-exporter`, `pg-cluster-init`, `pg-router`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03.identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

N/A - 현재 승인된 예외 없음.

#### Approval and Review

- PostgreSQL cluster compose image/profile/secret/port/network/init/exporter
  변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

## Enforcement

### Mechanisms

- Compose 변경 후 이 정책을
  [PostgreSQL cluster guide](../../01.guides/15.labs/0031-postgresql-cluster.md),
  [PostgreSQL cluster runbook](../../03.runbooks/15.labs/0031-postgresql-cluster.md),
  [LAB 설명](../../../../labs/postgresql-ha/README.md)와
  비교한다.
- 서비스 이름, image, route, secret, port, volume 문서 갱신을 승인하기 전에
  `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/postgresql-ha/docker-compose.yml --profile postgres-ha config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

### Limits

아래 규칙은 이름 붙은 검사가 규칙에 연결되어 있지 않거나 승인/검토에 의존하며, 정책은 Compose 렌더, 문서 링크 검사, 연결 문서 비교를 개별 규칙과 연결하지 않는다.

- 문서 기술: 강제 수단 없음 `POL-0031-R1`~`R6`, `POL-0031-R10`
- HAProxy stats: 강제 수단 없음 `POL-0031-R7`~`R9`
- backup/restore: 수동 검토 `POL-0031-R11`~`R16`
- upgrade/removal: 수동 검토 `POL-0031-R17`~`R18`; 강제 수단 없음 `POL-0031-R19`
- 허용 작업: 강제 수단 없음 `POL-0031-R20`~`R21`
- 금지 작업: 수동 검토 `POL-0031-R22`; 강제 수단 없음 `POL-0031-R23`
- 책임/수명주기 경계: 수동 검토 `POL-0031-R26`; 강제 수단 없음 `POL-0031-R24`~`R25`, `POL-0031-R27`~`R33`
- 실제 HA 복원 구현과 독립 검토가 없어 운영 복원은 중단 상태이며 복원 증거가 없다.
- WAL archiving, 일일 backup, DR drill은 추적된 구현 evidence가 없어 활성 통제로 주장할 수 없다.
- logical backup 구성, restore rehearsal, upgrade/removal 검토는 수동 검토에 의존한다(정책 Limits 기준).
- 정책에 승인된 예외는 없다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/15.labs/0031-postgresql-cluster.md) (`GDE-0031`), [Runbook](../../03.runbooks/15.labs/0031-postgresql-cluster.md) (`RUN-0031`)
- [PostgreSQL pg_dumpall reference](https://www.postgresql.org/docs/18/app-pg-dumpall.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Operations index](../../README.md)
- [Usage guide](../../01.guides/15.labs/0031-postgresql-cluster.md)
- [Recovery runbook](../../03.runbooks/15.labs/0031-postgresql-cluster.md)
- [LAB 설명](../../../../labs/postgresql-ha/README.md)
