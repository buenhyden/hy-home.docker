# Observability Guides

> Detailed guides for monitoring, logging, and tracing in hy-home.docker.

## Overview

The `06-observability` tier provides a comprehensive LGTM (Loki, Grafana, Tempo, Mimir/Prometheus) stack. This directory contains guides for instrumenting applications, querying data, and utilizing the visualization layer.

## Available Guides

| Guide | Description | Target |
| :--- | :--- | :--- |
| [LGTM Stack Overview](./lgtm-stack.md) | Understanding the combined telemetry pipeline. | Operators |
| [Querying with LogQL/PromQL](./querying.md) | Advanced data retrieval and filtering. | Developers |
| [Application Instrumentation](./instrumentation.md) | How to add OTLP/Prometheus to your apps. | Developers |
| [Dashboard Governance](./dashboards.md) | Best practices for creating and sharing dashboards. | Teams |

## Key Concepts

- **Metrics**: Time-series data scraped via Prometheus.
- **Logs**: Indexed metadata with chunked storage in Loki.
- **Traces**: Distributed Request tracking via Tempo.
- **Profiling**: Continuous performance profiling via Pyroscope.

## SSoT Links

- **Infrastructure**: [infra/06-observability/](file:///home/hy/projects/hy-home.docker/infra/06-observability/README.md)
- **Operations**: [docs/08.operations/06-observability/](file:///home/hy/projects/hy-home.docker/docs/08.operations/06-observability/README.md)
- **Runbooks**: [docs/09.runbooks/06-observability/](file:///home/hy/projects/hy-home.docker/docs/09.runbooks/06-observability/README.md)

---

Copyright (c) 2026. Licensed under the MIT License.
