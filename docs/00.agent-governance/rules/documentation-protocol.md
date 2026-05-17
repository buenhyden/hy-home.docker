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
- Active stage artifacts may exist only under canonical stage paths (`docs/01` to `docs/05`, `docs/90`, `docs/99`).
- Non-stage `docs/*` paths such as `docs/superpowers/` must not contain active specs or plans.
- `README.md` files and root instruction shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) are documentation surfaces for DOCS 3 unless a higher-priority runtime constraint explicitly exempts them.
- Root instruction shims must remain thin; their `## Related Documents` sections should point to canonical governance and provider docs instead of duplicating policy.
- **Template frontmatter exemption**: Files under `docs/99.templates/` use `status: draft` in YAML frontmatter instead of `layer:`. This is intentional. Agents performing `layer:` compliance audits must exempt all `docs/99.templates/*.md` files from that check. `memory.template.md` and `progress.template.md` are governance-memory templates, but they still keep this template frontmatter shape until copied into active governance memory files.

## 3. Document Type ↔ Template Mapping

| Stage/Folder                                  | Document Type          | Template                                     |
| --------------------------------------------- | ---------------------- | -------------------------------------------- |
| `docs/01.requirements/`                       | PRD                    | `docs/99.templates/prd.template.md`          |
| `docs/02.architecture/requirements/`          | ARD                    | `docs/99.templates/ard.template.md`          |
| `docs/02.architecture/decisions/`             | ADR                    | `docs/99.templates/adr.template.md`          |
| `docs/03.specs/`                              | Spec                   | `docs/99.templates/spec.template.md`         |
| `docs/03.specs/<feature-id>/api-spec.md`      | API Spec               | `docs/99.templates/api-spec.template.md`     |
| `docs/03.specs/<feature-id>/agent-design.md`  | Agent Design           | `docs/99.templates/agent-design.template.md` |
| `docs/04.execution/plans/`                    | Plan                   | `docs/99.templates/plan.template.md`         |
| `docs/04.execution/tasks/`                    | Task                   | `docs/99.templates/task.template.md`         |
| `docs/05.operations/`                         | Operations Knowledge   | `docs/99.templates/operation.template.md`    |
| `docs/05.operations/incidents/`               | Incident               | `docs/99.templates/incident.template.md`     |
| `docs/05.operations/incidents/`               | Postmortem             | `docs/99.templates/postmortem.template.md`   |
| `docs/00.agent-governance/memory/<note>.md`   | Governance Memory Note | `docs/99.templates/memory.template.md`       |
| `docs/00.agent-governance/memory/progress.md` | Agent Progress Log     | `docs/99.templates/progress.template.md`     |
| `docs/90.references/`                         | Reference              | `docs/99.templates/reference.template.md`    |
| `README.md` (per folder)                      | README                 | `docs/99.templates/readme.template.md`       |

For supporting contracts under `docs/03.specs/<feature-id>/`, use:

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
4. Cross-link related Requirements, Architecture, Spec, Plan, Task, Operations, Reference, and Incident files.
5. Run checklist gates from `rules/task-checklists.md`.

For `docs/90.references/`, verify that the document is stable reference context, contains source-backed facts, and does not define active policy, runtime truth, runbook procedure, plan, task evidence, or incident timeline.

## 5. Operational Procedures

Trigger documentation updates when:

- service topology changes,
- commands/workflows change,
- module ownership/scope changes,
- policy and repository reality diverge.

For completion, ensure affected README files and governance pointers remain accurate.

When legacy active-stage content is discovered in a non-stage `docs/*` path:

1. Rewrite it into the canonical stage document using the mapped template.
2. Sync parent README files to the canonical path.
3. Remove the legacy file and directory once no active references remain.

## 6. Maintenance and Safety

- Remove obsolete instructions quickly in editable scope.
- If breakages are found in read-only stages (`docs/01` to `docs/99`), log them in `docs/00.agent-governance/memory/` with recommended fixes.
- Keep policy wording concise, explicit, and conflict-free.

## 7. File Naming Conventions

- **Dated artifacts** (plans, tasks, memory notes, ADRs, specs with a date component): prefix with `YYYY-MM-DD-<topic>`. Example: `2026-05-15-network-standardization.md`.
- **All filenames**: use kebab-case; no spaces, no underscores, no uppercase letters in the filename itself.
- **Templates**: use the pattern `<type>.template.<ext>`. Example: `memory.template.md`.
- **Stage documents without a date**: use a stable descriptive kebab-case name. Example: `spec.md`, `agent-design.md`.
- **READMEs**: always named exactly `README.md` (uppercase, no date prefix).
- Agents enforcing naming must not flag `README.md`, template files, or files that predate this rule unless they are being actively edited.

## 8. DOCS 3 RULES — HALT CONDITIONS

These rules are blocking. Completion is **PROHIBITED** until all three pass.

**R1 — Template First:**
Read the matching template from `docs/99.templates/` → fill every section → set `status: draft`.
Infrastructure triggers: new service → ARD first; network change → ADR first; production procedure → `05.operations` first.

**R2 — README Sync:**
Any folder-level change (file added, moved, or removed) → the parent `README.md` MUST be updated.
Agent is **BLOCKED** from marking task complete until this is done.

**R3 — Related Documents:**
Every document MUST contain a `## Related Documents` section with upstream links.
A document without this section is **INCOMPLETE** regardless of content quality.

## Related Documents

- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/scopes/docs.md`
- `docs/99.templates/README.md`
