# Pushgateway

> Metrics buffer for ephemeral and batch jobs.

## Overview

Pushgateway allows ephemeral and batch jobs to expose metrics to Prometheus in cases where the standard pull model is not feasible (e.g., short-lived CI/CD tasks).

## Structure

```text
pushgateway/
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Buffer | prom/pushgateway:v1.11.2 | Metrics ingestion buffer |
| Scraper | Prometheus | Periodic push-to-pull bridge |

## Configuration

- **Ingestion**: Standard Prometheus Pushgateway API.
- **Exposure**: Exists only within the `infra_net` for Prometheus to scrape, or published via Traefik for external pushers.

## Persistence

- **State**: In-memory by default. Metrics will be lost upon container restart unless a persistent storage backend is configured.

## Operational Status

> [!CAUTION]
> Pushgateway is not a general-purpose metric proxy. Use only for batch jobs that cannot be scraped directly by Prometheus.

---

Copyright (c) 2026. Licensed under the MIT License.
