<!-- [ID:09-tooling:terrakube] -->
# Operations: Terrakube Policy

> Operational guidelines and governance for the centralized Terrakube IaC platform.

## Governance Overview

Terrakube serves as the authoritative source for infrastructure state. Strict access control and operational hygiene are required to prevent data loss or unauthorized provisioning.

## Access Control Policy

### 1. Workspace RBAC
- **Admin**: Full control over organization settings and workspace secrets (Senior DevOps only).
- **Maintainer**: Can trigger plans and applies for specific workspaces.
- **Reader**: View-only access to execution logs.

### 2. SSO Authentication
- All users must authenticate via Keycloak.
- Local admin accounts are disabled in production to ensure auditability.

## Resource & Execution Policy

| Policy Type | Setting | Description |
| :--- | :--- | :--- |
| **Execution Timeout** | 60 minutes | Jobs exceeding this limit are killed to prevent resource leaks. |
| **Max Concurrency** | 5 jobs | Maximum simultaneous executors per node. |
| **Log Retention** | 30 days | Execution logs are purged from the DB after one month. |

## Registry Maintenance

- **Module Versioning**: All modules must follow Semantic Versioning (SemVer).
- **Audit**: Monthly review of unused modules and old versions to reclaim storage.

## Security Standards

- **Secret Scanning**: All Git repositories integrated with Terrakube must undergo pre-commit scanning.
- **Sensitive Variables**: Mandatory encryption for all cloud provider secrets hosted within Terrakube.

## Routine Maintenance

### Weekly
- Monitor `terrakube-api` logs for worker drift or storage connectivity errors.
- Verify `tfstate` bucket health in MinIO.

### Monthly
- Perform a manual backup of the Terrakube metadata database (PostgreSQL).
- Update the base Docker images for executors to include the latest security patches.

## Related References

- **Infrastructure**: [Terrakube Platform](../../../infra/09-tooling/terrakube/README.md)
- **Guide**: [Terrakube System Guide](../../07.guides/09-tooling/terrakube.md)
- **Runbook**: [Terrakube Recovery Runbook](../../09.runbooks/09-tooling/terrakube.md)
