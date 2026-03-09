# Runbook: n8n Worker Recovery

## Given

- n8n workflows are stuck in "Started" or "Queued" state.
- Celery/RabbitMQ/Redis queue shows high backlog or unacknowledged messages.
- n8n worker containers are running but not processing tasks.

## When

- Worker logs show `Connection timeout` or `Heartbeat missed`.
- Redis/Valkey memory usage is spiked.

## Then

### 1. Check Queue Status

```bash
docker compose exec valkey-cluster redis-cli -a $(cat /run/secrets/service_valkey_password) info memory
```

### 2. Restart Workers

```bash
docker compose up -d --force-recreate n8n-worker
```

### 3. Clear Dead Jobs (Optional - Data Loss Risk)

If the queue is corrupted:

```bash
docker compose exec valkey-cluster redis-cli -a $(cat /run/secrets/service_valkey_password) FLUSHALL
```

### 4. Verify Recovery

Check active executions in n8n UI or logs:

```bash
docker compose logs -f n8n-worker
```
