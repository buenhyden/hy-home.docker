# Incident Runbook: Observability Storage Full

**Issue:** `LokiStorageHigh` or `PrometheusStorageHigh` alert triggered indicating >90% disk utilization.

## Definition

Loki and Prometheus both store timeseries and chunk data locally (or in MinIO). When host storage reaches capacity, these containers may crash-loop, leading to data loss or dropped telemetry.

## Resolution Steps

### 1. Identify Culprits

Check the physical disk utilization on the host.

```bash
# Verify local bind mounts sizes
sudo du -sh /mnt/wsl/data/observability/* | sort -rh
```

### 2. Immediate Relief (Prometheus)

If Prometheus TSDB is full:

1. Decrease retention time or size limits in `docker-compose.yml` or `prometheus.yml`:
   `--storage.tsdb.retention.time=15d`
   `--storage.tsdb.retention.size=10GB`
2. Force a restart of the Prometheus container.

```bash
docker restart infra-prometheus
```

### 3. Immediate Relief (Loki/MinIO)

If Loki logs are filling up MinIO:

1. Loki retention is configured via the `loki-config.yaml` `compactor` lifecycle limits. Update the `retention_period` to a smaller window (e.g., `168h`).
2. Restart Loki to trigger the compactor.

```bash
docker restart infra-loki
```

### 4. Expand Volume

If the underlying disk is genuinely full, expand the host VM's VHDX (if using WSL2) or attach a larger external volume to the mapped path.
