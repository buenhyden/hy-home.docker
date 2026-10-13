---
title: "Prompt v9 Residual Corrections Task"
version: "0.3.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0232-TSK-0001"
parent_ids:
- "SPEC-0232-PLAN-0001"
created: "2026-10-13"
---

# Prompt v9 Residual Corrections Task

## Objective

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

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |
| 7 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
