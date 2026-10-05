---
title: "Common Authorization and Safe Authoring Specification"
version: "1.0.1"
type: "sdlc/spec"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0207"
parent_ids:
- "REQ-0024"
- "AD-0027"
- "ADR-0032"
created: "2026-10-04"
---

# Common Authorization and Safe Authoring Specification

## Overview

Converge current governance on one authorization owner while preserving the
native provider sandbox and the distinct roles of approval, review, and Task
evidence. The original completed Task 0001 and Task 0002 implementation scopes
authorized reversible local P01 policy and documentation edits, bounded
archive-record consumer/helper/test work, safe hook diagnostic clarification,
and local logical commits. The latest authorized local main integration is
recorded in the [SPEC-0209 handoff](../0209-common-document-contract-adoption/tasks/tsk-0001-common-document-contract-adoption.md#local-integration-handoff).
SPEC-0182 and
SPEC-0204 remain unrelated active packages; archived SPEC-0193 and SPEC-0206
are not reopened.

## Scope

### Boundaries and Inputs

Inputs are REQ-0024, AD-0027, ADR-0032, the current canonical governance
sources, provider registry, tracked hooks, and the current Task. The baseline
observed before implementation is `830ab0583f65e1252badb6be34b79c92bcb3c293`.
Those original implementation scopes excluded secret values, auth files, raw
logs, live commands, provider/model calls, remote writes, pushes, PRs, merges,
and provider sandbox changes. The later user-authorized local main finish
follows the SPEC-0209 handoff. Current separately approved delivery scope is
recorded in Task 0003; the original exclusions do not authorize those operations.
The bounded consumer work covers the archive approval-record helper and direct consumer,
plus the existing pre-tool hook consumer and their focused tests; the shared
`tool_payload.py` parser remains unchanged.

### Open Questions

No automatic authorization authenticator is available. The supported current
trusted user/operator/native-channel procedure is documented; any durable
cryptographic or provider-native authentication needs separate approved design
and observed capability evidence.

### Operational Impact

The change narrows policy interpretation and does not execute an operational
action. Hosted, live, remote, and provider observations and authorization remain distinct
and are recorded only by the executing Task.

## Contracts

### Behavior Contract

1. `approval-boundaries.md` owns current protected-operation authorization:
   actor, operation, subject, revision or scope, and recovery are bound to a
   current trusted source. Task/schema/CLI fields and archive records are
   structural records only.
2. `environment-constraints.md` routes authorization to that owner and retains
   concrete runtime and secret protocols. `workflows.md` owns lifecycle order
   and separates approval from read-only review; `agentic.md` owns budget
   preflight and unsupported-native-control reporting.
3. Editing redacted documentation, synthetic inputs, metadata, or examples that
   contain dangerous commands is a local authoring operation. Executing such a
   command or accessing a sensitive target is separately authorized.
4. Historical, absent, mismatched, expired, or revoked approvals cannot grant a
   current operation. Hooks, archive validators, and provider fields cannot
   self-authorize or lower the native sandbox.

### Technical Approach

Task 0001 inventories and converges the authorization boundary. Task 0002
converges execution-boundary references and may make pre-tool payload denials
diagnosable without disclosing input. Both use canonical owners and their real
consumer routes; neither implements authentication or changes native limits.

Task 0003 reconciles the current P01 authority, implementation, evidence, and
blocker routes against the audit revision and current main. It preserves the
existing policies and completed Tasks, and records the bounded comparison in
its own Task without reopening unrelated recovery or operational work.

### Interfaces and Data

Inputs and outputs are policy text, metadata, redacted examples, synthetic
fixtures, links, and value-free command receipts. The authorization source is a
trusted user/operator/native channel; no automatic source authenticator is
introduced by this Spec. Repository fields cannot automatically verify the
account identity behind a trusted origin.

### Failure Modes and Guardrails

Stop protected operations when authorization is missing, mismatched, expired,
revoked, or outside scope. Do not claim that a Task field, review, hook, schema,
or provider delivery authenticates approval. Safety denial cannot be converted
into a budget exception; required-check budget and environment gaps stop through
agentic preflight. No wrapper or command variation bypasses a boundary.

## Acceptance Criteria

### Acceptance Contract

1. The current authorization owner and each consumer route are recorded in the
   Task conflict matrix with actual source locations and consumer status.
2. The canonical policies distinguish local safe authoring from real sensitive,
   live, remote, credential, and destructive operations.
3. Approval source authentication is distinct from structural record validation;
   invalid or Historical records do not authorize current work.
4. Review remains read-only and provider sandbox/native limits are not claimed
   to be relaxed.
5. Safety denials and cost/time/token guardrails have separate owners and a
   required check cannot be bypassed through budget or wrappers.
6. The Task records focused checks, review, promotion receipt, rollback, and
   remote finish state without fabricating unobserved evidence.

7. A frozen original disposition remains historical evidence while a pending or
   new archive action requires a current trusted-operator source; fixture checks
   cover missing and mismatched historical-record integrity without claiming
   automatic revocation enforcement.

## Related Documents

### Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0032](../../02.architecture/decisions/0032-canonical-agent-governance-home.md)
- [Plan](plan.md)
- [Task 0001](tasks/tsk-0001-policy-convergence.md)
- [Task 0002](tasks/tsk-0002-execution-boundary-and-safe-diagnostics.md)
- [Task 0003](tasks/tsk-0003-current-authority-and-blocker-reconciliation.md)
