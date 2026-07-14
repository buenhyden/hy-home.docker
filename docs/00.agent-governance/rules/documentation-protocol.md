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

- Select the target profile and mapped copyable template through the canonical
  Stage 99 registry and support contracts for every new or modified
  target-stage document under `docs/01.requirements/`,
  `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`,
  `docs/05.operations/`, `docs/90.references/`, and `docs/98.archive/`.
- Use only relative links; never use absolute `file://` links.
- Keep `docs/00.agent-governance/` English-only.
- Keep root `README.md` and human-facing folder READMEs Korean by default,
  while preserving commands, paths, service names, environment variables, stage
  names, and upstream terms exactly.
- Keep `docs/01.requirements/**` Korean by default for human-facing product
  intent and scope. Preserve technical identifiers and write formal acceptance
  criteria in the template's required structure.
- Keep `docs/02.architecture/**` mixed-audience: use Korean for explanatory
  rationale and human review context, while preserving English decision IDs,
  quality-attribute names, system terms, and required H1 title formats.
- Keep `docs/03.specs/**`, `docs/04.execution/plans/**`, and
  `docs/04.execution/tasks/**` English-only. These documents are technical
  contracts, implementation plans, and execution evidence for agents,
  reviewers, and CI checks.
- Keep `docs/05.operations/{guides,policies,runbooks,incidents,releases}/**`
  human-facing and Korean by default. Preserve code identifiers, service names,
  command names, environment variables, Docker profiles, secret IDs, evidence
  labels, and quoted upstream terms in their original form.
- In mixed-audience documents, keep policy, contracts, validation criteria,
  and machine-checkable instructions in English; use Korean only for
  human-facing usage context, operational explanation, or incident narrative.
- Keep `docs/90.references/**` audience-specific: generated LLM navigation,
  source-backed inventories, and machine-readable reference indexes may stay
  English; human learning/reference notes are Korean by default with quoted
  upstream terms preserved.
- Keep `docs/98.archive/**` as concise tombstone evidence. Use Korean for
  human-facing archive rationale unless the replacement/original artifact is an
  English-only contract; always preserve original paths, IDs, titles, and dates.
- Keep `docs/99.templates/**` aligned with the target folder language boundary.
  Template READMEs are human-facing and Korean by default; template source for
  English-only targets must not introduce Korean placeholders.
- PRD files under `docs/01.requirements/` use the canonical
  `NNN-feature-or-system.md` filename form.
- Spec folders under `docs/03.specs/` use the canonical `NNN-feature-id/`
  directory form; parent specs live at `docs/03.specs/NNN-feature-id/spec.md`.
- `docs/01` to `docs/99` are read-only by default; modify only with explicit user approval.
- Active stage artifacts may exist only under canonical stage paths (`docs/01` to `docs/05`, `docs/90`, `docs/99`). Archive tombstones live under `docs/98.archive` and are not active artifacts.
- Non-stage `docs/*` paths such as `docs/superpowers/` must not contain active specs or plans.
- `README.md` files and root instruction shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) are documentation surfaces for DOCS 3 unless a higher-priority runtime constraint explicitly exempts them.
- Root instruction shims must remain thin; their `## Related Documents` sections should point to canonical governance and provider docs instead of duplicating policy.
- **HADS reference profile**: HADS block structure is mandatory for non-README
  reference documents under `docs/90.references/data/hads/`. Outside that approved
  profile, HADS labels (`[SPEC]`, `[NOTE]`, `[BUG]`, `[?]`) remain optional
  unless a document type or approved plan explicitly requires them. Do not
  convert existing templates or active stage documents to HADS as incidental
  cleanup.
- **Template source metadata**: The Stage 99 registry owns each template
  source's exact metadata shape. Governance Memory and Progress template
  sources use exactly `layer: agentic` and `status: draft`; the README template
  source remains the registered status-only source; other typed template
  sources follow their registry-defined source metadata. The metadata checker
  validates registered placeholders without resolving them through the active
  artifact manifest, and copied targets must replace every placeholder.
  `docs/99.templates/README.md` is an active folder README and may use
  repository README frontmatter such as `layer: agentic`.
- **Frontmatter status (R5):** Every leaf document under `docs/01`–`docs/05`
  and `docs/90` MUST include YAML frontmatter with
  `status: draft | active | completed | superseded`.
  Archive tombstones under `docs/98.archive` MUST use `status: archived`.
  Governance memory files (`docs/00.agent-governance/`) use `layer:`
  frontmatter. Markdown template source metadata follows the Stage 99 registry:
  Governance Memory and Progress sources use exactly `layer: agentic` and
  `status: draft`, the README source is status-only, and other typed sources
  use their registered metadata shape.
  A document without this frontmatter is **INCOMPLETE**. Retired aliases such
  as `approved`, `done`, and `archived` must be normalized when found.
- **Typed metadata profiles (changed/new enforcement):**
  `docs/99.templates/support/document-metadata-profiles.yaml` is the
  machine-readable application-profile contract for stable identity, typed
  parents, supersession, review evidence, lifecycle transitions, and explicit
  README/generated/template/governance/archive exceptions. Task 7 inventory
  findings remain advisory for the full historical corpus. The approved
  agentic active chain is migrated, and `check-changed` blocks invalid new
  documents plus migrated or typed changed documents at pre-push. A changed
  legacy leaf outside the approved migration set is exempt only when it existed
  at the selected base, had no migration keys before or after the edit, and has
  no parser, forbidden-key, transition, or newly introduced typed-profile
  error. The checker validates the base record against a base manifest and
  requires every current legacy deficit's stable code/key-message identity to
  have existed at that base; disappearing deficits are allowed. New documents
  can never use this exception.

### 2.1 Registry-Driven Contract Selection

The
[document metadata registry](../../99.templates/support/document-metadata-profiles.yaml)
is the sole machine-readable owner for exact profiles, fields, value rules,
path matching, relations, serialization, lifecycle behavior, README consumers,
and exceptions. Stage 00 routes authors to that owner; it does not copy the
registry schema.

1. Resolve the intended target path and role, then require exactly one registry
   profile match. Zero matches, overlapping matches, an unsupported path, or an
   unclear role is blocking ambiguity; record the gap in Stage 04 and escalate
   instead of choosing the nearest profile.
2. Use the
   [SDLC document contract](../../99.templates/support/sdlc-document-contract.md)
   for lifecycle artifacts, the
   [common document contract](../../99.templates/support/common-document-contract.md)
   for repository/common artifacts, or the
   [README profile contract](../../99.templates/support/readme-profile-contract.md)
   for a `README.md`. These human contracts explain author intent while the
   registry and checker retain exact executable semantics.
3. Select the copyable template mapped by the resolved profile, instantiate it
   for the target path, replace every registered placeholder, and validate the
   result. Do not infer a template from a similar-looking document or copy
   machine-readable YAML, GraphQL, or Protobuf templates as Markdown.
4. For a README, select exactly one README profile before editing. Keep
   frontmatter absent by default and add or retain consumer-owned metadata only
   when the matched profile declares a real consumer; do not bulk-add or
   bulk-remove lifecycle fields by analogy.
5. Serialize frontmatter keys and `parent_ids` in the deterministic order owned
   by the registry and checker. Parent list position stabilizes presentation;
   it never assigns semantic priority. Record only evidence-backed direct
   parents and escalate ambiguity rather than inventing a relation.
6. When normalizing historical documents, preserve dated commands, counts,
   decisions, verdicts, timestamps, and execution results. Normalize only the
   approved metadata, section envelope, links, and current routing around that
   payload.

## 3. Document Type ↔ Template Mapping

| Stage/Folder                                          | Document Type          | Template                                     |
| ----------------------------------------------------- | ---------------------- | -------------------------------------------- |
| `docs/01.requirements/`                               | PRD                    | `docs/99.templates/templates/sdlc/prd.template.md`          |
| `docs/02.architecture/requirements/`                  | ARD                    | `docs/99.templates/templates/sdlc/ard.template.md`          |
| `docs/02.architecture/decisions/`                     | ADR                    | `docs/99.templates/templates/sdlc/adr.template.md`          |
| `docs/03.specs/`                                      | Spec                   | `docs/99.templates/templates/sdlc/spec.template.md`         |
| `docs/03.specs/NNN-feature-id/api-spec.md`              | API Spec               | `docs/99.templates/templates/spec-contracts/api-spec.template.md`     |
| `docs/03.specs/NNN-feature-id/agent-design.md`          | Agent Design           | `docs/99.templates/templates/spec-contracts/agent-design.template.md` |
| `docs/03.specs/NNN-feature-id/data-model.md`            | Data Model             | `docs/99.templates/templates/spec-contracts/data-model.template.md`   |
| `docs/03.specs/NNN-feature-id/service.md`               | Service Scaffold       | `docs/99.templates/templates/spec-contracts/service.template.md`      |
| `docs/03.specs/NNN-feature-id/tests.md`                 | Test Contract          | `docs/99.templates/templates/spec-contracts/tests.template.md`        |
| `docs/03.specs/NNN-feature-id/contracts/openapi.yaml`   | OpenAPI Contract       | `docs/99.templates/templates/spec-contracts/openapi.template.yaml`    |
| `docs/03.specs/NNN-feature-id/contracts/schema.graphql` | GraphQL Contract       | `docs/99.templates/templates/spec-contracts/schema.template.graphql`  |
| `docs/03.specs/NNN-feature-id/contracts/service.proto`  | Protobuf Contract      | `docs/99.templates/templates/spec-contracts/service.template.proto`   |
| `docs/04.execution/plans/`                            | Plan                   | `docs/99.templates/templates/sdlc/plan.template.md`         |
| `docs/04.execution/tasks/`                            | Task                   | `docs/99.templates/templates/sdlc/task.template.md`         |
| `docs/05.operations/guides/`                          | Operations Guide       | `docs/99.templates/templates/operations/guide.template.md`        |
| `docs/05.operations/policies/`                        | Operations Policy      | `docs/99.templates/templates/operations/policy.template.md`       |
| `docs/05.operations/runbooks/`                        | Operations Runbook     | `docs/99.templates/templates/operations/runbook.template.md`      |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` | Incident | `docs/99.templates/templates/operations/incident.template.md` |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` | Postmortem | `docs/99.templates/templates/operations/postmortem.template.md` |
| `docs/05.operations/releases/YYYY-MM-DD-release-name.md` | Release | `docs/99.templates/templates/operations/release.template.md` |
| `docs/00.agent-governance/memory/<note>.md`           | Governance Memory Note | `docs/99.templates/templates/governance/memory.template.md`       |
| `docs/00.agent-governance/memory/progress.md`         | Agent Progress Log     | `docs/99.templates/templates/governance/progress.template.md`     |
| `docs/90.references/`                                 | Reference              | `docs/99.templates/templates/common/reference.template.md`    |
| `docs/98.archive/`                                    | Archive Tombstone      | `docs/99.templates/templates/common/archive.template.md`      |
| `README.md` (per folder)                              | README                 | `docs/99.templates/templates/common/readme.template.md`       |

For optional supporting contracts under `docs/03.specs/NNN-feature-id/`, keep
Markdown support files in the feature directory and machine-readable contracts
under `contracts/`. Parent Markdown Spec or API Spec documents own the
cross-links for YAML, GraphQL, and Proto files.

Plan and Task are separate Stage 04 roles. Plan is prospective and records
sequence, intended verification, risk, rollback, and completion criteria. Task
is evidentiary and records attempted work, allowed and forbidden paths,
applicable protected-surface approval, impact, exact commands and results,
reviews, commits, and deferral routing. Ordinary and harness work use the same
Task template; conditional approval and controlled-wrapper evidence does not
create a Task subtype.

See `docs/99.templates/README.md` for the full catalog and usage rules.

## 3.1 Language Boundary by Stage

| Stage / Surface | Language Boundary | Rationale |
| --- | --- | --- |
| `docs/00.agent-governance/**` | English-only | Agent governance, policy, provider, and validation contracts must be stable across providers. |
| `docs/01.requirements/**` | Korean human-facing intent; technical identifiers unchanged | Requirements capture user value, scope, and acceptance criteria for human review. |
| `docs/02.architecture/**` | Mixed: Korean rationale with English IDs, titles, and technical terms preserved | Architecture documents are reviewed by humans and agents and must preserve decision/contracts. |
| `docs/03.specs/**` | English-only | Specs define technical contracts, interfaces, and verification criteria. |
| `docs/04.execution/plans/**` | English-only | Plans define implementation sequencing, risk controls, and validation gates. |
| `docs/04.execution/tasks/**` | English-only | Tasks are audit evidence and must stay machine-reviewable. |
| `docs/05.operations/guides/**` | Korean human-facing body; technical identifiers unchanged | Guides help operators and developers understand and use services. |
| `docs/05.operations/policies/**` | Korean human-facing body; control names and evidence identifiers unchanged | Policies define allowed/disallowed operational states for human review. |
| `docs/05.operations/runbooks/**` | Korean human-facing procedure; commands and expected evidence unchanged | Runbooks support incidents, recovery, rollback, and escalation. |
| `docs/05.operations/incidents/**` | Korean incident narrative; technical evidence unchanged | Incident records and postmortems preserve operator-readable timelines and actions. |
| `docs/05.operations/releases/**` | Korean release narrative; artifact identifiers, timestamps, commands, and evidence labels unchanged | Release records preserve evidence for an actual event and remain distinct from deployment runtime. |
| `docs/90.references/**` | Audience-specific: LLM/generated indexes may be English; human references Korean by default | References support active docs without replacing policy or runtime truth. |
| `docs/98.archive/**` | Concise tombstone language; preserve original paths, IDs, dates, and titles | Archive docs preserve migration traceability, not active current truth. |
| `docs/99.templates/**` | Match target stage; template READMEs Korean by default | Templates must not contradict the language contract of copied target documents. |
| Root `README.md`, service READMEs, and mixed docs | Korean by default with English identifiers preserved | These are human-facing entrypoints that still reference implementation artifacts. |

## 4. Authoring Protocol

1. Identify the target stage, path, and document role.
2. Load `rules/stage-authoring-matrix.md` and follow its stage row.
3. Resolve exactly one registry profile, load the matching human contract, and
   select the mapped template before drafting or updating the target document.
4. Instantiate and preserve the template contract: required headings,
   applicable conditional headings, resolved target-relative links, and one
   `## Related Documents` section.
5. Replace all template placeholders and serialize metadata deterministically
   without treating order as semantic priority.
6. Preserve historical evidence payloads and fail closed on profile, template,
   README-consumer, or direct-parent ambiguity.
7. Cross-link related Requirements, Architecture, Spec, Plan, Task, Operations, Reference, and Incident files.
8. Run checklist gates from `rules/task-checklists.md` and the metadata checker
   for the selected change scope.

For `docs/90.references/`, verify that the document is stable reference context, contains source-backed facts, and does not define active policy, runtime truth, runbook procedure, plan, task evidence, or incident timeline.

For `docs/98.archive/`, verify that the document is a tombstone only. It must
record the original path, archive reason, and current replacement while removing
stale original body content.

### 4.1 Template Deviation Audit

Before completing changes under `docs/01` to `docs/05`, `docs/90`, or
`docs/99`, compare each changed target against the mapped template and the
Stage Authoring Matrix row. If a document intentionally deviates, record the
exception in the related task evidence with:

- file path,
- expected template,
- deviation summary,
- reason the template cannot or should not be applied verbatim,
- approval or evidence owner,
- validation command or manual review evidence.

Do not use template-deviation cleanup as a reason to rewrite historical
evidence outside the approved scope. Already-valid documents should remain
unchanged.

## 5. Operational Procedures

Trigger documentation updates when:

- service topology changes,
- commands/workflows change,
- module ownership/scope changes,
- policy and repository reality diverge.

For completion, ensure affected README files and governance pointers remain accurate.
For typed metadata profile or parser changes, run the focused Python unit suite,
run `check-changed` with an explicit safe base, and regenerate/check the
canonical frontmatter semantic inventory. The full inventory remains advisory;
the pre-push hook enforces only the safely selected changed/new set.
For Stage 01-05 implementation reconciliation, also run
`bash scripts/validation/check-doc-implementation-alignment.sh`; it verifies
tracked implementation paths, removed template names, archive index-only links,
and Stage 05 service document coverage against `infra/**`.

When legacy active-stage content is discovered in a non-stage `docs/*` path:

1. Rewrite it into the canonical stage document using the mapped template.
2. Sync parent README files to the canonical path.
3. Remove the legacy file and directory once no active references remain.

When a whole document under `docs/01` to `docs/05` conflicts with current
implementation and should leave the active chain:

1. Remove active references to that document.
2. Create a tombstone under `docs/98.archive/<original-stage>/<original-path>.md`.
3. Record the migration in `docs/98.archive/README.md`.
4. Do not link active documents back to the archive tombstone.

### 5.1 Gap-to-Stage Routing

When an audit, review, validation failure, or agent handoff finds a gap, route
the gap to the canonical owner before editing. Do not duplicate the same rule
or evidence across stages.

| Gap Type | Canonical Owner | Routing Rule |
| --- | --- | --- |
| Governance, provider behavior, agent execution rule, approval boundary, or memory contract | `docs/00.agent-governance/` | Update the rule/provider/memory surface only when the policy change is approved; otherwise record a memory note or task gap. |
| User value, scope, acceptance criteria, or product intent | `docs/01.requirements/` | Create or update the numbered PRD. Link downstream architecture/spec work instead of embedding design details. |
| Architecture shape, major technical decision, quality attribute, or tradeoff | `docs/02.architecture/` | Use ARD for enduring architecture and ADR for a decision record. Link PRD/spec evidence. |
| Interface, data model, service contract, agent contract, or verification contract | `docs/03.specs/` | Update the numbered spec folder and optional support contract files. Do not record execution evidence here. |
| Work sequencing, approval gates, rollback strategy, or implementation backlog | `docs/04.execution/plans/` | Create or update a plan. Keep actual execution results in the sibling task document. |
| Completed work evidence, validation output, deviation, or implementation disposition | `docs/04.execution/tasks/` | Record the task result, checks, protected-surface boundary, and remaining gaps. |
| Operator usage, operational control, recovery procedure, incident, or postmortem | `docs/05.operations/` | Route usage to `guides/`, policy to `policies/`, recovery to `runbooks/`, and incident evidence to `incidents/`. |
| Source-backed research, audit snapshot, data reference, learning note, or LLM navigation | `docs/90.references/` | Keep it evidence-only. Do not make it active policy, plan, task evidence, or runtime truth. |
| Obsolete or implementation-conflicting document that must leave the active chain | `docs/98.archive/` | Create a tombstone, update the archive ledger, and remove active references. |
| Template, frontmatter, lifecycle, or authoring contract | `docs/99.templates/` | Put reusable rules in `support/` and copyable document shapes in `templates/`. |
| Runtime, secret value, credential, remote GitHub mutation, deployment, or uncertain implementation drift | Stage 04 task/audit gap first | Record as out-of-scope or approval-gated unless the current task explicitly approves that surface and names validation/rollback evidence. |

If one gap spans multiple stages, update the earliest canonical owner that
changes the decision or rule, then link downstream artifacts. For example, a
new operational requirement starts in `docs/01.requirements/`, design belongs
in `docs/02.architecture/` or `docs/03.specs/`, rollout belongs in
`docs/04.execution/`, and operator procedure belongs in `docs/05.operations/`.

## 6. Maintenance and Safety

- Remove obsolete instructions quickly in editable scope.
- If breakages are found in read-only stages (`docs/01` to `docs/99`), log them in `docs/00.agent-governance/memory/` with recommended fixes.
- Move implementation-conflicting whole-document old material to `docs/98.archive` tombstones instead of preserving stale body text in active docs.
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
Read the mapped template under `docs/99.templates/templates/` before writing or editing
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
- `incidents/YYYY/INC-###-<title>/INC-###-<title>.md` documents use
  `incident.template.md` (active incident record).
- `incidents/YYYY/INC-###-<title>/postmortem.md` documents use
  `postmortem.template.md` (post-incident review).
- `releases/YYYY-MM-DD-release-name.md` documents use the registry `release`
  profile and `release.template.md`; create one only from evidence for an
  actual release event. A changelog or readiness runbook is not a Release
  record, and deployment runtime remains separately owned.

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
- `docs/99.templates/support/document-metadata-profiles.yaml`
- `docs/99.templates/support/sdlc-document-contract.md`
- `docs/99.templates/support/common-document-contract.md`
- `docs/99.templates/support/readme-profile-contract.md`
