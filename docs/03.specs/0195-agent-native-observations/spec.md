---
title: "Agent Native Observation Follow-up"
version: "0.2.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0195"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-09-30"
---

# Agent Native Observation Follow-up

## Overview

Close the historically transferred native observations from SPEC-0194 after
the owner's 2026-09-30 necessity ruling and independent read-only review found
no necessary successor work. Closure withdraws unobserved native work; it does
not convert missing evidence into PASS.

## Boundaries and Inputs

Inputs are SPEC-0194, REQ-0024, AD-0027, current `main` at
`2dd9e805a5899d03a6221d29e3d64141ad7fd1af`, and the original immutable
SPEC-0190 hardening packet at commit `c86f55518b8a9a156e10e38fbd52d1a883063d6a`,
preserved by the integration handoff under
`docs/98.archive/superseded/03.specs/0190-agent-contract-hardening`.
Source R-identifiers below retain their original meaning.

The owner authorized necessity review and cancellation only, not runtime
execution. No provider call, spending, hook trust change, global configuration
change, editor action, service operation, credential access, authentication-file
read, or raw-log capture is authorized. SPEC-0182 remains separate. Prior
coverage and delivery evidence remain historically owned by completed SPEC-0194.
This package owns validation of its cancellation lifecycle only.

## Behavior Contract

Reuse the delivered deterministic checks and separate them from direct native
observations. Each receipt identifies the provider/editor version, reviewed
revision and synthetic target, exact invocation/event/action, authorization and
bounds, observed result, reviewer, and remaining limits. A reviewer is read-only
and independent of the implementer. Missing, unsupported, or unavailable evidence
remains BLOCKED/NOT_RUN and cannot become PASS through transfer or static review.

## Technical Approach

Apply only the registered four-stage lifecycle path: review/approved/ready,
then approved/approved/ready, then active/active/in-progress, then
cancelled/cancelled/cancelled for the Spec, Plan, and Task respectively. The
final Task records each numbered acceptance criterion as withdrawn with the
owner's cancellation reason. The final package then retires to the registered
Stage 98 route with its tombstone and inbound references updated. No successor
Task, provider invocation, synthetic target, model gateway, budget engine, or
evaluation framework is created. The current Task preserves the sanitized
preflight receipt and the limits that made every native result NOT_RUN or
BLOCKED.

## Interfaces and Data

Retain sanitized version, action, event, refusal, and outcome metadata. Never
copy credentials, account authentication files, raw private logs, or session
state. Public documentation, account information supplied by the owner, and
explicitly approved observations remain separate evidence sources.

## Failure Modes and Guardrails

Stop for missing approval, unexpected charge or secret contact, changed target
or revision, stale evidence, overlapping writers, or unclear enforcement. Keep
partial results visible. An unavailable observation is not non-applicability.

## Acceptance Contract

1. **R04:** Observe actual native hook delivery separately from the delivered
   payload, event, timeout, duplicate/re-entry, malformed-input, failure, and
   visible missing-lint regressions; record the installed provider/version and
   delivered event/result on the approved synthetic target.
2. **R15:** Test provider-specific invocation separately from native syntax for
   both Claude and Codex. Retain SPEC-0194 evidence that both consume one
   canonical source, generation preserves source with zero second-run drift,
   and derived modes do not inherit personal state or approvals.
3. **R18:** Observe editor version/action/selection/keybinding behavior on an
   approved synthetic document, separate from CLI evidence. Preserve user
   bindings; absent native observations remain incomplete.
4. **R19:** Separate API/subscription and observed/estimated usage; record approved
   request/token/time/concurrency/retry bounds and retain deterministic
   exhaustion/429/contention evidence. Evidence real supported hard enforcement
   or keep this criterion BLOCKED. A time limit or lexical refusal fixture is
   not proof of a monetary cap. Fulfill the original Plan's separate model
   entitlement requirement without reading authentication files or assuming
   documented support proves account access. Native invocations do not establish
   backend request counts; no verified monetary, request, or token hard envelope
   is available for Codex. The owner reports extra credits and automatic reload
   disabled; this owner-supplied fact does not verify native enforcement.
5. **R22:** Observe cross-provider handoff refusal before writes for stale HEAD
   or file digest, revoked approval, wrong worktree, overlapping writers, and
   ambiguous partial results; observe valid resumption from actual Task/commit
   evidence. Recorded-output fixtures alone do not prove native refusal.

All five criteria remain NOT_RUN or BLOCKED as recorded in the Task. They are
withdrawn because the owner authorized cancellation of the unnecessary
follow-up after independent necessity review, not because static checks,
subscription state, or lifecycle closure supply native evidence. This review-stage document is not terminal; the
remaining registered transitions and final cancellation evidence are required.

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [SPEC-0194](../0194-agent-contract-integration/spec.md)
- Original hardening packet: commit c86f55518b8a9a156e10e38fbd52d1a883063d6a,
  source R04/R15/R18/R19/R22 and Plan separately observed acceptance.

## Open Questions

No native observation remains planned. The preserved Task records unobserved
entitlement, editor behavior, and enforcement limits for historical clarity.

## Operational Impact

Drafting and transfer have no runtime effect. R27 is a read-only recovery-contract
review; this follow-up does not require or authorize a real restore.
