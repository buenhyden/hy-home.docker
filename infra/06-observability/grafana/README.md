# Grafana

> Unified visualization and dashboarding platform for metrics, logs, and traces.

## Overview

Grafana is the central UI for the observability tier, providing a single pane of glass for Prometheus metrics, Loki logs, Tempo traces, and Pyroscope profiles. It is integrated with Keycloak for secure SSO.

## Structure

```text
grafana/
├── dashboards/      # Pre-provisioned dashboard JSON files
├── provisioning/    # Auto-loaded datasources and alert rules
└── README.md        # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| UI | Grafana v12.3.3 | Visualization & Dashboards |
| Auth | Keycloak (OAuth2) | SSO & Role-based Access |
| Storage | SQLite (Internal) | Metadata & Dashboard storage |

## Security (SSO)

Grafana utilizes **Generic OAuth with PKCE (S256)** for authentication via Keycloak.

- **Client ID**: Managed via `${OAUTH2_PROXY_CLIENT_ID}`.
- **Role Mapping**:
  - `/admins` → Admin
  - `/editors` → Editor
  - Default → Viewer

## Provisioning

- **Datasources**: Automatically configured for Prometheus, Loki, Tempo, and Pyroscope via `provisioning/datasources/`.
- **Dashboards**: System-level dashboards are version-controlled in `dashboards/` and auto-imported.

## Persistence

- **Data Volume**: `grafana-data` (mounted to `/var/lib/grafana`).
- **Backup**: Database is stored as `grafana.db` (SQLite).

---

Copyright (c) 2026. Licensed under the MIT License.
