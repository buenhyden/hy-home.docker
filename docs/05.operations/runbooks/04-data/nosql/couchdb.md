---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/nosql/couchdb.md -->

# CouchDB Cluster Triage Runbook

## CouchDB Cluster Triage Procedure

> Scope: Triage CouchDB 3-node cluster health, cluster-init results, membership, and Traefik route assumptions.

### Overview

이 런북은 `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` 상태 이상이 발생했을 때 현재 compose에 맞는 점검 순서와 안전한 재시작 경계를 제공한다. 수동 재조인, 데이터베이스 compaction, shard 변경, cookie 교체는 현재 이 문서에서 검증된 복구 절차가 아니므로 에스컬레이션한다.

### Purpose

CouchDB cluster-init과 세 노드 health evidence를 수집하고, 현재 구현에 없는 서비스명이나 secret control을 사용하지 않도록 한다.

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: [CouchDB operations policy](../../../policies/04-data/nosql/couchdb.md)
- **Guide**: [CouchDB usage guide](../../../guides/04-data/nosql/couchdb.md)

## When to Use

- 한 개 이상의 CouchDB 노드가 unhealthy, stopped, or missing 상태일 때
- `couchdb-cluster-init`가 실패했거나 membership이 세 노드를 표시하지 않을 때
- Traefik route `couchdb.${DEFAULT_URL}` 또는 sticky routing 상태를 확인해야 할 때
- NoSQL operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 CouchDB include가 선택적으로 주석 처리되어 있는지, 이번 런타임에서 의도적으로 활성화했는지 확인한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] 서비스명은 `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`로만 기록한다.
- [ ] 수동 재조인, compaction, shard 변경, cookie 교체가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/couchdb/docker-compose.yml --profile data config
   ```

2. 컨테이너와 init job 상태를 확인한다.

   ```bash
   docker compose ps couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init
   ```

3. 각 노드와 init job 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init
   ```

4. `couchdb-1` 내부에서 health endpoint를 확인한다.

   ```bash
   docker exec couchdb-1 sh -lc 'COUCHDB_PASSWORD=$(cat /run/secrets/couchdb_password); curl -fsS "http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@localhost:${COUCHDB_PORT:-5984}/_up"'
   ```

5. membership을 확인한다.

   ```bash
   docker exec couchdb-1 sh -lc 'COUCHDB_PASSWORD=$(cat /run/secrets/couchdb_password); curl -fsS "http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@localhost:${COUCHDB_PORT:-5984}/_membership"'
   ```

6. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/couchdb/docker-compose.yml --profile data up -d couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init
   ```

### Verification Steps

- `docker compose ps couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init`에서 세 노드가 running 또는 healthy 상태인지 확인한다.
- `_membership` 결과에 `couchdb@couchdb-1.infra_net`, `couchdb@couchdb-2.infra_net`, `couchdb@couchdb-3.infra_net`가 포함되는지 확인한다.
- `couchdb-cluster-init` 로그가 cluster setup completion 또는 idempotent success/failure evidence를 제공하는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init`
- **Health**: `/_up`, `/_membership`, `/_scheduler/docs`
- **Route**: Traefik labels on `couchdb-1` and `couchdb_sticky` service cookie

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d` for the declared CouchDB services after evidence capture.
3. N/A — no verified manual rejoin, compaction rollback, shard relocation, or data restore procedure is documented yet.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, sanitized logs, and membership summary.
- Do not capture secret values, cookie values, or full authenticated HTTP output if it includes sensitive fields.
- Record whether CouchDB was optional/commented in root compose or explicitly included for the runtime session.

## Rollback or Recovery

N/A — no verified rollback or recovery procedure is documented beyond non-destructive compose restart and status verification. If cluster surgery, compaction, shard movement, cookie replacement, or data restore is required, preserve evidence and escalate.

## Escalation

Escalate to the owning operator when membership does not show the expected three nodes, cluster-init repeatedly fails, Traefik route assumptions diverge from compose labels, secret exposure risk appears, or any data operation is required. Include sanitized logs, membership summary, rendered compose evidence, service states, and attempted steps.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/nosql/couchdb.md)
- [Operations policy](../../../policies/04-data/nosql/couchdb.md)
- [Infra README](../../../../../infra/04-data/nosql/couchdb/README.md)
