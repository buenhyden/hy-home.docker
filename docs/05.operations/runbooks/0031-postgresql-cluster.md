---
title: "PostgreSQL Cluster Health and Recovery Triage Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0031"
parent_ids:
- "GDE-0031"
created: "2026-05-17"
---

# PostgreSQL Cluster Health and Recovery Triage Runbook

## Overview

> Scope: Triage optional PostgreSQL HA cluster health, etcd quorum symptoms, HAProxy routing, Patroni leadership, init job state, and exporter readiness without destructive data actions.

이 런북은 현재 compose 기준 health triage와, [RUN-0032](0032-postgresql-logical-upgrade-restore-rehearsal.md)에 위임한 logical backup의 격리 복원 계약을 제공한다. 이번 문서 변경에서 database 명령은 실행하지 않았다.

### Purpose

PostgreSQL HA cluster의 서비스 상태와 routing/leadership evidence를 수집하고, compose가 보장하는 범위 안에서만 비파괴 재기동과 상태 확인을 수행한다.

## When to Use

- `pg-router` write/read endpoint가 응답하지 않을 때
- `patronictl list`에서 leader/member 상태 확인이 필요할 때
- etcd node, PostgreSQL node, exporter, or `pg-cluster-init` 상태가 unhealthy/stopped일 때
- PostgreSQL cluster operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose의 `include:` 목록과 exact `postgres-ha` profile을 기록한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] DCS data deletion, forced cluster bootstrap, leadership mutation, backup restore, credential rotation, database mutation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 credential, SQL payload, application data는 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile postgres-ha config --quiet
   ```

2. 전체 서비스 상태를 확인한다.

   ```bash
   docker compose ps etcd-1 etcd-2 etcd-3 pg-router pg-cluster-init pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

3. etcd endpoint health를 각 etcd container에서 확인한다.

   ```bash
   docker exec etcd-1 etcdctl endpoint health --endpoints=http://127.0.0.1:${ETCD_CLIENT_PORT:-2379}
   ```

4. Patroni leadership을 확인한다.

   ```bash
   docker exec pg-0 patronictl -c /home/postgres/postgres.yml list
   ```

5. HAProxy와 init job 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 pg-router pg-cluster-init
   ```

6. PostgreSQL node와 exporter 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

7. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 해당 서비스만 재기동한다. 예시는 `pg-router` 기준이며, 대상 서비스명은 현재 `docker compose ps` 결과에서 확인한 declared service로 제한한다.

   ```bash
   docker compose --profile postgres-ha up -d pg-router
   ```

### Verification Steps

- `docker compose ps ...`에서 intended services가 running 또는 healthy 상태인지 확인한다.
- `patronictl list`에서 leader와 members가 표시되는지 확인한다.
- `pg-router` 로그와 HAProxy config validation healthcheck가 정상인지 확인한다.
- exporter logs 또는 `/metrics` checks가 secret 값을 출력하지 않고 정상 evidence를 제공하는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 pg-router pg-cluster-init pg-0 pg-1 pg-2`
- **Cluster state**: `patronictl list`
- **DCS state**: `etcdctl endpoint health`
- **Routing**: HAProxy stats route `pg-haproxy.${DEFAULT_URL}` and HAProxy healthcheck
- **Metrics**: `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d` for stopped declared services after evidence capture.
3. 실패한 격리 cluster와 전용 volumes를 폐기한다. source cluster, DCS와 tracked volumes는 변경하지 않는다.

### Planned Isolated Logical Restore

1. 사전 승인 후 source PostgreSQL/extension versions, databases, roles, ownership/ACLs, tablespaces, row-count invariants, Patroni topology와 free capacity를 기록한다. credential values는 기록하지 않는다.
2. primary write endpoint에서 protected credential handling으로 `pg_dumpall --globals-only`를 실행하고, 각 in-scope database를 custom/directory format으로 dump한다. manifests/checksums와 tool/server versions를 함께 보존한다.
3. production network/ports/volumes를 공유하지 않는 compatible empty `postgres-ha` target을 별도 secrets로 구성한다. Patroni/etcd membership은 새로 bootstrap하며 source DCS files나 live PGDATA를 복사하지 않는다.
4. globals/roles를 먼저 복원하고 databases, extensions/schema/data, ownership/ACLs 순으로 적재한다. 자세한 명령과 acceptance evidence는 `RUN-0032`를 따른다.
5. `patronictl list`, write/read routing through `pg-router`, roles/ACLs, extensions, schemas, sequences, row-count invariants와 representative transactions를 검증한다.
6. 실패하면 target을 승격하지 않고 폐기한다. production cutover, route change, secret rotation과 DCS mutation은 별도 승인 사항이다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `python3 scripts/validation/check-document-links.py --mode all` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, sanitized logs, and leadership/routing summary.
- Do not capture secret values, SQL payloads, database row contents, or credential-backed connection strings.
- Record that `postgres-ha` was selected; the root file includes the cluster compose file unconditionally.

## Rollback or Recovery

Logical recovery는 위 contract와 `RUN-0032`에서만 검증한다. 이 변경에서는 backup/restore, DCS reset, leadership mutation, credential rotation이나 volume replacement를 실행하지 않았다.

## Escalation

Escalate to the owning operator when no leader can be identified, etcd quorum symptoms appear, HAProxy routing diverges from compose, `pg-cluster-init` repeatedly fails, logs show storage corruption, secret exposure risk appears, or any data operation is required. Include sanitized logs, rendered compose evidence, service states, leadership summary, and attempted steps.

## Traceability

- Declared parent: [PostgreSQL Cluster Usage Guide](../guides/0031-postgresql-cluster.md) (`GDE-0031`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0031-postgresql-cluster.md) (`GDE-0031`), [Policy](../policies/0031-postgresql-cluster.md) (`POL-0031`)

## Related Documents

- [Compose implementation: infra/04-data/relational/postgresql-cluster/docker-compose.yml](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml)

- [PostgreSQL pg_dumpall reference](https://www.postgresql.org/docs/18/app-pg-dumpall.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Logical upgrade restore rehearsal](0032-postgresql-logical-upgrade-restore-rehearsal.md) (`RUN-0032`)

- [Operations index](../README.md)
- [Usage guide](../guides/0031-postgresql-cluster.md)
- [Operations policy](../policies/0031-postgresql-cluster.md)
- [Infra README](../../../infra/04-data/relational/postgresql-cluster/README.md)
