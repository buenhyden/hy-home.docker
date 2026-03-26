<!-- [ID:09-tooling:terraform] -->
# Operations: Terraform Policy

> Operational guidelines and policies for managing infrastructure via Terraform.

## Policy Overview

All infrastructure changes in `hy-home.docker` must be managed via Terraform to ensure auditability and reproducibility.

## State Management Policy

### 1. Remote State Requirement
- For any environment with more than one contributor, a **Remote Backend** (S3/MinIO) is mandatory.
- State locking must be enabled (via DynamoDB or MinIO Object Lock).

### 2. State Backups
- Remote states are automatically versioned by the backend.
- Monthly exports of the `.tfstate` to the `04-data/backups` tier are required for disaster recovery.

## Deployment Workflow

| Step | Action | Mandatory? |
| :--- | :--- | :--- |
| **Validation** | `validate` & `fmt` | Yes |
| **Planning** | `plan -out=tfplan` | Yes |
| **Peer Review** | Review `tfplan` output | Recommended |
| **Execution** | `apply tfplan` | Yes |

> [!IMPORTANT]
> Never use `terraform apply` without a pre-generated plan file in production environments.

## Maintenance Cycles

### Provider Updates
- Check for provider updates (AWS, Docker, Kubernetes) every **quarter**.
- Test updates in a non-production workspace before merging.

### Credential Rotation
- Host-level cloud credentials mounted to the Terraform container must be rotated every **90 days**.

## Compliance & Security

- **Secrets**: Never hardcode credentials in `.tf` files. Use environment variables or secret managers (Vault).
- **Versioning**: Pin all provider and module versions to prevent breaking changes during `init`.

## Related References

- **Infrastructure**: [Terraform Tool](../../../infra/09-tooling/terraform/README.md)
- **Guide**: [Terraform System Guide](../../07.guides/09-tooling/terraform.md)
- **Runbook**: [Terraform Recovery Runbook](../../09.runbooks/09-tooling/terraform.md)
