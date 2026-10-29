---
title: "Worktree Rule Scope Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0021"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Worktree Rule Scope Task

## Overview

### Objective

Execute W37: remove the conflict between the worktree location rule TSK-0019
added and a CI script. This Task owns criterion 32 only.

## Inputs and Authorization

A further re-read of the request, which asks that conflicting rules be found
and resolved, checked every `git worktree add` call. The owner asked on
2026-10-29 for the request review to continue through to merge. The input is
`main` at merged PR #618. The authorization covers this policy wording, this
branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0021 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0021 | ready | in-progress | #objective |
| SPEC-0212-TSK-0021 | in-progress | completed | #evidence |

### Conflict and fix

`scripts/validation/run-ci-precommit.sh` creates a detached worktree under its
own scratch directory, runs only under GitHub Actions, and removes it with
that directory. The TSK-0019 rule said every linked worktree goes under
`.worktrees/<branch>`, which that script does not follow. The rule in
`.agents/governance/git-workflow.md` now applies to a branch's linked worktree
and states that a script's detached scratch checkout is not one. The script is
unchanged.

### Kept

The SKILL.md links to `references/` and `scripts/` files all resolve, and no
canonical or provider surface names a dated model identifier. The
`test_generation6.py` and `test_generation7.py` modules guard current evidence
rules; only their names are historical.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Worktree call scan | 32 | W37 | `grep -rn "worktree add"` over scripts and provider surfaces | This branch | PASS | Two calls, both in the CI scratch checkout | required | - |
| Governance contract | 32 | W37 | `check-agent-governance-contract.py` | This branch | PASS | 0 failures | required | - |
| Provider render | 32 | W37 | `provider_surface_renderer.py --check` | This branch | PASS | 0 drift | required | - |
| Metadata contracts | 32 | W37 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 32 | accepted | Worktree call scan, Governance contract, Provider render, Metadata contracts | The worktree rule covers branch worktrees and no longer contradicts the CI scratch checkout. | SPEC-0212 TSK-0021 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
