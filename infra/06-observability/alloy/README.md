# Grafana Alloy

> Vendor-neutral OpenTelemetry Collector optimized for the LGTM stack.

## Overview

Alloy is the central telemetry hub for the hy-home.docker ecosystem. It handles log collection, metric scraping, trace ingestion, and profile forwarding in a single, unified pipeline.

## Structure

```text
alloy/
├── config/
│   └── config.alloy     # Telemetry pipeline configuration
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Collector | grafana/alloy:v1.13.1 | Telemetry orchestration |
| Protocols | OTLP, Prometheus, LogQL | Multi-protocol ingestion |
| Security | Docker Socket (RO) | Log discovery |

## Configuration

- **Pipeline Config**: `config/config.alloy`.
- **Active Streams**:
  - **Logs**: Docker container logs → Loki.
  - **Metrics**: Self-scraping → Prometheus.
  - **Traces**: OTLP (4317/4318) → Tempo.
  - **Profiling**: Profile forwarding → Pyroscope.

## Persistence

- **State**: Alloy is primarily stateless. Transient state for batching is stored in memory.

## Operational Status

> [!IMPORTANT]
> Alloy requires read-only access to the Docker socket (`/var/run/docker.sock`) and container log paths to perform automatic service discovery and log tailing.

---

Copyright (c) 2026. Licensed under the MIT License.
