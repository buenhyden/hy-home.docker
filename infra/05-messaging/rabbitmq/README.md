# RabbitMQ (rabbitmq)

> Lightweight, open-source message broker supporting AMQP 0-9-1.

## Overview

RabbitMQ is used for task queuing, background job distribution, and lightweight messaging where high-throughput partitioning is not required.

## Service Matrix

| Service | Image | Port | Role |
| :--- | :--- | :--- | :--- |
| **RabbitMQ** | `rabbitmq:4.2.3-management-alpine` | 5672, 15672 | AMQP Broker + Management UI |

## Connectivity Map

- **AMQP**: listen on port `5672`.
- **Web UI**: [RabbitMQ Management](https://rabbitmq.${DEFAULT_URL}) (Port 15672).

## Setup & Persistence

### 1. Persistence

- **Host Path**: `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq`
- **Mount Path**: `/var/lib/rabbitmq`

> [!WARNING]
> RabbitMQ requires UID `999` on the host volume. Run `sudo chown -R 999:999 ${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq` if you encounter permission errors.

### 2. Secrets

Credentials are managed via Docker Secrets:

- `rabbitmq_user`: Admin username.
- `rabbitmq_password`: Admin password.

---

## Operations

### Management Plugin

The `management-alpine` image includes the web dashboard and `rabbitmqadmin` CLI pre-enabled.

### Security

- **Hardening**: Container runs with `cap_drop: ALL` and `no-new-privileges`.

## Navigation
- [Messaging Tier Overview](../README.md)
- [RabbitMQ Guide](../../../docs/07.guides/05-messaging/03.rabbitmq-queues.md)
- [Operational Policy](../../../docs/08.operations/05-messaging/README.md)
