<!-- [ID:09-tooling:terrakube] -->
# Guide: Terrakube Platform

> User guide for managing infrastructure automation workflows via the Terrakube platform.

## Overview

Terrakube is an open-source alternative to Terraform Cloud, providing a centralized control plane for Infrastructure as Code (IaC). It manages workspaces, variables, team access, and private modules.

## Getting Started

### 1. Initial Login

Access the UI at `https://terrakube-ui.${DEFAULT_URL}`. Authentication is integrated with Keycloak; use your engineering credentials.

### 2. Organizations and Workspaces

- **Organizations**: High-level groups (e.g., `prod`, `dev`, `shared`).
- **Workspaces**: Individual projects mapped to a specific Git repository and set of variables.

## Feature Breakdown

### Private Module Registry

Terrakube allows you to host internal Terraform modules.

- To publish: Tag your module repository (e.g., `terraform-aws-s3-v1.0.0`).
- To consume: Reference the module using the Terrakube API URL in your `.tf` code.

### Variable Management

- **Environment Variables**: For provider credentials (AWS_ACCESS_KEY, etc.).
- **Terraform Variables**: For specific infrastructure parameters.
- **Sensitive Variables**: Marked as "Sensitive" are stored encrypted and never displayed in logs.

### UI-Driven Workflows

- **Plan**: Trigger a `terraform plan` to view proposed changes in the UI logs.
- **Apply**: Manual or automatic approval of plans to execute changes.

## Integration Details

### Remote State (MinIO)

Terrakube automatically manages its own internal state storage in the `tfstate` bucket of MinIO. Manual configuration of the `s3` backend in your `.tf` files is not required when running through the platform.

### Executor Model

The `terrakube-executor` spins up ephemeral Docker containers for every job. It requires access to `/var/run/docker.sock` on the host to manage these child containers.

## Troubleshooting

### Executor Timeout

If a job is stuck in "Pending" status, verify that the `terrakube-executor` container is healthy:

```bash
docker compose logs -f terrakube-executor
```

### SSO Failures

If OIDC logout occurs frequently, check the token expiration settings in the `hy-home.realm` of Keycloak.

## Related References

- **Infrastructure**: [Terrakube Platform](../../../infra/09-tooling/terrakube/README.md)
- **Operation**: [Terrakube Operations Policy](../../08.operations/09-tooling/terrakube.md)
- **Runbook**: [Terrakube Recovery Runbook](../../09.runbooks/09-tooling/terrakube.md)
