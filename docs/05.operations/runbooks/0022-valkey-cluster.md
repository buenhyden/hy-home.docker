---
title: "Valkey Cluster Health Runbook"
version: "2.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "operations"
artifact_id: "RUN-0022"
parent_ids:
- "GDE-0022"
created: "2026-05-17"
---

# Valkey Cluster Health and Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

이 subject의 승인된 static diagnosis, backup 계획, isolated recovery에
사용한다. live write, restore, cutover, cleanup, credential 변경은 별도로
승인된 task가 필요하다.

### Scope

static validation은 이 문서화 task에서 안전하게 수행할 수 있다. cluster
시작, 데이터 쓰기, live backup, restore, membership 변경은 계획된 operator
작업이며 실행하지 않았다.

### Execution and stop boundary

대상: `valkey-cluster-exporter`, `valkey-cluster-init`, `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

LAB 기동·정지는 `scripts/operations/lab.py`만 사용한다(`up valkey-cluster --purpose ... --lease ...`, `down valkey-cluster`, 만료 lease는 `reap`). 이 명령은 다른 LAB·HOME과의 충돌, 선언 한도 예산과 동시 LAB 수를 먼저 검사하고 `${LAB_DATA_DIR}/.ledger/valkey-cluster.json`에 정리 대상을 남기며, 정지는 이 project만 `-v` 없이 수행한다(SPEC-0215). 2026-10-08 합성 data·secret root로 `up`·`check`·`reap`을 실제 실행해 6 node `cluster_state:ok`, 동시 LAB 거부, container·network 0개 정리와 data 보존을 확인했다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

### Procedure

정적 검사는 `labs/.env.example`과 `labs/valkey-cluster.yml`을 사용한다. 실제 점검은 승인된 Docker context·project·port·network·volume·용량·정리 범위를 확인하고, 비공개 `labs/.env`를 준비한 뒤 `LAB_ENV_FILE`을 그 파일로 설정해야 한다. 이번 소스 작업에서 컨테이너 실행과 복구는 `NOT_RUN`이다.

repository root에서 독립 LAB 파일을 지정해 정적 렌더링한다. `labs/.env.example`은 합성 입력만 담고 실제 `labs/.env`와 secret은 실행 승인 후 별도 준비한다.

```bash
LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/valkey-cluster.yml --profile valkey-cluster config --quiet
LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/valkey-cluster.yml --profile valkey-cluster config --services
```

6개 node service, init job, exporter; 6개의 서로 다른 data volume; `lab_valkey_core_net`/`lab_valkey_obs_net`;
password secret; node health check; 기본 loopback host 17379–17384 → 내부 6379–6384 client와 16379–16384 bus
exposure을 확인한다. rendered 경로가 비어 있거나 예상과 다르면 중단한다.

### Planned backup procedure

1. 승인된 maintenance window를 열고 application writer를 식별한다.
2. engine/image source, cluster node ID, slot ownership, primary/replica
   관계, persistence mode를 기록한다. write를 일시 정지하거나 명시적으로
   합의한 consistency point를 정한다.
3. 각 primary에서 RDB checkpoint를 요청하고 검증한다. 완전한 RDB, 그리고 활성화된
   경우 모든 AOF base/increment 파일과 manifest를 한 세트로 복사한다.
   rewrite 중인 AOF는 복사하지 않는다.
4. configuration과 cluster metadata의 diagnostic copy를 포함하되,
   `nodes.conf`는 재사용할 파일이 아니라 source identity로 표시한다.
5. node role, timestamp, file size, checksum의 manifest를 작성한다. 세트는
   custody가 제한된 별도의 encrypted 목적지로 전송한다.

### Planned isolated restore

1. persistence-compatible Valkey version과 disposable credential을 사용해
   비어 있고 network-isolated된 6-node target을 준비한다. application
   client는 연결하지 않는다.
2. 새 cluster identity로 의도한 three-primary/three-replica topology를
   재구성한다. 각 primary backup을 문서화된 slot owner에 mapping하고
   관련 없는 node set은 절대 병합하지 않는다.
3. target node를 정지한 상태에서 완전한 persistence 세트 각각을 올바른
   ownership으로 빈 data 디렉터리에 배치한다. live `nodes.conf`는 재사용하지
   않는다.
4. isolated target만 시작한다. AOF loading이 truncation이나 repair 없이
   완료되는지, `cluster_state`가 healthy한지, 모든 slot이 커버되는지,
   replica가 의도한 primary에 연결되는지 확인한다.
5. slot/key count와 선택된 값을 manifest와 비교한 뒤, disposable
   cluster-aware client로 read/write/delete test를 실행한다.
6. 관찰된 recovery point와 소요 시간을 기록한다. 별도로 승인된 cutover는
   writer를 일시 정지하고, 최종 backup을 만들고, client를 전환하고,
   검증하고, rollback을 위해 이전 상태를 보존해야 한다.

## Verification

### Evidence

source revision/version, scope, timestamp, manifest/checksum 요약, command와
exit status, validation 결과, 관찰된 recovery point/time, 모든 미검증
gap을 기록한다. secret, raw payload, 비공개 resolved 경로는 제외한다.

## Rollback and Escalation

### Rollback or Recovery

실패한 cutover는 identity와 write boundary를 검증한 뒤 client를 보존된 원본
cluster로 되돌린다. backup 세트와 isolated target은 그대로 보존한다.
cutover는 owner approval, 최종 consistency capture, application validation,
보존된 rollback window를 거친 뒤에만 진행한다.

### Escalation

AOF segment 누락, checksum mismatch, 예기치 않은 identity, 커버되지 않은
slot, replica drift, persistence를 repair/truncate하라는 요청이 있으면
중단한다. secret 값 없이 로그를 보존하고 data @buenhyden에게 escalation한다.

### Traceability

- Runtime source: [Valkey Cluster Compose](../../../labs/valkey-cluster.yml).
- Artifact: `RUN-0022`; parent guide: `GDE-0022`.
- dated verification record가 실행 사실을 명시하지 않는 한, 이 절차는 계획 단계다.

### References

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial](https://valkey.io/topics/cluster-tutorial/)
- [Policy](../policies/0022-valkey-cluster.md)

## Related Documents

- [Domain catalog](../README.md)
