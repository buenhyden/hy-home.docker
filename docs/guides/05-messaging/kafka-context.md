---
layer: infra
---
# Kafka System Context

**Overview (KR):** Kafka KRaft 클러스터의 시스템 컨텍스트, 아키텍처, 의존성 및 생태계 내 역할을 설명합니다.

> **Component**: `kafka`
> **Architecture**: Confluent Platform on KRaft (ZooKeeper-less)
> **Profile**: `messaging`

## 1. Role in Ecosystem

Kafka is the **primary event streaming backbone** of the `hy-home.docker` infrastructure. It decouples producers and consumers, enabling asynchronous, durable, and replay-capable event flows across all services.

| Consumer / Integration | Purpose |
| --- | --- |
| `06-observability` stack | Receives `application-logs` topic for log shipping |
| `07-workflow` (n8n / Temporal) | Triggers workflows from Kafka events |
| `08-ai` workloads | Consumes inference results and model events |
| Application services | Produce/consume domain events via the REST Proxy or native clients |

## 2. Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                    kafka (messaging profile)                  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ kafka-1  │  │ kafka-2  │  │ kafka-3  │   KRaft Quorum    │
│  │ Broker + │  │ Broker + │  │ Broker + │   (no ZooKeeper)  │
│  │ Ctrl     │  │ Ctrl     │  │ Ctrl     │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       └─────────────┼─────────────┘                         │
│                     │ (infra_net: PLAINTEXT:19092)          │
│  ┌──────────────────┴────────────────────────────────────┐  │
│  │            Kafka Ecosystem Services                    │  │
│  │  Schema Registry (8081) | Connect (8083)              │  │
│  │  REST Proxy (8082)      | Exporter (9308)             │  │
│  │  Kafbat UI (8080) [SSO] | kafka-init (one-shot)       │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
         │ Traefik routing (TLS + SSO)
         ▼
   External: schema-registry.*, kafka-connect.*, kafbat-ui.*
```

## 3. KRaft Mode

KRaft (Kafka Raft) eliminates the ZooKeeper dependency for metadata management:

- All 3 brokers serve dual roles: **Broker** (handles topic data) + **Controller** (manages metadata quorum).
- Leader election managed internally via Raft consensus on port `9093`.
- The `KAFKA_CLUSTER_ID` must be pre-generated and set consistently across all brokers.

## 4. Networking & Listeners

Each broker exposes 3 listener types:

| Listener | Protocol | Port | Purpose |
| --- | --- | --- | --- |
| `PLAINTEXT` | Internal | `19092` | Client connections (internal services) |
| `CONTROLLER` | Internal | `9093` | KRaft quorum / inter-controller communication |
| `EXTERNAL` | External | `9092` (node 1), `9094` (node 2), `9096` (node 3) | Host-mapped for local dev access |

## 5. Security

- **Internal communication**: PLAINTEXT (traffic confined to `infra_net` Docker network).
- **Kafbat UI**: Protected by OAuth2 SSO via Keycloak (`02-auth`). Config in `kafbat-ui/dynamic_config.yaml`.
- **Schema Registry / Connect / REST Proxy**: Exposed via Traefik (TLS). No SSO on these endpoints currently.
- **Container hardening**: `no-new-privileges`, `cap_drop: ALL`, `init: true`, resource limits.

## 6. Default Bootstrap Topics

Created by `kafka-init` on first deployment:

| Topic | Partitions | Replication | Purpose |
| --- | --- | --- | --- |
| `infra-events` | 3 | 3 | Infrastructure lifecycle events |
| `application-logs` | 6 | 3 | Application log shipping |

## 7. JMX Monitoring

JMX metrics are exposed via the Prometheus JMX Exporter Java agent (JAR in `./jmx-exporter/`):

- Each broker exports metrics on port `9404`.
- Kafka Exporter (port `9308`) provides consumer group lag and topic metrics.
- Both are scraped by the `06-observability` Prometheus stack.

## 8. Lifecycle

### Startup Sequence

1. `kafka-1`, `kafka-2`, `kafka-3` start and elect a KRaft leader (~30-45s).
2. `schema-registry` starts (depends on all 3 brokers healthy).
3. `kafka-connect` starts (depends on all 3 brokers + schema-registry healthy).
4. `kafka-rest-proxy` starts (depends on all 3 brokers + schema-registry healthy).
5. `kafbat-ui` starts (depends on all 3 brokers + schema-registry + kafka-connect healthy).
6. `kafka-init` runs once (depends on kafka-1 healthy), creates bootstrap topics, then exits.

### Shutdown

```bash
docker compose --profile messaging stop
```

All broker data is persisted in named volumes — containers can be recreated without data loss.

### Complete Reset (Data Loss Warning)

```bash
docker compose --profile messaging down -v
# Then recreate host directories and restart
```

## 9. Development Mode

A single-node dev stack is available via `docker-compose.dev.yml`:

```bash
docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml up -d
```

This brings up `kafka-dev`, `schema-registry-dev`, `kafka-connect-dev`, `kafbat-ui-dev`, and `kafka-exporter-dev` — all with replication factor 1, suitable for local development and testing.
