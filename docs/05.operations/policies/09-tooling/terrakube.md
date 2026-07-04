---
status: active
---
<!-- Target: docs/05.operations/policies/09-tooling/terrakube.md -->

# Terrakube Operations Policy

<!-- [ID:09-tooling:terrakube] -->

## Overview

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

## Policy Scope

This policy applies to Terrakube workspace access, execution governance, registry maintenance, sensitive variable handling, and routine platform maintenance in the tooling tier.

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- Review this policy with its matching guide, runbook, and linked infra/config documents before material operations changes.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy or linked operations document updates.
- Run `bash scripts/validation/check-doc-traceability.sh` when execution or operations links change.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/terrakube.md)
- [Recovery runbook](../../runbooks/09-tooling/terrakube.md)
