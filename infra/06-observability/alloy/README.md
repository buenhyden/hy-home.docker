# Grafana Alloy Unified Collector

> Advanced telemetry pipeline and OTLP gateway.

## Overview

Alloy is the unified collection agent for the platform. It replaces legacy agents by providing a programmable configuration (Alloy HCL) to collect, process, and export metrics, logs, and traces. It acts as the OTLP gateway for all applications.

## Audience

- Developers (Data ingestion)
- SREs (Pipeline tuning)

## Structure

```text
alloy/
├── config/
│   └── config.alloy  # Telemetry pipeline definition
└── README.md
```

## How to Work in This Area

1. Follow the [Alloy Collector Guide](../../../docs/07.guides/06-observability/02.alloy-collector.md).
2. Modify `config.alloy` to add new pipeline components.
3. Access the Alloy UI at `http://alloy.${DEFAULT_URL}` to debug pipelines.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Collector | Grafana Alloy | v1.13.1 |
| Protocol | OTLP (gRPC/HTTP) | Standard interface |

## AI Agent Guidance

1. Prefer `OTLP` ingestion for all new application instrumentation.
2. Use Alloy's `discovery.docker` for automatic container metadata enrichment.
3. Monitor `batch` processing metrics to prevent data loss during high load.
