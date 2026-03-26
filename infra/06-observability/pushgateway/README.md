# Pushgateway

> Metrics buffer for ephemeral and batch jobs within the `06-observability` tier.

## Overview

Pushgateway allows ephemeral and batch jobs to expose metrics to Prometheus in cases where the standard pull model is not feasible (e.g., short-lived CI/CD tasks or batch scripts). It acts as a temporary buffer that Prometheus scrapes at its own pace.

## Audience

이 README의 주요 독자:

- DevOps Engineers
- Backend Developers (Batch/CI)
- AI Agents

## Scope

### In Scope

- Pushgateway service configuration and deployment.
- Metrics ingestion and exposure for ephemeral jobs.
- Integration with Prometheus scraping.

### Out of Scope

- General-purpose metrics proxy or long-term storage.
- High-cardinality time-series storage (use direct instrumentation where possible).

## Structure

```text
pushgateway/
└── README.md           # This file
```

## Tech Stack

| Category | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| Buffer | [prom/pushgateway](https://hub.docker.com/r/prom/pushgateway) | v1.11.2 | Metrics ingestion buffer |
| Ingress | [Traefik](../../01-gateway/README.md) | v3.3.4 | SSL Termination & Routing |
| Scraper | [Prometheus](../prometheus/README.md) | v3.9.0 | Scrape-to-pull bridge |

## Usage Instructions

### Pushing Metrics

Jobs can push metrics via simple HTTP POST/PUT requests:

```bash
echo "some_metric 42" | curl --data-binary @- http://pushgateway.local/metrics/job/some_job
```

## Configuration

- **Ingestion**: Standard Prometheus Pushgateway API (Port 9091).
- **Exposure**: Accessible via `pushgateway.${DEFAULT_URL}` with SSL.
- **Network**: Integrated into `infra_net`.

## Operational Status

> [!CAUTION]
> Pushgateway is **not** a general-purpose proxy. Metrics persist in the gateway until explicitly deleted or overwritten. Unmanaged metric growth can lead to memory exhaustion and performance degradation.

## AI Agent Guidance

1. **PromQL Optimization**: When querying metrics from Pushgateway, always include the `job` label to distinguish between different batch runs.
2. **Maintenance**: Periodically check for stale metrics that haven't been updated.
3. **Traceability**: Refer to the dedicated guide for complex TTL or cleanup logic.

## Related References

- [System Guide](../../../docs/07.guides/06-observability/pushgateway.md)
- [Operational Policy](../../../docs/08.operations/06-observability/pushgateway.md)
- [Recovery Runbook](../../../docs/09.runbooks/06-observability/pushgateway.md)

---

Copyright (c) 2026. Licensed under the MIT License.
