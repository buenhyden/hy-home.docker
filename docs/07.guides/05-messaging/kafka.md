# Kafka Event Streaming Guide (05-messaging)

> Zookeeper-less Kafka Cluster Setup & Management for hy-home.docker.

---

## Overview (KR)

이 문서는 KRaft(Kafka Raft) 모드 기반의 Apache Kafka 클러스터 시스템(05-messaging)의 설정 및 운영 방법을 설명한다. 대용량 이벤트 스트리밍, 메시지 스키마 거버넌스, 그리고 Kafka Connect 연동을 다룬다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Developer (Backend, Data)
- Operator
- Agent-tuner

## Purpose

이 가이드는 사용자가 Kafka 클러스터를 이해하고, 토픽을 생성하며, 스키마 레지스트리를 통해 메시지 정합성을 보장할 수 있도록 돕는다.

## Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Kafka CLI Tools](https://kafka.apache.org/downloads) (옵션, 컨테이너 내 실행 가능)
- [infra/05-messaging/kafka](../../../infra/05-messaging/kafka/README.md) 기반 클러스터 구동 환경

## Step-by-step Instructions

### 1. Cluster Execution

```bash
# Infrastructure root에서 실행
cd infra/05-messaging/kafka
docker compose up -d
```

- `kafka-init` 서비스가 가동되어 `infra-events`, `application-logs` 등의 시스템 토픽을 자동 생성한다.

### 2. Work Breakdown

```bash
# Create a new topic
kafka-topics --create --topic my-topic --bootstrap-server localhost:9092
```

- **Topic Creation**: Define partitions and replication factor.
- **CLI**: `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --create --topic <topic-name> --partitions 3 --replication-factor 3`
- **UI**: `https://kafbat-ui.${DEFAULT_URL}` 접속 후 GUI를 통해 생성/수정 가능.

### 3. Schema Registry Integration

### Implementation Snippet

- **Producer**: Configure `acks=all` for high durability.
- 모든 생산자(Producer)는 메시지 전송 전 Schema Registry에 스키마를 등록해야 한다.
- **Compatibility**: 기본 `BACKWARD` 정책을 준수하여 소비자의 호환성을 보장한다.

### 4. Data Pipeline with Connect

- Kafka Connect를 사용하여 데이터베이스(PostgreSQL 등)와 이벤트를 연동한다.
- `https://kafka-connect.${DEFAULT_URL}` REST API를 통해 커넥터를 등록/관리한다.

## Common Pitfalls

- **Quorum Stability**: 브로커 3개 중 2개 이상이 다운되면 클러스터가 읽기 전용으로 전환되거나 중단될 수 있다.
- **Schema Compatibility**: 스키마 변경 시 호환성 검사(`BACKWARD`)에 실패하면 `409 Conflict` 에러와 함께 생산자가 차단된다.
- **Retention Misconfig**: 디스크 용량을 고려하지 않은 긴 `retention.ms` 설정은 스토리지 고갈을 초래한다.

## Related Documents

- **Spec**: `[../../04.specs/05-messaging/spec.md]`

## Related Documents

- [Kafka Operation Policy](../../08.operations/05-messaging/kafka.md)
- **Operation**: `[../../08.operations/05-messaging/kafka.md]`
- **Runbook**: `[../../09.runbooks/05-messaging/kafka.md]`
