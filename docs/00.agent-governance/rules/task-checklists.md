---
layer: agentic
---

# Task Checklists

Unified task execution checklists for all agent work.

## 1. Pre-Task Checklist

- [ ] Confirm active persona, layer, and primary scope.
- [ ] Confirm editable scope for this task.
- [ ] Confirm whether `docs/01` to `docs/99` are in read-only mode.
- [ ] Identify required input documents (PRD, ARD, ADR, Specs, Plans, Tasks).
- [ ] Identify key risks (security, data loss, breaking changes, governance drift).
- [ ] Define verification commands and acceptance criteria before edits.

## 2. In-Task Checklist

- [ ] Keep changes within declared editable scope.
- [ ] Preserve SSoT traceability across affected documentation artifacts.
- [ ] Maintain language policy consistency (English governance, Korean human-facing docs).
- [ ] Validate new/changed links as edits are made.
- [ ] Remove stale, conflicting, or nonexistent references in editable scope.
- [ ] Record out-of-scope issues instead of patching read-only stages.

## 3. Completion Checklist

- [ ] Run relevant repository checks for changed layers.
- [ ] Validate link integrity for changed root/governance files.
- [ ] Confirm no contradictory policy statements were introduced.
- [ ] Confirm completion criteria are satisfied for the affected stage(s).
- [ ] Create/update out-of-scope issue report in `docs/00.agent-governance/memory/` when needed.
- [ ] Summarize what changed, what was verified, and what remains out-of-scope.
