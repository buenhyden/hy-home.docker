---
title: Terrakube Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0069
parent_ids:
  - AD-0009
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/09-tooling/0069-terrakube/policy.md -->

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
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` after policy or linked operations document updates.
- Run `python3 scripts/validation/check-document-links.py --mode traceability` when execution or operations links change.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Traceability

- Declared parent: [Tooling Tier Architecture Description](../../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- Subject peers: [Guide](guide.md) (`GDE-0069`), [Runbook](runbook.md) (`RUN-0069`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
