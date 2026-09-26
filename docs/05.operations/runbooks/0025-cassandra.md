---
title: "Cassandra Health and Recovery Triage Runbook"
version: "1.1.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
artifact_id: "RUN-0025"
parent_ids:
- "GDE-0025"
created: "2026-05-17"
---

# Cassandra Health and Recovery Triage Runbook

## Overview

> Scope: Triage Cassandra single-node runtime health, collect evidence, and perform only verified non-destructive recovery steps.

이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 Cassandra snapshot의 격리 복원 rehearsal 계약을 제공한다. 아래 데이터 명령은 이번 문서 변경에서 실행하지 않았다.

### Purpose

Cassandra 단일 노드 선택 서비스의 장애 증거를 빠르게 수집하고, compose가 보장하는 범위 안에서만 서비스를 재기동하거나 확인한다.

## When to Use

- `cassandra-node1`가 unhealthy, stopped, or missing 상태일 때
- `nodetool status`가 expected `UN` 상태를 반환하지 않을 때
- `cassandra-exporter`가 Cassandra health 이후에도 metrics endpoint를 제공하지 않을 때
- NoSQL operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose의 `include:` 목록과 정확한 `cassandra` profile을 기록한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] 데이터 복원, snapshot 교체, 볼륨 이동, credential rotation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 secret 값은 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile cassandra config --quiet
   ```

2. 컨테이너 상태를 확인한다.

   ```bash
   docker compose ps cassandra-node1 cassandra-exporter
   ```

3. Cassandra 로그에서 시작/health 관련 오류를 확인한다.

   ```bash
   docker compose logs --tail=120 cassandra-node1
   ```

4. 노드 상태를 확인한다.

   ```bash
   docker exec cassandra-node1 nodetool status
   ```

5. 컨테이너가 stopped 상태이고 데이터 복구 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile cassandra up -d cassandra-node1 cassandra-exporter
   ```

6. read-only CQL 확인을 수행한다.

   ```bash
   docker exec cassandra-node1 sh -lc 'cqlsh -u "$CASSANDRA_USER" -p "$(cat /run/secrets/cassandra_password)" -e "SELECT cluster_name, release_version FROM system.local;"'
   ```

### Verification Steps

- `docker compose ps cassandra-node1 cassandra-exporter`에서 `cassandra-node1`가 healthy 또는 running 상태인지 확인한다.
- `docker exec cassandra-node1 nodetool status`에서 node state가 `UN`인지 확인한다.
- read-only CQL query가 secret 값을 출력하지 않고 정상 종료되는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 cassandra-node1`, `docker compose logs --tail=120 cassandra-exporter`
- **Metrics**: `cassandra-exporter` exposed ports `${CASSANDRA_EXPORTER_PORT:-8080}` and `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}`
- **Config**: `docker compose ... config --quiet` rendered output without secret values

### Safe Rollback or Recovery Procedure

1. Runtime recovery in this runbook is limited to compose `up -d` for the declared services after evidence capture.
2. 복원 실패 시 격리 target과 그 전용 빈 volume을 폐기한다. source snapshot이나 tracked data volume은 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인과 유지보수 창을 확보하고 source release, keyspace/schema/replication, `nodetool status`, token/topology, snapshot tag를 기록한다. `/run/secrets/cassandra_password` 값은 evidence에 남기지 않는다.
2. 승인된 source에서 flush 후 `nodetool snapshot -t <backup-id>`를 수행한다. 각 keyspace/table snapshot SSTable, generated `schema.cql`, manifest/checksum을 하나의 immutable backup set으로 보존한다. running data directory를 `cp`하지 않는다.
3. production과 network/data volume을 공유하지 않는 빈 single-node target을 같은 호환 release와 `cassandra` topology로 준비한다. 별도 test credential을 사용한다.
4. `schema.cql`로 application schema를 먼저 생성한 뒤, upstream 문서에 따라 `sstableloader` 또는 올바른 table directory에 배치 후 `nodetool refresh`로 SSTable을 적재한다. system/local topology files를 source에서 복사하지 않는다.
5. `nodetool status`, keyspace/table 목록, schema agreement, representative partition reads와 expected row/count invariants를 확인한다. auth/role 복구가 범위에 포함되면 별도 보호된 role evidence로 검증한다.
6. 하나라도 실패하면 target을 데이터 원본으로 승격하지 않고 폐기한다. 성공 evidence에는 backup-id, release, schema hash, 검증 query와 결과 요약을 남긴다.

## Evidence

- Capture command names, pass/fail status, service states, image tags, and sanitized log summaries.
- Do not capture secret values or full secret-backed command output.
- Record that `cassandra` was selected; the root file includes the Cassandra compose file unconditionally.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이 저장소 변경에서는 backup/restore를 실행하지 않았으며, production cutover와 credential rotation은 별도 승인 사항이다.

## Escalation

Escalate to the owning operator when `nodetool status` does not return `UN`, logs show storage corruption, a restore is required, secret exposure risk appears, or the observed service set differs from `cassandra-node1` plus `cassandra-exporter`. Include sanitized logs, rendered compose evidence, service states, and attempted steps.

## Traceability

- Declared parent: [Cassandra Usage Guide](../guides/0025-cassandra.md) (`GDE-0025`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0025-cassandra.md) (`GDE-0025`), [Policy](../policies/0025-cassandra.md) (`POL-0025`)

## Related Documents

- [Compose implementation: infra/04-data/nosql/cassandra/docker-compose.yml](../../../infra/04-data/nosql/cassandra/docker-compose.yml)

- [Cassandra backup and restore](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
- [Cassandra security](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0025-cassandra.md)
- [Operations policy](../policies/0025-cassandra.md)
- [Infra README](../../../infra/04-data/nosql/cassandra/README.md)
