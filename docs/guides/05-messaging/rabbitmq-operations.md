---
layer: infra
---
# RabbitMQ Routine Operations

**Overview (KR):** RabbitMQ 큐 상태 모니터링 및 메시지 전달 보장 정책 등 루틴 오퍼레이션 설명입니다.

> **Component**: `rabbitmq`
> **Profile**: `rabbitmq`

## Run Commands

```bash
# Start the RabbitMQ service
docker compose --profile rabbitmq up -d

# Stop the RabbitMQ service
docker compose --profile rabbitmq stop

# View logs
docker compose logs -f rabbitmq
```

## Queue Management

### List Queues and Message Counts

```bash
docker compose exec rabbitmq rabbitmqctl list_queues name messages messages_ready messages_unacknowledged
```

### Purge a Queue

```bash
docker compose exec rabbitmq rabbitmqctl purge_queue my-queue
```

### Delete a Queue

```bash
docker compose exec rabbitmq rabbitmqctl delete_queue my-queue
```

## Exchange and Binding Management

### List Exchanges

```bash
docker compose exec rabbitmq rabbitmqctl list_exchanges
```

### List Bindings

```bash
docker compose exec rabbitmq rabbitmqctl list_bindings
```

## User and Permission Management

### List Users

```bash
docker compose exec rabbitmq rabbitmqctl list_users
```

### Add a User

```bash
docker compose exec rabbitmq rabbitmqctl add_user myuser mypassword
docker compose exec rabbitmq rabbitmqctl set_user_tags myuser administrator
docker compose exec rabbitmq rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"
```

## Consumer and Connection Monitoring

```bash
# List active consumers
docker compose exec rabbitmq rabbitmqctl list_consumers

# List active connections
docker compose exec rabbitmq rabbitmqctl list_connections

# List active channels
docker compose exec rabbitmq rabbitmqctl list_channels
```

## Health Checks

```bash
# Check if the node is running
docker compose exec rabbitmq rabbitmq-diagnostics -q check_running

# Check for local alarms (e.g., memory/disk alarm)
docker compose exec rabbitmq rabbitmq-diagnostics -q check_local_alarms

# Full cluster status
docker compose exec rabbitmq rabbitmqctl cluster_status
```

## Definition Backup

Export definitions (exchanges, queues, bindings, policies) from the Management UI:

- Navigate to `https://rabbitmq.${DEFAULT_URL}` → **Overview** → **Export definitions**.
- Or via CLI:

```bash
docker compose exec rabbitmq rabbitmqctl export_definitions /tmp/rabbit-definitions.json
docker cp rabbitmq:/tmp/rabbit-definitions.json ./rabbit-definitions-backup.json
```
