---
layer: infra
---

# Observability Tier: Maintenance & Procedures

This guide covers routine maintenance, backup/restore, and alerting lifecycle for the LGTM stack.

## 1. Stack Lifecycle

Use the `obs` profile to manage the observability services.

```bash
# Start the stack
COMPOSE_PROFILES=obs docker compose up -d

# Stop the stack (data persisted in volumes)
docker compose --profile obs stop
```

## 2. Alerting Procedures

### Silencing Alerts

If a service is under maintenance, silence the alerts in Alertmanager to avoid notification spam.

1. Access Alertmanager UI: `https://alertmanager.${DEFAULT_URL}`.
2. Click **New Silence**.
3. Add matchers (e.g., `service="infra-kafka"`) and set the duration.

### Reloading Rules

If you modify Prometheus alert rules or scraping configuration:

```bash
# Trigger hot-reload
curl -X POST http://localhost:9090/-/reload
```

## 3. Dashboard Management

Dashboards are provisioned from `./infra/06-observability/grafana/dashboards/`.

### Exporting New Dashboards

When a dashboard is created in the UI:
1. Export as JSON (Share -> Export -> Save to file).
2. Commit the file to the repository.
3. Update `infra/06-observability/grafana/provisioning/dashboards/all.yaml` if necessary.

## 4. Backup & Restore

### Data Persistence

All data is stored in Docker volumes mapped to `${DEFAULT_OBSERVABILITY_DIR}`.

### Backup Strategy

1. **Prometheus/Loki/Grafana**: Perform a filesystem backup of the mounted volumes.
2. **MinIO Buckets**: Ensure `loki-bucket` and `tempo-bucket` are backed up as part of the `04-data` tier procedures.

### Recovery

To restore from a backup:
1. Stop the stack.
2. Restore the volume contents to the host directory.
3. Restart the stack.

## 5. Troubleshooting LGTM

### Loki Ingestion Issues

If logs are missing, check the Alloy logs for push errors:

```bash
docker compose logs -f alloy | grep "loki"
```

### Prometheus Target Down

Check the targets page: `https://prometheus.${DEFAULT_URL}/targets`. Ensure the exporter containers are healthy and connected to `infra_net`.
