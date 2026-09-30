---
title: "Agent Contract Integration Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0194-PLAN-0001"
parent_ids:
- "SPEC-0194"
created: "2026-09-29"
---

# Agent Contract Integration Plan

## Objective

Promote SPEC-0194 through its lifecycle, integrate the reviewed
`codex/agent-contracts` source packet into `main`, and record only observed
outcomes.

## Dependencies

- REQ-0024 and AD-0027 remain the governance authority.
- Source branch `codex/agent-contracts` and packet
  `c86f55518b8a9a156e10e38fbd52d1a883063d6a` are evidence inputs until receipt.
- SPEC-0182 is separately active and excluded from stale-package disposition.
- Remote push, pull request, merge, and hosted checks use the authorized
  `buenhyden/hy-home.docker` scope and available forge permissions.

## Execution Sequence

1. W1: Validate draft Spec, Plan, and Task; record sequential review, approved,
   and active lifecycles before any integration receipt (criteria 1, 2). Seed
   the existing four-file recovery skill draft from 2efc0060a with its two
   registry sources and official Claude projection; activate only through its
   recorded review and active predecessors. Reuse its original discovery-only
   hook keywords and retain the exact inventory/routing tests.
2. W2: Reconcile source with `main`; inspect incomplete packages except
   SPEC-0182 and classify each from its own evidence as live, complete,
   superseded, or cancellation-pending (criteria 1, 5, 6). Preserve the original
   hardening packet bytes/statuses via the registered divergent-branch handoff
   only after SPEC-0194 is active and its Task in-progress. The existing immutable
   same-ID HOME classification archive remains unchanged. Carry source R01-R39
   one-to-one from its final Task reconciliation. Transfer only the actual
   R04/R15/R18/R19/R22 and model-entitlement observations to SPEC-0195 under the
   owner's 2026-09-30 decision; retain their conditions and missing status.
   Do not claim source completion. The same-ID/different-slug
   case requires the existing receipt validator to select a unique completed
   identity at its actual immutable path. W2 owns only
   `scripts/lib/document_governance/spec_packages.py` and
   `tests/lib/document_governance/test_spec_packages.py` for this correction;
   witness RED first and retain exact-byte, committed-blob, distinct-carrier,
   missing, modified and ambiguous-witness rejection checks.
3. W3: Run registered deterministic checks first; obtain narrowly scoped,
   independent read-only agent semantic review and escalate only exceptions
   requiring human judgment or approval (criterion 2).
4. W4: Run changed and full profiles on the exact merge candidate; retain
   BLOCKED/NOT_RUN results where authorization or environment prevents proof
   (criterion 3). Neither BLOCKED nor NOT_RUN permits terminal completion.
5. W5: Push, create and merge the pull request after hosted required checks;
   fast-forward local `main` from `origin/main` and record exact receipt
   (criteria 1, 4, 5).
6. W6: Verify merged `main`; remove only clean completed integration branch and
   worktree state; complete the package through its registered lifecycle
   (criteria 5, 6). Complete only after retained delivery requirements pass and
   the approved observation transfer to SPEC-0195 is committed and reviewed.
   SPEC-0195 remains open until its own observed acceptance passes; branch
   cleanup does not change those statuses.

## Risk and Rollback

No force-push or destructive cleanup. Failed checks, remote drift, and merge
conflicts leave branch/worktree intact. A later revert is a reviewed follow-up
commit; evidence records are preserved rather than rewritten.

## Verification

Use registered metadata/lifecycle checks for W1; Git diff/worktree checks for
W2/W6; deterministic validators and bounded review for W3; `python3
scripts/validation/run-ci-gate.py --profile changed` and `--profile full` for
W4; and forge required-check results plus matching local/remote `main` IDs for
W5.

## Rulings

- Automated classification reduces repeated human semantic review but does not
  replace required human approvals at protected boundaries.
- SPEC-0191 is already completed and preserved at acce0a6ba; its later
  completion receipt supersedes the earlier missing-evidence assessment.
