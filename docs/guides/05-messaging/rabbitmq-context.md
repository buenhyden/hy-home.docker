---
layer: infra
---
# RabbitMQ System Context

**Overview (KR):** RabbitMQ 메시지 브로커의 시스템 컨텍스트, 생태계 내 역할, 아키텍처 및 생명주기를 설명합니다.

> **Component**: `rabbitmq`
> **Profile**: `rabbitmq` (Optional Tier)
> **Image**: `rabbitmq:4.2.3-management-alpine`

## 1. Role in Ecosystem

RabbitMQ serves as the **secondary, optional message broker** in the `hy-home.docker` infrastructure, complementing Kafka with AMQP 0-9-1 semantics. It is activated only when the `rabbitmq` profile is enabled.

| Primary Use Case | Why RabbitMQ (not Kafka) |
| --- | --- |
| Task/job queues | AMQP semantics: per-message acknowledgments, per-consumer routing |
| Legacy system integration | Services that speak AMQP 0-9-1 natively |
| Complex routing | Flexible exchange types (direct, topic, fanout, headers) |
| Short-lived transient messages | No need for replay; messages consumed once and removed |

## 2. Architecture

```text
           Application Services (infra_net)
                        │
              ┌─────────▼──────────┐
              │      rabbitmq       │
              │  AMQP: 5672 (int)  │
              │  Mgmt: 15672 (int) │
              │  Profile: rabbitmq  │
              └─────────┬──────────┘
                        │ Traefik (TLS)
              ┌─────────▼──────────┐
              │  Management Web UI  │
              │  rabbitmq.${URL}   │
              └────────────────────┘
```

## 3. Messaging Model

RabbitMQ uses the AMQP exchange → binding → queue model:

| Concept | Description |
| --- | --- |
| **Exchange** | Routes messages based on routing key and exchange type |
| **Queue** | Stores messages until consumed |
| **Binding** | Links an exchange to a queue with an optional routing key |
| **Consumer** | Subscribes to a queue and ACKs messages on processing |

Exchange types available:

- **direct**: Route by exact routing key match
- **topic**: Route by wildcard pattern (`#`, `*`)
- **fanout**: Broadcast to all bound queues
- **headers**: Route by message header attributes

## 4. Secrets & Authentication

Credentials injected via Docker Secrets (no plaintext in environment):

| Secret | Env Variable | Purpose |
| --- | --- | --- |
| `rabbitmq_user` | `RABBITMQ_DEFAULT_USER_FILE` | Admin username |
| `rabbitmq_password` | `RABBITMQ_DEFAULT_PASS_FILE` | Admin password |

> If running a RabbitMQ cluster (multiple nodes), an `rabbitmq_erlang_cookie` secret must also be defined and mounted at `/var/lib/rabbitmq/.erlang.cookie`. The current single-node setup does not require this.

## 5. Persistence

- **Volume**: `rabbitmq-data-volume` → `/var/lib/rabbitmq`
- **Host path**: `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq`
- **Owner**: UID `999` (rabbitmq process user)

> **Permission Setup**:
>
> ```bash
> sudo chown -R 999:999 ${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq
> ```

## 6. Networking

| Port | Protocol | Access | Purpose |
| --- | --- | --- | --- |
| `5672` | AMQP | Internal (`infra_net`) | Client connections |
| `15672` | HTTP | Traefik (external) | Management Web UI |
| Host `${RABBITMQ_HOST_PORT:-5672}` | AMQP | Host-mapped | Dev client access |
| Host `${RABBITMQ_MANAGEMENT_HOST_PORT:-15672}` | HTTP | Host-mapped | Dev UI access |

## 7. Lifecycle

### Start

```bash
docker compose --profile rabbitmq up -d
```

### Stop

```bash
docker compose --profile rabbitmq stop
```

### Health Check

The container health check runs:

```bash
rabbitmq-diagnostics -q check_running
```

### Graceful Shutdown (Drain Queues)

Before stopping, drain queues to avoid message loss:

```bash
# Pause consumer dispatch on the node
docker compose exec rabbitmq rabbitmqctl pause_listeners

# Wait for queues to drain, then stop
docker compose --profile rabbitmq stop
```

### Data Reset (Warning: Data Loss)

```bash
docker compose --profile rabbitmq down -v
sudo rm -rf ${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq
```

## 8. Comparison with Kafka

| Feature | RabbitMQ | Kafka |
| --- | --- | --- |
| Protocol | AMQP 0-9-1 | Custom (Kafka protocol) |
| Message retention | Until consumed (or TTL) | Configurable retention period |
| Replay | Not supported | Supported (seek to offset) |
| Routing | Flexible (exchanges) | Topic-based partitioning |
| Ordering | Per-queue (single consumer) | Per-partition |
| Use case | Task queues, RPC | Event streaming, log aggregation |
