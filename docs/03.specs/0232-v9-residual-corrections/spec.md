---
title: "Prompt v9 Residual Corrections"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
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

F18 (non-gating workflows) and F42 (skill adapter routes) no longer hold. On
2026-10-13 the owner chose a validate-only hook, kept the Stop hook's
whole-worktree scope, and moved the shared memory work (F24, F27, F36) to a
later Spec.

## Scope

In scope: the PostToolUse dispatcher call, the check mode of
`post-tool-validate.sh`, the policy and README text describing them; the n8n
candidate rehearsal; one Registry assertion in the frozen payload test; root
`AGENTS.md`. Out of scope: the Stop hook, shared memory, historical SEC01
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

## Acceptance Criteria

1. A test shows check mode failing on an untracked file with trailing
   whitespace or no final newline without changing it, and the dispatcher
   passing `--check`; governance text matches.
2. The bundle test pins no n8n 2.42.6 image and its current-bundle tests pass.
3. The frozen payload test fails when the anchor and the Registry disagree.
4. `AGENTS.md` has three steps and the governance contract passes.
5. The changed gate and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-v9-residual-corrections.md)
