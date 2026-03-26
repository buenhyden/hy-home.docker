<!-- [ID:09-tooling:terrakube] -->
# Runbook: Terrakube Recovery (P2)

> Procedures for recovering the Terrakube platform from executor failures, sync drift, and database corruption.

## Symptoms

- UI shows jobs stuck in "Pending" or "Running" for hours.
- Login redirection loops between Terrakube and Keycloak.
- "Error: S3 Storage not reachable" in API logs.
- Workspace state is "Locked" permanently in the UI.

## Diagnostic Steps

### 1. Check API and Executor Health

Terrakube provides Spring Actuator endpoints for health checks.

```bash
curl -I https://terrakube-api.${DEFAULT_URL}/actuator/health
```

### 2. Verify Docker Socket Access

The executor requires a healthy Docker socket to spawn Terraform runs.

```bash
docker exec terrakube-executor docker info
```

## Recovery Procedures

### 1. Cleaning Up Hung Executors

If the UI shows a job as running but the host has no associated container:

1. Locate the `terrakube-executor` logs to find the orphan job ID.
2. Manually kill the subprocess if it exists on the host.
3. Restart the executor service to reset internal queue state:

   ```bash
   cd ${DEFAULT_TOOLING_DIR}/terrakube
   docker compose restart terrakube-executor
   ```

### 2. Resolving OIDC / DEX Auth Loops

If users cannot login despite valid Keycloak credentials:

1. Check the `terrakube-api` log for "Invalid Token" or "JWK extraction failure".
2. Ensure the `OAUTH2_PROXY_CLIENT_ID` and Secrets match between Keycloak and the `docker-compose.yml`.
3. Restart the API server to refresh the OIDC configuration.

### 3. Manual Workspace Unlock

If a workspace is stuck in a locked state and "Force Unlock" in the UI fails:

1. Connect to the `terrakube` database in PostgreSQL.
2. Update the workspace record status manually.

   ```sql
   UPDATE workspace SET locked = false WHERE name = '<workspace_name>';
   ```

> [!WARNING]
> Manual DB modifications are high-risk. Always back up the `terrakube` database before running raw SQL.

## Escalation Policy

- **P1**: Total loss of the `tfstate` bucket content in MinIO -> Follow Disaster Recovery Plan.
- **P2**: Intermittent executor failures or UI sync issues -> Follow manual restart and queue cleanup.

## Related References

- **Infrastructure**: [Terrakube Platform](../../../infra/09-tooling/terrakube/README.md)
- **Guide**: [Terrakube System Guide](../../07.guides/09-tooling/terrakube.md)
- **Operation**: [Terrakube Operations Policy](../../08.operations/09-tooling/terrakube.md)
