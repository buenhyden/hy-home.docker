# RabbitMQ

> High-performance AMQP message broker for reliable asynchronous communication.

---

## Overview (KR)

이 문서는 `hy-home.docker`의 메시징 인프라를 담당하는 RabbitMQ 설정 및 운영 체계를 설명한다. 비동기 작업 처리, 서비스 간 메시지 라우팅 및 큐 대기열 관리를 위한 핵심 인프라다.

## Target Audience

- Backend Developers (Service integration)
- SREs (Maintenance & Scaling)

## Scope

- **Broker**: RabbitMQ 4.x 기반 메시지 중개
- **Management**: Web-based console & REST API
- **VHost/Auth**: 가상 호스트 및 자격 증명 관리

## Structure

```text
rabbitmq/
├── docker-compose.yml  # RabbitMQ service configuration
└── README.md           # This document
```

## How to Work in This Area

1. **Service Guide**: 상세 아키텍처 및 연결 설정은 `[../../../docs/07.guides/05-messaging/rabbitmq.md]`를 참조한다.
2. **Operations**: 보안 규정 및 가용성 정책은 `[../../../docs/08.operations/05-messaging/rabbitmq.md]`에 정의되어 있다.
3. **Emergency**: 서비스 장애 상황 발생 시 `[../../../docs/09.runbooks/05-messaging/rabbitmq.md]`의 복구 절차를 따른다.

## Tech Stack

| Category | Technology | Version | Notes |
| :--- | :--- | :--- | :--- |
| **Core** | RabbitMQ | 4.2.5-management | Alpine-based image |
| **Management** | UI / HTTP API | Enabled | UI via port 15672 |
| **Protocol** | AMQP | 0-9-1 | Standard port 5672 |

## Available Scripts

### 1. Verification

```bash
# Check service status and erlang nodes
docker exec rabbitmq rabbitmqctl status

# List active queues and their states
docker exec rabbitmq rabbitmqctl list_queues
```

### 2. Maintenance

```bash
# Export broker definitions (backup)
# Requires authorized user credentials
mc admin definitions export ...
```

## Related References

- **ARD**: `[../../../docs/02.ard/0005-messaging-architecture.md]`
- **Runbook**: `[../../../docs/09.runbooks/05-messaging/rabbitmq.md]`
- **Monitoring**: `Grafana - Messaging Dashboard`
