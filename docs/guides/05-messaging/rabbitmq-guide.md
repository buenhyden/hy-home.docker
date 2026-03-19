---
layer: infra
---
# RabbitMQ Operational Blueprint

**Overview (KR):** RabbitMQ 메시지 브로커의 클러스터 구성 및 관리 청사진 가이드입니다.

> **Component**: `rabbitmq`
> **Profile**: `rabbitmq` (Optional Tier)

## 1. Role in Ecosystem

RabbitMQ serves as the secondary AMQP broker, typically utilized for task-based async worker queues and legacy system integrations requiring AMQP 0-9-1 semantics (exchanges, queues, bindings).

| Attribute | Value |
| --- | --- |
| **Internal DNS** | `rabbitmq` |
| **AMQP Port** | `5672` (Internal) |
| **Management UI** | `https://rabbitmq.${DEFAULT_URL}` |
| **Profile** | `rabbitmq` |

### Technical Specifications

| Service | Image | Port | Hardening |
| --- | --- | --- | --- |
| `rabbitmq` | `rabbitmq:4.2.3-management-alpine` | `5672` (AMQP), `15672` (Mgmt) | `no-new-privileges`, `cap_drop: ALL` |

## 2. Secrets

Credentials are provided via Docker Secrets — no plaintext values in environment variables.

| Secret Name | Purpose | Environment Variable |
| --- | --- | --- |
| `rabbitmq_user` | Default admin username | `RABBITMQ_DEFAULT_USER_FILE` |
| `rabbitmq_password` | Default admin password | `RABBITMQ_DEFAULT_PASS_FILE` |

> **Note**: The `rabbitmq_erlang_cookie` secret is referenced in the guide docs but is **NOT** currently defined in `docker-compose.yml`. If clustering multiple RabbitMQ nodes, add `rabbitmq_erlang_cookie` to the secrets block and mount it.

## 3. Initial Setup

The deployment is declarative via the management Alpine image. Plugins are pre-enabled by the `management-alpine` tag.

- **Default vhost**: `/`
- **Ports**: AMQP on `${RABBITMQ_HOST_PORT:-5672}`, Management on `${RABBITMQ_MANAGEMENT_HOST_PORT:-15672}`.
- **Traefik**: Management UI exposed at `https://rabbitmq.${DEFAULT_URL}`.

## 4. Configuration Standards

- **Definition Export**: Regularly export definitions from the Web UI (Overview → Export definitions) to keep a backup of all exchanges, queues, and bindings.
- **Policy Management**: Use the Management UI or `rabbitmqctl` to set queue policies (e.g., dead-lettering, TTL, max-length).

## 5. Persistence

Data is stored in a bind-mounted volume at `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq` → `/var/lib/rabbitmq`.

## 6. Troubleshooting

### Permission Denied on Startup

If the service fails to boot with "Permission Denied", check the host volume permissions. RabbitMQ requires UID `999`:

```bash
sudo chown -R 999:999 ${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq
```

### Verify Node Health

```bash
docker compose exec rabbitmq rabbitmq-diagnostics -q check_running
docker compose exec rabbitmq rabbitmq-diagnostics -q check_local_alarms
```

### Reset Node (Data Loss Warning)

```bash
docker compose exec rabbitmq rabbitmqctl stop_app
docker compose exec rabbitmq rabbitmqctl reset
docker compose exec rabbitmq rabbitmqctl start_app
```
