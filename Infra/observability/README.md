# Observability Stack

## Overview

A comprehensive observability stack including Prometheus, Grafana, Loki, Tempo, Alloy, and Alertmanager.

## Services

- **prometheus**: Metrics storage and querying.
  - URL: `https://prometheus.${DEFAULT_URL}`
- **loki**: Log aggregation system.
- **tempo**: Distributed tracing backend.
- **grafana**: Visualization and analytics software.
  - URL: `https://grafana.${DEFAULT_URL}`
- **alloy**: OpenTelemetry Collector & Prometheus Agent.
  - URL: `https://alloy.${DEFAULT_URL}`
- **cadvisor**: Container metrics collector.
- **alertmanager**: Alert handling.
  - URL: `https://alertmanager.${DEFAULT_URL}`

## Configuration

### Environment Variables

- `GF_SERVER_ROOT_URL`: Grafana root URL.
- `GF_AUTH_GENERIC_OAUTH_ENABLED`: `true` (Keycloak integration).
- `SMTP_USERNAME`/`PASSWORD`: Alerting email credentials.

### Volumes

- `prometheus-data`: `/prometheus`
- `loki-data`: `/loki`
- `tempo-data`: `/var/tempo`
- `grafana-data`: `/var/lib/grafana`
- `alertmanager-data`: `/alertmanager`
- `./**/config/*`: Configuration files for each service.

## Networks

- `infra_net`
  - Fixed IPs assigned for component communication (`172.19.0.30-36`).

## Traefik Routing

- Each service has its own subdomain (prometheus, grafana, alloy, alertmanager) under `${DEFAULT_URL}`.
- All use `infra_net` and are protected by TLS.
- Grafana and Alloy configured with SSO.
