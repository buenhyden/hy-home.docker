# RabbitMQ

RabbitMQ is the most widely deployed open source message broker.

## Services

| Service    | Image                        | Role           | Resources         |
| :--------- | :--------------------------- | :------------- | :---------------- |
| `rabbitmq` | `rabbitmq:3-management-alpine`| Message Broker | 0.5 CPU / 1GB RAM |

## Networking

| Port | Purpose                |
| :--- | :--------------------- |
| 5672 | AMQP protocol          |
| 15672| Management UI (Web)    |

## Persistence

- **Data**: `/var/lib/rabbitmq` (mounted to `rabbitmq-data` volume).

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and usage notes.   |
