# Observability Stack (06-observability)

> Centralized telemetry and monitoring hub for the hy-home.docker ecosystem.

## Overview

The `06-observability` tier implements the LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus) combined with Grafana Alloy and Pyroscope to provide comprehensive monitoring, logging, tracing, and profiling capabilities. It acts as the "Single Source of Truth" for system health and performance data.

## Structure

```text
06-observability/
├── alertmanager/    # Alert routing and notification logic
├── alloy/          # Unified telemetry collector (OTLP endpoint)
├── grafana/        # Visualization, dashboards, and provisioning
├── loki/           # Log aggregation and storage (S3 backend)
├── prometheus/     # Metrics storage and alerting rules
├── pushgateway/    # Ephemeral/short-lived metrics gateway
├── pyroscope/      # Continuous profiling backend
├── tempo/          # Distributed tracing storage (S3 backend)
├── docker-compose.yml
└── README.md
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Metrics | Prometheus v3.9.0 | Time-series storage & query |
| Logs | Loki v3.6.6 | Log aggregation (S3 via MinIO) |
| Traces | Tempo v2.10.1 | Distributed tracing (S3 via MinIO) |
| Profiling | Pyroscope v1.18.1 | Continuous performance profiling |
| Collector | Alloy v1.13.1 | Telemetry pipeline & OTLP gateway |
| Visualization | Grafana v12.3.3 | Unified dashboarding & SSO |
| Alerting | Alertmanager v0.30.0 | Multi-channel alert routing |

## Operational Status

> [!NOTE]
> This tier requires the `04-data` tier (MinIO) for Loki and Tempo persistence. Authentication is integrated with the `02-auth` tier (Keycloak).

## SSoT References

- [LGTM Stack Guide](../../docs/07.guides/06-observability/01.lgtm-stack.md)
- [Querying Data](../../docs/07.guides/06-observability/02.querying-data.md)
- [Retention Policies](../../docs/08.operations/06-observability/README.md)
- [Emergency Recovery](../../docs/09.runbooks/06-observability/README.md)

---

Copyright (c) 2026. Licensed under the MIT License.
