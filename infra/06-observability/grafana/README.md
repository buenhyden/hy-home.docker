# Grafana Visualization & Dashboards

Unified visualization hub for metrics, logs, traces, and profiling.

## Scope

Grafana serves as the primary observability portal for the `hy-home.docker` ecosystem. It integrates multiple data sources including Prometheus, Loki, Tempo, and Pyroscope into cohesive dashboards, providing a single pane of glass for monitoring, alerting, and debugging.

- **Primary URL**: `https://grafana.${DEFAULT_URL}`
- **Authentication**: Keycloak SSO (OIDC) with automatic role mapping.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Frontend | Grafana | v12.3.3 |
| Auth | Generic OAuth2 | Keycloak Integration |

## System Components

- **Dashboards**: 34+ provisioned JSON dashboards across domains.
  - **Infrastructure**: Node Exporter, cAdvisor, Docker, Linux Hosts.
  - **Middleware**: PostgreSQL, Redis, Kafka, MinIO.
  - **AI/ML**: Ollama, Qdrant.
  - **Services**: Application-specific metrics and SLI/SLO views.
- **Datasources**: Pre-integrated Prometheus (metrics), Loki (logs), Tempo (traces), and Pyroscope (profiles).
- **Provisioning**: Entirely code-based configuration for datasources and dashboards.

## Documentation

| Document | Description |
| :--- | :--- |
| [System Guide](file:///home/hy/project-infra/hy-home.docker/docs/07.guides/06-observability/grafana.md) | Architecture, SSO mapping, and datasource integration details. |
| [Operational Policy](file:///home/hy/project-infra/hy-home.docker/docs/08.operations/06-observability/grafana.md) | Dashboard provisioning, RBAC, and datasource maintenance. |
| [Recovery Runbook](file:///home/hy/project-infra/hy-home.docker/docs/09.runbooks/06-observability/grafana.md) | Troubleshooting failing logins, dashboards, or service unavailability. |

## AI Agent Guidance

1. **Provisioning**: Dashboards MUST NOT be edit-locked in production. Always use code-based provisioning in the `dashboards/` directory.
2. **SSO Mapping**: Role mapping is managed via `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH` in `docker-compose.yml`. Groups starting with `/admins` map to `Admin`.
3. **Variables**: Use Variables (Template tags) for cluster/node/service filtering to keep dashboards portable.
4. **Color Palette**: Adhere to the `hy-home.docker` visual standards for dashboard consistency.
