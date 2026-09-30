---
title: "Agent Native Observation Follow-up"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
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

Own the native observations transferred from SPEC-0194 by the owner's explicit
2026-09-30 decision to use a separate follow-up. Transfer changes ownership, not
the original acceptance conditions or the status of missing evidence.

## Boundaries and Inputs

Inputs are SPEC-0194, REQ-0024, AD-0027, and the original SPEC-0190 hardening
packet at commit c86f55518b8a9a156e10e38fbd52d1a883063d6a, to be preserved under
`docs/98.archive/superseded/03.specs/0190-agent-contract-hardening` by the
integration handoff. Source R-identifiers below retain their original meaning.

The user authorized transfer, not execution of these observations. No provider
call, spending, hook trust change, global configuration change, editor action,
service operation, or credential access is authorized by this draft. SPEC-0182
remains separate. Coverage, public changed/full gates, controlled all-files QA,
hosted checks, and Git delivery remain owned by SPEC-0194.

## Behavior Contract

Reuse the delivered deterministic checks and separate them from direct native
observations. Each receipt identifies the provider/editor version, reviewed
revision and synthetic target, exact invocation/event/action, authorization and
bounds, observed result, reviewer, and remaining limits. A reviewer is read-only
and independent of the implementer. Missing, unsupported, or unavailable evidence
remains BLOCKED/NOT_RUN and cannot become PASS through transfer or static review.

## Technical Approach

After the required lifecycle approvals, propose only bounded observations using
installed tools and synthetic inputs. Obtain concrete authorization before any
native action or metered call. Preserve user bindings and global configuration.
Use the current Task for evidence; introduce no model gateway, budget engine,
parallel ledger, or evaluation framework. If no supported hard-enforcement
route exists, keep that criterion blocked rather than inventing one.

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
   documented support proves account access.
5. **R22:** Observe cross-provider handoff refusal before writes for stale HEAD
   or file digest, revoked approval, wrong worktree, overlapping writers, and
   ambiguous partial results; observe valid resumption from actual Task/commit
   evidence. Recorded-output fixtures alone do not prove native refusal.

Every applicable criterion requires observed evidence and independent review
before completion. SPEC-0194 delivery completion does not complete this package.

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [SPEC-0194](../0194-agent-contract-integration/spec.md)
- Original hardening packet: commit c86f55518b8a9a156e10e38fbd52d1a883063d6a,
  source R04/R15/R18/R19/R22 and Plan separately observed acceptance.

## Open Questions

Installed provider/editor versions, supported account controls and entitlement,
concrete observation scope and limits, and execution authorization remain open.

## Operational Impact

Drafting and transfer have no runtime effect. R27 is a read-only recovery-contract
review; this follow-up does not require or authorize a real restore.
