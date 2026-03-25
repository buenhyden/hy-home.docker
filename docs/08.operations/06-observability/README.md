# Observability Operations

> Operational policies and governance for the observability tier.

## Overview

This document defines the lifecycle management of telemetry data, alerting thresholds, and backup strategies for the `06-observability` stack.

## Data Retention Policies

| Component | Storage Backend | Retention Period | Limit Type |
| :--- | :--- | :--- | :--- |
| **Prometheus** | Local Disk (TSDB) | 15 Days | Time-based |
| **Loki** | MinIO (S3) | 7 Days | Time-based |
| **Tempo** | MinIO (S3) | 24 Hours | Time-based |
| **Pyroscope** | Local Disk | 14 Days | Time-based |

## Alerting Governance

- **Severity Levels**:
  - `critical`: PagerDuty/Immediate Slack notify.
  - `warning`: Slack notify (non-urgent).
  - `info`: Dashboard only.
- **Inhibitions**: Alerting on dependent services is suppressed if the underlying infrastructure (e.g., Network) is down.

## Backup & Recovery

- **Grafana**: `grafana.db` (SQLite) is backed up daily to the `04-data` tier.
- **Alertmanager**: Configuration is version-controlled; runtime state is ephemeral.
- **Prometheus**: TSDB snapshots can be triggered via HTTP API for consistent backups.

## SSoT Links

- **Guides**: [docs/07.guides/06-observability/](file:///home/hy/projects/hy-home.docker/docs/07.guides/06-observability/README.md)
- **Infrastructure**: [infra/06-observability/](file:///home/hy/projects/hy-home.docker/infra/06-observability/README.md)

---

Copyright (c) 2026. Licensed under the MIT License.
