# RabbitMQ

RabbitMQ is the most widely deployed open source message broker.

## Services

| Service | Image | Role | Resources | Profile |
| :--- | :--- | :--- | :--- | :--- |
| `rabbitmq` | `rabbitmq:4.2.3-...` | Bus Broker | 0.5 CPU / 512M | `rabbitmq` |

## Networking

- **Static IP**: `172.19.0.21`
- **AMQP**: `${RABBITMQ_HOST_PORT}` (default 5672).
- **Management Web**: `${RABBITMQ_MANAGEMENT_HOST_PORT}` (default 15672).

## Persistence

- **Data**: `rabbitmq-data-volume` mapped to `/var/lib/rabbitmq`.
| ----------- | ----------------------------------- |
| `README.md` | Service overview and usage notes.   |
