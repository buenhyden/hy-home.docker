---
title: "MongoDB Operations Policy"
version: "2.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "POL-0027"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# MongoDB Operations Policy

## Overview

이 정책은 `hy-home.docker`의 `LAB` MongoDB replica set 운영 기준을 정의한다. runtime image/version은 Compose declaration이 소유하며, 정책 기준은 exact `mongodb` profile, `MyReplicaSet`, `mongo-key` named volume, Docker Secret 기반 root/UI credential이다.

## Policy Scope

- `labs/mongodb.yml`
- `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`
- `mongo-key`, `mongodb1-data`, `mongodb2-data`, `mongodb3-data`
- `lab_mongodb_root_password`, `lab_mongo_express_basicauth_password`, `LAB_MONGODB_ROOT_USERNAME`, `LAB_MONGO_EXPRESS_USERNAME`
- 기존 Traefik label은 HOME gateway에 연결되지 않음; exporter 내부 port `${LAB_MONGO_EXPORTER_PORT:-9216}`
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: 문서는 현재 replica set을 `mongo-init`으로 초기화된 두 개의
  data-bearing node와 하나의 arbiter로 기술해야 한다.
- **Required**: Replica set 이름 참조는 compose에 선언된 `MyReplicaSet`을
  사용해야 한다. 문서화되지 않은 replica-set-name 통제는 허용하지 않는다.
- **Required**: Root와 Mongo Express password 가이드는 plaintext 값이 아니라
  Docker Secret mount를 참조해야 한다.
- **Required**: Keyfile 가이드는 `mongo-key-generator`가 생성하는 `mongo-key`
  named volume을 참조해야 한다.
- **Required**: 일곱 개 서비스 모두 정확한 `mongodb` profile을 사용하며, 동일
  host topology를 host-level HA로 기술해서는 안 된다.
- **Required**: Backup은 data-bearing replica-set member에 대해 인증된
  `mongodump --oplog`를 사용하며, 필요한 모든 database와 user/role, index,
  oplog metadata를 포함하고, tool/server 호환성, checksum, retention, restore
  evidence를 기록한다.
- **Required**: Restore rehearsal은 새 isolated compatible replica set과
  `mongorestore --oplogReplay`를 사용한다. Password는 보호된 prompt/file
  처리로 제공하며 URI나 evidence에 절대 넣지 않는다.
- **Required**: Upgrade와 removal은 restore-tested backup, 용량 확인, 호환성
  검토, 명시적 승인을 요구한다. Arbiter를 절대 data 복사본으로 취급하지 않는다.
- **Allowed**: Evidence 수집을 위한 read-only `rs.status()`, `rs.conf()`, 로그,
  compose config, exporter readiness 확인.
- **Allowed**: 서비스 이름, profile, 링크를 compose와 일치시키는 문서 전용
  수정. Runtime pin은 계속 Compose가 소유한다.
- **Disallowed**: 별도 승인과 검증된 runbook evidence 없이 수행하는 파괴적
  resync, data directory 삭제, 강제 election, keyfile rotation, backup restore
  단계.
- **Disallowed**: `mongodb-arbiter`를 backup/data node로 취급하거나 compose에
  선언되지 않은 host port로 MongoDB를 직접 노출하는 것.

### Accountable lifecycle boundary

적용 identity: `mongo-express`, `mongo-init`, `mongo-key-generator`, `mongodb-arbiter`, `mongodb-exporter`, `mongodb-rep1`, `mongodb-rep2`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

N/A - 현재 승인된 예외 없음.

## Verification

- Compose 변경 후 이 정책을 [MongoDB guide](../guides/0027-mongodb.md),
  [MongoDB runbook](../runbooks/0027-mongodb.md),
  [LAB 설명](../../../labs/mongodb.md)와 비교한다.
- 서비스 이름, replica set, route, secret, keyfile, exporter 문서 갱신을
  승인하기 전에 `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/mongodb.yml --profile mongodb config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

## Review Cadence

- MongoDB compose image/profile/secret/keyfile/replica-member 변경 시
  검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0027-mongodb.md) (`GDE-0027`), [Runbook](../runbooks/0027-mongodb.md) (`RUN-0027`)

## Related Documents

- [Compose implementation: labs/mongodb.yml](../../../labs/mongodb.yml)

- [MongoDB backup and restore tools](https://www.mongodb.com/docs/v8.0/tutorial/backup-and-restore-tools/)
- [MongoDB security hardening](https://www.mongodb.com/docs/v8.0/core/security-hardening/)
- [MongoDB Community licensing](https://www.mongodb.com/legal/licensing/community-edition)

- [Operations index](../README.md)
- [Usage guide](../guides/0027-mongodb.md)
- [Recovery runbook](../runbooks/0027-mongodb.md)
- [LAB 설명](../../../labs/mongodb.md)
