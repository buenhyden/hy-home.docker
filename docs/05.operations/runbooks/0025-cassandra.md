---
title: "Cassandra Health and Recovery Triage Runbook"
version: "1.1.4"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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


### Execution and stop boundary

대상: `cassandra-exporter`, `cassandra-node1`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

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
   # STOP: reconcile official-image auth and /var/lib/cassandra ownership before activation/recreate
   ```

6. read-only CQL 확인을 수행한다.

   인증된 읽기 점검은 declared client/version, 승인된 endpoint/CA, TTY와 password 비노출 입력 방법을 먼저 확인한 뒤 진행한다. 기존 secret→URL/argv 예시는 사용하지 않는다. 이 전제가 입증되지 않으면 점검을 중단하고 @buenhyden에게 전달한다. 성공 응답만으로 무인증/오인증 거부를 증명하지 않는다.

### Verification Steps

- `docker compose ps cassandra-node1 cassandra-exporter`에서 `cassandra-node1`가 healthy 또는 running 상태인지 확인한다.
- `docker exec cassandra-node1 nodetool status`에서 node state가 `UN`인지 확인한다.
- read-only CQL query가 secret 값을 출력하지 않고 정상 종료되는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 cassandra-node1`, `docker compose logs --tail=120 cassandra-exporter`
- **Metrics**: `cassandra-exporter` exposed ports `${CASSANDRA_EXPORTER_PORT:-8080}` and `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}`
- **Config**: `docker compose ... config --quiet` rendered output without secret values

### Safe Rollback or Recovery Procedure

1. 이 triage는 data daemon의 무조건 재기동이나 init 재실행을 승인하지 않는다. 위 source 한계와 named-target lifecycle 승인을 먼저 확인한다.
2. 복원 실패 시 격리 target과 그 전용 빈 volume을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. source snapshot이나 tracked data volume은 변경하지 않는다.

### Planned Isolated Restore Rehearsal

아래 SSTable 계약은 보존 요구이며 현재 activation/restore는 BLOCKED다. 공식 image의auth와actualdata경로를 먼저 별도 source 변경으로 맞추고 기존 anonymous-volume 소유권을 승인된 방식으로 확정해야 한다. mounted Bitnami 경로의backup을현재data라고 가정하지 않는다.


1. 사전 승인과 유지보수 창을 확보하고 source release, keyspace/schema/replication, `nodetool status`, token/topology, snapshot tag를 기록한다. `/run/secrets/cassandra_password` 값은 evidence에 남기지 않는다.
2. 승인된 source에서 flush 후 `nodetool snapshot -t <backup-id>`를 수행한다. 각 keyspace/table snapshot SSTable, generated `schema.cql`, manifest/checksum을 하나의 immutable backup set으로 보존한다. running data directory를 `cp`하지 않는다.
3. production과 network/data volume을 공유하지 않는 빈 single-node target을 같은 호환 release와 `cassandra` topology로 준비한다. 별도 test credential을 사용한다.
4. `schema.cql`로 application schema를 먼저 생성한 뒤, upstream 문서에 따라 `sstableloader` 또는 올바른 table directory에 배치 후 `nodetool refresh`로 SSTable을 적재한다. system/local topology files를 source에서 복사하지 않는다.
5. `nodetool status`, keyspace/table 목록, schema agreement, representative partition reads와 expected row/count invariants를 확인한다. auth/role 복구가 범위에 포함되면 별도 보호된 role evidence로 검증한다.
6. 하나라도 실패하면 target을 데이터 원본으로 승격하지 않고 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. 성공 evidence에는 backup-id, release, schema hash, 검증 query와 결과 요약을 남긴다.

## Evidence

- 명령 이름, pass/fail 상태, service 상태, image tag와 민감 정보를 제거한 log 요약을 기록한다.
- secret 값이나 secret을 사용하는 명령의 전체 출력은 기록하지 않는다.
- `cassandra`를 선택했음을 기록한다. root 파일은 Cassandra compose 파일을 조건 없이 포함한다.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이 저장소 변경에서는 backup/restore를 실행하지 않았으며, production cutover와 credential rotation은 별도 승인 사항이다.

## Escalation

`nodetool status`가 `UN`을 반환하지 않거나, log에 storage 손상이 나타나거나, restore가 필요하거나, secret 노출 위험이 있거나, 관찰된 service 구성이 `cassandra-node1`과 `cassandra-exporter`의 조합과 다르면 저장소 소유자 @buenhyden에게 에스컬레이션한다. 민감 정보를 제거한 log, 렌더링된 compose evidence, service 상태와 시도한 단계를 포함한다.

## Traceability

- Declared parent: [Cassandra Usage Guide](../guides/0025-cassandra.md) (`GDE-0025`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0025-cassandra.md) (`GDE-0025`), [Policy](../policies/0025-cassandra.md) (`POL-0025`)

## Related Documents

- [Compose implementation: infra/04-data/cassandra/docker-compose.yml](../../../infra/04-data/cassandra/docker-compose.yml)

- [Cassandra backup and restore](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
- [Cassandra security](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0025-cassandra.md)
- [Operations policy](../policies/0025-cassandra.md)
- [Infra README](../../../infra/04-data/cassandra/README.md)
