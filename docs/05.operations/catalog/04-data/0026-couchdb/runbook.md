---
title: "CouchDB Cluster Triage Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0026"
parent_ids:
- "GDE-0026"
created: "2026-05-17"
---

# CouchDB Cluster Triage Runbook

## Overview

> Scope: Triage CouchDB 3-node cluster health, cluster-init results, membership, and Traefik route assumptions.

이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 fresh CouchDB cluster의 격리 복원 rehearsal 계약을 제공한다. 이번 문서 변경에서 데이터 명령은 실행하지 않았다.

### Purpose

CouchDB cluster-init과 세 노드 health evidence를 수집하고, 현재 구현에 없는 서비스명이나 secret control을 사용하지 않도록 한다.

## When to Use

- 한 개 이상의 CouchDB 노드가 unhealthy, stopped, or missing 상태일 때
- `couchdb-cluster-init`가 실패했거나 membership이 세 노드를 표시하지 않을 때
- Traefik route `couchdb.${DEFAULT_URL}` 또는 sticky routing 상태를 확인해야 할 때
- NoSQL operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose의 `include:` 목록에 CouchDB 파일이 있는지 확인하고, 이번 런타임에서 `couchdb` profile을 선택했는지 기록한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] 서비스명은 `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`로만 기록한다.
- [ ] 수동 재조인, compaction, shard 변경, cookie 교체가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile couchdb config --quiet
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
   docker compose --profile couchdb up -d couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init
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
3. 실패한 격리 cluster와 그 전용 storage를 폐기한다. source cluster와 tracked volumes는 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 source version, `/_membership`, `/_all_dbs`, shard placement, per-database `_security`, document-count invariants, configuration과 system database 범위를 기록한다. admin password와 Erlang cookie 값은 evidence에서 제외한다.
2. preferred path는 database replication이다. 승인된 fresh target으로 application databases와 필요한 system databases를 복제하고 completion/error state를 기록한다.
3. file backup을 선택한 경우 source를 일관되게 quiesce한 뒤 config, cluster metadata including `_dbs`, shard/database files, indexes, `_users`, `_replicator`, `_global_changes`를 checksum과 함께 보존한다. running `.couch` files를 복사하지 않는다.
4. production network/volumes를 공유하지 않는 호환 버전의 빈 3-node target을 준비한다. 별도 test admin/cookie를 사용하고 동일한 node count/shard assumptions를 명시한다.
5. file restore에서는 upstream 순서대로 index files를 database files보다 먼저 배치하고, config/metadata/data ownership을 검증한 뒤 target만 시작한다. replication path에서는 security objects와 system database scope를 별도로 확인한다.
6. `/_up`, `/_membership`, `/_all_dbs`, shard maps, per-database document counts, representative reads, `_security`, replication scheduler를 검증한다. 불일치가 있으면 target을 승격하지 않고 폐기한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `python3 scripts/validation/check-document-links.py --mode all` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, sanitized logs, and membership summary.
- Do not capture secret values, cookie values, or full authenticated HTTP output if it includes sensitive fields.
- Record which profiles were selected for the runtime session; the root file includes the CouchDB compose file unconditionally and the `couchdb` profile decides whether its services resolve.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. production cutover, membership 변경, cookie rotation은 별도 승인 사항이며 이 변경에서는 실행하지 않았다.

## Escalation

Escalate to the owning operator when membership does not show the expected three nodes, cluster-init repeatedly fails, Traefik route assumptions diverge from compose labels, secret exposure risk appears, or any data operation is required. Include sanitized logs, membership summary, rendered compose evidence, service states, and attempted steps.

## Traceability

- Declared parent: [CouchDB Usage Guide](guide.md) (`GDE-0026`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0026`), [Policy](policy.md) (`POL-0026`)

## Related Documents

- [Compose implementation: infra/04-data/nosql/couchdb/docker-compose.yml](../../../../../infra/04-data/nosql/couchdb/docker-compose.yml)

- [CouchDB backup guidance](https://docs.couchdb.org/en/stable/maintenance/backups.html)
- [CouchDB upgrade guidance](https://docs.couchdb.org/en/stable/install/upgrading.html)
- [CouchDB database security](https://docs.couchdb.org/en/stable/api/database/security.html)

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
- [Infra README](../../../../../infra/04-data/nosql/couchdb/README.md)
