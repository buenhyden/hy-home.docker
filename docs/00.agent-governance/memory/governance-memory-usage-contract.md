---
layer: agentic
---

# Memory: governance-memory-usage-contract

- Date: 2026-05-10
- Layer: agentic
- Status: superseded
- Applies To: `docs/00.agent-governance/memory/`, bootstrap, task checklists, repository validators
- Tags: #governance #memory #agentic
- Retrieval Keywords: governance memory, advisory memory, memory template, progress.md, progress template, out-of-scope findings, repeated failures, memory contract
- Last Verified: 2026-07-26

## Problem

This historical finding recorded the first repository memory workflow. Its
active-work-log assumptions are superseded by the bounded current-memory
contract and durable Stage 04 Task evidence.

## Context

`docs/00.agent-governance/memory/` remains advisory. The current replacement is
defined by [`README.md`](./README.md), [`current.md`](./current.md), and the
applicable Stage 04 Task; memory cannot override rules, scopes, provider
overlays, direct user instructions, or live repository evidence.

## Resolution

This finding is retained only for provenance. The replacement contract is:

- Review `memory/README.md` and `memory/current.md` for the bounded active
  handoff.
- Retrieve only relevant durable notes with targeted search and corroborate
  them against live evidence.
- Record progress, verification, final evidence, and durable links in the
  applicable Stage 04 Task.
- Refresh `current.md` in place after verified-state changes.
- Treat `progress.md` only as append-preserved historical navigation.
- Create durable out-of-scope or repeated-failure notes from
  `docs/99.templates/templates/governance/memory.template.md`.

## Prevention

Do not reactivate this finding as policy. Keep active policy in `rules/`,
`scopes/`, provider overlays, root shims, and runtime files. Use the replacement
links above, preserve `progress.md` as historical navigation, and validate
current memory through the Stage 00 repository contract.

## Evidence

- `AGENTS.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/memory/current.md`
- `docs/04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md`
- `docs/99.templates/templates/governance/memory.template.md`
- `docs/99.templates/templates/governance/progress.template.md`
- `scripts/validation/check-repo-contracts.sh`

## Related Documents

- `README.md`
- `current.md`
- `progress.md`
