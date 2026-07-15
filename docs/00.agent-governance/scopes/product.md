---
layer: product
---

# Product Requirements Scope

**Standardized procedures for defining intent, roadmap, and business impact.**

## 1. Context & Objective

- **Goal**: Ensure every technical initiative corresponds to a validated product need.
- **Reference**: All requirements live in `docs/01.requirements/` as the SSoT.
- **Standards**: Must comply with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Template**: Use `prd.template.md` for all new product definitions.
- **Impact**: Include a **Business Impact Analysis** (BIA) and success metrics for every major feature.
- **Visibility**: Stakeholder alignment must be documented via approved PRDs.

## 3. Implementation Flow

1. **Discovery**: Gather raw ideas via `brainstorming` workflow.
2. **Drafting**: Create PRD in `01.requirements/`.
3. **Approval**: Obtain explicit User/Stakeholder lock before moving to `03.specs/`.

## 4. Operational Procedures

- **Iterative Refinement**: Update PRDs to reflect changes in scope or priority during development.

## 5. Maintenance & Safety

- **Archive**: Move deprecated or implementation-conflicting product documents to `docs/98.archive/01.requirements/` tombstones after active references are removed.
- **Glossary**: Maintain a ubiquitous language glossary in project documentation under `docs/90.references/`.

## Related Documents

- [Agent governance hub](../README.md)
- [Bootstrap rule](../rules/bootstrap.md)
- [Persona protocol](../rules/persona.md)
- [Task checklists](../rules/task-checklists.md)
- [Agentic rule](../rules/agentic.md)
