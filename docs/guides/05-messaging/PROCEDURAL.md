---
layer: infra
---
# Kafka Routine Operations

**Overview (KR):** Kafka 클러스터의 일상적인 관리 과업 및 토픽 운영 절차를 설명합니다.

> **Component**: `kafka`
> **Profile**: `messaging`

## Run Profile

The Kafka stack is activated by the `messaging` profile.

```bash
# Start the full messaging stack
COMPOSE_PROFILES=messaging docker compose up -d

# Stop the messaging stack
docker compose --profile messaging stop

# Or, if COMPOSE_PROFILES is set in .env:
docker compose up -d
```

> **Note on ksqlDB**: The `ksqldb-server` service uses the `messaging-option` profile (not `ksql`). The `ksqldb-cli` and `ksql-datagen` use the `ksql` profile. ksqlDB is not started by the `messaging` profile alone.

## Kafka Cluster Usage

### 1. Accessing Kafka UI

- **URL**: `https://kafbat-ui.${DEFAULT_URL}`
- **Login**: Protected by SSO (Keycloak). Provides cluster management (topics, consumers, schemas, connectors).

### 2. CLI — Topic Operations

Create a topic:

```bash
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic my-topic --partitions 3 --replication-factor 3
```

List topics:

```bash
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
```

Describe a topic:

```bash
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --describe --topic my-topic
```

Delete a topic:

```bash
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --delete --topic my-topic
```

### 3. CLI — Message Testing

Produce messages:

```bash
docker compose exec -it kafka-1 kafka-console-producer \
  --bootstrap-server localhost:19092 --topic my-topic
```

Consume messages:

```bash
docker compose exec kafka-1 kafka-console-consumer \
  --bootstrap-server localhost:19092 \
  --topic my-topic --from-beginning
```

### 4. Consumer Group Management

List consumer groups:

```bash
docker compose exec kafka-1 kafka-consumer-groups --bootstrap-server localhost:19092 --list
```

Describe group lag:

```bash
docker compose exec kafka-1 kafka-consumer-groups --bootstrap-server localhost:19092 \
  --describe --group my-consumer-group
```

Reset consumer group offset:

```bash
docker compose exec kafka-1 kafka-consumer-groups --bootstrap-server localhost:19092 \
  --group my-consumer-group --reset-offsets --to-earliest --topic my-topic --execute
```

### 5. Kafka Connect

Check installed plugins:

```bash
curl -s https://kafka-connect.${DEFAULT_URL}/connector-plugins | jq .
```

Deploy a connector:

```bash
curl -X POST -H "Content-Type: application/json" --data @my-connector.json \
  https://kafka-connect.${DEFAULT_URL}/connectors
```

Get connector status:

```bash
curl -s https://kafka-connect.${DEFAULT_URL}/connectors/my-connector/status
```

Delete a connector:

```bash
curl -X DELETE https://kafka-connect.${DEFAULT_URL}/connectors/my-connector
```

### 6. Monitoring

Kafka Exporter metrics (Prometheus format) are exposed on port `9308`. These are scraped by the `06-observability` stack.

Check cluster health via KRaft quorum:

```bash
docker compose exec kafka-1 kafka-metadata-quorum \
  --bootstrap-server localhost:19092 describe --status
```

## ksqlDB Usage

> **Profile**: ksqlDB server requires the `messaging-option` profile. The CLI requires `ksql`.

### Starting ksqlDB

```bash
# Start the ksqlDB server (depends on kafka being up)
docker compose --profile messaging-option up -d ksqldb-server

# Open the interactive CLI
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

### Checking Logs

```bash
docker compose logs ksqldb-server
```
