---
title: "MongoDB Replica Set Triage Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
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

## Procedure

### Checklist

- [ ] 루트 compose의 `include:` 목록과 정확한 `mongodb` profile을 기록한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] destructive resync, data directory deletion, forced election, keyfile rotation, credential rotation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] replica set name은 compose-declared `MyReplicaSet`으로만 기록한다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile mongodb config --quiet
   ```

2. key generator, replica member, init job, UI, exporter 상태를 확인한다.

   ```bash
   docker compose ps mongo-key-generator mongodb-rep1 mongodb-rep2 mongodb-arbiter mongo-init mongo-express mongodb-exporter
   ```

3. init job과 replica nodes 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 mongo-init mongodb-rep1 mongodb-rep2 mongodb-arbiter
   ```

4. replica set 상태를 secret mount 기반으로 확인한다.

   ```bash
   docker exec mongodb-rep1 sh -lc 'MONGO_ROOT_PASSWORD=$(cat /run/secrets/mongodb_root_password | tr -d "\n"); mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().members.map(m => ({name:m.name,state:m.stateStr}))"'
   ```

5. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile mongodb up -d mongo-key-generator mongodb-rep1 mongodb-rep2 mongodb-arbiter mongo-init mongo-express mongodb-exporter
   ```

6. Mongo Express route는 Traefik label 기준으로 확인하고, password 값은 출력하지 않는다.

   ```bash
   docker compose logs --tail=80 mongo-express
   ```

### Verification Steps

- `docker compose ps ...`에서 `mongodb-rep1`과 `mongodb-rep2`가 healthy 또는 running 상태인지 확인한다.
- `rs.status()` member summary가 `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`를 포함하는지 확인한다.
- `mongo-init`가 completed 상태인지, `mongodb-exporter`가 running 상태인지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 mongo-init mongodb-rep1 mongodb-rep2 mongodb-arbiter mongodb-exporter`
- **Replica evidence**: sanitized `rs.status()` member summary
- **Route**: Traefik labels on `mongo-express`
- **Metrics**: `mongodb-exporter` exposed port `${MONGO_EXPORTER_PORT:-9216}`

### Safe Rollback or Recovery Procedure

1. Runtime recovery in this runbook is limited to compose `up -d` for the declared MongoDB services after evidence capture.
2. 실패한 격리 target과 전용 volume을 폐기한다. source replica set과 tracked volumes는 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 `rs.status()`와 `rs.conf()`, server/database-tools versions, database/collection/index 목록, users/roles scope, expected document-count invariants와 free space를 기록한다. password와 keyfile 값은 기록하지 않는다.
2. healthy data-bearing member에 `admin` authentication database로 접속해 `mongodump --oplog`를 수행한다. password는 prompt 또는 보호된 secret file로 제공하고 command line/URI에 넣지 않는다. arbiter volume은 backup하지 않는다.
3. dump, `oplog.bson`, metadata, manifest/checksums, server/tool versions와 scope를 immutable backup set으로 보존한다. live WiredTiger directory를 복사하지 않는다.
4. production과 network/volumes를 공유하지 않는 빈 compatible `MyReplicaSet` target을 별도 test credentials/keyfile로 준비하고 primary가 안정된 뒤 restore한다.
5. authenticated `mongorestore --oplogReplay`로 dump를 적재한다. target이 비어 있지 않거나 tool/server compatibility가 맞지 않으면 중단한다.
6. replica health, database/collection/index 목록, users/roles scope, representative reads, document-count invariants와 application smoke query를 검증한다. 불일치가 있으면 승격하지 않고 target을 폐기한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `python3 scripts/validation/check-document-links.py --mode all` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, sanitized logs, and replica member state summary.
- Do not capture secret values, full MongoDB documents, or credential-backed URI strings with passwords.
- Record that `mongodb` was selected; the root file includes the MongoDB compose file unconditionally.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. production cutover, election/member 변경, keyfile/credential rotation은 별도 승인 사항이며 이 변경에서는 실행하지 않았다.

## Escalation

Escalate to the owning operator when no primary can be identified, `mongo-init` repeatedly fails, replica member state diverges from `mongodb-rep1`/`mongodb-rep2`/`mongodb-arbiter`, secret exposure risk appears, or any data operation is required. Include sanitized logs, member summary, rendered compose evidence, service states, and attempted steps.

## Traceability

- Declared parent: [MongoDB Usage Guide](../guides/0027-mongodb.md) (`GDE-0027`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0027-mongodb.md) (`GDE-0027`), [Policy](../policies/0027-mongodb.md) (`POL-0027`)

## Related Documents

- [Compose implementation: infra/04-data/nosql/mongodb/docker-compose.yml](../../../infra/04-data/nosql/mongodb/docker-compose.yml)

- [MongoDB backup and restore tools](https://www.mongodb.com/docs/v8.0/tutorial/backup-and-restore-tools/)
- [MongoDB security hardening](https://www.mongodb.com/docs/v8.0/core/security-hardening/)
- [MongoDB Community licensing](https://www.mongodb.com/legal/licensing/community-edition)

- [Operations index](../README.md)
- [Usage guide](../guides/0027-mongodb.md)
- [Operations policy](../policies/0027-mongodb.md)
- [Infra README](../../../infra/04-data/nosql/mongodb/README.md)
