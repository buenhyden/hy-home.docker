# RabbitMQ Operations Policy (05-messaging)

> Service standards for queue governance, resource management, and security.

## Overview (KR)

이 문서는 RabbitMQ 서비스의 안정적인 운영을 위한 정책을 정의한다. 메시지 영속성, 큐 거버넌스, 리소스 임계치 관리 및 보안 표준을 포함하며, 모든 애플리케이션 팀은 이 정책을 준수해야 한다.

## Traceability (Golden 5)

- **PRD**: [05-messaging (2026-03-26)](../../01.prd/2026-03-26-05-messaging.md)
- **ARD**: [Messaging Architecture (0005)](../../02.ard/0005-messaging-architecture.md)
- **Spec**: [Messaging Specification](../../04.specs/05-messaging/spec.md)
- **Guide**: [RabbitMQ System Guide](../../07.guides/05-messaging/rabbitmq.md)

## Queue Governance

### 1. Durability Standards

- **Durable**: 서버 장애 시에도 큐 정의를 유지하기 위해 모든 큐는 `Durable: true`로 생성한다.
- **Persistent Messages**: 데이터 유실 방지가 필요한 경우 생산자(Producer)는 `delivery_mode: 2`를 사용하여 메시지 영속성을 보장한다.

### 2. High Availability (HA)

- **Quorum Queues**: 클러스터 환경에서 데이터 복제가 필요한 경우 `Classic Mirrored Queues` 대신 `Quorum Queues` 사용을 원칙으로 한다.

### 3. Error Handling

- **Dead Letter Exchange (DLX)**: 모든 작업 큐는 처리 실패 대비를 위해 DLX 및 DLQ를 사전에 구성해야 한다.

## Resource Management

### 1. Watermarks

- **Memory**: RAM의 40% 도달 시 흐름 제어(Flow Control)를 시작하며, 50% 도달 시 생산을 중단한다.
- **Disk**: 여유 공간이 2GB 미만일 경우 모든 메시지 수신을 거부한다.

### 2. Monitoring Alerts
- `rabbitmq_queue_messages_ready` > 10,000 (10분 지속 시 알람)
- `rabbitmq_unacknowledged_messages` > 1,000 (소비자 처리 지연 의심)

## Security Standards

- **Virtual Hosts**: 서비스/팀별로 독립적인 VHost를 할당하여 자원을 격리한다.
- **Permissions**: `Configure`, `Write`, `Read` 권한을 최소 권한 원칙(LoP)에 따라 부여한다.
- **Credentials**: Vault-injected 환경 변수를 통해서만 자격 증명을 관리한다.
