---
title: "MongoDB Replica Set Triage Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "operations"
artifact_id: "RUN-0027"
parent_ids:
- "GDE-0027"
created: "2026-05-17"
---

# MongoDB Replica Set Triage Runbook

## Overview

> Scope: Triage MongoDB replica set health, init job results, Mongo Express route, and exporter readiness without destructive data actions.

이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 oplog-consistent dump의 격리 복원 rehearsal 계약을 제공한다. 이번 문서 변경에서 MongoDB data command는 실행하지 않았다.

### Purpose

MongoDB replica set의 현재 member 상태와 init job evidence를 수집하고, destructive resync 또는 undocumented replica-set control이 운영 문서에 재유입되지 않도록 한다.

## When to Use

- `mongodb-rep1` 또는 `mongodb-rep2`가 unhealthy, stopped, or missing 상태일 때
- `mongo-init`가 replica set 초기화를 완료하지 못했거나 `rs.status()`가 실패할 때
- `mongo-express` route 또는 `mongodb-exporter` readiness를 확인해야 할 때
- NoSQL operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

### Execution and stop boundary

대상: `mongo-express`, `mongo-init`, `mongo-key-generator`, `mongodb-arbiter`, `mongodb-exporter`, `mongodb-rep1`, `mongodb-rep2`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

정적 검사는 `labs/.env.example`과 `labs/mongodb.yml`을 사용한다. 실제 점검은 승인된 Docker context·project·port·network·volume·용량·정리 범위를 확인하고, 비공개 `labs/.env`를 준비한 뒤 `LAB_ENV_FILE`을 그 파일로 설정해야 한다. 이번 소스 작업에서 컨테이너 실행과 복구는 `NOT_RUN`이다.

### Checklist

- [ ] `labs/mongodb.yml`의 독립 project와 `mongodb` profile을 확인하고 root include에서 제외됐는지 기록한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] destructive resync, data directory deletion, forced election, keyfile rotation, credential rotation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] replica set name은 compose-declared `MyReplicaSet`으로만 기록한다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/mongodb.yml --profile mongodb config --quiet
   ```

2. key generator, replica member, init job, UI, exporter 상태를 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml ps mongo-key-generator mongodb-rep1 mongodb-rep2 mongodb-arbiter mongo-init mongo-express mongodb-exporter
   ```

3. init job과 replica nodes 로그를 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml logs --tail=120 mongo-init mongodb-rep1 mongodb-rep2 mongodb-arbiter
   ```

4. replica set 상태를 승인된 custody와 client native password prompt로 확인한다.

   실제 TTY를 가진 비공개 운영 terminal에서만 client 자체 password prompt를 사용한다. tracing/verbose/terminal recording과 redirected stdin, `exec -T`를 금지한다. 승인된 custody에서 받은 credential을 prompt에만 입력하며 shell 변수·환경·argv·URL로 전달하지 않는다. prompt/권한/CA/endpoint가 없거나 인증이 실패하면 중단한다. root/Docker 관리자의 메모리 관찰까지 차단한다고 주장하지 않는다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml exec mongodb-rep1 sh -c 'exec mongosh --username "$MONGO_INITDB_ROOT_USERNAME" --authenticationDatabase admin --eval "rs.status().members.map(m => ({name:m.name,state:m.stateStr}))"'
   ```

5. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   # STOP: approve one daemon target; do not rerun mongo-key-generator or mongo-init during triage
   ```

6. Mongo Express의 label은 선언값으로만 확인한다. 현재 독립 LAB network에 HOME Traefik route가 없으므로 접속 성공을 기대하지 않는다. Password 값은 출력하지 않는다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml logs --tail=80 mongo-express
   ```

현재 key/init/exporter 경로는 비밀값을 argv에 싣지 않도록 수정했다. 실제 key 생성·replica 결성·exporter 인증은 격리 실행 전까지 NOT_RUN이다. member name/state만 기록한다.

### Verification Steps

- `docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml ps ...`에서 `mongodb-rep1`과 `mongodb-rep2`가 healthy 또는 running 상태인지 확인한다.
- `rs.status()` member summary가 `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`를 포함하는지 확인한다.
- `mongo-init`가 completed 상태인지, `mongodb-exporter`가 running 상태인지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml logs --tail=120 mongo-init mongodb-rep1 mongodb-rep2 mongodb-arbiter mongodb-exporter`
- **Replica evidence**: sanitized `rs.status()` member summary
- **Route**: 이전 Traefik label은 선언값이며 HOME gateway 경로는 없음
- **Metrics**: `mongodb-exporter` exposed port `${LAB_MONGO_EXPORTER_PORT:-9216}`

### Safe Rollback or Recovery Procedure

1. 이 triage는 data daemon의 무조건 재기동이나 init 재실행을 승인하지 않는다. 위 source 한계와 named-target lifecycle 승인을 먼저 확인한다.
2. 실패한 격리 target과 전용 volume을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. source replica set과 tracked volumes는 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 `rs.status()`와 `rs.conf()`, server/database-tools versions, database/collection/index 목록, users/roles scope, expected document-count invariants와 free space를 기록한다. password와 keyfile 값은 기록하지 않는다.
2. healthy data-bearing member에 `admin` authentication database로 접속해 `mongodump --oplog`를 수행한다. password는 prompt 또는 보호된 secret file로 제공하고 command line/URI에 넣지 않는다. arbiter volume은 backup하지 않는다.
3. dump, `oplog.bson`, metadata, manifest/checksums, server/tool versions와 scope를 immutable backup set으로 보존한다. live WiredTiger directory를 복사하지 않는다.
4. production과 network/volumes를 공유하지 않는 빈 compatible `MyReplicaSet` target을 별도 test credentials/keyfile로 준비하고 primary가 안정된 뒤 restore한다.
5. authenticated `mongorestore --oplogReplay`로 dump를 적재한다. target이 비어 있지 않거나 tool/server compatibility가 맞지 않으면 중단한다.
6. replica health, database/collection/index 목록, users/roles scope, representative reads, document-count invariants와 application smoke query를 검증한다. 불일치가 있으면 승격하지 않고 target을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다.

## Evidence

- 명령 이름, pass/fail 상태, service 상태, image tag, 민감 정보를 제거한 log와 replica member 상태 요약을 기록한다.
- secret 값, MongoDB document 전체 또는 password를 담은 credential 기반 URI 문자열은 기록하지 않는다.
- `mongodb`를 선택했음을 기록한다. root는 `labs/mongodb.yml`을 include하지 않는다.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. production cutover, election/member 변경, keyfile/credential rotation은 별도 승인 사항이며 이 변경에서는 실행하지 않았다.

## Escalation

primary를 확인할 수 없거나, `mongo-init`이 반복 실패하거나, replica member 상태가 `mongodb-rep1`/`mongodb-rep2`/`mongodb-arbiter`와 다르거나, secret 노출 위험이 있거나, data 작업이 필요하면 저장소 소유자 @buenhyden에게 에스컬레이션한다. 민감 정보를 제거한 log, member 요약, 렌더링된 compose evidence, service 상태와 시도한 단계를 포함한다.

## Traceability

- Declared parent: [MongoDB Usage Guide](../guides/0027-mongodb.md) (`GDE-0027`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0027-mongodb.md) (`GDE-0027`), [Policy](../policies/0027-mongodb.md) (`POL-0027`)

## Related Documents

- [Compose implementation: labs/mongodb.yml](../../../labs/mongodb.yml)

- [MongoDB backup and restore tools](https://www.mongodb.com/docs/v8.0/tutorial/backup-and-restore-tools/)
- [MongoDB security hardening](https://www.mongodb.com/docs/v8.0/core/security-hardening/)
- [MongoDB Community licensing](https://www.mongodb.com/legal/licensing/community-edition)

- [Operations index](../README.md)
- [Usage guide](../guides/0027-mongodb.md)
- [Operations policy](../policies/0027-mongodb.md)
- [Infra README](../../../labs/mongodb.md)
