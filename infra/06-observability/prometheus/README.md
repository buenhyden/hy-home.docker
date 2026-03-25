# Prometheus

> Core metrics collection and time-series database for the hy-home.docker ecosystem.

## Overview

Prometheus is the primary metrics engine, responsible for scraping targets, evaluating alert rules, and storing time-series data. It supports advanced querying via PromQL and integrates with Alertmanager for routing notifications.

## Structure

```text
prometheus/
├── config/
│   ├── alert_rules/    # Directory for alerting and recording rules
│   └── prometheus.yml  # Master scrape configuration (template)
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Engine | Prometheus v3.9.0 | Metrics storage & query |
| Scraping | Prometheus Scraper | HTTP-based pull model |
| Alerting | PromQL Rules | Threshold-based alerting |

## Configuration

- **Scrape Config**: Defined in `config/prometheus.yml`. Secrets (e.g., OpenSearch password) are injected at startup via template substitution.
- **Alerting Rules**: Managed in `config/alert_rules/` and automatically reloaded via `--web.enable-lifecycle`.

## Persistence

- **Data Volume**: `prometheus-data` (mounted to `/prometheus`).
- **Retention**: 15 days (default).
- **Cleanup**: Handled via Docker volume management.

## Operational Status

> [!TIP]
> Use `curl -X POST http://prometheus:9090/-/reload` to trigger a configuration reload without restarting the container.

---

Copyright (c) 2026. Licensed under the MIT License.
