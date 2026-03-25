# Observability Tier (06-observability)

> Centralized telemetry, monitoring, and debugging hub.

## Overview

The `06-observability` tier implements the LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus) combined with Grafana Alloy and Pyroscope to provide a unified "Single Source of Truth" for system health. It handles metrics, logs, traces, and continuous profiling across the entire `hy-home.docker` ecosystem.

## Audience

이 README의 주요 독자:

- SREs & Platform Engineers (Stack maintenance)
- Developers (Debugging & Performance tuning)
- AI Agents (Automated health monitoring)

## Scope

### In Scope

- LGTM Stack (Loki, Grafana, Tempo, Prometheus)
- Grafana Alloy (Unified collector)
- Pyroscope (Continuous profiling)
- Alertmanager (Alert routing)
- cAdvisor (Container metrics)

### Out of Scope

- Application-level business analytics
- External cloud monitoring (Datadog/New Relic)
- Long-term audit logs (handled by `04-data` / `03-security`)

## Structure

```text
06-observability/
├── alertmanager/    # Alert routing logic
├── alloy/          # Unified telemetry collection
├── grafana/        # Dashboards & Visualization
├── loki/           # Log aggregation
├── prometheus/     # Metrics storage
├── pyroscope/      # Continuous profiling
├── tempo/          # Distributed tracing
├── docker-compose.yml
└── README.md
```

## How to Work in This Area

1. Follow the [LGTM Stack Guide](../../docs/07.guides/06-observability/01.lgtm-stack.md).
2. Refer to the [Alloy Collector Guide](../../docs/07.guides/06-observability/02.alloy-collector.md) for data piping.
3. Check the [Operations Policy](../../docs/08.operations/06-observability/README.md) for retention.
4. Consult the [Observability Runbook](../../docs/09.runbooks/06-observability/README.md) for recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Metrics    | Prometheus                     | v3.9.0                    |
| Logs       | Loki                           | v3.6.6 (S3 Backend)       |
| Tracing    | Tempo                          | v2.10.1 (S3 Backend)      |
| Profiling  | Pyroscope                      | v1.18.1                   |
| Collector  | Grafana Alloy                  | v1.13.1                   |
| UI         | Grafana                        | v12.3.3                   |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `prometheus` | HTTP | `obs` | 9090 |
| `grafana` | HTTP | `obs` | 3000 |
| `loki` | HTTP | `obs` | 3100 |
| `tempo` | HTTP | `obs` | 3200 |
| `alloy` | HTTP | `obs` | 12345 (UI), 4317/4318 (OTLP) |

## Configuration

- **Persistence**: Loki and Tempo use MinIO (`04-data`) as the S3-compatible object store.
- **Auth**: Grafana is integrated with Keycloak (`02-auth`) for OAuth2 SSO.
- **Networking**: All telemetry traffic flows through the `infra_net`.

## Testing

```bash
# Check service health
docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy

# Verify Alloy configuration
docker exec infra-alloy alloy run --test /etc/alloy/config.alloy
```

## Change Impact

- Modifying retention periods in Loki/Tempo will affect MinIO storage usage.
- Changes in Alloy OTLP endpoints will break telemetry for all downstream services.
- Grafana plugin updates may require manual dashboard migration.

## Related References

- [04-data](../04-data/README.md) - MinIO for telemetry storage.
- [02-auth](../02-auth/README.md) - Keycloak for SSO.
- [01-gateway](../01-gateway/README.md) - Traefik routing to UIs.

## AI Agent Guidance

1. Always use `Alloy` as the primary entry point for telemetry data (OTLP).
2. Dashboards MUST be provisioned via code in `grafana/provisioning/dashboards`.
3. Recording rules and alerts MUST be defined in `prometheus/config/alert_rules`.
4. Monitor `MinIO` bucket health as it is critical for Loki/Tempo availability.
