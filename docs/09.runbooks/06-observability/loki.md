---
tier: 09.runbooks
component: 06-observability
title: Loki Recovery Runbook
status: production
updated: 2026-03-26
---

# Loki Recovery Runbook

> Critical recovery procedures for Loki logging service.

## 1. Service Health Check

Verify if Loki is healthy and ready to receive logs:

```bash
# Check readiness
wget -qO- http://loki:3100/ready

# Check service status (docker compose)
docker compose ps loki
```

## 2. Common Scenarios

### Scenario A: "No logs found" in Grafana

**Symptoms**: Explore shows empty results despite containers running.

1. **Verify Alloy Status**: Check `https://alloy.${DEFAULT_URL}`. Ensure `loki.write` components are healthy.
2. **Check Loki Ingestion**: Look for `entry out of order` or `rate limit exceeded` errors in Loki logs:

   ```bash
   docker compose logs --tail=100 loki
   ```

3. **Verify Labels**: Ensure the LogQL query labels match exactly what Alloy is sending.

### Scenario B: MinIO Connection Failure

**Symptoms**: Loki logs show `S3 storage: connection refused` or `access denied`.

1. **Check MinIO Status**: `docker compose ps minio`.
2. **Verify Credentials**: Ensure `MINIO_APP_USERNAME` and `minio_app_user_password` secret match the `loki-config.yaml` S3 settings.
3. **Bucket Existence**: Verify `loki-bucket` exists in MinIO UI.

### Scenario C: Loki Ingester OOM (Out Of Memory)

**Symptoms**: `infra-loki` container restarts frequently with exit code 137.

1. **Temporary Fix**: Increase memory limit in `infra/06-observability/docker-compose.yml` if traffic has surged.

```bash
docker compose -f infra/06-observability/docker-compose.yml restart loki
```

### 2. Check S3/MinIO Connectivity

1. **Root Cause**: Check for a specific service emitting massive log volume (log spikes).
2. **Mitigation**: Use `limits_config` in `loki-config.yaml` to throttle high-volume streams.

## 3. Emergency Maintenance

### Force Compaction

If storage is full and retention cleanup is pending:

```bash
# Compactor runs automatically, but check for errors:
docker compose -f infra/06-observability/docker-compose.yml logs -f loki | grep "compactor"
```

### Flush Chunks

If Loki needs to be shut down gracefully while ensuring all logs are committed to S3:

- Loki handles this automatically on `SIGTERM`. Ensure `stop_grace_period` is sufficient (min 30s).

---

- [Loki System Guide](../../07.guides/06-observability/loki.md)
 | [Operational Policy](../../08.operations/06-observability/loki.md)
