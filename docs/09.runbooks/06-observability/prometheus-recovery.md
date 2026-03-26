---
tier: 09.runbooks
component: 06-observability
title: Prometheus TSDB Hub Recovery
status: production
updated: 2026-03-25
---

# Prometheus TSDB Hub Recovery

**Symptoms**: Prometheus fails to start, logs show "TSDB block truncation error" or "corruption in segment".

## 1. Diagnosis

Check the logs of the Prometheus container:

```bash
docker logs <prometheus_container_id>
```

## 2. Immediate Action (Safe)

If the error is related to memory or locks:

1. Restart the container: `docker restart prometheus`.
2. Ensure the volume mount has correct permissions (`nobody:nogroup`).

## 3. Advanced Recovery (Data Loss Risk)

If the TSDB index is corrupted:

1. **Stop** Prometheus: `docker compose stop prometheus`.
2. **Snapshot** the data directory: `tar -czvf /tmp/prometheus_data_backup.tar.gz /var/lib/docker/volumes/prometheus_data`.
3. **Delete** the WAL (Write Ahead Log): `rm -rf /var/lib/docker/volumes/prometheus_data/_data/wal`.
4. **Restart** Prometheus.

## 4. Verification

Check if the metrics are visible in Grafana. If not, verify that Alloy is successfully pushing metrics.

---
[Return to Observability Index](./README.md)
