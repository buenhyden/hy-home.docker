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
- [ ] Review `docs/00.agent-governance/memory/README.md` and `progress.md`; retrieve relevant memory notes when the task touches governance, docs, runtime, or repeated failures.
- [ ] Identify key risks (security, data loss, breaking changes, governance drift).
- [ ] Define verification commands and acceptance criteria before edits.

## 2. In-Task Checklist

- [ ] Keep changes within declared editable scope.
- [ ] Preserve SSoT traceability across affected documentation artifacts.
- [ ] Maintain language policy consistency (English governance, Korean human-facing docs).
- [ ] Validate new/changed links as edits are made.
- [ ] Remove stale, conflicting, or nonexistent references in editable scope.
- [ ] Update `docs/00.agent-governance/memory/progress.md` for material task progress.
- [ ] Record out-of-scope issues instead of patching read-only stages.

## 3. Completion Checklist

- [ ] Run relevant repository checks for changed layers.
- [ ] Validate link integrity for changed root/governance files.
- [ ] Confirm no contradictory policy statements were introduced.
- [ ] Confirm completion criteria are satisfied for the affected stage(s).
- [ ] Update `docs/00.agent-governance/memory/progress.md` with final status, verification evidence, and memory note links.
- [ ] Create/update out-of-scope or durable finding reports from `docs/99.templates/memory.template.md` when needed.
- [ ] Summarize what changed, what was verified, and what remains out-of-scope.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/persona.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
