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

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Observability Tier (06-observability) service leaf in `06-observability`; services: `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, plus 11 more; root include active via [root docker-compose.yml](../../docker-compose.yml) -> `infra/06-observability/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Config files | `docker-compose.dev.yml`, `docker-compose.yml` |
| Config values | env keys: `MINIO_APP_USERNAME`, `GF_SERVER_ROOT_URL`, `GF_SERVER_DOMAIN`, `GF_AUTH_OAUTH_AUTO_LOGIN`, `GF_AUTH_DISABLE_LOGIN_FORM`, `GF_SECURITY_ADMIN_USER`, `GF_SECURITY_ADMIN_PASSWORD__FILE`, `GF_USERS_ALLOW_SIGN_UP`, plus 27 more; profiles: `obs`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../docker-compose.yml) -> `infra/06-observability/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Networks | `infra_net`, `k3d-hyhome` |
| Volumes | `./prometheus/config/prometheus.dev.yml:/etc/prometheus/prometheus.yml:ro`, `./prometheus/config/alert_rules:/etc/prometheus/alert_rules:ro`, `prometheus-data:/prometheus:rw`, `./loki/config/loki-config.yaml:/etc/loki/loki-config.yaml:ro`, `loki-data:/loki:rw`, `./tempo/config/tempo.yaml:/etc/tempo.yaml:ro`, `tempo-data:/var/tempo:rw`, `./alloy/config/config.alloy:/etc/alloy/config.alloy:ro`, plus 24 more |
| Ports | `${LOKI_HOST_PORT:-3100}:${LOKI_PORT:-3100}`, `${TEMPO_HOST_PORT:-3200}:${TEMPO_PORT:-3200}`, `${ALLOY_OTLP_GRPC_HOST_PORT:-4317}:${ALLOY_OTLP_GRPC_PORT:-4317}`, `${ALLOY_OTLP_HTTP_HOST_PORT:-4318}:${ALLOY_OTLP_HTTP_PORT:-4318}`, `${CADVISOR_PORT:-8080}`, `${PUSHGATEWAY_PORT:-9091}`, `${PYROSCOPE_HOST_PORT:-4040}:${PYROSCOPE_PORT:-4040}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.prometheus.rule`, `traefik.http.routers.prometheus.entrypoints`, `traefik.http.routers.prometheus.tls`, `traefik.http.routers.prometheus.middlewares`, `traefik.http.services.prometheus.loadbalancer.server.port`, `traefik.http.routers.loki.rule`, plus 40 more |
| Secret refs | names: `opensearch_exporter_password`, `vault_token`, `minio_app_user_password`, `grafana_admin_password`, `grafana_client_secret`, `smtp_username`, `smtp_password`, `slack_webhook`; mounts: `/run/secrets/opensearch_exporter_password`, `/run/secrets/vault_token`, `/run/secrets/minio_app_user_password`, `/run/secrets/grafana_admin_password`, `/run/secrets/grafana_client_secret`, `/run/secrets/smtp_username`, `/run/secrets/smtp_password`, `/run/secrets/slack_webhook` |
| Healthcheck | Compose healthcheck declared for `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `alertmanager`, `pushgateway`, plus 9 more |
| Operations | [Guide index](../../docs/05.operations/guides/06-observability/README.md), [Policy index](../../docs/05.operations/policies/06-observability/README.md), [Runbook index](../../docs/05.operations/runbooks/06-observability/README.md) |
| Validation | [validate-docker-compose.sh](../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Follow the [LGTM Stack Guide](../../docs/05.operations/guides/06-observability/01.lgtm-stack.md).
2. Refer to the [Alloy Collector Guide](../../docs/05.operations/guides/06-observability/alloy.md) for data piping.
3. Check the [Operations Policy](../../docs/05.operations/guides/06-observability/README.md) for retention.
4. Consult the [Observability Runbook](../../docs/05.operations/guides/06-observability/README.md) for recovery.

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

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect the observability stack.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking observability documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm LGTM service, network, volume, and secret references render.
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
