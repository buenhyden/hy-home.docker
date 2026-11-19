---
title: "CouchDB Operations Policy"
version: "2.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0026"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# CouchDB Operations Policy

## Purpose and Scope

### Objective

이 정책은 `hy-home.docker`의 선택 NoSQL 서비스인 CouchDB 3노드 클러스터 운영 기준을 정의한다. 기준은 현재 tracked compose의 [couchdb image declaration](../../../../labs/couchdb/docker-compose.yml), [curlimages/curl image declaration](../../../../labs/couchdb/docker-compose.yml), `couchdb-cluster-init`, loopback 단일 host port, Docker Secret 기반 admin password와 Erlang cookie 구성이다.

#### Authority

- Declared parent: [Data Tier (04-data) Architecture Description](../../../02.architecture/01.descriptions/0004-data-architecture.md) (`AD-0004`)

### Applies To

- `labs/couchdb/docker-compose.yml`
- `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`
- `couchdb1-data`, `couchdb2-data`, `couchdb3-data`
- `lab_couchdb_password`, `lab_couchdb_cookie`, `LAB_COUCHDB_USERNAME`
- HOME Traefik label과 gateway 연결 없음; `couchdb-1`만 loopback host port 게시
- Linked guide and runbook under `docs/05.operations`

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0026-R1 | 문서 작성/변경 시 | 필수: 문서는 현재 서비스 이름 `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`을 사용한다 | `docker compose ... --profile couchdb config --quiet` | none |
| POL-0026-R2 | cookie 가이드 작성 시 | 필수: Cluster cookie 가이드는 `/run/secrets/lab_couchdb_cookie`를 참조한다 | `docker compose ... --profile couchdb config --quiet` | none |
| POL-0026-R3 | 항상 | 금지: 레거시 shared-secret 환경 변수를 현재 compose 통제로 취급 | none | none |
| POL-0026-R4 | health/membership 확인 시 | 필수: CouchDB HTTP API를 사용하는 container-local client의 native password prompt와 비공개 실제 TTY를 사용한다 | none | none |
| POL-0026-R5 | health/membership 확인 시 | 필수: 승인된 credential custody에서 입력한다 | none | none |
| POL-0026-R6 | 항상 | 금지: password를 URL·argv·환경 변수·history·로그에 넣거나 화면에 출력 | none | none |
| POL-0026-R7 | Custody/TTY 또는 native prompt를 확보하지 못했을 때 | 필수: 중단한다 | none | none |
| POL-0026-R8 | 항상 | 필수: 보호된 secret 파일과 기존 접근 통제 요구사항을 유지한다 | none | none |
| POL-0026-R9 | 항상 | 필수: LAB 접근은 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_COUCHDB_HOST_PORT:-35984}` loopback port뿐이다 | `docker compose ... --profile couchdb config --quiet` | none |
| POL-0026-R10 | 항상 | 금지: HOME Traefik label이나 HOME domain route 추가 | `docker compose ... --profile couchdb config --quiet` | none |
| POL-0026-R11 | 항상 | 필수: 모든 서비스는 정확한 `couchdb` profile을 사용한다 | none | none |
| POL-0026-R12 | 항상 | 금지: 동일 host의 세 node를 host-level HA로 표현 | none | none |
| POL-0026-R13 | 복구 세트 구성 시 | 필수: database/shard 파일 또는 replication target, system database, `_dbs` metadata, security 객체, 구성, cluster membership, Erlang cookie 보관, checksum, retention, 검증된 restore 기록을 포함한다 | none | none |
| POL-0026-R14 | restore rehearsal 시 | 필수: 호환되는 version/topology를 가진 새 isolated cluster를 사용한다 | none | none |
| POL-0026-R15 | restore rehearsal 시 | 필수: database replication을 우선한다 | none | none |
| POL-0026-R16 | 파일 restore 시 | 필수: upstream 순서를 따라 database 파일 전에 index를 둔다 | none | none |
| POL-0026-R17 | 항상 | 금지: live 파일 복사 | none | none |
| POL-0026-R18 | retention 변경 전 | 필수: 용량과 compaction 여유를 검토한다 | 수동 | none |
| POL-0026-R19 | upgrade 시 | 필수: upstream 순서를 따른다 | none | none |
| POL-0026-R20 | upgrade 시 | 필수: restore-tested backup을 요구한다 | none | none |
| POL-0026-R21 | removal 시 | 필수: consumer shutdown을 확인한다 | none | none |
| POL-0026-R22 | removal 시 | 필수: expiry/owner가 있는 보관된 replication/file backup evidence를 갖춘다 | none | none |
| POL-0026-R23 | node나 volume 삭제 전 | 필수: 별도 승인을 받는다 | 수동 | none |
| POL-0026-R24 | evidence 수집 시 | 허용: read-only `_up`, `_membership`, `_scheduler/docs`, 로그 확인 | none | none |
| POL-0026-R25 | 문서 수정 시 | 허용: 3-node cluster-init model과 loopback-only 접근을 보존하는 문서 전용 수정 | none | none |
| POL-0026-R26 | 항상 | 금지: 현재 evidence와 runbook escalation 없이 수동 node rejoin·compaction·cluster surgery 가이드 제시 | none | none |
| POL-0026-R27 | 항상 | 금지: 정책 텍스트나 evidence 안에 secret 값·credential dump·Erlang cookie 자료 포함 | none | none |
| POL-0026-R28 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0026-R29 | 항상 | 필수: `@buenhyden`이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다 | none | none |
| POL-0026-R30 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0026-R31 | 항상 | 필수: engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 `POL-0079`를, source 반영·재기동은 `POL-0006`을, 보존·삭제는 `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0026-R32 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0026-R33 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- **Required**: 문서는 현재 서비스 이름인 `couchdb-1`, `couchdb-2`, `couchdb-3`,
  `couchdb-cluster-init`을 사용해야 한다.
- **Required**: Cluster cookie 가이드는 `/run/secrets/lab_couchdb_cookie`를 참조해야
  한다. 레거시 shared-secret 환경 변수는 현재 compose 통제가 아니다.
- **Required**: Health와 membership 확인은 CouchDB HTTP API를 사용하는
  container-local client의 native password prompt와 비공개 실제 TTY를 사용해야 한다.
  승인된 credential custody에서 입력하며 password를 URL·argv·환경 변수·history·로그에
  넣거나 화면에 출력해서는 안 된다. Custody/TTY 또는 native prompt를 확보하지 못하면
  중단한다. 보호된 secret 파일과 기존 접근 통제 요구사항은 유지한다.
- **Required**: LAB 접근은 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_COUCHDB_HOST_PORT:-35984}` loopback port뿐이다. HOME Traefik label이나 HOME domain route를 추가하지 않는다.
- **Required**: 모든 서비스는 정확한 `couchdb` profile을 사용하며, 동일 host의
  세 node를 host-level HA로 표현해서는 안 된다.
- **Required**: 복구 가능한 세트는 database/shard 파일 또는 replication target,
  system database, `_dbs` metadata, security 객체, 구성, cluster membership,
  Erlang cookie 보관, checksum, retention, 검증된 restore 기록을 포함한다.
- **Required**: Restore rehearsal은 호환되는 version/topology를 가진 새 isolated
  cluster를 사용한다. Database replication을 우선하며, 파일 restore는 upstream
  순서를 따라 database 파일 전에 index를 두고 live 파일은 절대 복사하지 않는다.
- **Required**: 용량과 compaction 여유는 retention 변경 전에 검토한다. Upgrade는
  upstream 순서를 따르며 restore-tested backup을 요구한다.
- **Required**: Removal은 consumer shutdown 확인, expiry/owner가 있는 보관된
  replication/file backup evidence, node나 volume 삭제 전 별도 승인을 요구한다.
- **Allowed**: Evidence 수집을 위한 read-only `_up`, `_membership`,
  `_scheduler/docs`, 로그 확인.
- **Allowed**: 3-node cluster-init model과 loopback-only 접근을 보존하는 문서 전용
  수정.
- **Disallowed**: 현재 evidence와 runbook escalation 없이 제시되는 수동 node
  rejoin, compaction, cluster surgery 가이드.
- **Disallowed**: 정책 텍스트나 evidence 안의 secret 값, credential dump,
  Erlang cookie 자료.

#### Accountable lifecycle boundary

적용 identity: `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03.identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

N/A - 현재 승인된 예외 없음.

#### Approval and Review

- CouchDB compose image/profile/secret/Traefik/cluster-init 변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

## Enforcement

### Mechanisms

- Compose 변경 후 이 정책을 [CouchDB guide](../../01.guides/15.labs/0026-couchdb.md),
  [CouchDB runbook](../../03.runbooks/15.labs/0026-couchdb.md),
  [LAB 설명](../../../../labs/couchdb/README.md)와 비교한다.
- 서비스 이름, port, Traefik, secret, cluster-init 문서 갱신을 승인하기 전에
  `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/couchdb/docker-compose.yml --profile couchdb config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(문서): `POL-0026-R3`
- 이름 있는 검사 없음(credential): `POL-0026-R4`, `POL-0026-R5`, `POL-0026-R6`, `POL-0026-R7`, `POL-0026-R8`
- 이름 있는 검사 없음(profile): `POL-0026-R11`, `POL-0026-R12`
- 이름 있는 검사 없음(복구): `POL-0026-R13`, `POL-0026-R14`, `POL-0026-R15`, `POL-0026-R16`, `POL-0026-R17`
- 이름 있는 검사 없음(변경): `POL-0026-R19`, `POL-0026-R20`
- 이름 있는 검사 없음(제거): `POL-0026-R21`, `POL-0026-R22`
- 이름 있는 검사 없음(evidence): `POL-0026-R24`, `POL-0026-R25`, `POL-0026-R26`, `POL-0026-R27`
- 이름 있는 검사 없음(lifecycle): `POL-0026-R28`, `POL-0026-R29`, `POL-0026-R31`, `POL-0026-R32`, `POL-0026-R33`
- 수동 검토·승인에 의존(변경): `POL-0026-R18`
- 수동 검토·승인에 의존(제거): `POL-0026-R23`
- 수동 검토·승인에 의존(lifecycle): `POL-0026-R30`
- 정책이 스스로 밝힌 한계: Mechanisms에는 Compose 렌더, 문서 링크 검사(`check-document-links.py --mode all`), 연결 문서 비교만 있으며 링크 검사와 비교는 어느 규칙에 대응하는지 정책이 연결하지 않았다.
- 정책에 승인된 예외는 없다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/15.labs/0026-couchdb.md) (`GDE-0026`), [Runbook](../../03.runbooks/15.labs/0026-couchdb.md) (`RUN-0026`)
- [CouchDB backup guidance](https://docs.couchdb.org/en/stable/maintenance/backups.html)
- [CouchDB upgrade guidance](https://docs.couchdb.org/en/stable/install/upgrading.html)
- [CouchDB database security](https://docs.couchdb.org/en/stable/api/database/security.html)
- [Operations index](../../README.md)
- [Usage guide](../../01.guides/15.labs/0026-couchdb.md)
- [Recovery runbook](../../03.runbooks/15.labs/0026-couchdb.md)
- [LAB 설명](../../../../labs/couchdb/README.md)
