# Prometheus Metrics Storage

> High-performance time-series database for system and application metrics.

## Overview

Prometheus is the core metrics engine for the `hy-home.docker` platform. It scrapes targets defined via service discovery, stores time-series data, and evaluates alerting rules. It supports high-cardinality data and provides a powerful query language (PromQL).

## Audience

- SREs (Monitoring architecture)
- Developers (Metric instrumentation)

## Structure

```text
prometheus/
├── config/
│   ├── alert_rules/    # YAML alerting rules
│   └── prometheus.yml  # Main configuration template
└── README.md
```

## How to Work in This Area

1. Add scrape targets to `prometheus.yml`.
2. Define alerting rules in `config/alert_rules/`.
3. Check the [Operations Guide](../../../docs/07.guides/06-observability/01.lgtm-stack.md).

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Engine | Prometheus | v3.9.0 |
| Storage | TSDB | Persistent Volume |

## Configuration

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PROMETHEUS_PORT` | 9090 | Internal API/UI port |

## Testing

```bash
# Check config syntax
docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
```

## AI Agent Guidance

1. Use `Recording Rules` for expensive queries to optimize dashboard performance.
2. Scrape intervals should follow the standard (15s for infra, 30s-60s for apps).
3. Ensure all scrape targets are reachable via the `infra_net`.
