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

## 3. Document Type ↔ Template Mapping

| Stage/Folder | Document Type | Template |
| --- | --- | --- |
| `docs/01.prd/` | PRD | `docs/99.templates/prd.template.md` |
| `docs/02.ard/` | ARD | `docs/99.templates/ard.template.md` |
| `docs/03.adr/` | ADR | `docs/99.templates/adr.template.md` |
| `docs/04.specs/` | Spec | `docs/99.templates/spec.template.md` |
| `docs/04.specs/<feature-id>/api-spec.md` | API Spec | `docs/99.templates/api-spec.template.md` |
| `docs/04.specs/<feature-id>/agent-design.md` | Agent Design | `docs/99.templates/agent-design.template.md` |
| `docs/05.plans/` | Plan | `docs/99.templates/plan.template.md` |
| `docs/06.tasks/` | Task | `docs/99.templates/task.template.md` |
| `docs/07.guides/` | Guide | `docs/99.templates/guide.template.md` |
| `docs/08.operations/` | Operation | `docs/99.templates/operation.template.md` |
| `docs/09.runbooks/` | Runbook | `docs/99.templates/runbook.template.md` |
| `docs/10.incidents/` | Incident | `docs/99.templates/incident.template.md` |
| `docs/11.postmortems/` | Postmortem | `docs/99.templates/postmortem.template.md` |
| `docs/90.references/` | Reference | `docs/99.templates/reference.template.md` |
| `README.md` (per folder) | README | `docs/99.templates/readme.template.md` |

For supporting contracts under `docs/04.specs/<feature-id>/`, use:

- `docs/99.templates/data-model.template.md`
- `docs/99.templates/tests.template.md`
- `docs/99.templates/openapi.template.yaml`
- `docs/99.templates/schema.template.graphql`
- `docs/99.templates/service.template.proto`

See `docs/99.templates/README.md` for the full catalog and usage rules.

## 4. Authoring Protocol

1. Identify target stage.
2. Load `rules/stage-authoring-matrix.md` and follow its stage row.
3. Draft or update using the mapped template and required input documents.
4. Cross-link related PRD, ARD, ADR, Spec, Plan, Task, Guide, Operation, and Runbook files.
5. Run checklist gates from `rules/task-checklists.md`.

## 5. Operational Procedures

Trigger documentation updates when:

- service topology changes,
- commands/workflows change,
- module ownership/scope changes,
- policy and repository reality diverge.

For completion, ensure affected README files and governance pointers remain accurate.

## 6. Maintenance and Safety

- Remove obsolete instructions quickly in editable scope.
- If breakages are found in read-only stages (`docs/01` to `docs/99`), log them in `docs/00.agent-governance/memory/` with recommended fixes.
- Keep policy wording concise, explicit, and conflict-free.

## 7. DOCS 3 RULES — HALT CONDITIONS

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
