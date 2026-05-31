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

- Use templates from `docs/99.templates/` for every new or modified target-stage
  document under `docs/01.requirements/`, `docs/02.architecture/`,
  `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and
  `docs/90.references/`.
- Use only relative links; never use absolute `file://` links.
- Keep `docs/00.agent-governance/` English-only.
- Keep human-facing docs in Korean unless interoperability requires English terms.
- `docs/01` to `docs/99` are read-only by default; modify only with explicit user approval.
- Active stage artifacts may exist only under canonical stage paths (`docs/01` to `docs/05`, `docs/90`, `docs/99`).
- Non-stage `docs/*` paths such as `docs/superpowers/` must not contain active specs or plans.
- `README.md` files and root instruction shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) are documentation surfaces for DOCS 3 unless a higher-priority runtime constraint explicitly exempts them.
- Root instruction shims must remain thin; their `## Related Documents` sections should point to canonical governance and provider docs instead of duplicating policy.
- **Template frontmatter exemption**: Template source files under `docs/99.templates/*.template.md` use `status: draft` in YAML frontmatter instead of `layer:`. This is intentional. Agents performing `layer:` compliance audits must exempt those template source files from that check. `docs/99.templates/README.md` is an active folder README and may use repository README frontmatter such as `layer: agentic`. `memory.template.md` and `progress.template.md` are governance-memory templates, but they still keep this template frontmatter shape until copied into active governance memory files.
- **Frontmatter status (R5):** Every leaf document under `docs/01`–`docs/05`
  and `docs/90` MUST include YAML frontmatter with `status: draft | active | superseded`.
  Governance memory files (`docs/00.agent-governance/`) use `layer:`
  frontmatter instead. Template source files (`docs/99.templates/*.template.md`)
  always use `status: draft` and are exempt from the `layer:` requirement.
  A document without this frontmatter is **INCOMPLETE**.

## 3. Document Type ↔ Template Mapping

| Stage/Folder                                          | Document Type          | Template                                     |
| ----------------------------------------------------- | ---------------------- | -------------------------------------------- |
| `docs/01.requirements/`                               | PRD                    | `docs/99.templates/prd.template.md`          |
| `docs/02.architecture/requirements/`                  | ARD                    | `docs/99.templates/ard.template.md`          |
| `docs/02.architecture/decisions/`                     | ADR                    | `docs/99.templates/adr.template.md`          |
| `docs/03.specs/`                                      | Spec                   | `docs/99.templates/spec.template.md`         |
| `docs/03.specs/<feature-id>/api-spec.md`              | API Spec               | `docs/99.templates/api-spec.template.md`     |
| `docs/03.specs/<feature-id>/agent-design.md`          | Agent Design           | `docs/99.templates/agent-design.template.md` |
| `docs/03.specs/<feature-id>/data-model.md`            | Data Model             | `docs/99.templates/data-model.template.md`   |
| `docs/03.specs/<feature-id>/tests.md`                 | Test Contract          | `docs/99.templates/tests.template.md`        |
| `docs/03.specs/<feature-id>/contracts/openapi.yaml`   | OpenAPI Contract       | `docs/99.templates/openapi.template.yaml`    |
| `docs/03.specs/<feature-id>/contracts/schema.graphql` | GraphQL Contract       | `docs/99.templates/schema.template.graphql`  |
| `docs/03.specs/<feature-id>/contracts/service.proto`  | Protobuf Contract      | `docs/99.templates/service.template.proto`   |
| `docs/04.execution/plans/`                            | Plan                   | `docs/99.templates/plan.template.md`         |
| `docs/04.execution/tasks/`                            | Task                   | `docs/99.templates/task.template.md`         |
| `docs/05.operations/guides/`                          | Operations Guide       | `docs/99.templates/guide.template.md`        |
| `docs/05.operations/policies/`                        | Operations Policy      | `docs/99.templates/policy.template.md`       |
| `docs/05.operations/runbooks/`                        | Operations Runbook     | `docs/99.templates/runbook.template.md`      |
| `docs/05.operations/incidents/YYYY/`                  | Incident               | `docs/99.templates/incident.template.md`     |
| `docs/05.operations/incidents/YYYY/`                  | Postmortem             | `docs/99.templates/postmortem.template.md`   |
| `docs/00.agent-governance/memory/<note>.md`           | Governance Memory Note | `docs/99.templates/memory.template.md`       |
| `docs/00.agent-governance/memory/progress.md`         | Agent Progress Log     | `docs/99.templates/progress.template.md`     |
| `docs/90.references/`                                 | Reference              | `docs/99.templates/reference.template.md`    |
| `README.md` (per folder)                              | README                 | `docs/99.templates/readme.template.md`       |

For optional supporting contracts under `docs/03.specs/<feature-id>/`, keep
Markdown support files in the feature directory and machine-readable contracts
under `contracts/`. Parent Markdown Spec or API Spec documents own the
cross-links for YAML, GraphQL, and Proto files.

See `docs/99.templates/README.md` for the full catalog and usage rules.

## 4. Authoring Protocol

1. Identify target stage.
2. Load `rules/stage-authoring-matrix.md` and follow its stage row.
3. Load the mapped template before drafting or updating the target document.
4. Preserve the template contract: required headings, target path guidance,
   target-relative links, and one `## Related Documents` section.
5. Remove all template placeholders before saving.
6. Cross-link related Requirements, Architecture, Spec, Plan, Task, Operations, Reference, and Incident files.
7. Run checklist gates from `rules/task-checklists.md`.

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
- **ADRs and ARDs**: use a four-digit zero-padded monotonically increasing sequence
  number: `NNNN-<short-title>.md`. This sequence is independent of tier prefixes.
- **ADR document H1 title format**: `# ADR-NNNN: English Short Title` — four-digit
  zero-padded number, colon, English-only title. Example:
  `# ADR-0003: HashiCorp Vault as Centralized Secrets Manager`.
- **ARD document H1 title format**: `# [Domain] Architecture Reference Document (ARD)` —
  must end with the `(ARD)` suffix. Example:
  `# Security Tier Architecture Reference Document (ARD)`.
- **Task document H1 title format**: `# Task: [Task Name]` — all task files under
  `docs/04.execution/tasks/` must use this prefix.
- **Operations policy required heading**: Use `## Policy Scope` (not `## Applies To`)
  as the audience and scope heading in all `docs/05.operations/policies/` documents.
- **Tier prefixes** (`01-gateway`, `02-auth`, …, `04-data`, `04-data-analytics`, `11-laboratory`):
  are two-digit service-tier identifiers used in `docs/03.specs/`, `docs/05.operations/`
  folder names, and PRD filename segments. `04-data` and `04-data-analytics` share the
  `04` prefix intentionally; analytics is a sub-tier of data. Do not rename a tier-prefix
  folder that already has active cross-links.
- Hardening/optimization PRDs reuse the original tier prefix with a new date:
  `YYYY-MM-DD-NN-<tier>-optimization-hardening.md`. The same tier number `NN` is
  intentional; the date and the `-optimization-hardening` suffix disambiguate.

## 8. DOCS 3 RULES — HALT CONDITIONS

These rules are blocking. Completion is **PROHIBITED** until all four pass.

**R1 — Template First:**
Read the matching template from `docs/99.templates/` before writing or editing
any target-stage document → keep required headings → fill every applicable
section → remove placeholders before completion.
Infrastructure triggers: new service → ARD first; network change → ADR first; production procedure → `05.operations` first.

**R2 — README Sync:**
Any folder-level change (file added, moved, removed, or **content-modified**) → the parent `README.md` MUST be updated to reflect the current state of the folder.
This applies when a document's title, status, scope, or summary-level content changes in a way that affects how the folder README describes that document.
Agent is **BLOCKED** from marking task complete until this is done.

**R3 — Related Documents:**
Every document MUST contain a `## Related Documents` section with upstream links.
A document without this section is **INCOMPLETE** regardless of content quality.

**R4 — Operations Profile Compliance (BLOCKING):**
Every non-README leaf document under `docs/05.operations/` MUST satisfy its
bucket's purpose-profile contract. Profile compliance is machine-verified by
`check-repo-contracts.sh` (section "Operations purpose profile contract").

- `guides/**` required: `## Usage` (enforced now); `## Common Checks`,
  `## Runbook Handoff` (Phase 4 script update will add enforcement).
  Forbidden in guides: `## Policy Scope`, `## Controls`, `## Exceptions`,
  `## Review Cadence`, `### When to Use`, `#### Procedure`.
- `policies/**` required: `## Policy Scope`, `## Controls`, `## Verification`,
  `## Review Cadence`. Forbidden in policies: `## Usage`, `## Runbook Handoff`,
  `### When to Use`, `#### Procedure`.
- `runbooks/**` required: `## When to Use`, `## Procedure`, `## Evidence`,
  `## Escalation`. Forbidden in runbooks: `## Usage`,
  `## Policy Scope`, `## Controls`, `## Exceptions`, `## Review Cadence`.
- `incidents/**` documents use `incident.template.md` (active incident record)
  or `postmortem.template.md` (post-incident review). Filename pattern:
  `YYYY-MM-DD-<incident-title>.md`.

A document violating R4 is **INCOMPLETE** regardless of content quality.
Completion is **PROHIBITED** until all profile checks pass.

## 8.5. Cross-Cutting Plans — Spec Link Exception

Plans under `docs/04.execution/plans/` that address cross-cutting concerns
(workspace audits, governance remediation, tooling lifecycle, agent harness work)
are **not required** to link a single parent Spec. They must instead reference the
governance document or operations artifact that scopes their work in
`## Related Documents`.

Tier-specific implementation plans (one plan ↔ one tier) **must** link the
corresponding Spec in `## Related Documents`:
`../../03.specs/<tier-id>/spec.md`.

## 9. Known Architecture Sequence Gaps

The following sequence numbers are reserved or were intentionally skipped.
Agents must not auto-assign these numbers without confirming with this table.

| Range     | Location                             | Reason                  |
| --------- | ------------------------------------ | ----------------------- |
| 0012–0014 | `docs/02.architecture/decisions/`    | Reserved / legacy merge |
| 0015–0017 | `docs/02.architecture/requirements/` | Reserved / legacy merge |

Update this table when a number is consumed or definitively retired.

## Related Documents

- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/scopes/docs.md`
- `docs/99.templates/README.md`
