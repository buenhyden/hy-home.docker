# Messaging Tier Operational Documentation (05-messaging)

> Event Streaming, Message Brokering, and Data Pipelines for the March 2026 "Thin Root" Architecture.

## Overview

이 디렉터리는 `hy-home.docker`의 메시징 인프라(05-messaging)에 대한 개발자 가이드, 운영 정책, 그리고 사고 대응 런북을 포함한다. 모든 문서는 아키텍처 연동(PRD/ARD/ADR)을 기반으로 작성되었다.

## Documentation Layers

### 1. Developer Guides (07.guides)
메시징 시스템을 사용하는 개발자를 위한 기술 가이드.
- [01. Kafka KRaft Guide](./01.kafka-kraft.md) - Zookeeper-less Kafka 클러스터 연동 및 스키마 관리.
- [02. RabbitMQ Guide](./02.rabbitmq-ops.md) - AMQP 기반 작업 큐 및 메시지 브로커 활용.
- [03. ksqlDB Streaming](./03.ksql-streaming.md) - 실시간 스트림 처리 및 SQL 변환.

### 2. Operational Policy (08.operations)
시스템 관리자를 위한 메시징 거버넌스 및 운영 표준.
- [Messaging Ops Policy](../../08.operations/05-messaging/README.md) - 보관 정책(Retention), 스키마 거버넌스, 모니터링 기준.

### 3. Incident Runbooks (09.runbooks)
장애 상황에서의 복구 절차 및 긴급 대응 가이드.
- [Messaging Runbook](../../09.runbooks/05-messaging/README.md) - 브로커 복구, 스키마 오류 해결, 백프레셔 대응.

## Traceability

- **PRD**: [2026-03-26-05-messaging.md](../../01.prd/2026-03-26-05-messaging.md)
- **ARD**: [0005-messaging-architecture.md](../../02.ard/0005-messaging-architecture.md)
- **Spec**: [05-messaging/spec.md](../../04.specs/05-messaging/spec.md)

---
*Maintained by DevOps & Infrastructure Team*
