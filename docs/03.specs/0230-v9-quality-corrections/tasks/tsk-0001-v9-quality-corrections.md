---
title: "Prompt v9 Quality Corrections Task"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0230-TSK-0001"
parent_ids:
- "SPEC-0230-PLAN-0001"
created: "2026-10-13"
---

# Prompt v9 Quality Corrections Task

## Overview

### Objective

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

### W4 PostToolUse Normalizer Agreement

The owner asked on 2026-10-13 whether the PostToolUse whitespace cleanup
conflicts with anything. Policy does not conflict: `quality-standards.md`
section 10 lets an agent editor hook format "only in agreement with the
registered owner", `agentic.md` describes this hook, `--check` stays
non-mutating, and the hook edits only the files in the current edit payload
and skips the frozen archive payloads it reads from `.pre-commit-config.yaml`.

The bytes did conflict. The normalizer used `str.splitlines()`, which also
breaks on form feed, vertical tab, U+2028 and other separators, and rejoined
with LF. Against the cached pre-commit-hooks v6.0.0 fixers on the same inputs:
`a\x0cb` became two lines, U+2028 became LF, and `a  \r\nb\r\n` lost its CRLF,
while the owners left all three unchanged. It also stripped only space and
tab where `trailing-whitespace` strips every trailing ASCII whitespace byte,
which flipped the `mixed-line-ending` majority in some mixed files.

The normalizer now mirrors `trailing-whitespace` line handling: lines split on
LF only, a CRLF ending kept, `bytes.rstrip()` on the rest, and one LF added
when the file does not end in LF or CR. It still leaves extra final blank
lines to `end-of-file-fixer`. A 3,000-case random comparison against the
owners' fixed point found 0 divergences on inputs without a bare CR; the 94
divergences with a bare CR come from `mixed-line-ending` treating CR as a line
ending, and none of the 1,706 tracked Markdown, shell, YAML and JSON files
contains a bare CR (`.gitattributes` sets `eol=lf`).

A new test pins six inputs to the owners' bytes. It failed for four inputs on
the previous normalizer and passes now; all 60 tests in
`test_agent_governance_ci_routing` pass, and `bash -n` and `shellcheck
--severity=warning` are clean.

### Owner Decisions

On 2026-10-13 the owner answered the review question by accepting the
criteria rated ready and approving this Spec and Plan; Review and Completion
lists the criteria and why the rest stay `pending`.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0230 | draft | approved | #owner-decisions |
| SPEC-0230-PLAN-0001 | draft | approved | #owner-decisions |
| SPEC-0230-TSK-0001 | draft | ready | #current-readiness-review-on-2026-10-22 |
| SPEC-0230-TSK-0001 | ready | in-progress | #current-lifecycle-reconciliation-on-2026-10-22 |
| SPEC-0230-TSK-0001 | in-progress | completed | #current-completion-decision-on-2026-10-22 |

### Current readiness review on 2026-10-22

The owner's current request explicitly authorizes status and lifecycle processing
for implemented work. This is a new reconciliation on 2026-10-22; it does not
backdate execution or replace the historical acceptance decisions. The review
used input `bd4168e20861d557c9a4f31025a2a649be3e8066` and the existing public
Task receipts. Both parents are already `approved`. All 4 assigned
criterion/Work Unit pairs have this Task's PASS evidence, all 4 owned
criteria are accepted, and no historical FAIL remains unresolved. The existing
completed-evidence reader accepted an in-memory completed assessment. The Task
therefore enters `ready` for the bounded lifecycle reconciliation.

### Current lifecycle reconciliation on 2026-10-22

The Task entered `in-progress` to reconcile its execution metadata with the
already accepted implementation. The review reused the recorded source,
tests, independent reviews and integration receipts, preserving their input
identities and limitations. It checked Plan assignment coverage and the
historical failure resolutions without changing Evidence, Criterion Acceptance
or the existing parent authorization events. Later generation and operational
follow-ups keep their own current owners; this work adds no implementation,
provider, credential, recovery or HOME observation.

### Current completion decision on 2026-10-22

The current reconciliation finished after the receipt and assignment review.
The existing Evidence and Criterion Acceptance sections, historical review
record and parent event prefix were verified unchanged. This Task is now
`completed` under the owner's current lifecycle instruction, using its existing
accepted criteria and PASS evidence. This is today's execution-state decision,
not a replacement or backdating of the earlier owner decisions.

The owner-accepted partial local gate limitation remains recorded; completion
does not claim a local changed gate covered the normalizer change.

Spec and Plan remain `approved`. Archive readiness is derived by the existing
reader after completion; no archive move, withdrawal or operational action is
part of this Task closure. The final documentation gates are recorded by the
current coordination Task.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mark-only inputs | 1 | W1 | Pinned `action.yml` text for `days-before-close`; workflow contract tests | Branch on `4af41f1a8` | PASS | W1 Mark-only Stale Workflow | - |
| Check repairs | 2 | W2 | Both tests RED on clean `4af41f1a8`; 65 workflow contract and update-gate tests GREEN | Branch on `4af41f1a8` | PASS | W2 Selector List and Ledger Digests | - |
| Normalizer agreement | 4 | W4 | Owner comparison; random comparison; new test RED then GREEN; module tests | Branch on `2a57d4122` | PASS | W4 PostToolUse Normalizer Agreement | - |
| Remote candidate | 3 | W3 | `candidate-quality` on PR #438 | `0b479b1a4` | PASS | Review and Completion | - |
| Changed gate | 3 | W3 | `run-ci-gate.py --profile changed`; rerun of two permission tests | Branch on `4af41f1a8` | PASS | W3 Changed Gate | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Mark-only inputs | Owner accepted 2026-10-13 |
| 2 | accepted | Check repairs | Owner accepted 2026-10-13 |
| 3 | accepted | Remote candidate, Changed gate | Owner accepted 2026-10-14 |
| 4 | accepted | Normalizer agreement | Owner accepted 2026-10-13 |

## Review and Completion

PR #438 head `0b479b1a4`: `candidate-quality` passed in run `38344684357` (job
`115123215753`, 4m55s); CodeQL and GitGuardian passed; `main-security` was
skipped as it runs on `main` only.

On 2026-10-13 the owner, answering the review question, accepted the criteria
rated ready (criteria 1, 2, 4) and approved this Spec and Plan. Criterion 3,
the gate, stays `pending`: the Changed gate row records a gate that exited 1
before only two permission modules were rerun, on a base before W4, so no
local changed gate covers the normalizer change.

On 2026-10-14 the owner, answering a second review question, accepted
criterion 3 on the remote candidate and the partial local gate as recorded,
knowing that no local changed gate covers the normalizer change.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
