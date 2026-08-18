---
layer: agentic
status: active
---

# Stop Gate Blocks Governance-Mandated Dirty Paths

- Date: 2026-08-12
- Layer: agentic
- Status: resolved
- Applies To: `scripts/hooks/agent-event-hook.sh` logical-commit Stop gate; resolved at `9bd40c1c`
- Tags: hooks, stop-gate, false-positive, handoff
- Retrieval Keywords: AGENT_ALLOW_UNCOMMITTED_STOP, logical_commit_stop_gate, uncommitted task-owned changes, stop hook loop
- Last Verified: 2026-08-12

## Problem

The logical-commit Stop gate blocks completion whenever the working tree is
dirty, including for paths that active governance explicitly forbids the
current unit from staging, editing, or reverting. Its message instructs the
agent to "stage only task-owned files or hunks", but the implementation has no
concept of task ownership, so a correctly bounded unit cannot satisfy it.

## Context

`scripts/hooks/agent-event-hook.sh` collects every `git status --porcelain=v1`
entry with no allowlist, ownership filter, or exception mechanism. The only
exits are a fully clean working tree or `AGENT_ALLOW_UNCOMMITTED_STOP=1` in the
hook process environment. The `stop_hook_active` escape is Claude-unreachable
because it is guarded by `HOOK_PROVIDER == "codex"`.

The agent cannot supply the override for a single stop attempt: Bash tool shell
state does not persist, and the hook runs as a separate process. Writing the
variable into `.claude/settings.local.json` would disable the team gate for
every future stop, which `providers/claude.md` prohibits. So the documented
mitigation is unreachable without user intervention.

This surfaced during the Task 0f.2 native-publisher unit, where
`scripts/validation/agentic-research-gate9-evidence.py` and
`tests/validation/test_agentic_research_gate9_evidence.py` must stay dirty and
byte-preserved until the reviewed Task 0f.3 unit adopts them.

## Resolution

Resolved by the user-approved harness unit at `9bd40c1c`. The gate now reads a
tracked declaration registry at
`docs/00.agent-governance/contracts/deferred-paths.yaml`, skips exactly the
declared paths, and keeps blocking every other uncommitted path. The two Step
0e evidence-helper paths are registered there with their reason and owning
Task, so the correctly bounded unit can complete without committing,
reverting, or stashing bytes it does not own.

## Prevention

The registry fails closed by design. A missing, untracked, unreadable, or
malformed registry grants no exemption; an entry without a non-empty reason or
an `owning_task` that resolves to an existing file is ignored; and a missing
PyYAML import yields no exemptions instead of an error. Requiring the registry
to be tracked keeps exempting a path a committed, reviewable act rather than a
local edit. Remove each entry as soon as its owning unit adopts the path, and
keep `tests/validation/test_stop_gate_deferred_paths.py` covering the
undeclared, incomplete, missing-task, malformed, and untracked cases so a
future change cannot silently widen the exemption.

## Evidence

- Gate collection and override branch: `scripts/hooks/agent-event-hook.sh`
  `logical_commit_stop_gate`
- Documented mitigation with reason requirement:
  `docs/04.execution/plans/2026-05-22-agent-hook-completion-style-automation.md`
- Registry and gate tests: `docs/00.agent-governance/contracts/deferred-paths.yaml`,
  `tests/validation/test_stop_gate_deferred_paths.py`
- Deferral rationale and preserved provenance digests:
  `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`

## Related Documents

- [Governance memory README](./README.md)
- [Claude provider overlay](../providers/claude.md)
- [Agent bootstrap governance](../rules/bootstrap.md)
- [Rebuild Task](../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
