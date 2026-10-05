---
title: "Cassandra Health and Recovery Triage Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0025"
parent_ids:
- "GDE-0025"
created: "2026-05-17"
---

# Cassandra Health and Recovery Triage Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

독립 Cassandra 단일 노드 LAB의 정적 점검과 승인 후 read-only triage 순서다. 이번 변경에서 실제 서비스·데이터를 실행하지 않았다.

### When to Use

`cassandra-node1`의 선언·건강·데이터 경로를 점검하거나 격리 복구 범위를 설계할 때 사용한다.

### Execution and stop boundary

실제 명령 전에 Docker context, 독립 Compose project, port, network, `${LAB_DATA_DIR}/cassandra/node1`, 용량, 기존 anonymous volume 소유자와 정확한 정리 범위를 확인한다. 무인증 내부 CQL이므로 신뢰하지 않는 peer를 연결하지 않는다. 기동·중단·복원·삭제는 별도 승인이다. 로그 원문과 비밀값은 증거에 복사하지 않는다.

## Procedure

### Procedure

### Checklist

- [ ] root include에 LAB가 없고 `labs/cassandra.yml`만 서비스 정의를 소유하는지 확인한다.
- [ ] `/var/lib/cassandra` mount와 `lab_cassandra_core_net`의 peer를 확인한다.
- [ ] 과거 데이터·snapshot 소유권을 확인하기 전 재생성·정리를 중단한다.

### Steps

1. 정적 구성만 확인한다.

   ```bash
   LAB_DATA_DIR=/tmp/hy-home-lab-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile cassandra config --quiet
   ```

2. 별도 실행 승인이 있을 때만 지정한 `labs/.env`와 context에서 `ps cassandra-node1`, `exec cassandra-node1 nodetool status`를 수행한다. `UN`은 프로세스 상태이며 인증·읽기·복원을 증명하지 않는다.
3. CQL 확인은 승인된 격리 peer에서 읽기 전용으로 시행한다. 현재 무인증임을 기록한다.

### Verification Steps

정적 렌더 exit code와 source SHA를 기록한다. 실제 node·CQL·restore는 수행하지 않았다면 `NOT_RUN`으로 남긴다.

### Observability and Evidence Sources

Compose health와 요약된 node 상태를 사용한다. exporter는 현재 LAB에 없다.

### Safe Rollback or Recovery Procedure

소스 rollback은 데이터 rollback이 아니다. 별도 승인된 빈 target, 호환 release와 schema, snapshot tag/SSTable 전체, owner·권한·건수 점검으로 격리 복원을 검증한다. 기존 volume을 덮어쓰거나 `down -v`를 실행하지 않는다.

## Verification

### Evidence

정적 명령·종료 코드·source SHA만 기록한다. 실제 상태 조회와 복원 증거는 별도 실행 승인 후 기록한다.

## Rollback and Escalation

### Rollback or Recovery

소스 rollback은 데이터 rollback이 아니다. 기존 데이터를 보존하고 빈 격리 대상에 호환 snapshot 전체를 복원해 검증한다.

### Escalation

데이터 소유권, 용량, 인증 필요성, 복구 세트가 불명확하면 @buenhyden에게 정확한 대상과 증거를 전달하고 mutation을 보류한다.

### Traceability

- Declared parent: [GDE-0025](../guides/0025-cassandra.md)
- Governing policy: [POL-0025](../policies/0025-cassandra.md)

## Related Documents

- [Guide](../guides/0025-cassandra.md)
- [Policy](../policies/0025-cassandra.md)
- [LAB 설명](../../../labs/cassandra.md)
