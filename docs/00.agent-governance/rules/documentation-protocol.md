---
layer: agentic
---

# Documentation Protocol

Protocol for maintaining documentation consistency and governance traceability.

## 1. Context and Objective

- Preserve stage-gate integrity.
- Keep documentation synchronized with implementation state.
- Enforce language, template, and traceability standards.

## 2. Requirements and Constraints

- Use templates from `docs/99.templates/` for new stage documents.
- Use only relative links; never use absolute `file://` links.
- Keep `docs/00.agent-governance/` English-only.
- Keep human-facing docs in Korean unless interoperability requires English terms.
- `docs/01` to `docs/99` are read-only by default; modify only with explicit user approval.

## 3. Authoring Protocol

1. Identify target stage.
2. Load `rules/stage-authoring-matrix.md` and follow its stage row.
3. Draft or update using the mapped template and required input documents.
4. Cross-link related PRD, ARD, ADR, Spec, Plan, Task, Guide, Operation, and Runbook files.
5. Run checklist gates from `rules/task-checklists.md`.

## 4. Operational Procedures

Trigger documentation updates when:

- service topology changes,
- commands/workflows change,
- module ownership/scope changes,
- policy and repository reality diverge.

For completion, ensure affected README files and governance pointers remain accurate.

## 5. Maintenance and Safety

- Remove obsolete instructions quickly in editable scope.
- If breakages are found in read-only stages (`docs/01` to `docs/99`), log them in `docs/00.agent-governance/memory/` with recommended fixes.
- Keep policy wording concise, explicit, and conflict-free.

## 6. DOCS 3 RULES — HALT CONDITIONS

These rules are blocking. Completion is **PROHIBITED** until all three pass.

**R1 — Template First:**
Read the matching template from `docs/99.templates/` → fill every section → set `status: draft`.
Infrastructure triggers: new service → ARD first; network change → ADR first; production procedure → OPER first.

**R2 — README Sync:**
Any folder-level change (file added, moved, or removed) → the parent `README.md` MUST be updated.
Agent is **BLOCKED** from marking task complete until this is done.

**R3 — Related Documents:**
Every document MUST contain a `## Related Documents` section with upstream links.
A document without this section is **INCOMPLETE** regardless of content quality.
