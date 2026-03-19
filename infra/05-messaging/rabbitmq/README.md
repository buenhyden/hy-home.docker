# RabbitMQ

RabbitMQ is a widely deployed open source message broker supporting AMQP 0-9-1.

## Services

| Service | Image | Role | Resources | Profile |
| :--- | :--- | :--- | :--- | :--- |
| `rabbitmq` | `rabbitmq:4.2.3-management-alpine` | AMQP Broker | 1.0 CPU / 512M | `rabbitmq` |

## Networking

- **AMQP**: `${RABBITMQ_HOST_PORT:-5672}` (host) → `${RABBITMQ_PORT:-5672}` (container).
- **Management Web UI**: `${RABBITMQ_MANAGEMENT_HOST_PORT:-15672}` (host) → `${RABBITMQ_MANAGEMENT_PORT:-15672}` (container).
- **Traefik**: Management UI also exposed at `https://rabbitmq.${DEFAULT_URL}`.

## Persistence

- **Data Volume**: `rabbitmq-data-volume` mapped to `/var/lib/rabbitmq`.
- **Host Path**: `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq`.

> **⚠️ Permissions**: RabbitMQ requires UID `999` on the host volume directory. If the service fails to start with "Permission Denied":
> ```bash
> sudo chown -R 999:999 ${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq
> ```

## Secrets

Credentials are provided via Docker Secrets.

| Secret | Purpose | Env Variable |
| --- | --- | --- |
| `rabbitmq_user` | Admin username | `RABBITMQ_DEFAULT_USER_FILE` |
| `rabbitmq_password` | Admin password | `RABBITMQ_DEFAULT_PASS_FILE` |

## Configuration

- **Security**: `no-new-privileges`, `cap_drop: ALL`.
- **Image**: The `management-alpine` image includes the management plugin pre-enabled.

## File Map

| Path | Description |
| --- | --- |
| `docker-compose.yml` | RabbitMQ service definition |
| `README.md` | Service overview and usage notes (this file) |

## Documentation References

| Topic | Guide |
| --- | --- |
| Architecture & Blueprint | [rabbitmq-guide.md](../../../docs/guides/05-messaging/rabbitmq-guide.md) |
| Routine Operations | [rabbitmq-operations.md](../../../docs/guides/05-messaging/rabbitmq-operations.md) |
