---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/nosql/mongodb.md -->

# MongoDB Replica Set Triage Runbook

## MongoDB Replica Set Triage Procedure

> Scope: Triage MongoDB replica set health, init job results, Mongo Express route, and exporter readiness without destructive data actions.

### Overview (KR)

이 런북은 `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` 상태 이상이 발생했을 때 현재 compose에 맞는 점검 순서와 안전한 재시작 경계를 제공한다. 강제 선출, secondary data wipe, keyfile rotation, restore는 현재 이 문서에서 검증된 복구 절차가 아니므로 에스컬레이션한다.

### Purpose

MongoDB replica set의 현재 member 상태와 init job evidence를 수집하고, destructive resync 또는 undocumented replica-set control이 운영 문서에 재유입되지 않도록 한다.

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: [MongoDB operations policy](../../../policies/04-data/nosql/mongodb.md)
- **Guide**: [MongoDB usage guide](../../../guides/04-data/nosql/mongodb.md)

## When to Use

- `mongodb-rep1` 또는 `mongodb-rep2`가 unhealthy, stopped, or missing 상태일 때
- `mongo-init`가 replica set 초기화를 완료하지 못했거나 `rs.status()`가 실패할 때
- `mongo-express` route 또는 `mongodb-exporter` readiness를 확인해야 할 때
- NoSQL operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 MongoDB include가 선택적으로 주석 처리되어 있는지, 이번 런타임에서 의도적으로 활성화했는지 확인한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] destructive resync, data directory deletion, forced election, keyfile rotation, credential rotation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] replica set name은 compose-declared `MyReplicaSet`으로만 기록한다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/mongodb/docker-compose.yml --profile data --profile obs config
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
   docker compose -f docker-compose.yml -f infra/04-data/nosql/mongodb/docker-compose.yml --profile data --profile obs up -d mongo-key-generator mongodb-rep1 mongodb-rep2 mongodb-arbiter mongo-init mongo-express mongodb-exporter
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

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d` for the declared MongoDB services after evidence capture.
3. N/A — no verified destructive resync, data directory rollback, forced election, keyfile rotation, or restore procedure is documented yet.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, sanitized logs, and replica member state summary.
- Do not capture secret values, full MongoDB documents, or credential-backed URI strings with passwords.
- Record whether MongoDB was optional/commented in root compose or explicitly included for the runtime session.

## Rollback or Recovery

N/A — no verified rollback or recovery procedure is documented beyond non-destructive compose restart and status verification. If forced election, member reconfiguration, data wipe, keyfile rotation, or restore is required, preserve evidence and escalate.

## Escalation

Escalate to the owning operator when no primary can be identified, `mongo-init` repeatedly fails, replica member state diverges from `mongodb-rep1`/`mongodb-rep2`/`mongodb-arbiter`, secret exposure risk appears, or any data operation is required. Include sanitized logs, member summary, rendered compose evidence, service states, and attempted steps.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/nosql/mongodb.md)
- [Operations policy](../../../policies/04-data/nosql/mongodb.md)
- [Infra README](../../../../../infra/04-data/nosql/mongodb/README.md)
