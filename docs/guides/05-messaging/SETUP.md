---
layer: infra
---

# Messaging Tier: Setup & Installation Guide

This guide covers the bootstrapping and verification of the messaging brokers.

## 1. Prerequisites

### Environment Profiles
The messaging tier is profile-driven. Ensure your `.env` or compose command includes the required profiles:
- `messaging`: Enables the Kafka cluster.
- `rabbitmq`: Enables the RabbitMQ broker.

### Secrets Generation
Generate the required broker credentials:

```bash
./scripts/gen-secrets.sh
```

## 2. Bootstrapping Kafka (KRaft)

Kafka requires a pre-generated `CLUSTER_ID`. This is handled automatically by the `kafka-init` service on first run.

```bash
# Start the Kafka stack
docker compose --profile messaging up -d

# Verify broker health
docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:9092
```

## 3. Bootstrapping RabbitMQ

RabbitMQ requires specific volume permissions for the data directory:

```bash
# 1. Set host directory permissions
sudo chown -R 999:999 ${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq

# 2. Start RabbitMQ
docker compose --profile rabbitmq up -d

# 3. Verify health
docker exec rabbitmq rabbitmq-diagnostics -q check_running
```
## 4. Verification Checklist


- [ ] **Kafbat UI**: Accessible at `https://kafbat-ui.${DEFAULT_URL}`.
- [ ] **RabbitMQ UI**: Accessible at `https://rabbitmq.${DEFAULT_URL}`.
- [ ] **Topic Initialization**: Run `docker exec kafka-1 kafka-topics --list --bootstrap-server localhost:9092` to see `infra-events`.
- [ ] **Connectivity**: Application containers can ping `kafka:19092` and `rabbitmq:5672`.
