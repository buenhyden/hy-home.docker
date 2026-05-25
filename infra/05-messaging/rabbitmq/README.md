# RabbitMQ

> High-performance AMQP message broker for reliable asynchronous communication.

---

## Overview (KR)

이 문서는 `hy-home.docker`의 메시징 인프라를 담당하는 RabbitMQ 설정 및 운영 체계를 설명한다. 비동기 작업 처리, 서비스 간 메시지 라우팅 및 큐 대기열 관리를 위한 핵심 인프라다.

## Audience

이 README의 주요 독자:

- Backend Developers
- SREs
- AI Agents

## Scope

### In Scope

- **Broker**: RabbitMQ 4.x 기반 메시지 중개
- **Management**: Web-based console & REST API
- **VHost/Auth**: 가상 호스트 및 자격 증명 관리

### Out of Scope

- Kafka event streaming configuration
- Application queue naming policy beyond documented broker controls
- Secret values or credential material

## Structure

```text
rabbitmq/
├── docker-compose.yml  # RabbitMQ service configuration
└── README.md           # This document
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | RabbitMQ service leaf in `05-messaging`; services: `rabbitmq`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/05-messaging/rabbitmq/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `RABBITMQ_DEFAULT_USER_FILE`, `RABBITMQ_DEFAULT_PASS_FILE`; profiles: `messaging`, `messaging-option` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/05-messaging/rabbitmq/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `rabbitmq-data-volume:/var/lib/rabbitmq:rw`, `rabbitmq-data-volume` |
| Ports | `${RABBITMQ_HOST_PORT:-5672}:${RABBITMQ_PORT:-5672}`, `${RABBITMQ_MANAGEMENT_HOST_PORT:-15672}:${RABBITMQ_MANAGEMENT_PORT:-15672}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.rabbitmq.rule`, `traefik.http.routers.rabbitmq.entrypoints`, `traefik.http.routers.rabbitmq.tls`, `traefik.http.routers.rabbitmq.middlewares`, `traefik.http.services.rabbitmq.loadbalancer.server.port` |
| Secret refs | names: `rabbitmq_user`, `rabbitmq_password`; mounts: `/run/secrets/rabbitmq_user`, `/run/secrets/rabbitmq_password` |
| Healthcheck | Compose healthcheck declared for `rabbitmq` |
| Operations | [Guide](../../../docs/05.operations/guides/05-messaging/rabbitmq.md), [Policy](../../../docs/05.operations/policies/05-messaging/rabbitmq.md), [Runbook](../../../docs/05.operations/runbooks/05-messaging/rabbitmq.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **Service Guide**: 상세 아키텍처 및 연결 설정은 [RabbitMQ guide](../../../docs/05.operations/guides/05-messaging/rabbitmq.md)를 참조한다.
2. **Operations**: 보안 규정 및 가용성 정책은 [RabbitMQ policy](../../../docs/05.operations/policies/05-messaging/rabbitmq.md)에 정의되어 있다.
3. **Emergency**: 서비스 장애 상황 발생 시 [RabbitMQ runbook](../../../docs/05.operations/runbooks/05-messaging/rabbitmq.md)의 복구 절차를 따른다.

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

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect RabbitMQ.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking RabbitMQ documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For queue errors: check queue state in the RabbitMQ management UI and verify consumer count and message backlog.
- For dead letter issues: review DLX exchange and routing key configuration in the queue definition.
- For credential errors: confirm `RABBITMQ_DEFAULT_USER` and `RABBITMQ_DEFAULT_PASS` secrets are correctly injected.

## Related Documents

- **ARD**: [Messaging architecture](../../../docs/02.architecture/requirements/0005-messaging-architecture.md)
- **Guide**: [RabbitMQ guide](../../../docs/05.operations/guides/05-messaging/rabbitmq.md)
- **Policy**: [RabbitMQ policy](../../../docs/05.operations/policies/05-messaging/rabbitmq.md)
- **Runbook**: [RabbitMQ runbook](../../../docs/05.operations/runbooks/05-messaging/rabbitmq.md)
- **Monitoring**: `Grafana - Messaging Dashboard`
