---
layer: infra
---

# Messaging Tier: Usage & Troubleshooting Guide

Operational guide for interacting with Kafka and RabbitMQ.

## 1. Kafka Operations

### Using Kafbat UI
Access the web-based management interface at `https://kafbat-ui.${DEFAULT_URL}`. Use this to:

- Inspect message contents in topics.
- Monitor consumer group lag.
- Create or modify topics.

### CLI Producer/Consumer
Test the stream from a shell:

```bash
# Produce a message
docker exec -it kafka-1 kafka-console-producer --bootstrap-server localhost:9092 --topic test-topic

# Consume messages
docker exec -it kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

## 2. RabbitMQ Operations

### Using Management UI
Access at `https://rabbitmq.${DEFAULT_URL}`.

- **Default Login**: Provided by Docker Secrets (`rabbitmq_user`, `rabbitmq_password`).

### CLI Management (rabbitmqctl)

```bash
# List all queues
docker exec rabbitmq rabbitmqctl list_queues

# List connections
docker exec rabbitmq rabbitmqctl list_connections
```

## 3. Troubleshooting

| Issue | Potential Cause | Fix |
| :--- | :--- | :--- |
| **Kafka: Metadata error** | KRaft quorum not reached. | Check logs of all 3 brokers: `docker compose logs kafka-1`. |
| **RabbitMQ: EACCES** | Incorrect volume permissions. | Re-run `sudo chown -R 999:999` on the host data dir. |
| **SSO: 403 Forbidden** | User not assigned to `messaging` role. | Check Keycloak client-role mappings for the UI client. |
| **Kafbat: No UI** | Broker or Schema Registry down. | Verify all dependencies are healthy in the dashboard. |

### Logs & Diagnostics

```bash
# Tail Kafka logs
docker compose logs -f kafka-1

# Tail RabbitMQ logs
docker compose logs -f rabbitmq
```
