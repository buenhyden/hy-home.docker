# RabbitMQ System Guide (05-messaging)

> Flexible AMQP Message Brokering and Task Queuing Patterns.

## Overview (KR)

이 가이드는 `hy-home.docker` 플랫폼에서 비동기 작업 큐 및 서비스 간 메시지 릴레이를 담당하는 RabbitMQ의 구조와 활용 가이드를 제공한다. RabbitMQ는 하드웨어 장애에 강한 Quorum Queue와 유연한 AMQP 라우팅을 통해 데이터 무결성과 시스템 결합도 해소(Decoupling)를 지원한다.

## Traceability (Golden 5)

- **PRD**: [05-messaging (2026-03-26)](../../01.prd/2026-03-26-05-messaging.md)
- **ARD**: [Messaging Architecture (0005)](../../02.ard/0005-messaging-architecture.md)
- **Spec**: [Messaging Specification](../../04.specs/05-messaging/spec.md)
- **Infra**: [RabbitMQ Infrastructure](../../../infra/05-messaging/rabbitmq/README.md)

## Core Concepts

### 1. AMQP Model

- **Exchange**: 메시지를 받아 큐로 전달하는 라우팅 엔진.
- **Queue**: 메시지가 소비되기 전까지 대기하는 저장소.
- **Binding**: Exchange와 Queue 사이의 라우팅 규칙.

### 2. Routing Patterns
- **Direct**: Routing Key가 일치하는 단일 큐로 전달 (1:1 작업 할당).
- **Topic**: 와일드카드(`#`, `*`) 패턴을 사용한 유연한 멀티캐스트 (Pub/Sub).
- **Fanout**: Routing Key 무시하고 연결된 모든 큐로 브로드캐스트.

## Implementation Guidelines

### Quorum Queues (Recommended)

고가용성이 필요한 핵심 데이터는 Raft 합의 알고리즘 기반의 `Quorum Queues` 사용을 강력히 권장한다.

```bash
# Example queue declaration via CLI (usually done via Client SDK)
rabbitmqadmin declare queue name=task.critical queue_type=quorum
```

### Dead Letter Exchange (DLX)

처리 실패한 메시지는 무한 루프를 방지하기 위해 반드시 `dead-letter-exchange` 속성을 정의하여 격리한다.

## Management & Monitoring

- **Console**: [https://rabbitmq.${DEFAULT_URL}](https://rabbitmq.${DEFAULT_URL})
- **Metrics**: Grafana Dashboard를 통해 메시지 입출력 속도(Rate) 및 컨슈머 상태를 실시간 모니터링한다.
- **Health Check**: `rabbitmq-diagnostics check_running`을 통해 노드 상태를 주기적으로 확인한다.

## Related Documents

- [RabbitMQ Operation Policy](../../08.operations/05-messaging/rabbitmq.md)
- [RabbitMQ Recovery Runbook](../../09.runbooks/05-messaging/rabbitmq.md)
