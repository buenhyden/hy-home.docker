---
title: "04-Data Optimization Hardening Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0030"
parent_ids:
- "AD-0004"
created: "2026-05-10"
---

# 04-Data Optimization Hardening Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

Every data service must have an explicit disposition/profile, one owner for every
writable state path, a health check or documented exception, shared resource
limits, an intended network/exposure boundary, secret-file custody where
credentials exist, and an engine-specific recovery method.

## Controls

- Validate through the root Compose project. Service-local project rendering is not accepted because root networks, secrets
  and `extends` paths change the rendered model.
- Keep HOME, OPTIONAL and LAB state directories distinct. Same-host replicas are
  topology tests, not host availability or backups.
- Never hardcode or print secrets. Gateway TLS does not establish internal TLS or
  backup encryption; document each boundary from source.
- Require engine-supported export/snapshot procedures and a separate encrypted
  destination. Raw copying active database/object-store directories is prohibited.
- Require an isolated compatible restore, application-level validation, observed
  RPO/RTO and rollback before promotion or cutover.
- Review upstream security, upgrade and license sources before pin changes. A
  current image declaration does not prove supported lifecycle.

## Validation and evidence

Root `config --quiet` for the affected exact profile and
`scripts/hardening/check-all-hardening.sh 04-data` are mandatory static checks.
Evidence records command, source revision, exit status, scope and unresolved gaps
without credentials or data. Runtime checks are separately approved and must not
be inferred from static success.

## Failure handling

Do not bypass a failed health, resource, secret, network, persistence or recovery
control. Patch within approved scope or escalate to the owning architecture and
operations subjects. Data deletion, volume reuse and destructive restore require
explicit approval.

## Exceptions

Documented job/health exceptions require the owning profile and recovery evidence. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Artifact: `POL-0030`; parent: `AD-0004`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

## Related Documents

- [Usage guide](guide.md)
- [Runbook](runbook.md)
- [Backup policy](../0021-backup-and-restore/policy.md)
