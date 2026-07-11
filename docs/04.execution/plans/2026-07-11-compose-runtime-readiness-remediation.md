---
status: draft
artifact_id: plan:2026-07-11-compose-runtime-readiness-remediation
artifact_type: plan
parent_ids:
  - spec:124-compose-runtime-readiness-remediation
---

<!-- Target: docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md -->

# Compose Runtime Readiness Remediation Implementation Plan

## Overview

This draft sequences the later implementation of the Compose startup,
readiness, recovery, and teardown contract in Spec 124. It is later-approvable
only: it creates no runtime authorization, task evidence, service action, secret
access, or remote change.

## Context

Static inventory, rendering, healthcheck declarations, and hardening are strong,
but current startup, observed readiness, and recovery evidence is absent or
partial. The plan closes that evidence gap only after architecture and protected
surface approvals are attached to a future task.

## Prerequisites and Approval State

| Gate | Current state | Required resolution |
| --- | --- | --- |
| Parent spec | Draft | Spec 124 reviewed and activated. |
| Architecture | Unresolved | Approved PRD, ARD, and ADRs named by Spec 124. |
| Human | Unresolved | Runtime owner approves service/profile scope, disruption, stop criteria, and risk. |
| Runtime | Unresolved | Exact target, files/profiles/services, commands, timeout, teardown, and recovery in a future Stage 04 task. |
| Secret | Unresolved/not authorized | Exact IDs/paths and metadata boundary plus redaction approval; no values. |
| Remote | Unresolved/not authorized | Exact remote target/repository, command class, permissions, evidence, and rollback. |

Spec 123 approval is audit/documentation lineage and is not evidence for any of
these gates.

## Goals & In-Scope

- **Goals**: Produce bounded startup, readiness, recovery, teardown, and
  escalation evidence that satisfies Spec 124.
- **In Scope**: Predecessor resolution, scoped scenario design, isolated
  harness/fixture implementation if approved, negative/stop paths, evidence,
  independent review, and operations handoff.

## Non-Goals & Out-of-Scope

- **Non-goals**: Prove production readiness from one run, expand profiles by
  default, or duplicate state recovery/security/deployment requirements.
- **Out of Scope now**: All runtime, Compose, infra, secret, remote, CI, and
  architecture mutations until separate approvals exist.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| `PLN-CRR-001` | Create and approve required PRD/ARD/ADRs; select bounded target/scenarios | Unresolved Stage 01/02 paths; update Spec 124 after approval | `CRR-001`–`CRR-003` | Canonical approved predecessors and exact scope exist. |
| `PLN-CRR-002` | Create a protected-surface Stage 04 task and redacted evidence schema | Future task path; no task exists now | `CRR-001`–`CRR-003` | Human/runtime/secret/remote approvals and recovery/teardown are bound. |
| `PLN-CRR-003` | Implement the smallest approved isolated startup/readiness scenario | Paths selected only by approved architecture/task | `CRR-001`, `CRR-002` | Initialization and service criteria pass or stop safely; teardown verified. |
| `PLN-CRR-004` | Add one approved bounded failure/recovery and negative stop-path scenario | Approved runtime/test/ops surfaces | `CRR-003` | Recovery time/state/escalation and failure behavior are recorded. |
| `PLN-CRR-005` | Review evidence, rollback/recover changes, and update operations docs | Future task/operations paths | `CRR-001`–`CRR-003` | Independent reviews approve; no unexpected state remains. |

## Sequencing, Migration, and Rollout

1. Resolve PRD/ARD/ADR and spec approval.
2. Inventory exact target/profile/service/secret/remote boundaries.
3. Approve a future task with before/after, teardown, recovery, and redaction.
4. Run static preflight, then the smallest isolated startup/readiness scenario.
5. Add one bounded recovery/negative scenario only after reviewed baseline.
6. Expand scope only through another explicit approval.

## Rollback and Recovery Strategy

- Revert test-only configuration/harness changes by reviewed commit or approved
  override removal; preserve existing Compose defaults.
- Use approved teardown without deleting uncertain persistent state.
- Hand data restoration to Spec 125; config rollback and data recovery remain
  distinct.
- Stop and escalate when teardown, state, target, or secret boundary is uncertain.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| `VAL-PLN-CRR-001` | Documentation | Typed metadata and traceability | Metadata checker with explicit task base; traceability/alignment/contracts | Draft resolves structurally with zero new violations. |
| `VAL-PLN-CRR-002` | Static preflight | Render exact approved Compose scope without startup | Future task supplies exact command | Expected services only; no runtime mutation. |
| `VAL-PLN-CRR-003` | Runtime | Startup/readiness and teardown | Future approved task only | Scoped criteria and teardown pass with redacted evidence. |
| `VAL-PLN-CRR-004` | Recovery | Bounded failure/stop path | Future approved task only | Recovery or safe stop/escalation satisfies Spec 124. |
| `VAL-PLN-CRR-005` | Review | Independent spec/quality/security review | Review future task report and exact diff/evidence | No unresolved critical/important finding. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Wrong target/profile expansion | Critical | Exact inventory, isolated target, fail-closed preflight. |
| Persistent state damage | Critical | Exclude until approved; verified backup/recovery dependency. |
| Secret leakage in observations | Critical | Metadata-only evidence and approved redaction. |
| Teardown failure/resource residue | High | Stop, isolate, and escalate; no blind deletion. |
| Static evidence mislabeled runtime | High | Separate evidence classes and dated observations. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Documentation, static rendering, fixture/schema, and
  negative-path review before runtime.
- **Sandbox / Canary Rollout**: Smallest isolated non-production scenario only
  after approvals.
- **Human Approval Gate**: Required before each runtime scope expansion.
- **Rollback Trigger**: Scope drift, readiness failure, state/secret risk,
  teardown failure, or recovery ambiguity.
- **Prompt / Model Promotion Criteria**: Not applicable; model policy unchanged.

## Completion Criteria

- [ ] Required PRD/ARD/ADRs exist and are approved.
- [ ] Spec 124 and this plan are reviewed and activated.
- [ ] A separate protected-surface Stage 04 task authorizes exact execution.
- [ ] Human, runtime, secret, remote, and architecture gates are resolved.
- [ ] Startup, readiness, recovery/negative path, teardown, and redaction pass.
- [ ] Rollback/recovery and operations handoff are independently reviewed.

## Related Documents

- **Spec**: [Compose runtime readiness](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **Umbrella lineage**: [Spec 123](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- **Operations dependency**: [Infrastructure operations plan](./2026-07-11-infrastructure-operations-readiness-remediation.md)
- **Security dependency**: [Security supply-chain plan](./2026-07-11-security-supply-chain-remediation.md)
- **Deployment dependency**: [Deployment/release plan](./2026-07-11-deployment-release-engineering-remediation.md)
- **Operations**: [Operations index](../../05.operations/README.md)
