# Observability Runbooks

> Emergency procedures and troubleshooting for the observability tier.

## Overview

This directory contains actionable runbooks for recovering the observability stack from various failure states.

## Critical Runbooks

| Scenario | Action | Link |
| :--- | :--- | :--- |
| **Prometheus Corruption** | Repair/Rebuild TSDB index. | [prometheus-recovery.md](./prometheus-recovery.md) |
| **Ingestion Backend Down** | Recover MinIO connectivity for Loki/Tempo. | [minio-incident.md](./minio-incident.md) |
| **High Cardinality Bloom** | Mitigate Prometheus memory exhaustion. | [cardinality-mitigation.md](./cardinality-mitigation.md) |
| **Alerting Silence** | Debug Alertmanager delivery failures. | [alert-delivery.md](./alert-delivery.md) |

## Immediate Actions (Emergency)

1. **Check Connectivity**: Verify `infra_net` is routing between Alloy and backends.
2. **Check Storage**: Verify MinIO buckets (`loki-bucket`, `tempo-bucket`) are accessible.
3. **Restart Sequence**:
   - `docker compose restart alloy`
   - `docker compose restart prometheus`
   - `docker compose restart loki`

## SSoT Links

- **Infrastructure**: [infra/06-observability/](file:///home/hy/projects/hy-home.docker/infra/06-observability/README.md)
- **Operations**: [docs/08.operations/06-observability/](file:///home/hy/projects/hy-home.docker/docs/08.operations/06-observability/README.md)

---

Copyright (c) 2026. Licensed under the MIT License.
