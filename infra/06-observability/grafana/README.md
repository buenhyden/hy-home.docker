# Grafana

Grafana provides the visualization layer for metrics, logs, and traces.

## Services

| Service   | Image                    | Role         | Resources       |
| :-------- | :----------------------- | :----------- | :-------------- |
| `grafana` | `grafana/grafana:11.5.2` | Visualization| 0.5 CPU / 1GB RAM |

## Networking

| Endpoint                | Port | Purpose                |
| :---------------------- | :--- | :--------------------- |
| `grafana.${DEFAULT_URL}`| 3000 | Web UI                 |

## Security (SSO)

Grafana is integrated with Keycloak for SSO via Generic OAuth.

- **Client**: `grafana`
- **Scopes**: `openid`, `profile`, `email`, `groups`
- **Role Mapping**: Admin/Editor/Viewer roles mapped from Keycloak groups.

## Persistence

- **DB**: Local SQLite (default) or shared PostgreSQL.
- **Plugins**: Persisted in `grafana-plugins` volume.

## File Map

| Path                   | Description                           |
| ---------------------- | ------------------------------------- |
| `provisioning/`        | Auto-loaded datasources and dashboards. |
| `README.md`            | Service notes and SSO setup.          |
