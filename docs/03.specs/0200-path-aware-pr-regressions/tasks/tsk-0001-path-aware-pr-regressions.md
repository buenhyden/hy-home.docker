---
title: "Path-Aware PR Regression Execution"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0200-TSK-0001"
parent_ids:
- "SPEC-0200"
- "SPEC-0200-PLAN-0001"
created: "2026-10-02"
---

# Path-Aware PR Regression Execution

## Objective

Execute [SPEC-0200](../spec.md) and its [Plan](../plan.md) through W0-W4. Preserve the single required PR status and every document content contract while routing two expensive regression groups only to changes that can affect them.

## Inputs

The user approved the written Spec, the Plan, and same-session implementation with independent final review on 2026-10-02. The user selected a main-only delivery flow and change-path-specific required PR regressions with manual full coverage. The worktree branch is `codex/spec-0200-pr-gate-latency`. The trusted parent package was activated through protected PRs [#338](https://github.com/buenhyden/hy-home.docker/pull/338), [#339](https://github.com/buenhyden/hy-home.docker/pull/339), [#340](https://github.com/buenhyden/hy-home.docker/pull/340), and [#341](https://github.com/buenhyden/hy-home.docker/pull/341), each after the required `validation-changed` result passed. The active main base is `d46d892380d1d2faad234df6d9b872b928a61c6a`.

## Work Log

- W0: The Spec advanced draft to review to approved to active, and the Plan advanced draft to approved to active on successive trusted main bases. This Task begins in draft and will advance through its registered ready and in-progress states before implementation.
- W1: Baseline and dependency inventory are in progress. The two measured regression leaves are `leaf.local-document-metadata-tests` and `leaf.document-governance-library-regressions`; both currently run on Stage 03 and Stage 05 document-only PRs. Exact path ownership, retained content validators, and script/test disposition will be recorded before routing changes.
- W2-W4: Pending implementation, hosted acceptance, lifecycle closure, and branch cleanup.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1, W3 | Pending phase-matrix and hosted timing comparison | [Quality standards](../../../../.agents/governance/quality-standards.md) |
| 2 | W2, W3 | Pending document-only validator parity proof | [Workflow contract](../../../../.github/workflow-contract.yml) |
| 3 | W2 | Pending owner-path, unknown-path, and bounded-root tests | [Gate contract](../../../../scripts/lib/gate/ci_gate_contract.py) |
| 4 | W2, W3 | Pending full-plan exact-count and hosted route receipts | [Quality workflow](../../../../.github/workflows/ci-quality.yml) |
| 5 | W1 | Pending consumer/replacement disposition for any removal | [Script manifest](../../../../scripts/manifest.yaml) |
| 6 | W3 | Pending governance alignment, independent review, and protected PR result | [Quality standards](../../../../.agents/governance/quality-standards.md) |

## Review Evidence

Independent final diff review is pending after the implementation candidate passes focused and changed-profile validation.

## Commit Ledger

W0 parent activation merged as `d46d892380d1d2faad234df6d9b872b928a61c6a` through PR #341. Implementation commits and merge receipts are pending.

## Rulings

- The required PR check remains `validation-changed`; no second status or dev branch is introduced.
- A script or test is removed only when its callers and replacement are evidenced. Name or age alone is insufficient.
- The two slow test groups contain some current-corpus assertions. W1 must confirm equivalent direct validation before W2 prunes them from documentation-only routes.

## Deferred Items

None at Task creation. Any failed, skipped, or unobserved acceptance evidence will be recorded before terminal status.
