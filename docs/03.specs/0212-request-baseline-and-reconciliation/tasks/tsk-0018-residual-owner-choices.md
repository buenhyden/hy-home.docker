---
title: "Residual Owner Choices Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0018"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Residual Owner Choices Task

## Overview

### Objective

Execute W34: apply the owner's choices on the four items TSK-0017 left open.
This Task owns criterion 29 only.

## Inputs and Authorization

On 2026-10-29 the owner chose, per item: allow merge commits only; validate
Compose statically without starting anything; diagnose the pre-existing unit
failures and report them, fixing only what touches no secret surface; and hand
the cross-repository gaps off without writing to another repository. The input
is `main` at merged PR #614. The authorization covers the one repository
setting change, this branch, its pull request, and merge.

The owner's handoff choice named a Stage 90 document. The audits index
retires that category under SPEC-0158 and places a cross-stage audit in a Task
under its governing Spec, so the handoff is recorded here instead.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0018 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0018 | ready | in-progress | #objective |
| SPEC-0212-TSK-0018 | in-progress | completed | #evidence |

### Merge methods

`gh api -X PATCH repos/buenhyden/hy-home.docker` set
`allow_squash_merge=false` and `allow_rebase_merge=false`, keeping
`allow_merge_commit=true`. The read-back matched, and branch protection read
back unchanged. The before-state, after-state, and rollback are recorded in
`.github/rulesets/main-protection.md`.

### Pre-existing unit failures

The 18 failures TSK-0015 recorded have one cause: the system Python
`jsonschema` is 4.10.3, which predates the `referencing` package that
`scripts/lib/ops/secret_catalog.py`, `root_resource_assessment.py`, and
`wiki_preparation.py` import. `load_catalog` raises, so `gen-secrets.sh`
reports `GENERATION rejected: invalid public catalog` or `METADATA rejected`,
and the contract modules fail to import. CI installs
`scripts/requirements-controller.lock` (`jsonschema` 4.26.0, `referencing`
0.37.0) and passes. With that lock in an isolated venv placed first on `PATH`,
all 124 tests in the six affected modules pass. No code or secret surface is
wrong; `scripts/README.md` now says how to run them locally. The system Python
was not changed.

### Static Compose validation

`scripts/validation/validate-docker-compose.sh` in its default mode creates
placeholder `.env` and secret files where they are missing. To keep it away
from the operator's real files, it ran in a temporary detached worktree of
`main`, which was then removed. It rendered 66 profile selections and 341
service definitions and passed. The log holds profile names only. Nothing was
started or stopped; containers already running were not touched.

### Cross-repository handoff

Read without writing on 2026-10-29: Project-Template and hy-home.k8s from
their local checkouts at `HEAD` without fetching, blog-data from its remote
`dev` branch. TSK-0017 holds the governance file versions.

| Repository | Required QA route | Observed workflows | Stage 98 layout | Gap for that repository's owner |
| --- | --- | --- | --- | --- |
| Project-Template (`dev`) | Local action runner | 8, all `self-hosted` | `completed`, `retired`, `superseded`; no `tombstones`, `migrations`, or catalog | Archive route records and catalog |
| hy-home.k8s (`main`) | Local QA | 3, none `self-hosted` | `completed`, `superseded`, `migrations`; no `retired`, `tombstones`, or catalog | Confirm whether its workflows run QA remotely; archive route records and catalog |
| blog-data (`dev`) | Local action runner | 4; `self-hosted` appears in 18 files | `completed`, `retired`, `superseded`, `catalog.md`; no `tombstones` or `migrations` | Archive route records; catalog name and fields |

The four repositories share no edition identifier for their governance or
archive contract. Common adoption needs one agreed edition and a change in
each repository under that repository's own approval. Nothing here claims it.

### Codex loader

The Codex loader stays `NOT_RUN`: it is not observable from a Claude Code
session, and the owner did not choose to supply a Codex session's output.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Merge-method read-back | 29 | W34 | `gh api repos/buenhyden/hy-home.docker` and `…/branches/main/protection` | 2026-10-29 | PASS | Merge commits only; protection unchanged | required | - |
| Isolated-venv test run | 29 | W34 | Six affected modules with the controller lock first on `PATH` | This branch; Python 3.12.3 | PASS | 124 tests OK | required | - |
| System-Python reproduction | 29 | W34 | Same modules with system Python | This branch | PASS | Failures reproduce; `ModuleNotFoundError: referencing` | required | - |
| Static Compose validation | 29 | W34 | `validate-docker-compose.sh` in a clean detached worktree | `main`@`43053ea32`; Compose 5.6.1 | PASS | 66 selections, 341 services | required | - |
| Cross-repository read | 29 | W34 | `git ls-tree`/`git grep` in two checkouts; `gh api` and `gh search code` for blog-data | 2026-10-29 | PASS | Gaps listed per repository | required | - |
| Metadata contracts | 29 | W34 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Codex loader acceptance | 29 | W34 | Native Codex session load | - | NOT_RUN | Not observable from this session | optional | - |
| Runtime acceptance | 29 | W34 | Compose start and health | - | NOT_RUN | Owner chose static validation only | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 29 | accepted | Merge-method read-back, Isolated-venv test run, System-Python reproduction, Static Compose validation, Cross-repository read, Metadata contracts | Merge commits only, applied and read back; the pre-existing failures are a local dependency gap, not a defect; Compose validates statically; cross-repository gaps handed to their owners; Codex loader and runtime stay not run. | SPEC-0212 TSK-0018 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
