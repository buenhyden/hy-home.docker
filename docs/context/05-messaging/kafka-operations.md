# Kafka Routine Operations

> **Component**: `kafka`
> **Profile**: `messaging`

## Run Profile

```bash
# Start the standard baseline stack (profiles are read from `.env`)
docker compose up -d

# Enable messaging profile (example)
COMPOSE_PROFILES=core,data,obs,messaging docker compose up -d

# Stream SQL (optional)
# (Not enabled by default in the root compose)
# docker compose --profile ksql up -d
```

## Kafka Cluster Usage

### 1. Accessing Kafka UI

- **URL**: `https://kafbat-ui.${DEFAULT_URL}`
- **Login**: Protected by SSO. Provides cluster management (topics, consumers, schemas).

### 2. CLI Operations

Create a topic:

```bash
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic my-topic --partitions 3 --replication-factor 3
```

List topics:

```bash
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
```

Consume messages:

```bash
docker compose exec kafka-1 kafka-console-consumer --bootstrap-server localhost:19092 \
  --topic my-topic --from-beginning
```

### 3. Kafka Connect

Check installed plugins:

```bash
curl -k https://kafka-connect.${DEFAULT_URL}/connector-plugins
```

Deploy a connector (Example):

```bash
curl -X POST -H "Content-Type: application/json" --data @my-connector.json \
  -k https://kafka-connect.${DEFAULT_URL}/connectors
```

## ksqlDB Usage

### Accessing via CLI (Internal)

`ksqldb-cli` 서비스를 통해 접속할 수 있습니다:

```bash
# (Not enabled by default in the root compose)
# docker compose exec -it ksqldb-cli ksql http://ksqldb-server:${KSQLDB_PORT}
```

### Checking Logs

```bash
# docker compose logs ksqldb-server
```
