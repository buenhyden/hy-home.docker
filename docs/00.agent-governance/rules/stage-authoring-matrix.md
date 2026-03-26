---
layer: agentic
---

# Stage Authoring Matrix (00-11)

Single source of truth for stage-level authoring expectations.

## 1. Matrix

| Stage | Purpose | Authoring Timing | Primary Persona | Input Docs | Output Docs | Required Template | Done Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 00 | Agent governance and routing rules | Before implementation and whenever governance drifts | Agentic Workflow Specialist / Documentation Specialist | Root shims, provider docs, active workflow constraints | Rules, scopes, providers, memory notes | N/A (governance style), `memory/template.md` for memory entries | Governance stays English-only, links valid, no contradictory policy |
| 01 | Product intent and requirements | At discovery and scope definition | Product Manager | Stakeholder intent, problem statements, constraints | PRD docs | `docs/99.templates/prd.template.md` | Requirements are testable, traceable, and linked to downstream artifacts |
| 02 | Architecture reference | After PRD baseline | System Architect | PRD, existing architecture context | ARD docs | `docs/99.templates/ard.template.md` | Boundaries and quality attributes are explicit and aligned with PRD |
| 03 | Architecture decisions | When a non-trivial architectural trade-off is made | System Architect | PRD, ARD, alternative options | ADR docs | `docs/99.templates/adr.template.md` | Decision, alternatives, and consequences are explicitly documented |
| 04 | Technical specifications | Before implementation tasks start | Backend/Frontend/Infra Engineer | PRD, ARD, ADR | Spec docs and optional contracts | `docs/99.templates/spec.template.md`, `api-spec.template.md`, contract templates | Interfaces, data contracts, and verification criteria are complete |
| 05 | Implementation planning | After specs are stable, before coding | Project Lead / Engineering Lead | PRD, ARD, ADR, Specs | Plan docs | `docs/99.templates/plan.template.md` | Plan includes sequencing, risks, verification commands, and completion criteria |
| 06 | Task execution evidence | During implementation and validation | Implementation Engineer / QA Engineer | Plans, Specs | Task docs with evidence | `docs/99.templates/task.template.md` | Task states and verification evidence are current and auditable |
| 07 | Human guides | After capability is implemented or changed | Documentation Specialist | Specs, Plans, Tasks, Operations context | Guide docs | `docs/99.templates/guide.template.md` | Steps are reproducible and linked to authoritative sources |
| 08 | Operations policy | When operational controls or standards change | Operations/SRE Engineer | Specs, ADRs, compliance constraints | Operations docs | `docs/99.templates/operation.template.md` | Policy is enforceable, scoped, and linked to runbooks |
| 09 | Runbook procedures | When repeatable operational execution is required | Operations/SRE Engineer | Operations policy, system behavior | Runbook docs | `docs/99.templates/runbook.template.md` | Procedure is executable with validation and rollback paths |
| 10 | Incident records | During/after incidents | Operations/SRE Engineer | Monitoring evidence, runbook execution logs | Incident docs | `docs/99.templates/incident.template.md` | Timeline, impact, and mitigation are recorded with evidence links |
| 11 | Postmortems | After incident stabilization | Operations/SRE Engineer / Security Auditor | Incident records, root-cause analysis data | Postmortem docs | `docs/99.templates/postmortem.template.md` | Root cause and prevention actions are complete and assigned |

## 2. Appendix: Supporting Stages

| Stage | Purpose | Template |
| :--- | :--- | :--- |
| 90 | Stable references and evergreen knowledge | `docs/99.templates/reference.template.md` |
| 99 | Source templates for all stages | `docs/99.templates/readme.template.md` and stage templates |

## 3. Usage Rules

1. Load this matrix for any documentation authoring/refactoring task.
2. Use the row for the target stage as a mandatory authoring contract.
3. If a stage is read-only for the current task, record findings instead of mutating the stage.
