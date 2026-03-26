<!-- [ID:09-tooling:terraform] -->
# Guide: Terraform System

> Comprehensive guide for managing Infrastructure as Code (IaC) using the containerized Terraform environment.

## Overview

Terraform is used in `hy-home.docker` to provision and manage cloud resources (AWS, Azure) and local infrastructure (Docker, Kubernetes). To ensure environment parity and eliminate "works on my machine" issues, we use a containerized CLI approach.

## Key Concepts

### 1. Job-based Execution

Instead of a long-running service, Terraform is treated as a **job**.

- Always use `docker compose run --rm terraform` to clean up containers after execution.
- Profiles: Ensure the `tooling` profile is active or specified if needed.

### 2. State Management

- **Local State**: Stored in `infra/09-tooling/terraform/workspace/terraform.tfstate`.
- **Remote Backend**: It is highly recommended to use the `s3` backend (integrated with MinIO in `04-data`) for shared state and locking.

### 3. Credential Handling

Credentials are not stored in the container. They are mounted from the host:

- AWS: `/root/.aws` maps to your host `$HOME/.aws`.
- Azure: `/root/.azure` maps to your host `$HOME/.azure`.

## Common Workflows

### Initializing a Project

```bash
cd infra/09-tooling/terraform
docker compose run --rm terraform init
```

### Resource Provisioning (Plan & Apply)

Always generate a plan file before applying to prevent accidental changes.

```bash
# 1. Generate plan
docker compose run --rm terraform plan -out=tfplan

# 2. Review the plan
# 3. Apply the plan
docker compose run --rm terraform apply tfplan
```

### Formating and Validation

Maintain code quality by using built-in tools.

```bash
docker compose run --rm terraform fmt
docker compose run --rm terraform validate
```

## Troubleshooting

### Lock File Issues

If Terraform fails with "Error acquiring the state lock", ensure no other group members are applying changes. If a process crashed, refer to the [Runbook](./terraform.md#state-lock-recovery).

### Network Connectivity

The container uses `infra_net`. If you cannot reach local services (like MinIO), verify the network labels in `docker-compose.yml`.

## Related References

- **Infrastructure**: [Terraform Tool](../../../infra/09-tooling/terraform/README.md)
- **Operation**: [IaC Operations Policy](../../08.operations/09-tooling/terraform.md)
- **Runbook**: [Terraform Recovery Runbook](../../09.runbooks/09-tooling/terraform.md)
