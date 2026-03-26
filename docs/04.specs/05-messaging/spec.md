# Messaging Tier Technical Specification (Spec)

## Messaging Tier (05-messaging) Specification

## Overview (KR)

이 문서는 메시징 계층(`05-messaging`)의 기술 설계와 구현 계약을 정의한다. Kafka 클러스터 및 RabbitMQ 브로커의 세부 구성, 포트 맵핑, 스키마 관리 전략을 구체화한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Kafka Clusters (3 Brokers), Schema Registry, Kafka Connectors.
  - RabbitMQ (Management node).
  - Messaging Dynamic Config (`dynamic_config.yaml`).
- **Does Not Own**:
    - Consumer/Producer 비즈니스 로직.
    - 데이터 계층의 RDBMS 저장소.

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-26-05-messaging.md]`
- **ARD**: `[../../02.ard/0005-messaging-architecture.md]`
- **Related ADRs**: `[../../03.adr/0005-kafka-vs-rabbitmq-selection.md]`

## Contracts

- **Config Contract**:
  - `CLUSTER_ID`: ${KAFKA_CLUSTER_ID} 필수.
  - `DEFAULT_MESSAGE_BROKER_DIR`: 영구 데이터 루트 경로.
- **Data / Interface Contract**:
  - Kafka: Avro/Protobuf (via Schema Registry).
  - RabbitMQ: JSON (Standard).
- **Governance Contract**:
  - 모든 토픽은 3개 이상의 복제본(Replication Factor: 3)을 가져야 함.
  - RabbitMQ 큐는 Quorum Queue 패턴 사용 권장.

## Core Design

- **Component Boundary**:
  - `kafka-1/2/3`: 메시지 저장 및 라우팅.
  - `schema-registry`: 데이터 타입 메타데이터 관리.
  - `rabbitmq`: 실시간 비동기 작업 큐.
- **Key Dependencies**:
  - `infra_net` (Docker Network).
  - `02-auth` (Secrets Management).
- **Tech Stack**:
  - Confluent Platform CP-Kafka v8.1.1.
  - RabbitMQ v4.2.5 (Management).
  - ksqlDB.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: 스키마 레지스트리를 통한 하위 호환성 (BACKWARD) 정책 강제.
- **Migration / Transition Plan**: Kafka는 KRaft 로그 재조정을 통해 무중단 마이그레이션 지원.

## Interfaces & Data Structures

### Kafka Internal Config Structure

```yaml
KAFKA_LISTENERS: 'PLAINTEXT://0.0.0.0:19092,CONTROLLER://0.0.0.0:9093,EXTERNAL://0.0.0.0:9092'
KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka-1:9093,2@kafka-2:9093,3@kafka-3:9093'
```

## API Contract (If Applicable)

- **Kafka REST Proxy**: `http://kafka-rest.${DEFAULT_URL}`
- **RabbitMQ Management**: `http://rabbitmq.${DEFAULT_URL}`

## Evaluation (If Applicable)

- **Metrics**: `UnderReplicatedPartitions`, `ConsumerLag`, `QueueLength`.
- **How to Run**: `docker exec kafka-1 kafka-topics --list --bootstrap-server localhost:19092`

## Edge Cases & Error Handling

- **Error 1**: Broker Partition Offline.
    - **Fallback**: ISR(In-Sync Replicas) 내의 리더 선출 자동 수행.
- **Error 2**: RabbitMQ Queue Full.
    - **Fallback**: Max-length 정책에 따른 Rejected Message 처리 (Dead Letter Exchange).

## Verification

```bash
# Kafka health check
docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092

# RabbitMQ diagnostics
docker exec rabbitmq rabbitmq-diagnostics check_running
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 3노드 중 1개 노드 정지 시에도 리더 재선출 및 서비스 유지 확인.
- **VAL-SPC-002**: Schema Registry를 통한 유효하지 않은 스키마 전송 시 거부 확인.

## Related Documents

- **Plan**: `[../../05.plans/2026-03-26-05-messaging-standardization.md]`
- **Tasks**: `[../../06.tasks/2026-03-26-05-messaging-tasks.md]`
- **Runbook**: `[../../09.runbooks/05-messaging/README.md]`
