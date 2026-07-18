---
layer: agentic
---

# Stage Authoring Matrix (00-05, 90, 98, 99)

Single source of truth for stage-level authoring expectations.

## 1. Matrix

| Area                         | Purpose                                  | Authoring Timing                                                                            | Primary Persona                                        | Input Docs                                                            | Output Docs                                                      | Required Template                                                                                                                                                                                       | Done Criteria                                                                                                                                           |
| :--------------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------ | :----------------------------------------------------- | :-------------------------------------------------------------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 00 agent governance          | Agent governance and routing rules       | Before implementation and whenever governance drifts                                        | Agentic Workflow Specialist / Documentation Specialist | Root shims, provider docs, active workflow constraints                | Rules, scopes, providers, memory notes, progress log             | N/A (governance style), `docs/99.templates/templates/governance/memory.template.md` for memory entries, `docs/99.templates/templates/governance/progress.template.md` for `memory/progress.md`                                                    | Governance stays English-only, links valid, no contradictory policy, progress log updated                                                               |
| 01 requirements              | Product intent and requirements          | At discovery and scope definition                                                           | Product Manager                                        | Stakeholder intent, problem statements, constraints                   | PRD docs at `docs/01.requirements/NNN-feature-or-system.md`       | `docs/99.templates/templates/sdlc/prd.template.md`                                                                                                                                                                     | Requirements are testable, traceable, and linked to downstream artifacts                                                                                |
| 02 architecture requirements | Architecture reference                   | After PRD baseline                                                                          | System Architect                                       | PRD, existing architecture context                                    | ARD docs                                                         | `docs/99.templates/templates/sdlc/ard.template.md`                                                                                                                                                                     | Boundaries and quality attributes are explicit and aligned with PRD                                                                                     |
| 02 architecture decisions    | Architecture decisions                   | When a non-trivial architectural trade-off is made                                          | System Architect                                       | PRD, ARD, alternative options                                         | ADR docs                                                         | `docs/99.templates/templates/sdlc/adr.template.md`                                                                                                                                                                     | Decision, alternatives, and consequences are explicitly documented                                                                                      |
| 03 specifications            | Technical specifications                 | Before implementation tasks start                                                           | Backend/Frontend/Infra Engineer                        | PRD, ARD, ADR                                                         | Spec docs at `docs/03.specs/NNN-feature-id/spec.md` and optional contracts | `docs/99.templates/templates/sdlc/spec.template.md`, `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `service.template.md`, `tests.template.md`, and machine-readable contract templates | Interfaces, data contracts, and verification criteria are complete                                                                                      |
| 04 execution plans           | Prospective implementation planning      | After specs are stable, before coding                                                       | Project Lead / Engineering Lead                        | PRD, ARD, ADR, Specs                                                  | Plan docs                                                        | `docs/99.templates/templates/sdlc/plan.template.md`                                                                                                                                                                    | Plan includes sequence, dependencies, intended verification, risks, rollback, and completion criteria without claiming actual results                    |
| 04 execution tasks           | Ordinary and harness execution evidence  | During implementation, validation, review, and deferral                                     | Implementation Engineer / QA Engineer                  | Plans, Specs, approvals, implementation and validation results        | Task docs with evidence                                          | `docs/99.templates/templates/sdlc/task.template.md`                                                                                                                                                                    | Task records boundaries, applicable approvals, impact, exact commands and results, reviews, commits, deferrals, and conditional controlled-wrapper evidence |
| 05 operations                | Operations knowledge base                | When operational guidance, controls, or repeatable procedures change                        | Documentation Specialist / Operations/SRE Engineer     | Specs, Plans, Tasks, ADRs, compliance constraints, system behavior    | Operations docs with usage, controls, procedures, and validation | `docs/99.templates/templates/operations/guide.template.md` (guides/**), `docs/99.templates/templates/operations/policy.template.md` (policies/**), `docs/99.templates/templates/operations/runbook.template.md` (runbooks/\*\*)                                        | Usage guides, policies, runbooks, validation, and related references live in one canonical operations stage; each service leaf maps to tracked `infra/**` implementation or is explicitly non-service |
| 05 incidents                 | Incident records and postmortems         | During/after incidents and after stabilization                                              | Operations/SRE Engineer / Security Auditor             | Monitoring evidence, applicable runbook evidence, root-cause analysis data | Incident and postmortem docs                                     | `docs/99.templates/templates/operations/incident.template.md`, `docs/99.templates/templates/operations/postmortem.template.md`                                                                                                                    | A root Incident or evidenced Runbook-linked Incident records timeline, impact, response, and handoff; its Postmortem remains a strict Incident child with owned prevention actions |
| 05 releases                  | Evidence for an executed release event   | After a real release has artifacts, validation, approval, and outcome evidence               | Operations/SRE Engineer / Release Owner                 | Specs, Plans, Tasks, immutable artifacts, approvals, rollout evidence | Release records at `docs/05.operations/releases/YYYY-MM-DD-release-name.md` | `docs/99.templates/templates/operations/release.template.md`                                                                                                                                                | Included changes, artifacts, validation, approvals, rollout or rollback, outcome, and known issues are evidence-backed; deployment runtime remains in Spec 127 or a later approved runtime chain |
| 98/archive                   | Provenance tombstones for documents or content removed from current truth | After an approved manifest classifies the source and safe provenance, consumer, replacement, preservation, and review evidence pass | Documentation Specialist / Agentic Workflow Specialist | Approved manifest row, original identity/path, conditional replacement, Git provenance, preservation evidence | `docs/98.archive/**` SDLC tombstone or root `archive/**` content tombstone | `archive.template.md` for `sdlc-archive`; `content-archive.template.md` for `content-archive`; exact semantics route to the corpus and archive contracts | Stale body is absent, provenance is verified, the path matches exactly one archive profile, and active docs do not consume tombstones as current guidance |

## 2. Appendix: Supporting Stages

| Stage | Purpose                                                                                                                                                                                                                                              | Template                                                   |
| :---- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------- |
| 90    | Stable references, glossary, source-backed facts, inventories, and evergreen learning context. This stage supports active docs, must state repository role and lifecycle, and does not replace policy, plans, runbooks, incidents, or runtime truth. | `docs/99.templates/templates/common/reference.template.md`                  |
| 98    | Archive provenance tombstones and approved immutable evidence snapshots. Stage 98 preserves migration traceability, not historical current truth; the current hand-maintained README ledger remains transitional until Wave D. | `docs/99.templates/templates/common/archive.template.md`; route conditions to `docs/99.templates/support/archive-retention-contract.md` |
| 99    | Source templates for all stages                                                                                                                                                                                                                      | `docs/99.templates/templates/common/readme.template.md` and stage templates |

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

## 3. Language Boundary by Stage

| Stage / Folder | Language Boundary |
| :------------- | :---------------- |
| `docs/00.agent-governance/**` | English-only governance, policy, and provider contracts |
| `docs/01.requirements/**` | Korean human-facing requirements and scope; preserve technical identifiers and acceptance-criteria structure |
| `docs/02.architecture/**` | Mixed-audience architecture docs: Korean rationale, English IDs/titles/quality attributes/technical terms preserved |
| `docs/03.specs/**` | English-only technical specifications and contracts |
| `docs/04.execution/plans/**` | English-only implementation plans |
| `docs/04.execution/tasks/**` | English-only task evidence |
| `docs/05.operations/guides/**` | Korean human-facing usage guidance; preserve commands, paths, identifiers, and service names |
| `docs/05.operations/policies/**` | Korean human-facing controls; preserve control names, evidence IDs, and technical identifiers |
| `docs/05.operations/runbooks/**` | Korean human-facing procedures; preserve commands, expected output names, and escalation evidence |
| `docs/05.operations/incidents/**` | Korean incident narrative; preserve timestamps, IDs, commands, and evidence labels |
| `docs/05.operations/releases/**` | Korean release narrative; preserve versions, artifact identifiers, timestamps, commands, and evidence labels |
| `docs/90.references/**` | Audience-specific reference docs: LLM/generated indexes may be English; human references Korean by default |
| `docs/98.archive/**` and root `archive/**` | Concise tombstone language; preserve original paths, IDs, dates, titles, and profile-admitted replacement links |
| `docs/99.templates/**` | Match the target stage language boundary; template READMEs are Korean by default |
| Root `README.md` and human-facing folder READMEs | Korean by default; preserve commands, paths, service names, environment variables, and upstream terms |

## 4. Agent Skills by Stage

The following `.claude/skills/` skills are recommended for each stage. Load a skill when its domain matches the active task.

| Skill                          | Primary Stage(s)                  | Purpose                                                               |
| :----------------------------- | :-------------------------------- | :-------------------------------------------------------------------- |
| `compose-stack-agent`          | 03 specs, 05 operations           | Docker Compose stack design, audit, and compliance                    |
| `requirements-to-design-agent` | 01 requirements → 02 architecture | Translates requirements into architecture artifacts                   |
| `execution-plan-agent`         | 04 execution plans                | Generates structured implementation plans                             |
| `task-breakdown-agent`         | 04 execution tasks                | Decomposes plans into auditable task evidence                         |
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

## Related Documents

- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/99.templates/README.md`
- `docs/99.templates/support/corpus-migration-contract.md`
- `docs/99.templates/support/archive-retention-contract.md`
