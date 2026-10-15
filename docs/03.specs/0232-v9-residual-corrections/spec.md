---
title: "Prompt v9 Residual Corrections"
version: "1.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0232"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-10-13"
---

# Prompt v9 Residual Corrections

## Overview

After SPEC-0230 and SPEC-0231 a read-only check of the remaining prompt v9
findings on `main` `baffae4c7` found four that still hold:

- F26: `scripts/hooks/agent-event-hook.sh` runs
  `post-tool-validate.sh --write` after every edit, so the hook rewrites
  files the agent did not ask it to change.
- F20: `tests/validation/test_workflow_version_bundle.py` still pins the n8n
  2.42.6 candidate images beside the 2.42.7 bundle it checks.
- F22: the frozen archive payload anchor in `.pre-commit-config.yaml` is
  compared with the markdownlint ignore list but not with the Registry that
  declares what is frozen.
- F02: root `AGENTS.md` repeats bootstrap step 3 and the Codex adapter.

The same request asks to correct existing QA. On `main`
`test_tombstone_identity_inherits_the_retired_artifact_id` fails three
subtests: `6056788a5` moved its role-layout inputs under a numbered
classification directory, and `tombstone_identity` still matches only the
flat layout, so those paths take the tombstone number instead of their own.

F18 (non-gating workflows) and F42 (skill adapter routes) no longer hold. On
2026-10-13 the owner chose a validate-only hook, kept the Stop hook's
whole-worktree scope, and moved the shared memory work (F24, F27, F36) to a
later Spec.

## Scope

In scope: the PostToolUse dispatcher call, the check mode of
`post-tool-validate.sh`, the policy and README text describing them; the n8n
candidate rehearsal; one Registry assertion in the frozen payload test; root
`AGENTS.md`; how the dispatcher returns a PostToolUse failure; the role-layout pattern in `tombstone_identity`; and, added on 2026-10-13, the
read-only pre-commit wrapper (F22), the LAB isolation test's duplicate guide
dependency (F31), and the per-finding record of F01, F19, F28, F29, F38 and
F41. Out of scope: the Stop hook, shared memory, historical SEC01
receipts and README records, the Airflow candidate rehearsal.

## Contracts

1. The PostToolUse hook runs `post-tool-validate.sh --check` and never
   rewrites a file. Check mode reports a changed Markdown, shell, YAML or
   JSON file that `--write` would normalize, tracked or not, and leaves its
   bytes unchanged. `--write` stays an explicit fix command and still changes
   bytes only where the registered owner would.
2. No repository test pins a candidate image built for a version other than
   the current bundle. The current n8n bundle regression is unchanged.
3. The frozen payload anchor selects exactly the tracked archive files under
   an unmanaged archive record profile or on a `frozen-legacy-status` path.
4. `AGENTS.md` keeps exactly its three entry steps and adds nothing beyond
   them.
5. A PostToolUse validation failure reaches the model: the dispatcher exits 0
   and prints the report as `hookSpecificOutput.additionalContext`.
6. A retired Stage 05 guide, policy or runbook inherits the artifact number
   in its filename whether it sat directly in its family directory or in a
   numbered classification directory under it.
7. `run-ci-precommit.sh` keeps every hook from the source configuration in
   its read-only copy, and in both modes a hook that changes the isolated
   candidate fails the run: as its own failure when it fails, as a hidden
   mutator when it passes.
8. The LAB isolation test reads Project and Services rows only for LABs that
   no Stage 05 guide binds through `implementation_services`; the operations
   catalog owns the bound ones.
9. The Task records, per finding, what F01, F19, F28, F29, F38 and F41 asked,
   the current evidence and the outcome.

## Acceptance Criteria

1. A test shows check mode failing on an untracked file with trailing
   whitespace or no final newline without changing it, and the dispatcher
   passing `--check`; governance text matches.
2. The bundle test pins no n8n 2.42.6 image and its current-bundle tests pass.
3. The frozen payload test fails when the anchor and the Registry disagree.
4. `AGENTS.md` has three steps and the governance contract passes.
5. The changed gate and `candidate-quality` pass.
6. The tombstone identity test passes and archive recovery reports no
   violation.
7. A test shows a whitespace defect producing exit 0 and the context JSON,
   and a clean file producing no output.
8. The wrapper test fails on `main` and passes after the change, and a real
   `pre-commit` run fails a staged TOML file with trailing whitespace that
   `main` passes.
9. The LAB isolation test passes with the Supabase guide's Project and
   Services rows removed, and the catalog test for an unbound LAB service
   passes.
10. Each of the six findings has a record with evidence and an outcome.

## Failure Conditions

PostToolUse validation fails on normalization defects while preserving
bytes and returning the failure context to the model. A pre-commit hook that
mutates the isolated candidate fails even if it exits successfully;
classified tombstone identity and guide-bound LAB ownership must retain
their canonical consumers rather than duplicate them.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-v9-residual-corrections.md)
