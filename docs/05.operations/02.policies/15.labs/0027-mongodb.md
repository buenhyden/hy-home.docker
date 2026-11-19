---
title: "MongoDB Operations Policy"
version: "2.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0027"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# MongoDB Operations Policy

## Purpose and Scope

### Objective

이 정책은 `hy-home.docker`의 `LAB` MongoDB replica set 운영 기준을 정의한다. runtime image/version은 Compose declaration이 소유하며, 정책 기준은 exact `mongodb` profile, `MyReplicaSet`, `mongo-key` named volume, Docker Secret 기반 root/UI credential이다.

#### Authority

- Declared parent: [Data Tier (04-data) Architecture Description](../../../02.architecture/01.descriptions/0004-data-architecture.md) (`AD-0004`)
- [Compose implementation: labs/mongodb/docker-compose.yml](../../../../labs/mongodb/docker-compose.yml)

### Applies To

- `labs/mongodb/docker-compose.yml`
- `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`
- `mongo-key`, `mongodb1-data`, `mongodb2-data`, `mongodb3-data` (`${LAB_DATA_DIR}/mongodb/` bind)
- `lab_mongodb_root_password`, `lab_mongo_express_basicauth_password`, `LAB_MONGODB_ROOT_USERNAME`, `LAB_MONGO_EXPRESS_USERNAME`
- HOME Traefik label 없음; Mongo Express loopback port `${LAB_MONGO_EXPRESS_HOST_PORT:-38081}`
- Linked guide and runbook under `docs/05.operations`

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0027-R1 | 문서 작성/변경 시 | 필수: 현재 replica set을 `mongo-init`으로 초기화된 두 data-bearing node와 하나의 arbiter로 기술한다 | none | none |
| POL-0027-R2 | replica set 이름 참조 시 | 필수: compose에 선언된 `MyReplicaSet`을 쓴다 | none | none |
| POL-0027-R3 | replica set 이름을 통제할 때 | 금지: 문서화되지 않은 replica-set-name 통제 | none | none |
| POL-0027-R4 | password 가이드 작성 시 | 필수: Root와 Mongo Express password 가이드는 plaintext 값이 아니라 Docker Secret mount를 참조한다 | none | none |
| POL-0027-R5 | keyfile 가이드 작성 시 | 필수: `mongo-key-generator`가 생성하는 `mongo-key` bind volume(`${LAB_DATA_DIR}/mongodb/mongo-key`)을 참조한다 | none | none |
| POL-0027-R6 | 항상 | 필수: 여섯 서비스 모두 정확한 `mongodb` profile을 쓴다 | none | none |
| POL-0027-R7 | 동일 host topology 기술 시 | 금지: 동일 host topology를 host-level HA로 기술 | none | none |
| POL-0027-R8 | backup 시 | 필수: data-bearing replica-set member에 인증된 `mongodump --oplog`를 쓰고 필요한 모든 database와 user/role, index, oplog metadata를 포함한다 | 수동 | none |
| POL-0027-R9 | backup 시 | 필수: tool/server 호환성, checksum, retention, restore evidence를 기록한다 | 수동 | none |
| POL-0027-R10 | restore rehearsal 시 | 필수: 새 isolated compatible replica set과 `mongorestore --oplogReplay`를 쓴다 | 수동 | none |
| POL-0027-R11 | restore rehearsal 시 | 필수: password는 보호된 prompt/file 처리로 제공한다 | 수동 | none |
| POL-0027-R12 | restore rehearsal 시 | 금지: password를 URI나 evidence에 포함 | 수동 | none |
| POL-0027-R13 | upgrade/removal 시 | 필수: restore-tested backup, 용량 확인, 호환성 검토, 명시적 승인을 요구한다 | 수동 | none |
| POL-0027-R14 | upgrade/removal 시 | 금지: arbiter를 data 복사본으로 취급 | 수동 | none |
| POL-0027-R15 | evidence 수집 시 | 허용: read-only `rs.status()`, `rs.conf()`, 로그, compose config 확인 | none | none |
| POL-0027-R16 | 문서 수정 시 | 허용: 서비스 이름, profile, 링크를 compose와 일치시키는 문서 전용 수정(runtime pin은 Compose 소유) | none | none |
| POL-0027-R17 | 항상 | 금지: 별도 승인과 검증된 runbook evidence 없는 파괴적 resync, data directory 삭제, 강제 election, keyfile rotation, backup restore 단계 | 수동 | none |
| POL-0027-R18 | 항상 | 금지: `mongodb-arbiter`를 backup/data node로 취급 | none | none |
| POL-0027-R19 | 항상 | 금지: compose에 선언되지 않은 host port로 MongoDB를 직접 노출 | none | none |
| POL-0027-R20 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0027-R21 | 항상 | 필수: `@buenhyden`이 named consumer/target/중단 영향/보존 기간/예외를 소유한다 | none | none |
| POL-0027-R22 | service image/profile/port/secret/mount, DDL/init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0027-R23 | engine secret/certificate 적용 시 | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0027-R24 | 앱 인증 연동 시 | 필수: 적용되는 `POL-0079` 통제를 따른다 | none | none |
| POL-0027-R25 | source 반영/재기동 시 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0027-R26 | 보존/삭제 시 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0027-R27 | exporter/stateless job 적용 시 | 필수: database restore가 없더라도 설정/credential과 그 작업이 변경하는 upstream state를 통제 범위에 포함한다 | none | none |
| POL-0027-R28 | 소유 artifact/복구 지점/expiry가 불명확할 때 | 금지: 삭제/재생성 | none | none |
| POL-0027-R29 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- **Required**: 문서는 현재 replica set을 `mongo-init`으로 초기화된 두 개의
  data-bearing node와 하나의 arbiter로 기술해야 한다.
- **Required**: Replica set 이름 참조는 compose에 선언된 `MyReplicaSet`을
  사용해야 한다. 문서화되지 않은 replica-set-name 통제는 허용하지 않는다.
- **Required**: Root와 Mongo Express password 가이드는 plaintext 값이 아니라
  Docker Secret mount를 참조해야 한다.
- **Required**: Keyfile 가이드는 `mongo-key-generator`가 생성하는 `mongo-key`
  bind volume(`${LAB_DATA_DIR}/mongodb/mongo-key`)을 참조해야 한다.
- **Required**: 여섯 개 서비스 모두 정확한 `mongodb` profile을 사용하며, 동일
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
  compose config 확인.
- **Allowed**: 서비스 이름, profile, 링크를 compose와 일치시키는 문서 전용
  수정. Runtime pin은 계속 Compose가 소유한다.
- **Disallowed**: 별도 승인과 검증된 runbook evidence 없이 수행하는 파괴적
  resync, data directory 삭제, 강제 election, keyfile rotation, backup restore
  단계.
- **Disallowed**: `mongodb-arbiter`를 backup/data node로 취급하거나 compose에
  선언되지 않은 host port로 MongoDB를 직접 노출하는 것.

#### Accountable lifecycle boundary

적용 identity: `mongo-express`, `mongo-init`, `mongo-key-generator`, `mongodb-arbiter`, `mongodb-rep1`, `mongodb-rep2`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03.identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

N/A - 현재 승인된 예외 없음.

#### Approval and Review

- MongoDB compose image/profile/secret/keyfile/replica-member 변경 시
  검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

## Enforcement

### Mechanisms

- Compose 변경 후 이 정책을 [MongoDB guide](../../01.guides/15.labs/0027-mongodb.md),
  [MongoDB runbook](../../03.runbooks/15.labs/0027-mongodb.md),
  [LAB 설명](../../../../labs/mongodb/README.md)와 비교한다.
- 서비스 이름, replica set, route, secret, keyfile 문서 갱신을
  승인하기 전에 `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/mongodb/docker-compose.yml --profile mongodb config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

### Limits

아래 규칙은 이름 붙은 검사가 규칙에 연결되어 있지 않거나 승인/검토에 의존하며, 정책은 Compose 렌더, 문서 링크 검사, 연결 문서 비교를 개별 규칙과 연결하지 않는다.

- 문서 기술: 강제 수단 없음 `POL-0027-R1`~`R5`
- 프로필/토폴로지: 강제 수단 없음 `POL-0027-R6`~`R7`
- backup/restore: 수동 검토 `POL-0027-R8`~`R12`
- upgrade/removal: 수동 검토 `POL-0027-R13`~`R14`
- 허용 작업: 강제 수단 없음 `POL-0027-R15`~`R16`
- 금지 작업: 수동 검토 `POL-0027-R17`; 강제 수단 없음 `POL-0027-R18`~`R19`
- 책임/수명주기 경계: 수동 검토 `POL-0027-R22`; 강제 수단 없음 `POL-0027-R20`~`R21`, `POL-0027-R23`~`R29`
- backup/restore/upgrade 절차와 파괴적 단계의 승인은 이름 붙은 자동 검사가 없고 수동 검토에 의존한다(정책 Limits 기준).
- 정책에 승인된 예외는 없다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/15.labs/0027-mongodb.md) (`GDE-0027`), [Runbook](../../03.runbooks/15.labs/0027-mongodb.md) (`RUN-0027`)
- [MongoDB backup and restore tools](https://www.mongodb.com/docs/v8.0/tutorial/backup-and-restore-tools/)
- [MongoDB security hardening](https://www.mongodb.com/docs/v8.0/core/security-hardening/)
- [MongoDB Community licensing](https://www.mongodb.com/legal/licensing/community-edition)
- [Operations index](../../README.md)
- [Usage guide](../../01.guides/15.labs/0027-mongodb.md)
- [Recovery runbook](../../03.runbooks/15.labs/0027-mongodb.md)
- [LAB 설명](../../../../labs/mongodb/README.md)
