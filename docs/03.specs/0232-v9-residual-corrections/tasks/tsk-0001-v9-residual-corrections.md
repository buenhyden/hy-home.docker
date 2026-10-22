---
title: "Prompt v9 Residual Corrections Task"
version: "0.8.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0232-TSK-0001"
parent_ids:
- "SPEC-0232-PLAN-0001"
created: "2026-10-13"
---

# Prompt v9 Residual Corrections Task

## Overview

### Objective

Close the four prompt v9 findings that still hold on `main` after SPEC-0230
and SPEC-0231: F26, F20, F22 and F02.

## Inputs and Authorization

The owner pasted the prompt v9 execution request on 2026-10-13 and answered
"이어서 계속 진행한다" to the SPEC-0231 report. Asked the same day, the owner
chose a validate-only PostToolUse hook, kept the Stop hook's whole-worktree
scope, and moved F24, F27 and F36 to a later Spec. The request authorizes
source, test and document changes, logical commits, the branch push, its pull
request and per-Spec integration. Baseline `main` `baffae4c7`.

## Work Log

### Starting State

A read-only check of the remaining findings on `baffae4c7`:

- F18 does not hold: `.github/workflow-contract.yml` classifies only
  `ci-quality.yml` as `required-quality`; greeting, labeler, stale and
  changelog are `non-gating` and no gate node reads them.
- F42 does not hold: `.claude/provider.md`, `.codex/provider.md` and the
  Provider Registry agree that Claude uses generated skill adapters and Codex
  discovers `.agents/skills` directly.
- F26, F20, F22 and F02 hold as the Spec states.

### W1 Validate-only Hook

`post_tool_use()` in `scripts/hooks/agent-event-hook.sh` now passes
`--check`. In check mode `post-tool-validate.sh` runs the same normalization
in memory and fails with `<path>: trailing whitespace or a missing final
newline` when it would change the file; it skips frozen payloads as before.
`git diff --check` alone missed untracked files and a missing final newline.
On an untracked `note.md` without a final newline the `main` script exited 0
and this one exits 1, leaving the bytes unchanged. The agentic policy (1.5.0),
quality standards section 10 (1.6.0) and `scripts/README.md` (1.4.2) say the
hook validates and `--write` is the explicit fix. SPEC-0230 contract 4 still
holds: the normalizer is opt-in and agrees with its owner.

The report reaches the provider the way the hook's existing lint failures
do: the dispatcher passes the exit status through unchanged, and a status
other than 2 is a non-blocking error. Whether the agent sees that message in
a live Claude or Codex session was not observed and is `NOT_RUN`; W7
replaces this channel.

### W2 n8n Candidate Rehearsal

The two `sec01-n8n-*:2.42.6-candidate` manifest and index pins and
`test_n8n_both_variants_actual_uid_version_and_font_receipt` are removed. The
rehearsal ran only with `HYHOME_WORKFLOW_REHEARSAL=1`, CI skips it, and the
bundle is 2.42.7. The Airflow rehearsal matches its current 3.3.2 bundle and
stays. The SEC01 ledger and verification records bind earlier bytes of this
file (`f4c9a775…`, current `main` is `914412e4…`), so they are historical and
unchanged. The n8n README notes the removal.

### W3 Frozen Payload Registry Assertion

`test_every_text_mutator_excludes_the_same_frozen_payloads` now also compares
the anchor with the Registry: a tracked archive file must match the anchor
exactly when it lies under an unmanaged `docs/98.archive/` record profile or
on a `frozen-legacy-status` path. Dropping `retired` from the anchor makes
149 files disagree. `resolved/` has no tracked file yet, so the archive README
rule that its first record adds it to the ignore lists is now enforced.

### W4 Root Shim

`AGENTS.md` keeps its three steps. The removed step 4 repeated bootstrap load
order step 3 and `.codex/provider.md` lines 22 to 37.

### Review

An independent read-only `rules-engineer` review found nothing blocking and
four other findings. Fixed: Spec contract 4 now says `AGENTS.md` adds nothing
beyond its three steps, since step 3 itself repeats bootstrap step 4; the
section 10 rule covers repository-registered hooks only, because a hook
outside the repository is what `.prettierignore` handles; `agentic.md` links
section 10 instead of restating the explicit-fix rule. Recorded, not changed:
live agent visibility of the check-mode report (W1). The review found no other
current text that says the hook rewrites files, and confirmed every removed
`AGENTS.md` statement keeps an owner Codex reads.

### W5 Gate

The W1 and W3 test edits share commit `aa5dd3128` because both change
`tests/validation/test_agent_governance_ci_routing.py`.

Hosted `candidate-quality` on pull request #443 (head `cc8a880dc`, run
38366462481) passed. The local changed gate on `cc8a880dc` passed the active
and changed metadata checks (0 violations), the document links, the corpus
lifecycle and archive recovery (0 violations) and the 15-, 15- and 148-test
suites, then reached its local 3600 s limit inside the document governance
suite and was stopped (exit 124). That suite's local result is `NOT_RUN`.

The owner merged pull request #443 as merge commit `8a3155daa` (parents
`baffae4c7` and `cc8a880dc`).

On 2026-10-14 the change was replayed through the local changed gate in a
scratch clone. The base was the PR parent `baffae4c7` with the three SPEC-0235
changes (both local timeouts and the reachability test) and the one-line
tombstone identity fix `61f3b99ef` from this package's W6 (PR #445); the head
was that base plus the #443 merge diff; every other ref was removed, and the
checkout used umask 022. The gate exited 0 after 2998 s: the metadata node
ran 148 tests in 733 s and the governance node 753 tests in 1072 s, all OK.
Three earlier replays are not counted, each for a cause in the replay rather
than the change: later refs in the clone failed the identity history test,
which also confirms the cause the Governance Suite record below suspected;
without `61f3b99ef` the tombstone test failed as it had on `main` since
`6056788a5` (2026-10-12); and under umask 002 two entrypoint permission tests
saw group-writable files.

### W6 Tombstone Identity

The owner chose this fix next on 2026-10-13. `_ROLE_MEMBER` in
`scripts/lib/document_governance/archive.py` accepted only
`docs/05.operations/<family>/NNNN-slug.md`; since `6056788a5` the files sit
under `<family>/NN-classification/`, so the three role-layout subtests fell
through to the tombstone number (`tomb-GDE-0235` for `tomb-GDE-0051`). The
pattern now takes an optional classification segment, spelled as
`operations_moves._DOMAIN` spells it; flat paths that existing tombstones
record still match. The only production caller is the tombstone identity
check at `archive.py:924`. `test_archive` went from 3 failures to 71 passing;
the corpus lifecycle check and archive recovery (140 tombstones) report 0
violations and `tests.validation.lifecycle.test_recovery` passes. Pull
request #445 passed hosted `candidate-quality` (run 38372338395) and the
owner's request merged it as `b1a6976f4`.

### W7 PostToolUse Failure as Context

The owner asked on 2026-10-13 to review the hook's exit status. The Claude
Code hooks reference (<https://code.claude.com/docs/en/hooks>) shows stderr
to the model for a PostToolUse exit 2 only; any other non-zero exit is a
non-blocking error the model does not see, and stdout on exit 0 reaches it
only as `hookSpecificOutput.additionalContext`. The Codex hooks page
documents `additionalContext` for PostToolUse, says exit 2 with stderr is
feedback that replaces the tool result, and does not describe exit 1. So
every PostToolUse failure, including the shellcheck and yamllint failures
that predate W1, never reached the model.

`post_tool_use()` now captures the check output and, on failure, prints
`{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext":
...}}` with at most the last 8000 characters and exits 0. On a whitespace
defect the `main` dispatcher exited 1 with stderr only; this one exits 0 with
that JSON. The agentic policy (1.5.1) states the channel. Live delivery in a
Claude or Codex session is observed only after merge, from the main checkout.

PR #446 passed hosted `candidate-quality` (run 38374565260) and merged as
`958349408`. Live delivery was then observed in both providers on
2026-10-13:

- **Claude Code 2.1.296**, main checkout at `958349408`: a Write of a probe
  file with trailing spaces returned `PostToolUse:Write hook additional
  context: Post-edit validation failed...` to the model, and the file kept
  its trailing spaces.
- **codex-cli 0.162.1**, `codex exec` in a disposable worktree of
  `958349408`: an `apply_patch` appending a line with trailing spaces led the
  model to quote `Post-edit validation failed; fix before committing:
  scripts/README.md: trailing whitespace or a missing final newline; fix it,
  or run post-tool-validate.sh --write` verbatim, and the spaces were kept.
  Codex's `workspace-write` sandbox cannot start on this host (`bwrap:
  loopback: Failed RTM_NEWADDR: Operation not permitted`), so every write
  failed before a hook ran; the observed run used `-s danger-full-access`
  with a prompt limited to that one edit. The worktree was then removed.

### Governance Suite

The full document governance suite (`python3 -m unittest discover -s
tests/lib/document_governance -t .`) ran with no time limit in a detached
scratch worktree on `b1a6976f4` on 2026-10-13: 894 tests in 1844 s, 893
passed and one failed. `test_registry_high_water_is_not_below_repository_history`
reported `registry high_water=232 observed=234`. That test reads every local
ref (`--all`), and the unmerged local branches for SPEC-0233 and SPEC-0234
already issue Spec numbers 233 and 234. That cause is likely but not yet
verified; the test is rerun once both branches merge.

### W8 Pre-commit Wrapper (F22)

`run-ci-precommit.sh` dropped `end-of-file-fixer` and `trailing-whitespace`
from the read-only copy of `.pre-commit-config.yaml`, so neither the local
staged check nor the PR merge check saw trailing whitespace or a missing final
newline in a file no other hook covers, such as TOML, a Dockerfile or `.env`.
No test compared the copy's hooks with the source's; the fake `pre-commit` in
`test_run_ci_precommit.sh` asserted the two hooks were absent.

The wrapper now keeps every hook. A fixer without a check mode changes only the
isolated checkout, and `pre-commit` fails a hook that changes a file. Both
modes now take the before/after snapshot that only `local-staged` took: a hook
that changes the candidate and fails returns its own exit with a note to fix
the files explicitly, and one that changes it and passes still fails with exit
2. `quality-standards.md` (1.6.1) states this.

- **RED:** the updated test, whose fake `pre-commit` requires the copy to
  list exactly the source's hook IDs and adds the failing-mutator cases for
  both modes, failed against the `main` wrapper at its first `pr-merge` call.
- **GREEN:** `bash tests/validation/test_run_ci_precommit.sh` printed `PASS:
  CI pre-commit wrapper contract`; shellcheck reported nothing.
- **Real hooks:** in a scratch repository with this repository's
  `.pre-commit-config.yaml`, a staged `x.toml` holding `a = 1` plus three
  trailing spaces made the new wrapper exit 1 in `local-staged` and the `main`
  wrapper exit 0. The staged bytes were unchanged afterwards.

### W9 LAB Isolation Test (F31)

`test_each_lab_guide_names_exactly_its_project_and_services` read Project and
Services rows from `0029-supabase.md` through `LAB_GUIDE_PATHS`. That guide
binds `labs/supabase.yml` through `implementation_services`, which the
operations catalog already checks in both directions:
`operations_catalog.py` `_inventory_bindings` reports a bound name the Compose
file lacks (`service-operations-removed`) and a declared LAB service no guide
binds (`service-operations-missing`). The test now skips any LAB a Stage 05
guide binds and keeps the README rows of the other eight LABs, which are
current. The guide's rows stay as reader documentation.

- **RED:** with the guide's Project and Services rows deleted, the old test
  failed (`guide lacks a Project row`, lab `supabase.yml`).
- **GREEN:** with the same deletion it passes; the rows were restored.
- **Catalog:** `test_bound_lab_source_requires_every_declared_service_owner`
  already shows an unbound service in a bound LAB failing with
  `service-operations-missing`, so no new catalog test was added; it is a
  characterization of existing behaviour, not a RED.
- `test_lab_isolation` and `test_operations_catalog` ran 140 tests, OK. PR
  #428's local aggregate FAIL listed two LAB document and README failures that
  reproduced on `main`; this duplicate dependency was one source of that
  class.

### W10 Finding Records

The prompt's D-P0 to D-P5 order applies only to this repository. Per finding:

- **F01.** Asked that the source hash and the 333 non-blank lines bind to the
  four targets, and that work continue from current state without resetting
  to an old SHA. The v9 prompt file given to this session has SHA-256
  `79dd3930a64dd65cf81755685ca3e46db6d8f603592d401910e7ddbb28143b09`, 911
  lines and 666 non-blank lines. The 333-line count belongs to the v8
  attachment, which is not in this repository, so that binding is NOT_RUN.
  Every change here started from the then-current `main` and nothing was
  reset.
- **F19.** Asked to keep candidate quality, main security and the release
  workflow separate and not to count `--requirements` as a second QA run.
  Satisfied: `ci-quality.yml:18-19` runs `candidate-quality` on pull requests
  only, `:44` runs `--requirements` to select prerequisites and `:54` runs
  the gate; `main-security` is separate at `:56-57`; and
  `generate-changelog.yml:1,39` publishes the release.
- **F28.** Asked that one sufficient run may serve several criteria, with
  claim, input, method, result, failure and follow-up linked, and that static
  checks never stand in for live ones. Satisfied: the Task template's
  Evidence row has a plural Criteria cell and `Resolves`
  (`task.template.md:19,39`), SPEC-0231 split Evidence from Criterion
  Acceptance, and `quality-standards.md:244` calls source-only evidence
  insufficient for runtime settings.
- **F29.** Asked not to force the four Registries' `schema_version` values to
  match. Satisfied here: `docs/99.templates/registry.json:2` holds `1` and no
  test compares it with another repository. The cross-repository comparison
  is outside this repository.
- **F38.** Asked to record merge, candidate, local aggregate and service
  acceptance separately. PR #428 merged as `62556dc63b66c828c27e9c33017d26cdf70b8542`
  at 2026-10-12T16:14:06Z. Run 38275029067 (`CI Quality Gates`,
  `pull_request`, head `c402f165140fa9c63dc3710ffc2c20eb7f312ce6`) concluded
  success with `candidate-quality` success and `main-security` skipped, read
  with `gh` on 2026-10-13. The PR body records the local-only aggregate as
  FAIL (exit 1), and SEC01 security and HOME acceptance as not accepted;
  those results stay separate and none of them is replaced by the hosted
  success.
- **F41.** Asked that the Task stay the single progress record, that only
  affected checks run at the end, and that other writers' worktrees and
  memory are never deleted automatically. Satisfied: `agentic.md:113-114`
  forbids inferring a review from a label, `:125-127` keeps execution and
  acceptance in the Task, and `approval-boundaries.md:88-93` limits deletion
  to scratch with proven ownership. This session removed only its own merged,
  clean worktrees and left the other writers' `codex/*` worktrees.

### Owner Decisions

On 2026-10-13 the owner answered the review question by accepting the
criteria rated ready and approving this Spec and Plan; Review and Completion
lists the criteria and why the rest stay `pending`.

Later on 2026-10-13 the owner wrote "Prompt findings not done or only partly
done 검토후 진행" and "Not all work is done 검토후 진행". Because the prompt
says to reuse existing Specs, that instruction extends this approved Spec and
Plan (1.1.0) with W8 to W10 and criteria 8 to 10; the new criteria start
`pending`.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0232 | draft | approved | #owner-decisions |
| SPEC-0232-PLAN-0001 | draft | approved | #owner-decisions |
| SPEC-0232-TSK-0001 | draft | ready | #current-readiness-review-on-2026-10-22 |
| SPEC-0232-TSK-0001 | ready | in-progress | #current-lifecycle-reconciliation-on-2026-10-22 |
| SPEC-0232-TSK-0001 | in-progress | completed | #current-completion-decision-on-2026-10-22 |

### Direct Push and Review — 2026-10-13

W8 to W10 (`273871804`, `5e4689a2c`, `e42655ef8`) reached `main` at
2026-10-13T12:10:11Z by a direct push of the merge `5a93ea054` ("Merge branch
'main' ... into claude/v9-residual-closure"), without a pull request. The
worktree's reflog shows `pull --tags origin main`, the form VS Code Source
Control sync uses, on a branch that tracked `origin/main`. The pusher is not
identified; neither this session
nor its forked workers issued that pull or push. The owner chose on
2026-10-13 to keep the commits and review and verify them afterwards, and to
create every later branch with `--no-track` and push with an explicit refspec.

- Hosted push runs on `5a93ea054`: CI Quality Gates 38395326780 and Push on
  main 38395326315, both success. `leaf.changed-style` runs only in the PR
  candidate, so these runs do not exercise the wrapper.
- An independent `ci-cd-engineer` review of `40f194e99..5a93ea054` approved
  with notes. It ran the wrapper test (PASS) and the LAB isolation tests (12,
  OK) in a scratch worktree, and real pre-commit 4.6.2 on a staged file with
  trailing whitespace and no final newline: the isolated copy was fixed, the
  wrapper exited non-zero, and the source index and worktree were unchanged.
  Its notes were applied in `quality-standards.md`: the `pr-merge` bullet now
  says hooks run on an isolated copy, and the Validation bullet no longer
  claims every hook has a check mode. Its remaining notes stay open: the
  test's hook-ID comparison is a loose `grep`, it runs no real fixer, and
  `pr-merge` index preservation is tested only through the stand-in.

### Current readiness review on 2026-10-22

The owner's current request explicitly authorizes status and lifecycle processing
for implemented work. This is a new reconciliation on 2026-10-22; it does not
backdate execution or replace the historical acceptance decisions. The review
used input `bd4168e20861d557c9a4f31025a2a649be3e8066` and the existing public
Task receipts. Both parents are already `approved`. All 10 assigned
criterion/Work Unit pairs have this Task's PASS evidence, all 10 owned
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

The historical candidate, replay and dated native observations retain their
original scope; completion does not certify fresh provider delivery.

Spec and Plan remain `approved`. Archive readiness is derived by the existing
reader after completion; no archive move, withdrawal or operational action is
part of this Task closure. The final documentation gates are recorded by the
current coordination Task.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hook | 1 | W1 | New check-mode test RED on `main` then GREEN; dispatcher test; routing suite (61) | Branch | PASS | W1 Validate-only Hook | - |
| Rehearsal | 2 | W2 | Bundle tests (7, 2 skipped); update-gate and SEC01 routing tests (31) | Branch | PASS | W2 n8n Candidate Rehearsal | - |
| Frozen | 3 | W3 | Registry assertion; anchor mutation shows 149 disagreements | Branch | PASS | W3 Frozen Payload Registry Assertion | - |
| Shim | 4 | W4 | Governance contract (failures=0) | Branch | PASS | W4 Root Shim | - |
| Gate | 5 | W5 | Local changed gate; stopped at its 3600 s limit in the governance suite | `cc8a880dc` | NOT_RUN | W5 Gate | - |
| Tombstone | 6 | W6 | `test_archive` RED (3 failures) then GREEN (71); corpus lifecycle; archive recovery; recovery tests | Branch on `7325f1af2` | PASS | W6 Tombstone Identity | - |
| Context | 7 | W7 | Dispatcher test RED on `main` (exit 1, no JSON) then GREEN; post_tool tests (15) | Branch on `b1a6976f4` | PASS | W7 PostToolUse Failure as Context | - |
| Candidate | 5 | W5 | Hosted `candidate-quality`, changed profile | PR #443 at `cc8a880dc` | PASS | W5 Gate | - |
| Context candidate | 7 | W7 | Hosted `candidate-quality`, run 38374565260 | PR #446 | PASS | W7 PostToolUse Failure as Context | - |
| Live Claude | 7 | W7 | Live PostToolUse delivery, Claude Code 2.1.296 | `958349408` | PASS | W7 PostToolUse Failure as Context | - |
| Live Codex | 7 | W7 | Live PostToolUse delivery, codex-cli 0.162.1, sandbox off | `958349408` | PASS | W7 PostToolUse Failure as Context | - |
| Governance suite | 5 | W5 | Full document governance suite, 893 of 894 passed | `b1a6976f4` | FAIL | Governance Suite | - |
| Gate replay | 5 | W5 | Local changed gate replay of the #443 diff on its parent with the SPEC-0235 changes and `61f3b99ef`: exit 0, 2998 s | `baffae4c7` to `8a3155daa` | PASS | W5 Gate | Governance suite |
| Wrapper | 8 | W8 | Wrapper test RED on `main` then GREEN; shellcheck; real `pre-commit` TOML whitespace case (new exit 1, `main` exit 0) | Branch on `ec0877f10` | PASS | W8 Pre-commit Wrapper (F22) | - |
| LAB guide | 9 | W9 | Old test RED with the guide rows deleted, GREEN after; `test_lab_isolation` and `test_operations_catalog` (140) | Branch on `ec0877f10` | PASS | W9 LAB Isolation Test (F31) | - |
| Finding records | 10 | W10 | Per-finding records with file:line evidence; PR #428 and run 38275029067 read with `gh` | Branch on `ec0877f10` | PASS | W10 Finding Records | - |
| Wrapper review | 8 | W8 | Independent `ci-cd-engineer` review: approve with notes; wrapper test PASS, LAB isolation (12) OK, real pre-commit fixer case kept source bytes | `5a93ea054` | PASS | Direct Push and Review — 2026-10-13 | - |
| Policy review | 8 | W8 | Independent `rules-engineer` review of the `quality-standards.md` wording and this record: pass, notes applied | `claude/v9-residual-followup` | PASS | Direct Push and Review — 2026-10-13 | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Hook | Owner accepted 2026-10-13 |
| 2 | accepted | Rehearsal | Owner accepted 2026-10-13 |
| 3 | accepted | Frozen | Owner accepted 2026-10-13 |
| 4 | accepted | Shim | Owner accepted 2026-10-13 |
| 5 | accepted | Candidate, Gate replay | Owner rule 2026-10-14: replay counts, accept on pass |
| 6 | accepted | Tombstone | Owner accepted 2026-10-13 |
| 7 | accepted | Context, Context candidate, Live Claude, Live Codex | Owner accepted 2026-10-13 |
| 8 | accepted | Wrapper, Wrapper review, Policy review | Owner accepted 2026-10-14 |
| 9 | accepted | LAB guide | Owner accepted 2026-10-14 |
| 10 | accepted | Finding records | Owner accepted 2026-10-14 |

## Review and Completion

On 2026-10-13 the owner, answering the review question, accepted the criteria
rated ready (criteria 1, 2, 3, 4, 6, 7) and approved this Spec and Plan.
Criteria 8, 9 and 10 were not asked then; on 2026-10-14 the owner accepted
all three.
Criterion 5, the gate, was `pending`: its local changed gate had no PASS,
and the governance suite FAIL was unresolved. On 2026-10-14 the owner
answered (AskUserQuestion) that a replay through the local changed gate
counts and that the criterion is accepted if it passes, and confirmed that
rule again after the base gained `61f3b99ef`. The W5 replay passed, so
criterion 5 is accepted.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
