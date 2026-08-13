---
layer: agentic
---

# Stage Authoring Matrix (00-05, 90, 98, 99)

Single source of truth for stage-level authoring expectations.

## 1. Matrix

| Area                         | Purpose                                                                   | Authoring Timing                                                                                                                    | Primary Persona                                        | Input Docs                                                                                                    | Output Docs                                                                 | Required Template                                                                                                                                                                                                               | Done Criteria                                                                                                                                                                                         |
| :--------------------------- | :------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 00 agent governance          | Agent governance and routing rules                                        | Before implementation and whenever governance drifts                                                                                | `rules-engineer`; `doc-writer` contributes             | Root shims, typed contracts, provider docs, active workflow constraints                                       | Rules, scopes, providers, memory notes, bounded `memory/current.md` handoff | N/A (governance style), `docs/99.templates/templates/governance/memory.template.md` for memory entries, `docs/99.templates/templates/governance/progress.template.md` for historical `memory/progress.md`                       | Rules Engineer policy ownership is preserved, governance stays English-only, links valid, typed provider projections fresh, applicable co-located Task evidence recorded, and current handoff bounded |
| 01 requirements              | Product intent and requirements                                           | At discovery and scope definition                                                                                                   | `doc-writer`; `workflow-supervisor` routes approval    | Stakeholder intent, problem statements, constraints                                                           | PRD docs at `docs/01.requirements/prd-####-<slug>.md`                       | `docs/99.templates/templates/sdlc/prd.template.md`                                                                                                                                                                              | Requirements are testable, traceable, and linked to downstream artifacts                                                                                                                              |
| 02 architecture descriptions | Architecture Description                                                  | After requirements baseline                                                                                                         | Owning registered role; `doc-writer` contributes       | PRD, SRS, Interface Requirements, existing architecture context                                               | `docs/02.architecture/descriptions/ad-####-<slug>.md`                       | `docs/99.templates/templates/sdlc/architecture-description.template.md`                                                                                                                                                         | Boundaries and quality attributes are explicit and aligned with requirements                                                                                                                         |
| 02 architecture decisions    | Architecture decisions                                                    | When a non-trivial architectural trade-off is made                                                                                  | Owning registered role; `doc-writer` contributes       | Architecture Description and alternative options                                                              | `docs/02.architecture/decisions/adr-####-<slug>.md`                         | `docs/99.templates/templates/sdlc/adr.template.md`                                                                                                                                                                              | Decision, alternatives, and consequences are explicitly documented                                                                                                                                    |
| 03 specifications            | Technical specifications                                                  | Before implementation tasks start                                                                                                   | Owning registered role; `doc-writer` contributes       | Architecture Description, applicable ADRs, and parent Specs                                                   | `docs/03.specs/spec-####-<capability>/spec.md` and optional contracts       | `docs/99.templates/templates/sdlc/spec.template.md`, `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `service.template.md`, `tests.template.md`, and machine-readable contract templates          | Interfaces, data contracts, and verification criteria are complete                                                                                                                                    |
| 03 capability plans          | Prospective implementation planning                                       | After a Spec is stable, before coding                                                                                                | `workflow-supervisor`                                  | Owning Spec and approved architecture inputs                                                                  | `docs/03.specs/spec-####-<capability>/plan.md`                              | `docs/99.templates/templates/sdlc/plan.template.md`                                                                                                                                                                             | Plan includes sequence, dependencies, intended verification, risks, rollback, and completion criteria without claiming actual results                                                                 |
| 03 capability tasks          | Ordinary and harness execution evidence                                   | During implementation, validation, review, and deferral                                                                             | Owning registered implementation/review roles          | Owning Spec, Plan, approvals, implementation and validation results                                            | `docs/03.specs/spec-####-<capability>/task.md`                              | `docs/99.templates/templates/sdlc/task.template.md`                                                                                                                                                                             | Task records boundaries, applicable approvals, impact, exact commands and results, reviews, commits, deferrals, and conditional controlled-wrapper evidence                                           |
| 05 operations                | Operations knowledge base                                                 | When operational guidance, controls, or repeatable procedures change                                                                | `incident-responder`; `doc-writer` contributes         | Specs, Plans, Tasks, ADRs, compliance constraints, system behavior                                            | `docs/05.operations/<domain>/ops-####-<subject>/{guide,policy,runbook}.md`  | `docs/99.templates/templates/operations/guide.template.md`, `docs/99.templates/templates/operations/policy.template.md`, `docs/99.templates/templates/operations/runbook.template.md`                                           | Usage guides, policies, runbooks, validation, and related references live in one canonical operations subject; each service leaf maps to tracked `infra/**` implementation or is explicitly non-service |
| 05 incidents                 | Incident records and postmortems                                          | During/after incidents and after stabilization                                                                                      | `incident-responder`; `security-auditor` reviews       | Monitoring evidence, applicable runbook evidence, root-cause analysis data                                    | Incident and postmortem docs                                                | `docs/99.templates/templates/operations/incident.template.md`, `docs/99.templates/templates/operations/postmortem.template.md`                                                                                                  | A root Incident or evidenced Runbook-linked Incident records timeline, impact, response, and handoff; its Postmortem remains a strict Incident child with owned prevention actions                    |
| 05 releases                  | Evidence for an executed release event                                    | After a real release has artifacts, validation, approval, and outcome evidence                                                      | Owning registered operations role                      | Specs, Plans, Tasks, immutable artifacts, approvals, rollout evidence                                         | Release records at `docs/05.operations/releases/rel-####-<slug>/release.md` | `docs/99.templates/templates/operations/release.template.md`                                                                                                                                                                    | Included changes, artifacts, validation, approvals, rollout or rollback, outcome, and known issues are evidence-backed; deployment runtime remains in Spec 127 or a later approved runtime chain      |
| 98/archive                   | Provenance tombstones for documents removed from current truth            | After an approved manifest classifies the source and safe provenance, consumer, replacement, preservation, and review evidence pass | Owning registered role; `doc-writer` contributes       | Approved manifest row, original identity/path, conditional replacement, Git provenance, preservation evidence | `docs/98.archive/**` tombstone                                               | `archive.template.md` for `sdlc-archive`; exact semantics route to the corpus and archive contracts                                                                                                                             | Stale body is absent, provenance is verified, and active docs do not consume tombstones as current guidance                                                                                           |

## 2. Appendix: Supporting Stages

> **Convergence authority:** the earlier legacy rows are transitional source
> observations only. New and migrated documents use the canonical table below;
> no Stage 04 target, ARD role, dated identity, or parallel Operations role
> root is authorized.

| Area | Canonical target | Template |
| :-- | :-- | :-- |
| Requirements | `prd-`, optional `srs-`, optional `interface-` leaves in `docs/01.requirements/` | SDLC PRD, SRS, Interface Requirement |
| Architecture | `descriptions/ad-####-<slug>.md` and `decisions/adr-####-<slug>.md` | Architecture Description and ADR |
| Capability | `docs/03.specs/spec-####-<slug>/{spec,plan,task}.md` | Spec, Plan, Task |
| Operations | `docs/05.operations/<domain>/ops-####-<subject>/{guide,policy,runbook}.md` | Operations role templates |
| Event records | `incidents/<year>/inc-####-<slug>` and `releases/rel-####-<slug>` directories | Incident, Postmortem, Release |

| Stage | Purpose                                                                                                                                                                                                                                              | Template                                                                                                                                |
| :---- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| 90    | Stable references, glossary, source-backed facts, inventories, and evergreen learning context. This stage supports active docs, must state repository role and lifecycle, and does not replace policy, plans, runbooks, incidents, or runtime truth. | `docs/99.templates/templates/common/reference.template.md`                                                                              |
| 98    | Archive provenance tombstones and approved immutable evidence snapshots. Stage 98 preserves migration traceability, not historical current truth; the current hand-maintained README ledger remains transitional until Wave D.                       | `docs/99.templates/templates/common/archive.template.md`; route conditions to `docs/99.templates/support/archive-retention-contract.md` |
| 99    | Source templates for all stages                                                                                                                                                                                                                      | `docs/99.templates/templates/common/readme.template.md` and stage templates                                                             |

### Typed Metadata Profile Overlay

`docs/99.templates/support/document-metadata-profiles.yaml` overlays the
human-readable stage matrix with machine-readable required, optional,
forbidden, parent, lifecycle, and exception rules. Human numbering and template
selection remain stage-specific. Stable `artifact_id`, `artifact_type`, and
`parent_ids` are migration fields, not permission to rewrite existing stage
documents. Task 7 keeps the exhaustive inventory advisory; Task 8 owns the
approved active-chain migration and first changed/new blocking activation.
Corpus waves additionally use
`docs/99.templates/support/document-corpus-migration-contract.yaml` and the
Stage 99 human owners for manifest and archive/retention semantics. Stage 00
controls authorization and evidence duties without copying exact values.

## 3. Language Routing

Apply the document-role language authority in
`rules/documentation-protocol.md#31-language-boundary-by-document-role`. This
matrix selects roles and templates; it does not define a second language table.

## 4. Agent Skills by Stage

The following `.claude/skills/` skills are recommended for each stage. Load a skill when its domain matches the active task.

| Skill                          | Primary Stage(s)                  | Purpose                                                               |
| :----------------------------- | :-------------------------------- | :-------------------------------------------------------------------- |
| `compose-stack-agent`          | 03 specs, 05 operations           | Docker Compose stack design, audit, and compliance                    |
| `requirements-to-design-agent` | 01 requirements → 02 architecture | Translates requirements into architecture artifacts                   |
| `execution-plan-agent`         | 03 capability plans               | Generates structured implementation plans                             |
| `task-breakdown-agent`         | 03 capability tasks               | Decomposes plans into auditable task evidence                         |
| `ops-runbook-agent`            | 05 operations                     | Authoring and validating runbooks and operational procedures          |
| `knowledge-map-agent`          | 00 governance, 90 references      | Maps codebase knowledge and reference relationships                   |
| `policy-gate-agent`            | All stages                        | Validates stage artifacts against governance policy before completion |

Claude skill projections are available in `.claude/skills/<skill>/SKILL.md`.
Shared Codex and Gemini discovery uses `.agents/skills/<skill>/SKILL.md`.

## 5. Usage Rules

1. Load this matrix for any documentation authoring/refactoring task.
2. Use the row for the target stage as a mandatory authoring contract.
3. Load the required template from `docs/99.templates/` before creating or
   modifying the target document.
4. Remove all template placeholders, keep required headings, and sync the
   parent README before completion.
5. Run `bash scripts/validation/check-repo-contracts.sh` for changed
   target-stage documents.
6. If a stage is read-only for the current task, record findings instead of mutating the stage.
7. If a changed document intentionally deviates from its mapped template,
   record the file, expected template, reason, approval/evidence owner, and
   validation evidence in the related task record.

## Not-Yet-Exercised Templates

These templates are registered, valid, and retained. No document has been
authored from them. They are retained because the lifecycle event they serve has
not yet occurred, not because they are defective.

| Template       | Target path                                | Trigger that would create the first instance  |
| :------------- | :----------------------------------------- | :-------------------------------------------- |
| `incident`     | `docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md` | A recorded production incident                |
| `postmortem`   | `docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md` | A reviewed incident                           |
| `release`      | `docs/05.operations/releases/rel-####-<slug>/release.md` | A tagged release                              |
| `api-spec`     | `docs/03.specs/spec-####-<capability>/api-spec.md`     | A specification defining an HTTP or RPC API   |
| `data-model`   | `docs/03.specs/spec-####-<capability>/data-model.md`   | A specification defining persisted entities   |
| `service`      | `docs/03.specs/spec-####-<capability>/service.md`      | A specification introducing a Compose service |
| `tests`        | `docs/03.specs/spec-####-<capability>/tests.md`        | A specification with a formal test matrix     |
| `agent-design` | `docs/03.specs/spec-####-<capability>/agent-design.md` | A specification defining a new agent role     |

Authoring against one of these is expected to require template revision, since
none has been validated against a real document.

## Related Documents

- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/99.templates/README.md`
- `docs/99.templates/support/corpus-migration-contract.md`
- `docs/99.templates/support/archive-retention-contract.md`
