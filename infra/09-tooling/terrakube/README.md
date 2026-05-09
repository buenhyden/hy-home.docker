<!-- [ID:09-tooling:terrakube] -->
# Terrakube IaC Automation Platform

> Terraform orchestration, remote state, and private registry service stack

## Overview

`infra/09-tooling/terrakube/` defines the Terrakube service stack for centralized Terraform workflows. The stack includes API, UI, and executor services using Terrakube 2.29.0 images, integrates with Keycloak for identity, stores metadata in the management PostgreSQL service, and uses MinIO-compatible S3 storage for Terraform state.

This README is the service-level entrypoint. It summarizes the Compose surface and links to the canonical guide, operations policy, and runbook.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Terrakube API, UI, and executor Compose service boundaries
- Gateway hostnames and internal service relationships
- Metadata, state storage, and Docker secret usage at a high level
- Related guide, operation, and runbook links

### Out of Scope

- Secret values or credential material
- Terraform module authoring standards
- Long-form IaC governance policy
- Cloud provider account setup

## Structure

```text
terrakube/
├── docker-compose.yml  # Terrakube API, UI, and executor service definitions
└── README.md           # This file
```

## How to Work in This Area

1. Read the parent [`../README.md`](../README.md) and this service Compose file before changing Terrakube.
2. Keep secret material in Docker secrets; document only secret names and purpose.
3. Verify API, UI, executor, PostgreSQL, MinIO, Valkey, and Keycloak assumptions together when changing the stack.
4. Update the related guide, operation, or runbook when user access, state handling, or recovery behavior changes.

## Tech Stack

| Component | Image / Source | Role |
| --- | --- | --- |
| `terrakube-api` | `azbuilder/api-server:2.29.0` | API server and metadata orchestration |
| `terrakube-ui` | `azbuilder/terrakube-ui:2.29.0` | Web management UI |
| `terrakube-executor` | `azbuilder/executor:2.29.0` | Terraform job execution |
| Metadata | Management PostgreSQL | Terrakube database |
| State storage | MinIO S3-compatible bucket `tfstate` | Terraform state and output storage |
| Identity | Keycloak / DEX validation | SSO integration |

## Usage Instructions

After the stack is enabled with the `tooling` or `iac` profile, use these routed endpoints:

- API: `https://terrakube-api.${DEFAULT_URL}`
- UI: `https://terrakube-ui.${DEFAULT_URL}`
- API docs: `https://terrakube-api.${DEFAULT_URL}/swagger-ui.html`

## Related References

- [Tooling tier README](../README.md)
- [Terrakube guide](../../../docs/07.guides/09-tooling/terrakube.md)
- [Terrakube operations policy](../../../docs/08.operations/09-tooling/terrakube.md)
- [Terrakube recovery runbook](../../../docs/09.runbooks/09-tooling/terrakube.md)
- [Root infra README](../../README.md)
