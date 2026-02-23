# Kafka Routine Operations

> **Component**: `kafka`, `ksql`

## Run Profile

```bash
# Core streaming (Kafka)
docker compose up -d kafka

# Stream SQL (optional)
docker compose --profile ksql up -d ksqldb-server
```

## Kafka Cluster Usage

### 1. Accessing Kafka UI

- **URL**: `https://kafka-ui.${DEFAULT_URL}`
- **Login**: Protected by SSO. Provides full cluster management (Topics, Connectors, Schemas).

### 2. CLI Operations

Create a topic:

```bash
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic my-topic --partitions 3 --replication-factor 3
```

List topics:

```bash
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
```

Consume messages:

```bash
docker exec kafka-1 kafka-console-consumer --bootstrap-server localhost:19092 \
  --topic my-topic --from-beginning
```

### 3. Kafka Connect

Check installed plugins:

```bash
curl http://localhost:8083/connector-plugins | jq
```

Deploy a connector (Example):

```bash
curl -X POST -H "Content-Type: application/json" --data @my-connector.json \
  http://localhost:8083/connectors
```

## ksqlDB Usage

### Accessing via CLI (Internal)

`ksqldb-cli` 서비스를 통해 접속할 수 있습니다:

```bash
docker exec -it ksqldb-cli ksql http://ksqldb-server:${KSQLDB_PORT}
```

### Checking Logs

```bash
docker logs ksqldb-server
```
