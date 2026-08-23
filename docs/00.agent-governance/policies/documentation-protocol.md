---
profile_id: governance-policy
layer: agentic
---

# Documentation Protocol

## Authority

The Stage 99 registry is the only machine authority for paths, profiles,
required sections, lifecycle values, and identifier relations. Stage 00 owns
authoring behavior and `scripts/` owns executable validation.

## Document Boundaries

- Stage 01 owns long-lived solution-independent requirements.
- Stage 02 owns current architecture descriptions and durable decisions.
- Stage 03 owns a change behavior contract, technical approach, plan, Tasks,
  and executable interface contracts.
- Stage 05 owns operator guidance, policies, runbooks, and incidents.
- Stage 90 owns non-normative research, audits, and reference data.
- Stage 98 owns minimal migration and tombstone navigation; Git stores history.
- Stage 99 owns profiles, schemas, and copyable templates.

Do not create parallel PRD, SRS, interface-requirement, design, tests, release,
progress, or handoff authorities when the canonical package already owns the
content. Root `DESIGN.md` remains UI and design-system authority only.

## Authoring Rules

1. Select the registry profile before creating or moving a document.
2. Use four-digit numbered slugs where the profile requires an identity.
3. Keep dates in frontmatter; the incident year directory is the only path exception.
4. Store incident packets only at `docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md` and `docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md`.
5. Link canonical IDs in full and never reuse an issued ID.
6. Update cross-links in the same logical change.
7. Record execution evidence in the co-located Stage 03 Task.
8. Validate metadata, links, and stage-specific contracts before completion.

Governance and internal technical authority is written in English. User-facing
guidance may follow the audience language when its template permits it.

### 5.1 Gap-to-Stage Routing

| Gap Type | Owner | Rule |
| --- | --- | --- |
| Governance behavior | `docs/00.agent-governance/` | Change canonical policy, role, skill, or provider facts first. |
| Long-lived need | `docs/01.requirements/` | Record solution-independent requirements and acceptance. |
| Structure or durable decision | `docs/02.architecture/` | Update a description or ADR. |
| Change contract | `docs/03.specs/` | Update the bounded Spec Package. |
| Implementation sequencing | `docs/03.specs/####-<slug>/plan.md` | Record the approved implementation order. |
| Implementation evidence | `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` | Record result, deviation, and validation evidence. |
| Operator knowledge | `docs/05.operations/` | Update the applicable guide, policy, runbook, or incident. |
| External evidence | `docs/90.references/` | Preserve non-normative research, audit, or data. |
| Historical lookup | `docs/98.archive/` | Add only minimal migration or tombstone navigation. |
| Shape or lifecycle | `docs/99.templates/` | Change the registry, schema, or copyable template. |
| Protected or ambiguous change | `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` Task/audit gap first | Stop mutation and bind approval, scope, and recovery first. |

## Related Documents

- [Stage authoring matrix](stage-authoring-matrix.md)
- [Stage 99 registry](../../99.templates/registry.json)
- [SDLC](../sdlc.md)
- [Task checklists](task-checklists.md)
