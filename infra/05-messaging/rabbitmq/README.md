# RabbitMQ Message Broker

> Lightweight AMQP broker for task queuing and asynchronous messaging.

## Overview

A standalone RabbitMQ instance providing reliable AMQP-based message queuing. It is primarily used for background tasks and decoupling lightweight microservices that do not require the high-throughput streaming capabilities of Kafka.

## Audience

- Backend Developers (Task queuing)
- SREs (Broker maintenance)

## Scope

- RabbitMQ Management Server
- Virtual Host (VHost) configuration
- User & Permissions management

## Structure

```text
rabbitmq/
├── docker-compose.yml  # RabbitMQ service orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [RabbitMQ Operations Guide](../../../docs/07.guides/05-messaging/02.rabbitmq-ops.md).
2. Access the UI at `http://rabbitmq-ui.${DEFAULT_URL}` with secret-based credentials.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Broker     | RabbitMQ                       | Alpine-based              |
| Interface  | Management Plugin              | Enabled by default        |
| Protocol   | AMQP 0-9-1                     | Primary interface         |

## Configuration

| Endpoint | Port | Description |
| :--- | :--- | :--- |
| `AMQP` | 5672 | Message producing/consuming |
| `Management` | 15672 | Web-based management console |

## Testing

```bash
# Check node status
docker exec rabbitmq rabbitmqctl status
```

## AI Agent Guidance

1. Use `Quorum Queues` for critical data that requires durability and replication.
2. Avoid using the default `guest/guest` credentials; use Vault-injected secrets.
3. Monitor `Message Rates` to identify bottleneck services.
