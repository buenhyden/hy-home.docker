---
title: "Native Memory Controlled Verification Task"
version: "0.1.3"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0244-TSK-0001"
parent_ids:
- "SPEC-0244-PLAN-0001"
created: "2026-10-16"
---

# Native Memory Controlled Verification Task

## Overview

### Objective

Record only what an authorized, non-mutating native-session verification can
prove about memory and hooks, with unsupported state left visible as
unverified or unknown.

## Inputs and Authorization

- **Request:** on 2026-10-16 the owner asked to continue Claude memory-off
  and hook verification as part of the bounded operational follow-up.
- **Authorization boundary:** a normal Claude session may use the approved
  read-only status and menu actions. After it proves effective memory-off, one
  provider prompt may read and write only the exact ignored fixture, with at
  most three turns, USD 0.10, strict empty MCP, and no Chrome, Bash, or network
  tools. It may not read or write native/shared memory, change settings or
  trust, inspect raw private diagnostics, or widen the fixture boundary.
- **Baseline:** `main` `89eb43f683a11587cf4f125be534ae720c20a55c`.
- **Related evidence:** SPEC-0212 TSK-0009 contains the prior sanitized menu
  observation. It is historical input only; this Task does not reopen it.

## Work Log

### Initial State

The approved Spec and Plan define W1 through W6. No new native-session action
has run under this Task.

### Ready Transition

On 2026-10-16, a security review approved one final non-mutating UI attempt
that recognizes only the provider-exposed `Auto-memory` boolean, without
activating its control. The same review approved the conditional fixture probe
only after the UI proves effective memory-off: one exact ignored-fixture
read/write prompt, at most three turns and USD 0.10, strict empty MCP, no
Chrome/Bash/network tools, raw-output disposal, and wrapper cleanup. This
reviewed plan is sufficient to make the Task `ready`; it is not an attempt,
effective-memory proof, fixture execution, or hook-delivery receipt.

### In-progress Observation

The approved final UI attempt started and completed on 2026-10-16. Its
event-name-only wrapper witnessed `SessionStart=1` and `SessionEnd=1`, but the
provider's effective `Auto-memory` boolean remained unknown. No provider
prompt or tool ran, so the conditional fixture probe remains `NOT_RUN`.

The attempt also left thirteen newly created zero-byte untracked markers in an
older isolated native checkout. The markers contain no observed payload, but
their cleanup remains a required open finding. Security approved a narrowly
proven-new cleanup method; its cause and execution result remain separate from
this observation until recorded.

### Lifecycle Delivery Note

The first post-draft source commit recorded the already observed `draft` to
`ready` planning event and the subsequent `ready` to `in-progress` UI attempt
together. It contains both registered direct-edge rows but no separate ready
Git snapshot. This is a delivery-granularity limitation, not a claim that a
direct `draft` to `in-progress` transition occurred. Future transitions record
one clear actual event per commit where practical.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0244-TSK-0001 | draft | ready | Ready security plan review |
| SPEC-0244-TSK-0001 | ready | in-progress | Final UI witness observation |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial native execution state | 1, 2, 3, 4, 5, 6 | W1, W2, W3, W4, W5, W6 | No controlled session, review, conditional fixture probe, or selected document gate had run when this Task was created | Initial record on `89eb43f683a11587cf4f125be534ae720c20a55c` | NOT_RUN | Initial State | optional | - |
| Ready security plan review | 1, 3, 4, 5, 6 | W1, W3, W4, W5, W6 | Independent security review approved the exact UI recognition rule and conditional fixture bounds | Sanitized security GO, Claude Code 2.1.301 | PASS | Ready Transition | required | - |
| Scoped metadata pre-ready attempt | 6 | W6 | `check-document-metadata.py --mode check-changed` | Session 60502 against `92b16fe`; cancelled before completion because the ready transition changed this Task source | CANCELLED | Ready Transition | optional | - |
| Final UI witness observation | 4 | W4 | Event-name-only wrapper witnesses SessionStart and SessionEnd around the final allowed UI attempt | `SessionStart=1`; `SessionEnd=1`; no provider prompt or tool | PASS | In-progress Observation | required | - |
| Effective memory-off view | 3 | W3 | Provider exposes a non-mutating effective Auto-memory value | Final UI attempt: value unknown | NOT_RUN | In-progress Observation | required | - |
| Conditional fixture probe | 4, 5 | W4, W5 | Exact ignored-fixture read/write provider prompt after effective-memory-off proof | Precondition not met because effective value is unknown | NOT_RUN | In-progress Observation | required | - |
| Native marker cleanup finding | 5 | W5 | Detect and remove only proven-new zero-byte markers from the old isolated native checkout | Thirteen untracked zero-byte markers; security-approved cleanup method not yet executed | FAIL | In-progress Observation | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Await W1 control record | @buenhyden |
| 2 | pending | - | Await W2 observation | @buenhyden |
| 3 | pending | - | Await W3 non-mutating effective-memory-off proof | @buenhyden |
| 4 | pending | - | Await W4 receipt classification | @buenhyden |
| 5 | pending | - | Await W5 boundary and cleanup record | @buenhyden |
| 6 | pending | - | Await W6 review and gates | @buenhyden |

## Review and Completion

This draft has no accepted criterion. Completion is limited to the source
verification contract in SPEC-0244; it does not accept provider-global state,
individual hook delivery without a receipt, or shared-memory implementation.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
