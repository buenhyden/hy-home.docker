# [INFRA] 06-observability: prometheus

> High-performance time-series database for system and application metrics.

## Scope

Prometheus is the core metrics engine for the `hy-home.docker` platform. It scrapes targets defined via service discovery, stores time-series data, and evaluates alerting rules. It supports high-cardinality data and provides a powerful query language (PromQL).

- **Role**: Metrics Aggregation & Alerting Engine.
- **Layer**: `06-observability` (Telemetry Storage).
- **Interface**: [http://prometheus.hy-home.local](http://prometheus.hy-home.local) (via Traefik).

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Metrics DB | Prometheus | v3.9.0 |
| Configuration | YAML-based | Static & File-based SD |
| Tooling | promtool | Config/Rule Validation |

## System Components

- **Scrape Configs**: Defined in `config/prometheus.yml` (20+ internal & infra jobs).
- **Alerting Rules**: Modularized in `config/alert_rules/` (9+ files by domain).
- **Storage**: Persistent TSDB volume with retention policies.

## Management Guide

### 1. Operations & Configuration

- **Scrape Targets**: Update `scrape_configs` in `prometheus.yml`.
- **Alerting Rules**: Add/Modify YAML files in `config/alert_rules/`.
- **Validation**:

  ```bash
  docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
  ```

### 2. Traceability

- **System Guide**: [docs/07.guides/06-observability/prometheus.md](../../../docs/07.guides/06-observability/prometheus.md)
- **Operations Guide**: [docs/08.operations/06-observability/prometheus.md](../../../docs/08.operations/06-observability/prometheus.md)
- **Runbook**: [docs/09.runbooks/06-observability/prometheus.md](../../../docs/09.runbooks/06-observability/prometheus.md)

## AI Agent Guidance

1. **PromQL Optimization**: Use Recording Rules for expensive dashboard queries.
2. **Rule Management**: Always validate with `promtool` before applying changes.
3. **Scrape Settings**: Standard intervals: 15s (infra), 30s-60s (apps).
4. **Networking**: Scrape targets must be reachable via the `infra_net`.
