---
title: "04-Data Optimization Hardening Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0030"
parent_ids:
- "GDE-0030"
created: "2026-05-17"
---

# 04-Data Optimization Hardening Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

## Procedure

1. Identify the affected service and its current root profile from the owning
   Compose file and M0021 disposition.
2. From the repository root, run the relevant command(s):

   ```bash
   docker compose --env-file .env.example --profile mng config --quiet
   docker compose --env-file .env.example --profile valkey-cluster config --quiet
   docker compose --env-file .env.example --profile seaweedfs config --quiet
   docker compose --env-file .env.example --profile storage config --quiet
   bash scripts/hardening/check-all-hardening.sh 04-data
   ```

3. Inspect services, profiles, networks, secret references, volumes, health checks,
   resource limits and port publication. Avoid emitting the full substituted
   configuration into durable evidence.
4. Confirm the owning policy/runbook names backup scope, separate destination,
   isolation, validation and rollback. Record any unverified runtime property.
5. Review the exact diff. Correct only the owning source and repeat the same
   checks.

### Regression response

A parse failure is corrected at the root include, leaf source or shared template
that owns it. A missing secret is restored through the secret-management process;
it is never replaced with inline plaintext. A state-path collision stops the
change until ownership is proven.

For actual data loss or corruption, stop writes and use the engine runbook:
management PostgreSQL/Valkey [RUN-0028](../0028-management-database/runbook.md),
Valkey Cluster [RUN-0022](../0022-valkey-cluster/runbook.md), or SeaweedFS
[RUN-0024](../0024-seaweedfs/runbook.md). This generic runbook does not supply a
restore shortcut.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

Rollback returns clients to the previously valid source configuration and engine-specific runbook. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

Stop on scope, identity, checksum, security, compatibility or ownership drift;
preserve safe evidence and escalate to the service/data owner.

## Verification Record

### Acceptance

Static acceptance requires root configuration parse success, scoped hardening
success, accurate classification/profile documentation and an explicit recovery
owner. Runtime health, encryption, capacity and restore remain unproven unless a
dated scoped evidence package says otherwise.

## Traceability

- Artifact: `RUN-0030`; parent guide: `GDE-0030`.
- Procedures are planned unless a dated verification record explicitly says they ran.

## Related Documents

- [Policy](policy.md)
- [Guide](guide.md)
