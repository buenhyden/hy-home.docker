---
title: "Tag and Worktree Rule Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0019"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Tag and Worktree Rule Task

## Overview

### Objective

Execute W35: apply the owner's choices on two gaps found by re-reading the
original request against the current repository. This Task owns criterion 30
only.

## Inputs and Authorization

On 2026-10-29 a re-read of the request found that tags must be SemVer and
that worktrees must be created under `.worktrees`. The owner then approved
deleting the stale `main-current` tag and adding the worktree location rule.
`.agents/governance/git-workflow.md` said that policy alone does not authorize
deleting a historical ref; the owner's direct approval is a higher authority
for this one ref. The input is branch `chore/merge-method-and-residual-review`
(PR #615). The authorization covers that tag deletion, this branch, its pull
request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0019 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0019 | ready | in-progress | #objective |
| SPEC-0212-TSK-0019 | in-progress | completed | #evidence |

### Tag cleanup

`main-current` was a lightweight tag on `849ef009a` (2026-10-06), left by the
retired `update-main-current` job. No workflow, script, or document used it.
It was deleted from `origin` and locally; the commit stays reachable from
`main`. The remaining tag is `0.0.1`, which has a Release. The policy sentence
now reads that deleting or rewriting a historical ref needs the owner's
approval for that ref.

### Worktree rule

`.gitignore` already ignored `.worktrees/`, but no policy named it.
`git-workflow.md` now says linked worktrees go under `.worktrees/<branch>`
and are removed with their merged branch when the work ends.

### Request re-read

The tests that name Task paths use synthetic fixture packages, not completed
documents, so the request's rule against tests bound to a completed
document's state already holds.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Remote tag read-back | 30 | W35 | `git ls-remote --tags origin` | 2026-10-29 | PASS | Only `0.0.1` remains | required | - |
| Tag consumer scan | 30 | W35 | `grep -rn main-current` over code, workflows, and policy | This branch | PASS | No consumer outside the protection record | required | - |
| Governance contract | 30 | W35 | `check-agent-governance-contract.py` | This branch | PASS | 0 failures | required | - |
| Provider render | 30 | W35 | `provider_surface_renderer.py --check` | This branch | PASS | 0 drift | required | - |
| Gate adapter tests | 30 | W35 | `python3 -m unittest tests.lib.gate.test_ci_gate_adapters` | This branch | PASS | OK | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 30 | accepted | Remote tag read-back, Tag consumer scan, Governance contract, Provider render, Gate adapter tests | The stale tag is gone with its commit kept; the worktree location is a policy rule. | SPEC-0212 TSK-0019 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
