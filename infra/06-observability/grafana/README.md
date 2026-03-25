# Grafana Visualization & Dashboards

> Unified visualization hub for metrics, logs, traces, and profiling.

## Overview

Grafana serves as the primary observability portal. It integrates multiple data sources (Prometheus, Loki, Tempo, Pyroscope) into cohesive dashboards. Access is secured via Keycloak SSO with role-based access control (RBAC).

## Audience

- All users (Monitoring & Debugging)
- SREs (Dashboard provisioning)

## Structure

```text
grafana/
├── dashboards/      # Provisioned JSON dashboards
├── provisioning/    # Datasource & dashboard YAMLs
└── README.md
```

## How to Work in This Area

1. Add new dashboards by placing JSON files in `dashboards/`.
2. Configure datasources in `provisioning/datasources/`.
3. Refer to the [SSO Setup](../../../docs/07.guides/02-auth/01.keycloak-setup.md) for auth issues.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Frontend | Grafana | v12.3.3 |
| Auth | Generic OAuth2 | Keycloak Integration |

## Configuration

| Feature | Status | Notes |
| :--- | :--- | :--- |
| `OAuth2` | Enabled | Auto-assign Editor/Viewer |
| `S3 Backend` | Enabled | For remote caching (experimental) |

## AI Agent Guidance

1. Dashboards MUST NOT be edit-locked in production; use code-based provisioning.
2. Use Variables (Template tags) for cluster/node/service filtering.
3. Consistently use the `hy-home.docker` color palette for consistency.
