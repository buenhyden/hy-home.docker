---
layer: agentic
---

# Stage Authoring Matrix (00-05, 90, 99)

Single source of truth for stage-level authoring expectations.

## 1. Matrix

| Area | Purpose | Authoring Timing | Primary Persona | Input Docs | Output Docs | Required Template | Done Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 00 agent governance | Agent governance and routing rules | Before implementation and whenever governance drifts | Agentic Workflow Specialist / Documentation Specialist | Root shims, provider docs, active workflow constraints | Rules, scopes, providers, memory notes, progress log | N/A (governance style), `docs/99.templates/memory.template.md` for memory entries, `docs/99.templates/progress.template.md` for `memory/progress.md` | Governance stays English-only, links valid, no contradictory policy, progress log updated |
| 01 requirements | Product intent and requirements | At discovery and scope definition | Product Manager | Stakeholder intent, problem statements, constraints | PRD docs | `docs/99.templates/prd.template.md` | Requirements are testable, traceable, and linked to downstream artifacts |
| 02 architecture requirements | Architecture reference | After PRD baseline | System Architect | PRD, existing architecture context | ARD docs | `docs/99.templates/ard.template.md` | Boundaries and quality attributes are explicit and aligned with PRD |
| 02 architecture decisions | Architecture decisions | When a non-trivial architectural trade-off is made | System Architect | PRD, ARD, alternative options | ADR docs | `docs/99.templates/adr.template.md` | Decision, alternatives, and consequences are explicitly documented |
| 03 specifications | Technical specifications | Before implementation tasks start | Backend/Frontend/Infra Engineer | PRD, ARD, ADR | Spec docs and optional contracts | `docs/99.templates/spec.template.md`, `api-spec.template.md`, contract templates | Interfaces, data contracts, and verification criteria are complete |
| 04 execution plans | Implementation planning | After specs are stable, before coding | Project Lead / Engineering Lead | PRD, ARD, ADR, Specs | Plan docs | `docs/99.templates/plan.template.md` | Plan includes sequencing, risks, verification commands, and completion criteria |
| 04 execution tasks | Task execution evidence | During implementation and validation | Implementation Engineer / QA Engineer | Plans, Specs | Task docs with evidence | `docs/99.templates/task.template.md` | Task states and verification evidence are current and auditable |
| 05 operations | Operations knowledge base | When operational guidance, controls, or repeatable procedures change | Documentation Specialist / Operations/SRE Engineer | Specs, Plans, Tasks, ADRs, compliance constraints, system behavior | Operations docs with usage, controls, procedures, and validation | `docs/99.templates/operation.template.md` | Usage, policy, procedure, validation, and related references are in one canonical operations document |
| 05 incidents | Incident records and postmortems | During/after incidents and after stabilization | Operations/SRE Engineer / Security Auditor | Monitoring evidence, runbook execution logs, root-cause analysis data | Incident and postmortem docs | `docs/99.templates/incident.template.md`, `docs/99.templates/postmortem.template.md` | Timeline, impact, mitigation, root cause, and prevention actions are complete and assigned |

## 2. Appendix: Supporting Stages

| Stage | Purpose | Template |
| :--- | :--- | :--- |
| 90 | Stable references, glossary, source-backed facts, inventories, and evergreen learning context. This stage supports active docs, must state repository role and lifecycle, and does not replace policy, plans, runbooks, incidents, or runtime truth. | `docs/99.templates/reference.template.md` |
| 99 | Source templates for all stages | `docs/99.templates/readme.template.md` and stage templates |

## 3. Usage Rules

1. Load this matrix for any documentation authoring/refactoring task.
2. Use the row for the target stage as a mandatory authoring contract.
3. If a stage is read-only for the current task, record findings instead of mutating the stage.
