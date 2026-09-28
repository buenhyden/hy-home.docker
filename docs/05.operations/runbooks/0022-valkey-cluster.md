---
title: "Valkey Cluster Health Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0022"
parent_ids:
- "GDE-0022"
created: "2026-05-17"
---

# Valkey Cluster Health and Recovery Runbook

## When to Use

이 subject의 승인된 static diagnosis, backup 계획, isolated recovery에
사용한다. live write, restore, cutover, cleanup, credential 변경은 별도로
승인된 task가 필요하다.

### Scope

static validation은 이 문서화 task에서 안전하게 수행할 수 있다. cluster
시작, 데이터 쓰기, live backup, restore, membership 변경은 계획된 operator
작업이며 실행하지 않았다.

## Procedure

repository root에서 실행한다.

```bash
docker compose --env-file .env.example --profile valkey-cluster config --quiet
docker compose --env-file .env.example --profile valkey-cluster config --services
```

6개 node service, init job, exporter; 6개의 서로 다른 data volume; `lab_net`;
password secret; node health check; 6379–6384 client와 16379–16384 bus
mapping을 확인한다. rendered 경로가 비어 있거나 예상과 다르면 중단한다.

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

## Evidence

source revision/version, scope, timestamp, manifest/checksum 요약, command와
exit status, validation 결과, 관찰된 recovery point/time, 모든 미검증
gap을 기록한다. secret, raw payload, 비공개 resolved 경로는 제외한다.

## Rollback or Recovery

실패한 cutover는 identity와 write boundary를 검증한 뒤 client를 보존된 원본
cluster로 되돌린다. backup 세트와 isolated target은 그대로 보존한다.
cutover는 owner approval, 최종 consistency capture, application validation,
보존된 rollback window를 거친 뒤에만 진행한다.

## Escalation

AOF segment 누락, checksum mismatch, 예기치 않은 identity, 커버되지 않은
slot, replica drift, persistence를 repair/truncate하라는 요청이 있으면
중단한다. secret 값 없이 로그를 보존하고 data owner에게 escalation한다.

## Traceability

- Runtime source: [Valkey Cluster Compose](../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml).
- Artifact: `RUN-0022`; parent guide: `GDE-0022`.
- dated verification record가 실행 사실을 명시하지 않는 한, 이 절차는 계획 단계다.

### References

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial](https://valkey.io/topics/cluster-tutorial/)
- [Policy](../policies/0022-valkey-cluster.md)

## Related Documents

- [Domain catalog](../README.md)
