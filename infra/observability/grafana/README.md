# Grafana

Grafana is the open-source analytics & monitoring solution for every database. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## 🚀 Overview

- **Service**: `grafana`
- **Docker Image**: `grafana/grafana:12.3.1`
- **Port**: `3000` (Web UI)

## ⚙️ Configuration

Grafana is configured primarily through **Environment Variables** in `docker-compose.yml` and **Provisioning files**.

### 1. Environment Variables (Authentication)

Authentication (Keycloak OAuth2) is configured via environment variables in `infra/observability/docker-compose.yml`.
Key variables include:
- `GF_AUTH_GENERIC_OAUTH_CLIENT_ID`: OAuth2 Client ID (from `.env`)
- `GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET`: OAuth2 Client Secret (from `.env`)
- `GF_SECURITY_ADMIN_USER` / `PASSWORD`: Initial admin credentials.

### 2. Provisioning

Grafana uses "Provisioning" to automatically configure datasources and dashboards on startup, avoiding manual setup.

- **Datasources**: `provisioning/datasources/datasource.yml`
  - **Prometheus**: Metrics backend.
  - **Loki**: Logs backend.
  - **Tempo**: Traces backend (includes links to Loki for Trace-to-Log correlation).
  - **Alertmanager**: Alert handling.

- **Dashboards**: `provisioning/dashboards/dashboard.yml`
  - Loads JSON dashboards from the `dashboards/` directory.

## 📊 Dashboards

Pre-configured dashboards are stored in `dashboards/*.json`:
- **Infrastructure**: Node Exporter, cAdvisor.
- **Databases**: PostgreSQL, Redis, MongoDB.
- **Apps**: Keycloak, MinIO, N8n, Traefik, etc.

## 🔗 Integration

- **Traefik**: Exposed via `grafana.${DEFAULT_URL}` (HTTPS).
- **Keycloak**: SSO Login enabled.

## 🛠 Directory Structure

```text
grafana/
├── dashboards/                  # JSON files for dashboards
│   ├── *.json
├── provisioning/
│   ├── dashboards/
│   │   └── dashboard.yml        # Config to load dashboards from filesystem
│   └── datasources/
│   │   └── datasource.yml       # Config for Prometheus, Loki, Tempo
└── README.md
```
