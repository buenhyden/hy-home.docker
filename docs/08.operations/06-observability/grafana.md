# Grafana Operational Policy (06-observability)

Policies and procedures for maintaining the visualization and alerting hub.

## Dashboard Provisioning

1. **Code-First Mandate**: All production dashboards MUST be stored as JSON files in `infra/06-observability/grafana/dashboards/`.
2. **Directory Structure**:
   - `provisioning/dashboards/dashboards.yml`: Configuration for the dashboard provider.
   - `dashboards/`: Directory containing all `.json` dashboard definitions.
3. **Standard Headers**: Dashboards should include a standardized title, version, and appropriate template variables (e.g., `$job`, `$instance`).
4. **Lock Policy**: Provisioned dashboards are immutable in the UI to prevent drift. Changes must be committed to git.
5. **Adding a New Dashboard**:
   - Place the JSON file in `infra/06-observability/grafana/dashboards/`.
   - Ensure a unique `uid` is set in the JSON to prevent collisions.
   - Restart Grafana or wait for the provider to re-scan.

## RBAC Management

- **External Groups**: User access is exclusively managed through Keycloak groups (`/admins`, `/editors`).
- **Admin Access**: Limited to core infrastructure maintainers.
- **Editor Access**: Granted to developers for creating/testing new visualization patterns in development.

## Maintenance Procedures

### Datasource Management

New datasources must be added via `infra/06-observability/grafana/provisioning/datasources/datasource.yml`. Avoid manual datasource creation to ensure service portability and reliability. Note the `uid` mapping (e.g., `Prometheus`, `Loki`, `Tempo`) used in dashboard references.

### Version Upgrades

Grafana version updates are managed via `docker-compose.yml`. Before upgrading, verify compatibility with existing plugins and OIDC mapping logic.

### Backup & Persistence

- **Data Volume**: The `/var/lib/grafana` directory is persisted via a Docker volume (`grafana-data`).
- **Dashboard Backup**: Since dashboards are provisioned from git, recovery is as simple as restarting the container with the correct volume mount.

## References

- [Grafana System Guide](../../07.guides/06-observability/grafana.md)
- [Loki Operational Policy (Retention)](loki.md)
