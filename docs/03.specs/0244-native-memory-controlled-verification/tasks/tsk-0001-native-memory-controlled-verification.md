---
title: "Native Memory Controlled Verification Task"
version: "0.1.9"
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

### Spec Approval

The direct 2026-10-16 user authorization approved the bounded SPEC-0244
contract before this Task was created.

### Plan Approval

The same direct authorization approved SPEC-0244-PLAN-0001's bounded work and
verification sequence before this Task was created.

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

### Cleanup Follow-up

The thirteen proven-new zero-byte markers in the old isolated checkout were
removed and its Git status returned to the recorded state. A privacy environment
scrub also created eight proven-new zero-byte placeholders at a user-global
location. Automatic deletion there was rejected because it would mutate global
state; four ambiguous files and all directories remain untouched. The owner
then approved guarded removal of exactly those eight proven-new files, which
completed without touching the retained entries. No provider retry or further
probe ran.

### Forced-off Hook Delivery Plan

Security approved one conditional, session-only hook-delivery attempt after the
guarded global cleanup. It sets `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` for that
session only and does not use the privacy-environment scrub that created the
placeholders. Its sole successful label is
`HOOK_DELIVERY_VERIFIED_WITH_SESSION_FORCED_MEMORY_OFF`. The attempt is a
distinct hook-delivery proof class: it neither changes configuration nor proves
that the normal merged project setting is effectively off, so criterion 3
remains pending. The operator may start the one frozen attempt after this Task
record; all other boundaries and stop conditions in the approved plan remain
in force.

### Forced-off Hook Attempt

The one authorized forced-off provider attempt failed closed at startup with
exit 1. It produced no stdout; stderr was discarded. No hook, tool, or model
output occurred and no timeout was observed. Therefore its sole successful
label was not earned. The normal no-model UI observation remains limited to
`SessionStart=1` and `SessionEnd=1`, and normal merged auto-memory remains
unknown.

### Forced-off Hook Retry 02 Plan

Security approved one fresh retry plan with digest
`4f59ea1279ac9233b50cc33262a3ca50a3015920a6b1f1ce37280e389d92e414`.
It is session-only forced-off with `sandbox=false`, so it makes no OS
confinement claim. The task-owned witness accepts only the exact guarded
fixture `Write` payload and denies every other operation. The attempt permits
no Read, Bash, or MCP tool; it has at most two turns, USD 1, and 180 seconds.
It is one new retry only. Guard tests passed before release. Normal merged
auto-memory remains unknown, and this plan does not change its criterion.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0244 | draft | approved | #spec-approval |
| SPEC-0244-PLAN-0001 | draft | approved | #plan-approval |
| SPEC-0244-TSK-0001 | draft | ready | #ready-transition |
| SPEC-0244-TSK-0001 | ready | in-progress | #in-progress-observation |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial native execution state | 1 | W1 | No controlled session, review, conditional fixture probe, or selected document gate had run when this Task was created | Initial record on `89eb43f683a11587cf4f125be534ae720c20a55c` | NOT_RUN | Initial State | optional | - |
| Ready security plan review | 1 | W1 | Independent security review approved the exact UI recognition rule and conditional fixture bounds | Sanitized security GO, Claude Code 2.1.301 | PASS | Ready Transition | required | - |
| Scoped metadata pre-ready attempt | 6 | W6 | `check-document-metadata.py --mode check-changed` | Session 60502 against `92b16fe`; cancelled before completion because the ready transition changed this Task source | CANCELLED | Ready Transition | optional | - |
| Final UI witness observation | 4 | W4 | Event-name-only wrapper witnesses SessionStart and SessionEnd around the final allowed UI attempt | `SessionStart=1`; `SessionEnd=1`; no provider prompt or tool | PASS | In-progress Observation | required | - |
| Effective memory-off view | 3 | W3 | Provider exposes a non-mutating effective Auto-memory value | Final UI attempt: value unknown | NOT_RUN | In-progress Observation | required | - |
| Conditional fixture probe | 4 | W4 | Exact ignored-fixture read/write provider prompt after effective-memory-off proof | Precondition not met because effective value is unknown | NOT_RUN | In-progress Observation | required | - |
| Native marker cleanup finding | 5 | W5 | Detect and remove only proven-new zero-byte markers from the old isolated native checkout | Thirteen untracked zero-byte markers; security-approved cleanup method not yet executed | FAIL | In-progress Observation | required | - |
| Local marker cleanup | 5 | W5 | Detect and remove only proven-new zero-byte markers from the old isolated native checkout | Thirteen proven-new zero-byte markers removed; Git status restored | PASS | Cleanup Follow-up | required | Native marker cleanup finding |
| Global marker cleanup boundary | 5 | W5 | Delete only proven-new zero-byte privacy-environment placeholders at the user-global location | Eight proven-new zero-byte files detected; automatic deletion rejected; four ambiguous files and all directories retained | FAIL | Cleanup Follow-up | required | - |
| Global marker cleanup | 5 | W5 | Delete only proven-new zero-byte privacy-environment placeholders at the user-global location | Guarded cleanup deleted all eight approved proven-new zero-byte files; four ambiguous files and all directories preserved | PASS | Cleanup Follow-up | required | Global marker cleanup boundary |
| Forced-off hook plan review | 4 | W4 | Security review of one session-only forced-off hook-delivery attempt without privacy-environment scrub | `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; sole PASS label `HOOK_DELIVERY_VERIFIED_WITH_SESSION_FORCED_MEMORY_OFF`; normal merged effective-off remains unknown | PASS | Forced-off Hook Delivery Plan | required | - |
| Forced-off hook attempt | 4 | W4 | One approved session-only forced-off hook-delivery attempt | Startup exit 1; stdout absent; stderr discarded; zero hooks, tools, and model output; no timeout | FAIL | Forced-off Hook Attempt | required | - |
| Forced-off hook retry 02 plan review | 4 | W4 | Security review of one fresh session-only forced-off retry with guarded Write-only witness | Plan `4f59ea1279ac9233b50cc33262a3ca50a3015920a6b1f1ce37280e389d92e414`; sandbox false with no OS-confinement claim; no Read/Bash/MCP; max two turns/USD 1/180 seconds; guard tests PASS | PASS | Forced-off Hook Retry 02 Plan | required | - |

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
