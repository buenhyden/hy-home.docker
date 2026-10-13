---
title: "Prompt v9 Quality Corrections Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0230-TSK-0001"
parent_ids:
- "SPEC-0230-PLAN-0001"
created: "2026-10-13"
---

# Prompt v9 Quality Corrections Task

## Objective

Stop the stale workflow from closing threads on inactivity alone, and repair
the two checks that fail on `main` for every branch that selects them.

## Inputs and Authorization

The owner pasted the prompt v9 execution request on 2026-10-13 and answered
"계속 진행한다" to the first progress report. The request authorizes
repository source, test, workflow and document changes, logical commits, the
branch push, its pull request and per-Spec integration. Baseline `main`
`4af41f1a8`. No repository setting, label, closed thread or image is changed.

## Work Log

### W1 Mark-only Stale Workflow

`days-before-close` was `7`. The pinned manifest
(`actions/stale@4391f3da665fdf50b6810c1a66712fb9ba21aa93`, `action.yml`
line 32) reads "Set to -1 to never close stale issues or pull requests", so
the input is now `-1`. The notices say the thread will not close and that
closing is the owner's decision. The workflow is renamed `Mark Stale Issues &
PRs` and its step `Mark stale threads`; the contract entry and the
duplicate-key fixture that edits the real workflow name follow. Job
permissions are unchanged: labelling and commenting still need
`issues: write` and `pull-requests: write`.

### W2 Selector List and Ledger Digests

Both failures reproduce on a clean detached checkout of `4af41f1a8`:

- `test_optional_runtime_skips_keep_all_required_module_selectors` expected
  the selector list before `c80915370` registered
  `tests.validation.test_opsflow_database_rehearsal.OpsflowDatabaseRehearsalBoundaryTests`.
  The registration is intended (its rehearsal module landed in the same
  commit), so the test list gains that selector.
- `test_current_root_census_excludes_relocated_lab_history` compared the
  ledger `include_inputs` with the census computed by
  `expected_from_root`. `b8d3ea818` replaced the certificate directory mounts
  in the `infra/01-gateway/nginx`, `infra/01-gateway/traefik` and
  `infra/04-data/opensearch` Compose files after the ledger commit
  `256d5f833`. A diff of those files across that range changes no `image`,
  `build` or Dockerfile line, so the image census is unaffected and only the
  three `sha256` values in `include_inputs` were replaced with the computed
  ones. The edit went through the JSON model after a byte-exact round-trip
  check, so `historical_root_census`, which holds an equal digest, is
  untouched.

No other branch in this clone or on the remote carried either fix when
checked.

### W3 Changed Gate

The first run stopped on `identity-allocation-not-advanced`: a new SPEC ID
must advance `identity_spaces.spec`, so `high_water` is now 230 and
`next_number` 231. The second run exited 1: metadata, corpus lifecycle and
archive recovery reported no violation, 265 contract tests passed, and 645
validation tests had two failures, both
`test_script_is_*_group_or_world_writable` for the Gatus and Open WebUI
entrypoints. Git records both as `100755`; the worktree was checked out under
umask 002, which left them group-writable on disk. After `chmod g-w` on the
two files, which Git does not track, both modules passed (19 tests).

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mark-only inputs | 1 | W1 | Pinned `action.yml` text for `days-before-close`; workflow contract tests | Branch on `4af41f1a8` | PASS | W1 Mark-only Stale Workflow | pending |
| Check repairs | 2 | W2 | Both tests RED on clean `4af41f1a8`; 65 workflow contract and update-gate tests GREEN | Branch on `4af41f1a8` | PASS | W2 Selector List and Ledger Digests | pending |
| Changed gate | 3 | W3 | `run-ci-gate.py --profile changed`; rerun of two permission tests | Branch on `4af41f1a8` | PASS | W3 Changed Gate | pending |

## Review and Completion

`candidate-quality` is recorded here when the pull request has a result. No
row is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
