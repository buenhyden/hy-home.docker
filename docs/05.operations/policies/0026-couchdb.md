---
title: "CouchDB Operations Policy"
version: "2.1.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0026"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# CouchDB Operations Policy

## Overview

이 정책은 `hy-home.docker`의 선택 NoSQL 서비스인 CouchDB 3노드 클러스터 운영 기준을 정의한다. 기준은 현재 tracked compose의 [couchdb image declaration](../../../labs/couchdb.yml), [curlimages/curl image declaration](../../../labs/couchdb.yml), `couchdb-cluster-init`, Traefik sticky route, Docker Secret 기반 admin password와 Erlang cookie 구성이다.

## Scope

- `labs/couchdb.yml`
- `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`
- `couchdb1-data`, `couchdb2-data`, `couchdb3-data`
- `lab_couchdb_password`, `lab_couchdb_cookie`, `LAB_COUCHDB_USERNAME`
- HOME Traefik label과 gateway 연결 없음; `couchdb-1`만 loopback host port 게시
- Linked guide and runbook under `docs/05.operations`

## Rules

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
- **Allowed**: 3-node cluster-init model과 sticky routing을 보존하는 문서 전용
  수정.
- **Disallowed**: 현재 evidence와 runbook escalation 없이 제시되는 수동 node
  rejoin, compaction, cluster surgery 가이드.
- **Disallowed**: 정책 텍스트나 evidence 안의 secret 값, credential dump,
  Erlang cookie 자료.

### Accountable lifecycle boundary

적용 identity: `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

N/A - 현재 승인된 예외 없음.

### Verification

- Compose 변경 후 이 정책을 [CouchDB guide](../guides/0026-couchdb.md),
  [CouchDB runbook](../runbooks/0026-couchdb.md),
  [LAB 설명](../../../labs/couchdb.md)와 비교한다.
- 서비스 이름, port, Traefik, secret, cluster-init 문서 갱신을 승인하기 전에
  `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/couchdb.yml --profile couchdb config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

### Review Cadence

- CouchDB compose image/profile/secret/Traefik/cluster-init 변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

### Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0026-couchdb.md) (`GDE-0026`), [Runbook](../runbooks/0026-couchdb.md) (`RUN-0026`)

## Related Documents

- [CouchDB backup guidance](https://docs.couchdb.org/en/stable/maintenance/backups.html)
- [CouchDB upgrade guidance](https://docs.couchdb.org/en/stable/install/upgrading.html)
- [CouchDB database security](https://docs.couchdb.org/en/stable/api/database/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0026-couchdb.md)
- [Recovery runbook](../runbooks/0026-couchdb.md)
- [LAB 설명](../../../labs/couchdb.md)
