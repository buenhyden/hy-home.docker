---
layer: product
title: 'Product Requirements Scope'
---

# Product Requirements Scope

**Standardized procedures for defining intent, roadmap, and business impact.**

## 1. Context & Objective

- **Goal**: Ensure every technical initiative corresponds to a validated product need.
- **Reference**: All requirements live in `docs/01.prd/` as the SSoT.
- **Standards**: Must comply with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Template**: Use `prd.template.md` for all new product definitions.
- **Impact**: Include a **Business Impact Analysis** (BIA) and success metrics for every major feature.
- **Visibility**: Stakeholder alignment must be documented via approved PRDs.

## 3. Implementation Flow

1. **Discovery**: Gather raw ideas via `brainstorming` workflow.
2. **Drafting**: Create PRD in `01.prd/`.
3. **Approval**: Obtain explicit User/Stakeholder lock before moving to `04.specs/`.

## 4. Operational Procedures

- **Iterative Refinement**: Update PRDs to reflect changes in scope or priority during development.

## 5. Maintenance & Safety

- **Archive**: Move deprecated product ideas to an `archive/` subfolder within `01.prd/`.
- **Glossary**: Maintain a ubiquitous language glossary in the project root README or `docs/common/`.
