# [Feature or System Name] Product Requirements Document (PRD)

> Use this template for `docs/prd/<feature-or-system>-prd.md`.
>
> Repository-derived contract:
>
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Allowed PRD status values: `Approved | Superseded | Deprecated`.
> - Allowed scope values where your doc set uses them: `master | domain | historical`.
> - Allowed scope values layer values: `common | architecture | backend | frontend | infra | mobile | product | qa | security`
> - `domain` documents should name their parent master PRD where applicable.
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.

## Optional Frontmatter

```yaml
---
title: '[Feature or System Name] Product Requirements Document'
status: 'Approved'
version: 'v1.0.0'
owner: 'buenhyden'
stakeholders: ['buenhyden']
scope: 'master'
parent_epic: 'N/A'
tags: ['prd', 'requirements']
layer: '<layer>'
---
```

## H1 and Metadata

# [Feature or System Name] Product Requirements Document (PRD)

> **Status**: [Approved | Superseded | Deprecated]
> **Target Version**: [v1.0.0]
> **Owner**: [Repository Owner]
> **Stakeholders**: [Repository Owner, Frontend Engineer]
> **Scope**: [master | domain | historical]
> **layer:** [common | architecture | backend | frontend | infra | mobile | product | qa | security]
> **Parent Epic**: [N/A or parent PRD] (Optional)
> **Parent Master PRD**: `[./system-master-prd.md]` (Optional for `domain`)

**Overview (KR):** [Write a 1-2 sentence Korean summary of the product intent, the problem space, and why this document matters.]

## Required Core Sections

These sections should exist in every PRD, even in a compressed active-chain document.

## Vision

[State the user, maintainer, or platform outcome this document is meant to achieve.]

## Requirements

- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Use explicit IDs when the downstream spec or plan will trace against them.

## Success Criteria

- [Success criterion 1]
- [Success criterion 2]

If the document defines visual or information-architecture families, this section may instead be named `Families` and list each family boundary explicitly.

## Related

- `[../ard/system-or-domain-ard.md]`
- `[../specs/YYYY-MM-DD-feature.md]`
- `[../plans/YYYY-MM-DD-feature.md]`
- `[../adr/NNNN-decision.md]`

## Optional Extended Sections

Use these when the PRD needs full product framing, personas, milestones, or acceptance criteria.

## 1. Vision & Problem Statement

**Vision**: [One paragraph describing the desired outcome and user or platform value.]

**Problem Statement**: [Explain what is broken, unclear, fragmented, or missing today, and why it matters now.]

## 2. Target Personas

- **Persona 1 ([Name / Role])**:
  - **Pain Point**: [Describe the problem]
  - **Goal**: [Describe the desired result]
- **Persona 2 ([Name / Role])**:
  - **Pain Point**: [Describe the problem]
  - **Goal**: [Describe the desired result]

## 3. Success Metrics (Quantitative)

| ID                 | Metric Name | Baseline (Current) | Target (Success) | Measurement Period |
| ------------------ | ----------- | ------------------ | ---------------- | ------------------ |
| **REQ-PRD-MET-01** | [Metric]    | [Current]          | [Target]         | [Window]           |
| **REQ-PRD-MET-02** | [Metric]    | [Current]          | [Target]         | [Window]           |

## 4. Key Use Cases & Acceptance Criteria (GWT)

| ID           | User Story (INVEST)                                                 | Acceptance Criteria (Given-When-Then)                             |
| ------------ | ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **STORY-01** | **As a** [Persona],<br>**I want** [action],<br>**So that** [value]. | **Given** [context],<br>**When** [action],<br>**Then** [outcome]. |
| **STORY-02** | **As a** [Persona],<br>**I want** [action],<br>**So that** [value]. | **Given** [context],<br>**When** [action],<br>**Then** [outcome]. |

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]** [Requirement]
- **[REQ-PRD-FUN-02]** [Requirement]
- **[REQ-PRD-FUN-03]** [Requirement]

## 6. Out of Scope

- [Out-of-scope item 1]
- [Out-of-scope item 2]

## 7. Milestones & Roadmap

- **PoC**: YYYY-MM-DD - [Early validation goal]
- **MVP**: YYYY-MM-DD - [Minimum useful delivery]
- **Beta**: YYYY-MM-DD - [Limited validation or rollout]
- **v1.0**: YYYY-MM-DD - [Completion state]

## 8. Risks, Security & Compliance

- **Risks & Mitigation**: [List the main risks and mitigation strategy]
- **Compliance & Privacy**: [List relevant compliance or privacy constraints]
- **Security Protocols**: [List security-related controls or assumptions]

## 9. Assumptions & Dependencies

- [Assumption or dependency 1]
- [Assumption or dependency 2]

## 10. Q&A / Open Issues

- **[ISSUE-01]**: [Open issue] - **Update**: [Current answer or status]

## 11. Related Documents

- **Parent Master PRD**: `[./system-master-prd.md]` (Optional for `domain`)
- **Architecture Reference**: `[../ard/system-or-feature-ard.md]`
- **Technical Specification**: `[../specs/YYYY-MM-DD-feature.md]`
- **Implementation Plan**: `[../plans/YYYY-MM-DD-feature.md]`
- **Decision Record**: `[../adr/NNNN-decision.md]`
