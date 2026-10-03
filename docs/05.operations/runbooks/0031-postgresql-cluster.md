---
title: "PostgreSQL Cluster Health and Recovery Triage Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "operations"
artifact_id: "RUN-0031"
parent_ids:
- "GDE-0031"
created: "2026-05-17"
---

# PostgreSQL Cluster Health and Recovery Triage Runbook

## Overview

> Scope: Triage optional PostgreSQL HA cluster health, etcd quorum symptoms, HAProxy routing, Patroni leadership, init job state, and exporter readiness without destructive data actions.

이 런북은 현재 compose 기준 health triage와, 아직 실행 구현이 없는 실제 HA logical backup의 필수 격리 복원 계약을 제공한다. 이번 문서 변경에서 database 명령은 실행하지 않았다.

### Purpose

PostgreSQL HA cluster의 서비스 상태와 routing/leadership evidence를 수집하고, 승인된 상태 확인으로 범위를 좁힌다. 상태 triage는 재기동을 승인하지 않는다.

## When to Use

- `pg-router` write/read endpoint가 응답하지 않을 때
- `patronictl list`에서 leader/member 상태 확인이 필요할 때
- etcd node, PostgreSQL node, exporter, or `pg-cluster-init` 상태가 unhealthy/stopped일 때
- PostgreSQL cluster operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

### Execution and stop boundary

대상: `etcd-1`, `etcd-2`, `etcd-3`, `pg-0`, `pg-0-exporter`, `pg-1`, `pg-1-exporter`, `pg-2`, `pg-2-exporter`, `pg-cluster-init`, `pg-router`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

정적 검사는 `labs/.env.example`과 `labs/postgresql-ha.yml`을 사용한다. 실제 점검은 승인된 Docker context·project·port·network·volume·용량·정리 범위를 확인하고, 비공개 `labs/.env`를 준비한 뒤 `LAB_ENV_FILE`을 그 파일로 설정해야 한다. 이번 소스 작업에서 컨테이너 실행과 복구는 `NOT_RUN`이다.

### Checklist

- [ ] `labs/postgresql-ha.yml`의 독립 project와 `postgres-ha` profile을 확인하고 root include에서 제외됐는지 기록한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] DCS data deletion, forced cluster bootstrap, leadership mutation, backup restore, credential rotation, database mutation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 credential, SQL payload, application data는 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/postgresql-ha.yml --profile postgres-ha config --quiet
   ```

2. 전체 서비스 상태를 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml ps etcd-1 etcd-2 etcd-3 pg-router pg-cluster-init pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

3. etcd endpoint health를 각 etcd container에서 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml exec etcd-1 etcdctl endpoint health --endpoints=http://127.0.0.1:${LAB_PG_ETCD_CLIENT_PORT:-2379}
   ```

4. Patroni leadership을 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml exec pg-0 patronictl -c /home/postgres/postgres.yml list
   ```

5. HAProxy와 init job 로그를 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml logs --tail=120 pg-router pg-cluster-init
   ```

6. PostgreSQL node와 exporter 로그를 확인한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml logs --tail=120 pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

7. `pg-router`만 stopped이고 etcd/Patroni 의존성이 이미 정상이며 owner가 해당 router 재기동을 승인한 경우에만 아래를 사용한다. init, DCS, PostgreSQL member는 이 예시의 대체 대상이 아니다. 의존성 불명·leader 부재면 중단한다.

   ```bash
   docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml --profile postgres-ha up -d --no-deps pg-router
   ```

### Verification Steps

- `docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml ps ...`에서 intended services가 running 또는 healthy 상태인지 확인한다.
- `patronictl list`에서 leader와 members가 표시되는지 확인한다.
- `pg-router` 로그와 HAProxy config validation healthcheck가 정상인지 확인한다.
- exporter logs 또는 `/metrics` checks가 secret 값을 출력하지 않고 정상 evidence를 제공하는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose --env-file "$LAB_ENV_FILE" -f labs/postgresql-ha.yml logs --tail=120 pg-router pg-cluster-init pg-0 pg-1 pg-2`
- **Cluster state**: `patronictl list`
- **DCS state**: `etcdctl endpoint health`
- **Routing**: HAProxy healthcheck; 이전 stats label은 HOME gateway와 연결되지 않음
- **Metrics**: `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`

### Safe Rollback or Recovery Procedure

1. 승인된 router-only 재생성만 위 조건에서 가능하다. `pg-cluster-init` 재실행은 role/database mutation이며 triage나 rollback이 아니다.
2. 실패한 격리 cluster와 전용 volumes를 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. source cluster, DCS와 tracked volumes는 변경하지 않는다.

### Planned Isolated Logical Restore

1. 사전 승인 후 source PostgreSQL/extension versions, databases, roles, ownership/ACLs, tablespaces, row-count invariants, Patroni topology와 free capacity를 기록한다. credential values는 기록하지 않는다.
2. primary write endpoint에서 protected credential handling으로 `pg_dumpall --globals-only`를 실행하고, 각 in-scope database를 custom/directory format으로 dump한다. manifests/checksums와 tool/server versions를 함께 보존한다.
3. production network/ports/volumes를 공유하지 않는 compatible empty `postgres-ha` target을 별도 secrets로 구성한다. Patroni/etcd membership은 새로 bootstrap하며 source DCS files나 live PGDATA를 복사하지 않는다.
4. globals/roles를 먼저 복원하고 databases, extensions/schema/data, ownership/ACLs 순으로 적재한다. 이 HA 계약을 구현한 tracked restore command/harness는 없다. 아래 acceptance를 갖춘 별도 승인·stateful review 전 실제 복원은 BLOCKED다.
5. `patronictl list`, write/read routing through `pg-router`, roles/ACLs, extensions, schemas, sequences, row-count invariants와 representative transactions를 검증한다.
6. 실패하면 target을 승격하지 않고 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. production cutover, route change, secret rotation과 DCS mutation은 별도 승인 사항이다.

## Evidence

- 명령 이름, pass/fail 상태, service 상태, image tag, 민감 정보를 제거한 log와 leadership/routing 요약을 기록한다.
- secret 값, SQL payload, database row 내용 또는 credential을 담은 connection string은 기록하지 않는다.
- `postgres-ha`를 선택했음을 기록한다. root는 `labs/postgresql-ha.yml`을 include하지 않는다.

## Rollback or Recovery

위 HA 계약은 미구현이다. RUN-0032는 별도 fixture 한 DB의 synthetic PG17→18 logical rehearsal이며 `--no-owner --no-acl`을 사용하고 globals/roles, 모든 DB, Patroni/etcd, pg-router를 복원·검증하지 않는다. 성공해도 이 HA 계약의 acceptance가 아니다. 이 변경에서는 backup/restore, DCS reset, leadership mutation, credential rotation이나 volume replacement를 실행하지 않았다.

## Escalation

leader를 확인할 수 없거나, etcd quorum 관련 증상이 나타나거나, HAProxy routing이 compose와 다르거나, `pg-cluster-init`이 반복 실패하거나, log에 storage 손상이 나타나거나, secret 노출 위험이 있거나, data 작업이 필요하면 저장소 소유자 @buenhyden에게 에스컬레이션한다. 민감 정보를 제거한 log, 렌더링된 compose evidence, service 상태, leadership 요약과 시도한 단계를 포함한다.

## Traceability

- Declared parent: [PostgreSQL Cluster Usage Guide](../guides/0031-postgresql-cluster.md) (`GDE-0031`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0031-postgresql-cluster.md) (`GDE-0031`), [Policy](../policies/0031-postgresql-cluster.md) (`POL-0031`)

## Related Documents

- [Compose implementation: labs/postgresql-ha.yml](../../../labs/postgresql-ha.yml)

- [PostgreSQL pg_dumpall reference](https://www.postgresql.org/docs/18/app-pg-dumpall.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Logical upgrade restore rehearsal](0032-postgresql-logical-upgrade-restore-rehearsal.md) (`RUN-0032`)

- [Operations index](../README.md)
- [Usage guide](../guides/0031-postgresql-cluster.md)
- [Operations policy](../policies/0031-postgresql-cluster.md)
- [Infra README](../../../labs/postgresql-ha.md)
