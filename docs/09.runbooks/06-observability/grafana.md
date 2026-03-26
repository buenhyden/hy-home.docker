# Grafana Recovery Runbook (06-observability)

Standardized procedures for resolving common Grafana service disruptions.

## SSO Authentication Failures

### Symptom: "OAuth Login Failed" or redirection loops

1. **Verify Keycloak Status**: Ensure the Keycloak service is healthy and reachable.
2. **Check Secrets**: Ensure `oauth2_proxy_client_secret` is correctly loaded as a secret in the `06-observability` tier.
3. **Inspect Logs**: Check Grafana logs for OAuth2 token validation errors:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml logs grafana | grep -i "oauth"
   ```

4. **Group Synchronization**: If a user has incorrect roles, verify their group membership in Keycloak. Groups must start with `/admins` or `/editors`.
5. **Time Sync**: Ensure clocks are synchronized between Grafana and Keycloak (NTP check).

## Datasource Connection Issues

### Symptom: Dashboard panels show "Datasource not found" or "Query error"

1. **Verify Backend Status**: Check if Prometheus, Loki, or Tempo containers are running and healthy.
2. **Check UID Matching**: Ensure the dashboard expects the same `uid` defined in `datasource.yml` (e.g., `Prometheus` vs `prometheus`).
3. **Trace-to-Log Link Break**: If "Logs" button disappears in Tempo, verify `tracesToLogsV2` configuration in `datasource.yml`.

## Dashboard Provisioning Issues

1. **Verify Volume Mount**: Ensure `./grafana/dashboards` is correctly mounted to `/etc/grafana/dashboards`.
2. **Check YAML Config**: Inspect `infra/06-observability/grafana/provisioning/dashboards/dashboards.yml` for correct path references.
3. **Grafana Refresh**: Restart the Grafana service to force a re-scan of the provisioning directory:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml restart grafana
   ```

## Service Unavailability

### Symptom: HTTP/503 or healthcheck failed

1. **Resource Check**: Verify Grafana memory usage. By default, it is limited to 1GB.
2. **Database Integrity**: Check `/var/lib/grafana/grafana.db` (SQLite) for corruption if the service fails to start.
3. **Healthcheck Probe**: Run the healthcheck command manually:

   ```bash
   docker exec grafana wget -q --spider http://localhost:3000/api/health
   ```

## References

- [Grafana System Guide](file:///home/hy/projects/hy-home.docker/docs/07.guides/06-observability/grafana.md)
- [Keycloak Recovery Runbook](file:///home/hy/projects/hy-home.docker/docs/09.runbooks/02-auth/keycloak.md)
