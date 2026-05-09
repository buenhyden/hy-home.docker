<!-- [ID:09-tooling:terraform] -->
# Terraform Infrastructure Tool

> Containerized Terraform CLI workspace for IaC plan/apply workflows

## Overview

`infra/09-tooling/terraform/` provides a standardized Terraform execution container. The service uses `hashicorp/terraform:1.14.4`, mounts a local `workspace/` directory, and exposes host cloud credential directories as read-only mounts for local IaC workflows.

This README is the service-level entrypoint. It describes the Compose surface and links to the canonical guide, operations policy, and runbook.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Terraform CLI Compose service definition
- Local `workspace/` mount and credential mount boundaries
- Service-level usage commands and related stage document links

### Out of Scope

- Terraform module source authoring policy
- Cloud account credential values or private keys
- Terrakube orchestration workflows
- Long-form IaC operations policy or recovery procedure

## Structure

```text
terraform/
├── docker-compose.yml  # Terraform CLI service with tooling/iac profiles
├── workspace/          # Local Terraform working directory
└── README.md           # This file
```

## How to Work in This Area

1. Read the parent [`../README.md`](../README.md) and this service Compose file before changing Terraform tooling.
2. Keep cloud credentials outside the repository; this service mounts `$HOME/.aws` and `$HOME/.azure` read-only.
3. Put Terraform working files under `workspace/` only when they are intentionally part of the local workflow.
4. Update the related guide, operation, or runbook when usage, state handling, or recovery behavior changes.

## Tech Stack

| Component | Technology | Version / Source | Role |
| --- | --- | --- | --- |
| Engine | HashiCorp Terraform | `hashicorp/terraform:1.14.4` | IaC CLI |
| Runtime | Docker Compose | `tooling`, `iac` profiles | Containerized execution |
| Workspace | Bind mount | `./workspace:/workspace:rw` | Terraform working directory |
| Credentials | Host bind mounts | `$HOME/.aws`, `$HOME/.azure` read-only | Cloud provider access |

## Usage Instructions

```bash
cd infra/09-tooling/terraform
docker compose run --rm terraform init
docker compose run --rm terraform plan
docker compose run --rm terraform apply
```

## Related References

- [Tooling tier README](../README.md)
- [Terraform guide](../../../docs/07.guides/09-tooling/terraform.md)
- [IaC operations policy](../../../docs/08.operations/09-tooling/terraform.md)
- [Terraform recovery runbook](../../../docs/09.runbooks/09-tooling/terraform.md)
- [Root infra README](../../README.md)
