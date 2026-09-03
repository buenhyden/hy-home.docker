---
title: Terraform Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0068
parent_ids:
  - AD-0009
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/09-tooling/0068-terraform/policy.md -->

# Terraform Operations Policy

<!-- [ID:09-tooling:terraform] -->

## Overview

All infrastructure changes in `hy-home.docker` must be managed via Terraform to ensure auditability and reproducibility.

## Policy Scope

This policy applies to Terraform state management, deployment workflow, provider maintenance, and infrastructure change auditability in the tooling tier.

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

### State Management Policy

#### 1. Remote State Requirement

- For any environment with more than one contributor, a **Remote Backend** (S3/MinIO) is mandatory.
- State locking must be enabled (via DynamoDB or MinIO Object Lock).

#### 2. State Backups

- Remote states are automatically versioned by the backend.
- Monthly exports of the `.tfstate` to the `04-data/backups` tier are required for disaster recovery.

### Deployment Workflow

| Step | Action | Mandatory? |
| :--- | :--- | :--- |
| **Validation** | `validate` & `fmt` | Yes |
| **Planning** | `plan -out=tfplan` | Yes |
| **Peer Review** | Review `tfplan` output | Recommended |
| **Execution** | `apply tfplan` | Yes |

> [!IMPORTANT]
> Never use `terraform apply` without a pre-generated plan file in production environments.

### Maintenance Cycles

#### Provider Updates

- Check for provider updates (AWS, Docker, Kubernetes) every **quarter**.
- Test updates in a non-production workspace before merging.

#### Credential Rotation

- Host-level cloud credentials mounted to the Terraform container must be rotated every **90 days**.

### Compliance & Security

- **Secrets**: Never hardcode credentials in `.tf` files. Use environment variables or secret managers (Vault).
- **Versioning**: Pin all provider and module versions to prevent breaking changes during `init`.

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
- Subject peers: [Guide](guide.md) (`GDE-0068`), [Runbook](runbook.md) (`RUN-0068`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
