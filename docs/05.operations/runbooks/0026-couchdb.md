---
title: "CouchDB Cluster Triage Runbook"
version: "1.1.4"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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


### Execution and stop boundary

대상: `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

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

   실제 TTY를 가진 비공개 운영 terminal에서만 client 자체 password prompt를 사용한다. tracing/verbose/terminal recording과 redirected stdin, `exec -T`를 금지한다. 승인된 custody에서 받은 credential을 prompt에만 입력하며 shell 변수·환경·argv·URL로 전달하지 않는다. prompt/권한/CA/endpoint가 없거나 인증이 실패하면 중단한다. root/Docker 관리자의 메모리 관찰까지 차단한다고 주장하지 않는다.

   ```bash
   docker compose exec couchdb-1 sh -c 'exec curl -fsS --user "$COUCHDB_USER" "http://localhost:${COUCHDB_PORT:-5984}/_up"'
   ```

5. membership을 확인한다.

   실제 TTY를 가진 비공개 운영 terminal에서만 client 자체 password prompt를 사용한다. tracing/verbose/terminal recording과 redirected stdin, `exec -T`를 금지한다. 승인된 custody에서 받은 credential을 prompt에만 입력하며 shell 변수·환경·argv·URL로 전달하지 않는다. prompt/권한/CA/endpoint가 없거나 인증이 실패하면 중단한다. root/Docker 관리자의 메모리 관찰까지 차단한다고 주장하지 않는다.

   ```bash
   docker compose exec couchdb-1 sh -c 'exec curl -fsS --user "$COUCHDB_USER" "http://localhost:${COUCHDB_PORT:-5984}/_membership"'
   ```

6. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   # STOP: confirm membership/quorum and approve one node; cluster-init is a separate mutation
   ```



source health/init/exporter의 기존 password argv 노출은 이 문서 수정으로 고쳐지지 않았다. 별도 구현 변경과 검증이 필요하다. source image가 제공하는 client를 쓰며 실제 packaged prompt 동작이 다르면 우회하지 않는다. 예시 port는 선언된 listener와 대조한다. `_up` 결과와 세 member identity만 요약하며 raw response/transcript는 보존하지 않는다.

### Verification Steps

- `docker compose ps couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init`에서 세 노드가 running 또는 healthy 상태인지 확인한다.
- `_membership` 결과에 `couchdb@couchdb-1.infra_net`, `couchdb@couchdb-2.infra_net`, `couchdb@couchdb-3.infra_net`가 포함되는지 확인한다.
- `couchdb-cluster-init` 로그가 cluster setup completion 또는 idempotent success/failure evidence를 제공하는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init`
- **Health**: `/_up`, `/_membership`, `/_scheduler/docs`
- **Route**: Traefik labels on `couchdb-1` and `couchdb_sticky` service cookie

### Safe Rollback or Recovery Procedure

1. 이 triage는 data daemon의 무조건 재기동이나 init 재실행을 승인하지 않는다. 위 source 한계와 named-target lifecycle 승인을 먼저 확인한다.
2. 실패한 격리 cluster와 그 전용 storage를 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. source cluster와 tracked volumes는 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 source version, `/_membership`, `/_all_dbs`, shard placement, per-database `_security`, document-count invariants, configuration과 system database 범위를 기록한다. admin password와 Erlang cookie 값은 evidence에서 제외한다.
2. preferred path는 database replication이다. 승인된 fresh target으로 application databases와 필요한 system databases를 복제하고 completion/error state를 기록한다.
3. file backup을 선택한 경우 source를 일관되게 quiesce한 뒤 config, cluster metadata including `_dbs`, shard/database files, indexes, `_users`, `_replicator`, `_global_changes`를 checksum과 함께 보존한다. running `.couch` files를 복사하지 않는다.
4. production network/volumes를 공유하지 않는 호환 버전의 빈 3-node target을 준비한다. 별도 test admin/cookie를 사용하고 동일한 node count/shard assumptions를 명시한다.
5. file restore에서는 upstream 순서대로 index files를 database files보다 먼저 배치하고, config/metadata/data ownership을 검증한 뒤 target만 시작한다. replication path에서는 security objects와 system database scope를 별도로 확인한다.
6. `/_up`, `/_membership`, `/_all_dbs`, shard maps, per-database document counts, representative reads, `_security`, replication scheduler를 검증한다. 불일치가 있으면 target을 승격하지 않고 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다.

## Evidence

- 명령 이름, pass/fail 상태, service 상태, image tag, 민감 정보를 제거한 log와 membership 요약을 기록한다.
- secret 값, cookie 값 또는 민감한 field를 포함한 인증된 HTTP 전체 출력은 기록하지 않는다.
- runtime session에 선택한 profile을 기록한다. root 파일은 CouchDB compose 파일을 조건 없이 포함하며 실제 service 구성에 포함되는지는 `couchdb` profile이 결정한다.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. production cutover, membership 변경, cookie rotation은 별도 승인 사항이며 이 변경에서는 실행하지 않았다.

## Escalation

membership에 예상한 node 3개가 나타나지 않거나, cluster-init이 반복 실패하거나, Traefik route 전제가 compose label과 다르거나, secret 노출 위험이 있거나, data 작업이 필요하면 저장소 소유자 @buenhyden에게 에스컬레이션한다. 민감 정보를 제거한 log, membership 요약, 렌더링된 compose evidence, service 상태와 시도한 단계를 포함한다.

## Traceability

- Declared parent: [CouchDB Usage Guide](../guides/0026-couchdb.md) (`GDE-0026`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0026-couchdb.md) (`GDE-0026`), [Policy](../policies/0026-couchdb.md) (`POL-0026`)

## Related Documents

- [Compose implementation: infra/04-data/couchdb/docker-compose.yml](../../../infra/04-data/couchdb/docker-compose.yml)

- [CouchDB backup guidance](https://docs.couchdb.org/en/stable/maintenance/backups.html)
- [CouchDB upgrade guidance](https://docs.couchdb.org/en/stable/install/upgrading.html)
- [CouchDB database security](https://docs.couchdb.org/en/stable/api/database/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0026-couchdb.md)
- [Operations policy](../policies/0026-couchdb.md)
- [Infra README](../../../infra/04-data/couchdb/README.md)
