# Kafka Recovery & Maintenance Runbook (05-messaging)

: Kafka Infrastructure

> Step-by-step procedures for broker recovery, partition rebalancing, and system maintenance.

---

## Overview (KR)

이 런북은 `hy-home.docker`의 Kafka 인프라(05-messaging)에서 발생할 수 있는 주요 장애 상황의 복구 절차와 정기 점검 단계를 정의한다. 운영자가 즉시 따라 할 수 있는 명령어와 검증 기준을 제공한다.

## Purpose

이 런북은 브로커 다운, 메시지 지연(Lag), 복제본 불일치 및 스키마 등록 오류를 신속히 해결하고 클러스터 상태를 정상으로 복구하는 것을 목적으로 한다.

## Canonical References

- `[../../02.ard/0005-messaging-architecture.md]`
- `[../../04.specs/05-messaging/spec.md]`
- `[../../08.operations/05-messaging/kafka.md]`

## When to Use

- **Emergency**: 브로커 쿼럼 붕괴 (`No Leader found` 발생 시).
- **Incident**: `UnderReplicatedPartitions` 지표가 0보다 클

### 1. Quorum Failure (KRaft)

- **Issue**: 클러스터 내 브로커 과반수 이상 다운되어 리더 선출이 불가능한 경우.

## Procedure or Checklist

### Checklist

- [ ] [ ] 모든 브로커 컨테이너가 `Up (healthy)` 상태인지 확인.
- [ ] [ ] `Kafbat UI`에서 `Offline Partitions`가 존재하는지 확인.
- [ ] [ ] `docker logs`를 통해 `Fatal` 또는 `OutOfMemory` 에러가 있는지 조사.

### Procedure

#### 1. Broker Quorum Recovery (Single node down)

1. 실패한 노드 식별: `docker compose ps`
2. 컨테이너 재시작: `docker compose restart kafka-X`
3. 복제 상태 확인: `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --under-replicated-partitions`

#### 2. Partition Rebalancing

- **Issue**: 특정 브로커에 파티션이 몰려 부하가 불균형한 경우.

1. 리더 선출 강제: `kafka-leader-election --bootstrap-server localhost:19092 --election-type PREFERRED --all-topic-partitions`
2. 지표 확인: `UnderReplicatedPartitions`가 0으로 수렴하는지 관찰.

#### 3. Schema Registry Incompatibility

- **Issue**: 잘못된 스키마 업데이트로 인해 생산/소비가 중단된 경우.

1. 레지스트리 상태 체크: `curl -fsS http://schema-registry.localhost/subjects`
2. 연결 실패 시 레지스트리 노드 재시작: `docker compose restart schema-registry`
3. 메타데이터 토픽(`_schemas`)의 가용성 확인.

## Verification Steps

- [ ] `docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092` 명령어 실행 성공 확인.
- [ ] `Kafbat UI`의 Topic Dashboard에서 모든 파티션의 `In-Sync Replicas`가 정수값인 3인지 확인.

## Observability and Evidence Sources

- **Signals**: Grafana Alert (UnderReplicatedPartitions > 0), Kafbat UI Health Indicator.
- **Evidence to Capture**: `docker logs kafka-X`, `kafka-topics --describe` 출력물.

## Safe Rollback or Recovery Procedure

- [ ] 브로커 설정 변경 시 `docker-compose.yml`을 이전 상태로 롤백하고 재구동.
- [ ] 스키마 변경 실패 시 `Schema Registry` 백업본을 통해 `_schemas` 토픽을 복구.

## Agent Operations

- **Tool Disable**: 메시징 오류 시 AI Agent의 생산 도구(Tool) 실행을 일시적으로 비활성화.
- **Trace Capture**: `docs/10.incidents`에 자동으로 장애 타임라인과 로그 캡처본을 기록.

## Related Operational Documents

- **Incident examples**: `[../../10.incidents/2026/2026-03-26-kafka-quorum-loss.md]` (예시)
- **Postmortem examples**: `[../../11.postmortems/2026/2026-03-26-kafka-balancing-failure.md]` (예시)
