---
title: "04-Data Optimization Hardening Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
artifact_id: "GDE-0030"
parent_ids:
- "POL-0030"
created: "2026-05-17"
---

# 04-Data Optimization Hardening Usage Guide

## Usage

This subject verifies static controls across the data tier: root profile validity,
explicit persistence ownership, secrets, health checks, resources, network
boundaries and recovery ownership. It does not authorize service activation,
data access, cleanup, migration or tuning.

### Root validation

Run from the repository root because leaf files depend on root-owned networks,
secrets and shared templates. Select representative current profiles rather than
rendering a leaf file directly:

Render each representative current profile with the root `.env.example` and run
the shared hardening check script for this tier. The exact command sequence is
owned by the [04-Data Optimization Hardening runbook](../runbooks/0030-data-optimization-hardening.md#procedure).

Inspect the rendered services without printing substituted private values. Verify
classification/profile alignment, unique writable volumes, the declared networks, secret
files, health checks, CPU/memory limits, intended port publication and an
engine-specific backup/restore owner.

### Interpretation

A static pass proves parse and policy conformance only. It does not prove runtime
health, storage capacity, backup completeness, recovery time, encryption at rest,
application compatibility or same-host availability. Record those as unverified
until a scoped runtime test or isolated rehearsal supplies evidence.

### Correction workflow

Fix the owning leaf Compose source or shared template inside an approved task,
re-render the same root profiles, rerun the scoped hardening check and inspect the
exact diff. Use the engine runbook for recovery; do not apply a generic data-copy
or cleanup command.

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0030`; governing policy: `POL-0030`.
- Runtime authority: `root Compose plus scripts/hardening/check-all-hardening.sh`.

## Related Documents

- [Hardening policy](../policies/0030-data-optimization-hardening.md)
- [Hardening runbook](../runbooks/0030-data-optimization-hardening.md)
- [Backup policy](../policies/0021-backup-and-restore.md)
- [Storage exhaustion runbook](../runbooks/0035-storage-exhaustion.md)
