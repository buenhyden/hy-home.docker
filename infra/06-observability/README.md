# Observability Tier (06-observability)

## Overview

The `06-observability` tier implements the current LGTM stack (Loki, Grafana, Tempo, Prometheus) combined with Grafana Alloy, Alertmanager, Pushgateway, cAdvisor, and Pyroscope. External long-term metric storage is not declared in the tracked compose files.

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
├── docker-compose.dev.yml  # Root-included observability compose
├── docker-compose.yml      # Local obs compose
└── README.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Observability Tier (06-observability) folder index; services `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `pyroscope`, `alertmanager`, `pushgateway`; root include active via [root docker-compose.yml](../../docker-compose.yml) -> `infra/06-observability/docker-compose.dev.yml`; local obs compose is `docker-compose.yml` |
| Config files | `docker-compose.dev.yml`, `docker-compose.yml` |
| Config values | Uses non-secret env keys for MinIO app username, Grafana server/OAuth settings, and service ports; profiles: `obs`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../docker-compose.yml) -> `infra/06-observability/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Networks | `infra_net`, `k3d-hyhome` |
| Volumes | Prometheus/Loki/Tempo/Alloy/Grafana/Pyroscope config mounts plus bind-backed named data volumes under `${DEFAULT_OBSERVABILITY_DIR}` |
| Ports | `${LOKI_HOST_PORT:-3100}:${LOKI_PORT:-3100}`, `${TEMPO_HOST_PORT:-3200}:${TEMPO_PORT:-3200}`, `${ALLOY_OTLP_GRPC_HOST_PORT:-4317}:${ALLOY_OTLP_GRPC_PORT:-4317}`, `${ALLOY_OTLP_HTTP_HOST_PORT:-4318}:${ALLOY_OTLP_HTTP_PORT:-4318}`, `${CADVISOR_PORT:-8080}`, `${PUSHGATEWAY_PORT:-9091}`, `${PYROSCOPE_HOST_PORT:-4040}:${PYROSCOPE_PORT:-4040}` |
| Labels | `hy-home.tier` plus Traefik router/service labels for Prometheus, Loki, Tempo, Alloy, Grafana, cAdvisor, Pyroscope, Alertmanager, and Pushgateway |
| Secret refs | names: `opensearch_exporter_password`, `vault_token`, `minio_app_user_password`, `grafana_admin_password`, `grafana_client_secret`, `smtp_username`, `smtp_password`, `slack_webhook`; mounts: `/run/secrets/opensearch_exporter_password`, `/run/secrets/vault_token`, `/run/secrets/minio_app_user_password`, `/run/secrets/grafana_admin_password`, `/run/secrets/grafana_client_secret`, `/run/secrets/smtp_username`, `/run/secrets/smtp_password`, `/run/secrets/slack_webhook` |
| Healthcheck | Compose healthcheck declared for `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `pyroscope`, `alertmanager`, `pushgateway` |
| Operations | [Guide index](../../docs/05.operations/guides/06-observability/README.md), [Policy index](../../docs/05.operations/policies/06-observability/README.md), [Runbook index](../../docs/05.operations/runbooks/06-observability/README.md) |
| Validation | [validate-docker-compose.sh](../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose -f infra/06-observability/docker-compose.yml --profile obs config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Follow the [LGTM Stack Guide](../../docs/05.operations/guides/06-observability/01.lgtm-stack.md).
2. Refer to the [Alloy Collector Guide](../../docs/05.operations/guides/06-observability/alloy.md) for data piping.
3. Check the [Operations Policy](../../docs/05.operations/policies/06-observability/README.md) for retention.
4. Consult the [Observability Runbook](../../docs/05.operations/runbooks/06-observability/README.md) for recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Metrics    | Prometheus                     | v3.13.0                   |
| Logs       | Loki                           | v3.7.3-custom, MinIO bucket `loki-bucket` |
| Tracing    | Tempo                          | v3.0.2-custom, MinIO bucket `tempo-bucket` |
| Profiling  | Pyroscope                      | v2.1.0                    |
| Collector  | Grafana Alloy                  | v1.17.1                   |
| UI         | Grafana                        | v13.1.0                   |
| Alerting   | Alertmanager                   | v0.33.0                   |
| Batch metrics | Pushgateway                 | v1.11.3                   |
| Container metrics | cAdvisor                | v0.55.1                   |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `prometheus` | HTTP | `obs` | 9090 |
| `grafana` | HTTP | `obs` | 3000 |
| `loki` | HTTP | `obs` | 3100 |
| `tempo` | HTTP | `obs` | 3200 |
| `alloy` | HTTP | `obs` | 12345 (UI), 4317/4318 (OTLP) |
| `cadvisor` | HTTP | `obs` | 8080 |
| `pyroscope` | HTTP | `obs` | 4040 |
| `alertmanager` | HTTP | `obs` | 9093 |
| `pushgateway` | HTTP | `obs` | 9091 |

## Configuration

- **Persistence**: Loki and Tempo use MinIO (`04-data`) as the S3-compatible object store; Prometheus and Pyroscope use local bind-backed volumes.
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

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect the observability stack.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking observability documentation ready.

## Troubleshooting

- Start with `docker compose -f infra/06-observability/docker-compose.yml --profile obs config` to confirm LGTM service, network, volume, and secret references render.
- Check service-specific logs first, then follow the linked observability runbook for data-path failures.

## Related Documents

- [04-data](../04-data/README.md) - MinIO for telemetry storage.
- [02-auth](../02-auth/README.md) - Keycloak for SSO.
- [01-gateway](../01-gateway/README.md) - Traefik routing to UIs.

## AI Agent Guidance

1. Always use `Alloy` as the primary entry point for telemetry data (OTLP).
2. Dashboards MUST be provisioned via code in `grafana/provisioning/dashboards`.
3. Recording rules and alerts MUST be defined in `prometheus/config/alert_rules`.
4. Monitor `MinIO` bucket health as it is critical for Loki/Tempo availability.
