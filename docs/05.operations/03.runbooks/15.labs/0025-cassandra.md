---
title: "Cassandra Health and Recovery Triage Runbook"
version: "2.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0025"
parent_ids:
- "GDE-0025"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Cassandra Health and Recovery Triage Runbook

## Trigger and Scope

### Trigger

독립 Cassandra 단일 노드 LAB의 정적 점검과 승인 후 read-only triage 순서다. 이번 변경에서 실제 서비스·데이터를 실행하지 않았다.

`cassandra-node1`의 선언·건강·데이터 경로를 점검하거나 격리 복구 범위를 설계할 때 사용한다.

### Targets

- Declared parent: [GDE-0025](../../01.guides/15.labs/0025-cassandra.md)
- Governing policy: [POL-0025](../../02.policies/15.labs/0025-cassandra.md)

- [Guide](../../01.guides/15.labs/0025-cassandra.md)
- [Policy](../../02.policies/15.labs/0025-cassandra.md)
- [LAB 설명](../../../../labs/cassandra/README.md)

## Preflight

### Authority

기동·중단·복원·삭제는 별도 승인이다. 무인증 내부 CQL이므로 신뢰하지 않는 peer를 연결하지 않는다.

### Environment

실행 전 확인할 경계와 정적 사전 점검은 다음과 같다.

#### Execution and stop boundary

실제 명령 전에 Docker context, 독립 Compose project, port, network, `${LAB_DATA_DIR}/cassandra/node1`, 용량, 기존 anonymous volume 소유자와 정확한 정리 범위를 확인한다. 무인증 내부 CQL이므로 신뢰하지 않는 peer를 연결하지 않는다. 기동·중단·복원·삭제는 별도 승인이다. 로그 원문과 비밀값은 증거에 복사하지 않는다.

먼저 다음을 확인한다.

- [ ] root include에 LAB가 없고 `labs/cassandra/docker-compose.yml`만 서비스 정의를 소유하는지 확인한다.
- [ ] `/var/lib/cassandra` mount와 `lab_cassandra_core_net`의 peer를 확인한다.
- [ ] 과거 데이터·snapshot 소유권을 확인하기 전 재생성·정리를 중단한다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 정적 구성 렌더(`docker compose ... config --quiet`) 확인 | 정적 구성 렌더가 성공 (exit code와 source SHA 기록) | 중단하고 Stop Conditions에 따라 mutation을 보류하고 @buenhyden에게 escalation |
| 2 | 별도 실행 승인 시 `ps cassandra-node1`, `exec cassandra-node1 nodetool status` 수행 | `nodetool status`의 `UN`은 프로세스 상태일 뿐 인증/읽기/복원을 증명하지 않음 | 승인이 없으면 `NOT_RUN`으로 남기고 mutation을 보류하며 @buenhyden에게 escalation |
| 3 | 승인된 격리 peer에서 읽기 전용 CQL 확인 (현재 무인증 기록) | 문서에 기록 없음 | 데이터 소유권/용량/인증/복구 세트가 불명확하면 mutation을 보류하고 @buenhyden에게 escalation |

1. 정적 구성만 확인한다.

   ```bash
   LAB_DATA_DIR=/tmp/hy-home-lab-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra/docker-compose.yml --profile cassandra config --quiet
   ```

2. 별도 실행 승인이 있을 때만 지정한 `labs/.env`와 context에서 `ps cassandra-node1`, `exec cassandra-node1 nodetool status`를 수행한다. `UN`은 프로세스 상태이며 인증·읽기·복원을 증명하지 않는다.
3. CQL 확인은 승인된 격리 peer에서 읽기 전용으로 시행한다. 현재 무인증임을 기록한다.

### Stop Conditions

과거 데이터·snapshot 소유권을 확인하기 전에는 재생성·정리를 중단한다. 데이터 소유권, 용량, 인증 필요성, 복구 세트가 불명확하면 mutation을 보류한다.

## Verification

### Expected Results

#### Service Checks

정적 구성 렌더가 성공해야 하며, 승인된 실행에서 `nodetool status`의 `UN`은 프로세스 상태일 뿐 인증·읽기·복원을 증명하지 않는다.

#### Evidence

정적 명령·종료 코드·source SHA만 기록한다. 실제 상태 조회와 복원 증거는 별도 실행 승인 후 기록한다.

정적 렌더 exit code와 source SHA를 기록한다. 실제 node·CQL·restore는 수행하지 않았다면 `NOT_RUN`으로 남긴다.

#### Observability and Evidence Sources

Compose health와 요약된 node 상태를 사용한다. exporter는 현재 LAB에 없다.

### Unverified Conditions

이 runbook이 아직 관찰하지 못한 항목은 다음과 같다. 문서는 실제 node/CQL/restore를 수행하지 않았다면 `NOT_RUN`으로 남기라고 규정한다.

- `ps cassandra-node1`과 `nodetool status`: 별도 실행 승인이 필요하며 이 문서에는 실행 결과가 기록되어 있지 않다. 승인된 실행에서 `UN` 상태가 관찰되면 프로세스 상태만 검증된다.
- 격리 peer에서의 CQL 읽기: 승인이 필요하며 실행 결과가 기록되어 있지 않다. 읽기 전용 질의 결과가 관찰되면 검증된다.
- snapshot 격리 복원: 빈 target에 호환 snapshot 전체를 복원한 뒤 owner/권한/건수 점검이 관찰되면 검증된다. 이 문서에는 복원 결과가 기록되어 있지 않다.

## Escalation

### Next Owner

데이터 소유권, 용량, 인증 필요성, 복구 세트가 불명확하면 @buenhyden에게 정확한 대상과 증거를 전달하고 mutation을 보류한다.

### Recovery or Forward Repair

소스 rollback은 데이터 rollback이 아니다. 기존 데이터를 보존하고 빈 격리 대상에 호환 snapshot 전체를 복원해 검증한다.

소스 rollback은 데이터 rollback이 아니다. 별도 승인된 빈 target, 호환 release와 schema, snapshot tag/SSTable 전체, owner·권한·건수 점검으로 격리 복원을 검증한다. 기존 volume을 덮어쓰거나 `down -v`를 실행하지 않는다.
