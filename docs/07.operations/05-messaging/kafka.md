# Kafka Cluster Operations Policy (05-messaging)

> Governance, Data Retention, and Reliability Standards for Kafka.

---

## Overview (KR)

이 문서는 Kafka 클러스터(05-messaging)의 운영 정책을 정의한다. 메시지 보관(Retention), 복제(Replication), 그리고 스키마 거버넌스에 대한 필수 통제 기준을 포함한다.

## Policy Scope

이 정책은 Kafka 브로커, 스키마 레지스트리, 그리고 클러스터 내의 모든 토픽 설정을 제어한다.

## Applies To

- **Systems**: Kafka Broker Cluster (3-node), Schema Registry
- **Agents**: AI Infrastructure Agent, CI/CD Deployer
- **Environments**: Production (Default), Development

## Controls

### 1. Topic## Replication Policy

- **Min ISR**: 2 (가용성 확보).
토픽은 최소 `replication.factor=3` 및 `min.insync.replicas=2`를 유지해야 한다.
- **Required**: `infra-events`, `application-logs` 등 핵심 토픽은 삭제(`delete`) 정책을 비활성화하거나 유예 기간을 두어야 한다.

### 2. Data## Retention Standards

- **Internal Events**: 7일 보관 (Compact 정책 병행).
ms`는 7일(604,800,000ms)로 설정한다.
- **Allowed**: 중요 회계/보안 이벤트의 경우 최대 30일까지 확장 가능하나 인프라 용량 검토가 선행되어야 한다.
- **Disallowed**: 스토리지 고갈 방지를 위해 `retention.bytes` 제한 없는 토픽 생성을 금지한다.

### 3.## Schema Governance

- **Compatibility**: `BACKWARD`를 기본값으로 설정.
`Schema Registry`를 통해 메시지 형식을 유효화해야 한다.
- **Allowed**: `BACKWARD` 호환성 모드를 기본값으로 사용한다.
- **Disallowed**: 시스템 중단을 초래할 수 있는 호환성 없는 스키마의 강제 업데이트(`NONE` 모드)를 금지한다.

## Exceptions

- 단기 성능 테스트용 토픽의 경우 `replication.factor=1`을 부분적으로 허용하나, 작업 완료 후 즉각 삭제해야 한다. (DevOps 팀 승인 필요)

## Verification

- **Compliance Check**: Kafbat UI 또는 CLI를 통해 토픽 설정이 정책과 일치하는지 주간 단위로 감사한다.
- **Cluster Audit**: `UnderReplicatedPartitions` 지표를 상시 감시하여 가용성 정책 위반을 감지한다.

## Review Cadence

- Quarterly (분기별) 데이터 용량 및 정책 실효성 검토.

## AI Agent Policy Section

- **Automated Topic Creation**: `kafka-init` 서비스를 통해서만 자동 생성이 허용되며, 생성 시 필수 라벨(`hy-home.tier`)이 포함되어야 한다.
- **Health Guardrails**: 복제 오류 발생 시 AI Agent는 신규 생산자 연결을 일시 중단하거나 경고를 전송해야 한다.

## Related Documents

- **ARD**: `[../../02.ard/0005-messaging-architecture.md]`
- **Procedure**: `[../../07.operations/05-messaging/kafka.md]`
- **Usage**: `[../../07.operations/05-messaging/kafka.md]`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/05-messaging/kafka.md` during the 2026-05-10 operations taxonomy consolidation.

### Kafka Event Streaming Usage (05-messaging)

> Zookeeper-less Kafka Cluster Setup & Management for hy-home.docker.

---

#### Overview (KR)

이 문서는 KRaft(Kafka Raft) 모드 기반의 Apache Kafka 클러스터 시스템(05-messaging)의 설정 및 운영 방법을 설명한다. 대용량 이벤트 스트리밍, 메시지 스키마 거버넌스, 그리고 Kafka Connect 연동을 다룬다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Developer (Backend, Data)
- Operator
- Agent-tuner

#### Purpose

이 가이드는 사용자가 Kafka 클러스터를 이해하고, 토픽을 생성하며, 스키마 레지스트리를 통해 메시지 정합성을 보장할 수 있도록 돕는다.

#### Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Kafka CLI Tools](https://kafka.apache.org/downloads) (옵션, 컨테이너 내 실행 가능)
- [infra/05-messaging/kafka](../../../infra/05-messaging/kafka/README.md) 기반 클러스터 구동 환경

#### Step-by-step Instructions

##### 1. Cluster Execution

```bash
### Infrastructure root에서 실행
cd infra/05-messaging/kafka
docker compose up -d
```

- `kafka-init` 서비스가 가동되어 `infra-events`, `application-logs` 등의 시스템 토픽을 자동 생성한다.

##### 2. Work Breakdown

```bash
### Create a new topic
kafka-topics --create --topic my-topic --bootstrap-server localhost:9092
```

- **Topic Creation**: Define partitions and replication factor.
- **CLI**: `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --create --topic <topic-name> --partitions 3 --replication-factor 3`
- **UI**: `https://kafbat-ui.${DEFAULT_URL}` 접속 후 GUI를 통해 생성/수정 가능.

##### 3. Schema Registry Integration

##### Implementation Snippet

- **Producer**: Configure `acks=all` for high durability.
- 모든 생산자(Producer)는 메시지 전송 전 Schema Registry에 스키마를 등록해야 한다.
- **Compatibility**: 기본 `BACKWARD` 정책을 준수하여 소비자의 호환성을 보장한다.

##### 4. Data Pipeline with Connect

- Kafka Connect를 사용하여 데이터베이스(PostgreSQL 등)와 이벤트를 연동한다.
- `https://kafka-connect.${DEFAULT_URL}` REST API를 통해 커넥터를 등록/관리한다.

#### Common Pitfalls

- **Quorum Stability**: 브로커 3개 중 2개 이상이 다운되면 클러스터가 읽기 전용으로 전환되거나 중단될 수 있다.
- **Schema Compatibility**: 스키마 변경 시 호환성 검사(`BACKWARD`)에 실패하면 `409 Conflict` 에러와 함께 생산자가 차단된다.
- **Retention Misconfig**: 디스크 용량을 고려하지 않은 긴 `retention.ms` 설정은 스토리지 고갈을 초래한다.

#### Related Documents

- **Spec**: `[../../04.specs/05-messaging/spec.md]`

#### Related Documents

- [Kafka Operation Policy](../../07.operations/05-messaging/kafka.md)
- **Operation**: `[../../07.operations/05-messaging/kafka.md]`
- **Procedure**: `[../../07.operations/05-messaging/kafka.md]`

## Procedure

> Migrated from `docs/07.operations/05-messaging/kafka.md` during the 2026-05-10 operations taxonomy consolidation.

### Kafka Recovery & Maintenance Procedure (05-messaging)

: Kafka Infrastructure

> Step-by-step procedures for broker recovery, partition rebalancing, and system maintenance.

---

#### Overview (KR)

이 런북은 `hy-home.docker`의 Kafka 인프라(05-messaging)에서 발생할 수 있는 주요 장애 상황의 복구 절차와 정기 점검 단계를 정의한다. 운영자가 즉시 따라 할 수 있는 명령어와 검증 기준을 제공한다.

#### Purpose

이 런북은 브로커 다운, 메시지 지연(Lag), 복제본 불일치 및 스키마 등록 오류를 신속히 해결하고 클러스터 상태를 정상으로 복구하는 것을 목적으로 한다.

#### Canonical References

- `[../../02.ard/0005-messaging-architecture.md]`
- `[../../04.specs/05-messaging/spec.md]`
- `[../../07.operations/05-messaging/kafka.md]`

#### When to Use

- **Emergency**: 브로커 쿼럼 붕괴 (`No Leader found` 발생 시).
- **Incident**: `UnderReplicatedPartitions` 지표가 0보다 클

##### 1. Quorum Failure (KRaft)

- **Issue**: 클러스터 내 브로커 과반수 이상 다운되어 리더 선출이 불가능한 경우.

#### Procedure or Checklist

##### Checklist

- [ ] [ ] 모든 브로커 컨테이너가 `Up (healthy)` 상태인지 확인.
- [ ] [ ] `Kafbat UI`에서 `Offline Partitions`가 존재하는지 확인.
- [ ] [ ] `docker logs`를 통해 `Fatal` 또는 `OutOfMemory` 에러가 있는지 조사.

##### Procedure

###### 1. Broker Quorum Recovery (Single node down)

1. 실패한 노드 식별: `docker compose ps`
2. 컨테이너 재시작: `docker compose restart kafka-X`
3. 복제 상태 확인: `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --under-replicated-partitions`

###### 2. Partition Rebalancing

- **Issue**: 특정 브로커에 파티션이 몰려 부하가 불균형한 경우.

1. 리더 선출 강제: `kafka-leader-election --bootstrap-server localhost:19092 --election-type PREFERRED --all-topic-partitions`
2. 지표 확인: `UnderReplicatedPartitions`가 0으로 수렴하는지 관찰.

###### 3. Schema Registry Incompatibility

- **Issue**: 잘못된 스키마 업데이트로 인해 생산/소비가 중단된 경우.

1. 레지스트리 상태 체크: `curl -fsS http://schema-registry.localhost/subjects`
2. 연결 실패 시 레지스트리 노드 재시작: `docker compose restart schema-registry`
3. 메타데이터 토픽(`_schemas`)의 가용성 확인.

#### Verification Steps

- [ ] `docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092` 명령어 실행 성공 확인.
- [ ] `Kafbat UI`의 Topic Dashboard에서 모든 파티션의 `In-Sync Replicas`가 정수값인 3인지 확인.

#### Observability and Evidence Sources

- **Signals**: Grafana Alert (UnderReplicatedPartitions > 0), Kafbat UI Health Indicator.
- **Evidence to Capture**: `docker logs kafka-X`, `kafka-topics --describe` 출력물.

#### Safe Rollback or Recovery Procedure

- [ ] 브로커 설정 변경 시 `docker-compose.yml`을 이전 상태로 롤백하고 재구동.
- [ ] 스키마 변경 실패 시 `Schema Registry` 백업본을 통해 `_schemas` 토픽을 복구.

#### Agent Operations

- **Tool Disable**: 메시징 오류 시 AI Agent의 생산 도구(Tool) 실행을 일시적으로 비활성화.
- **Trace Capture**: `docs/10.incidents`에 자동으로 장애 타임라인과 로그 캡처본을 기록.

#### Related Operational Documents

- **Incident examples**: `[../../10.incidents/2026/2026-03-26-kafka-quorum-loss.md]` (예시)
- **Postmortem examples**: `[../../10.incidents/2026/2026-03-26-kafka-balancing-failure-postmortem.md]` (예시)

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
