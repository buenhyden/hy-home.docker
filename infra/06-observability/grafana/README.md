# Grafana

Grafana provides the visualization layer for metrics, logs, and traces.

## Services

| Service   | Image                    | Role       | Resources       |
| :-------- | :----------------------- | :--------- | :-------------- |
| `grafana` | `grafana/grafana:12.3.3` | Dashboard  | 0.5 CPU / 512MB |

## Networking

| Endpoint                | Port | Purpose |
| :---------------------- | :--- | :------ |
| `grafana.${DEFAULT_URL}`| 3000 | Web UI  |

## Security (SSO)

Grafana integrates with Keycloak for SSO via Generic OAuth with PKCE (`S256`).

- **Client**: Uses `${OAUTH2_PROXY_CLIENT_ID}` and the `oauth2_proxy_client_secret` Docker Secret.
- **Scopes**: `openid`, `profile`, `email`, `offline_access`, `groups`
- **Role mapping**: Keycloak group `/admins` → Grafana Admin; `/editors` → Editor; otherwise Viewer.
- **Auto-login**: Login form is disabled; SSO is mandatory.

## Persistence

- **DB**: SQLite stored in `grafana-data` volume (bind-mounted to `${DEFAULT_OBSERVABILITY_DIR}/grafana`).

## File Map

| Path                   | Description                              |
| ---------------------- | ---------------------------------------- |
| `provisioning/`        | Auto-loaded datasources and alert rules. |
| `dashboards/`          | Pre-provisioned dashboard JSON files.    |
| `README.md`            | Service notes and SSO setup.             |
