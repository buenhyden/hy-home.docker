---
title: "Agent Contract Integration Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0194"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-09-29"
---

# Agent Contract Integration Specification

## Overview

Integrate the reviewed implementation from `codex/agent-contracts` into `main`
without rewriting its source package. The source packet is
`c86f55518b8a9a156e10e38fbd52d1a883063d6a`; its receipt is recorded only after
this package is active and an integration result exists.

## Boundaries and Inputs

Inputs are REQ-0024, AD-0027, source branch `codex/agent-contracts`, current
`main`, and the existing Stage 01, Stage 02, Stage 05, and Stage 99 owners.
The target is `buenhyden/hy-home.docker` branch `main`. SPEC-0182 is separate
active HOME work and is excluded. SPEC-0191 was subsequently completed and preserved by acce0a6ba; retain that
verified successor state and its frozen packet unchanged.

Source public changed/full gates, coverage, native/provider and editor behavior,
hosted CI, budget enforcement, and runtime recovery remain unobserved unless
this Task records a separately authorized result.

## Behavior Contract

The exact original packet at
`docs/03.specs/0190-agent-contract-hardening` is preserved byte-for-byte under
`docs/98.archive/superseded/03.specs/0190-agent-contract-hardening` through the
existing divergent-branch handoff. Main already preserves a different completed
SPEC-0190 at `docs/98.archive/completed/03.specs/0190-home-classification-remaining`.
This source packet retains its original statuses, including unresolved work;
preservation is not completion. SPEC-0194 retains the source delivery and deterministic-verification obligations.
On 2026-09-30 the owner explicitly transferred outstanding actual observations
for R04/R15/R18/R19/R22, including the original Plan model-entitlement requirement,
to [SPEC-0195](../0195-agent-native-observations/spec.md). Their original
conditions and BLOCKED/NOT_RUN status remain; transfer is neither a waiver nor
execution approval. Coverage, public profiles, controlled all-files QA, hosted
checks, and Git delivery remain here.

Integration preserves source obligations at their existing canonical owners and
records source branch, commit, target branch, observed checks, and limits in the
current Task. It creates no parallel authority or integration ledger.

Deterministic path, schema, registry, metadata, link, and generated-surface
checks run first. Routine semantic conclusions receive bounded independent read-only agent
review of the same diff and revision. Only unresolved ambiguity, reviewer
disagreement, high-risk uncertainty, new scope, or required human gates are
escalated to a human. The reviewer records question, files, outcome, and limit and
cannot approve its own protected change. Existing human approval requirements
for runtime, secrets, deployment, remote state, and protected actions remain.

## Technical Approach

Promote this package through draft, review, approved, and active lifecycle
before writing a branch-integration receipt. Reconcile the source with `main`,
run changed/full profiles on the exact merge candidate, push and merge a pull
request after hosted checks, then fast-forward local `main` and verify
`origin/main` resolves to the merged result.

Inspect earlier incomplete packages except SPEC-0182 using their own evidence:
keep live work active; complete only verified work; supersede only criteria
actually taken by a successor; and cancel only with registered approval and
per-criterion disposition.

## Interfaces and Data

Git, the pull-request workflow, registered validation commands, and Stage 99
lifecycle/receipt fields are used. No service, secret, provider account, model
call, or external data store is added.

## Failure Modes and Guardrails

Remote drift, conflicts, failed required gates, or missing hosted results keep
the package open. Never force-push, overwrite unrelated work, delete an unclean
worktree, or report local evidence as hosted/runtime evidence. The review filter
fails closed for absent deterministic results, ambiguity, or protected changes.

## Acceptance Contract

1. The source packet is integrated into `main` with current Stage 01, 02, 05,
   99, and governance obligations preserved and an exact active-Task receipt.
2. Deterministic checks precede bounded independent semantic review, preserving
   required human approvals.
3. The exact merge candidate has observed PASS from registered changed/full
   profiles. Unavailable or failed checks keep this package nonterminal.
4. Required hosted checks pass before merge, or the package remains nonterminal.
5. Local `main` and `origin/main` resolve to the merged result; only clean,
   completed integration branch/worktree state is removed.
6. Every source R01-R39 obligation has an evidenced disposition: delivered
   implementation and applicable deterministic checks have observed PASS; the
   unobserved portions of R04/R15/R18/R19/R22 and the original Plan's
   model-entitlement observation are assigned one-to-one to SPEC-0195 with
   unchanged acceptance and explicit BLOCKED/NOT_RUN status. Delivery may
   complete only after that transfer is committed and independently reviewed.
   Transferred observations and the original source package are not reported as
   completed. Coverage and all other retained delivery requirements must be
   accurately resolved here.

7. Under the owner's 2026-09-30 ruling, aggregate coverage of added or modified
   executable Python lines in the approved implementation diff is at least 80%.
   The Task records the source base/head, rename-aware line mapping, actual
   observed line sets and counts, and measurement limits. This does not claim
   80% whole-file or branch coverage. A time-limited instrumentation sample
   does not replace the required passing registered tests.

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [SPEC-0182](../0182-home-residual-backlog/spec.md) (separate active work)
- Source packet `c86f55518b8a9a156e10e38fbd52d1a883063d6a`

## Open Questions

Docker-backed profile availability and forge hosted-check visibility must be
observed during execution; neither absence authorizes bypass.

## Operational Impact

Only approved repository and remote Git state changes occur; no service,
secret, or recovery operation is performed.
