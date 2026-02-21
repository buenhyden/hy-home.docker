---
title: "[Feature Name] Product Requirements Document"
status: "Draft | Review | Approved | Deprecated"
version: "v1.x.x"
owner: "[Name]"
stakeholders: "[Project Manager, Lead Engineer, Designer, etc.]"
parent_epic: "[Link to Epic PRD]"
tags: ["prd", "requirements", "product"]
---

# Product Requirements Document (PRD)

> **Status**: [Draft | Review | Approved | Deprecated]
> **Target Version**: [e.g., v1.x.x]
> **Owner**: [Name]
> **Stakeholders**: [Project Manager, Lead Engineer, Designer, etc.]
> **Parent Epic**: [Link to Epic PRD] (Optional)

*Target Directory: `docs/prd/<feature>-prd.md`*
*Note: This document defines the What and Why. It must be approved before Spec generation.*

---

## 0. Pre-Review Checklist (Business & Product)

> This PRD is the single source of truth for the business/product checklist.
> Complete the PRD sections referenced below and capture alignment notes before approval.

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     |                             | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     |                             | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     |                             | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     |                             | Section 4   |
| Scope (In)            | Is the feature list included in this release clearly defined?          | Must     |                             | Section 5   |
| Not in Scope          | Is what we will NOT build in this release explicitly listed?           | Must     |                             | Section 6   |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated?                          | Must     |                             | Section 7   |
| Risks & Compliance    | Are major risks, privacy, or regulatory constraints documented?        | Must     |                             | Section 8   |

---

## 1. Vision & Problem Statement

**Vision**: [Provide a one-paragraph vision statement of what this feature aims to achieve and its business value.]

**Problem Statement**: [Provide a clear, concise description of the problem being solved. What is the explicit pain point?]

## 2. Target Personas

> **Important**: Link every core requirement to a specific persona defined here.

- **Persona 1 ([Name/Role])**: [e.g., "Sarah the Data Scientist"]
  - **Pain Point**: [Describe a specific frustration they face today]
  - **Goal**: [What does this persona want to achieve with this feature?]
- **Persona 2 ([Name/Role])**: [e.g., "Bob the DevOps Engineer"]
  - **Pain Point**: [Specific frustration]
  - **Goal**: [Desired outcome]

## 3. Success Metrics (Quantitative)

> **Important**: Metrics MUST be measurable and time-bound. Avoid vague terms like "improve" without a quantitative target.

| ID                 | Metric Name        | Baseline (Current) | Target (Success) | Measurement Period  |
| ------------------ | ------------------ | ------------------ | ---------------- | ------------------- |
| **REQ-PRD-MET-01** | [e.g., Latency]    | 500ms              | < 200ms          | 30 days post-launch |
| **REQ-PRD-MET-02** | [e.g., Conversion] | 2%                 | > 5%             | First 1,000 users   |

## 4. Key Use Cases & Acceptance Criteria (GWT)

> **Important**: Acceptance criteria MUST follow the **Given-When-Then** format for testability.

| ID           | User Story (INVEST)                                                                      | Acceptance Criteria (Given-When-Then)                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **STORY-01** | **As a** [Persona Name],<br>**I want** [action/feature],<br>**So that** [value/benefit]. | **Given** [initial context/precondition],<br>**When** [the user performs an action],<br>**Then** [the system produces this outcome]. |
| **STORY-02** | **As a** [Persona Name],<br>**I want** [action],<br>**So that** [value].                 | **Given** [context],<br>**When** [action],<br>**Then** [outcome].                                                                    |

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]** [Requirement Description linked to STORY-XX]
- **[REQ-PRD-FUN-02]** [Requirement Description]

## 6. Out of Scope

- [Explicitly state what features or capabilities are NOT included in this iteration to prevent scope creep.]

## 7. Milestones & Roadmap

- **PoC**: [Target Date] - [Key deliverables]
- **MVP**: [Target Date] - [Core functionality]
- **Beta**: [Target Date] - [External validation / limited release]
- **v1.0**: [Target Date] - [Full release]

## 8. Risks, Security & Compliance

- **Risks & Mitigation**: [Market, Technical, or Operational risks and blockers]
- **Compliance & Privacy**: [Personal data, GDPR/CCPA, industry regulations]
- **Security Protocols**: [Specific security requirements for this feature, e.g., encryption, audit logs]

## 9. Assumptions & Dependencies

- **Assumptions**: [What are we assuming to be true? (e.g., Users have X device)]
- **External Dependencies**: [Does this rely on external APIs, specific hardware, or other teams?]

## 10. Q&A / Open Issues

- **[ISSUE-01]**: [Describe open question] - **Update**: [Resolution]

## 11. Related Documents (Reference / Traceability)

- **Technical Specification**: [Link to Spec](../../specs/<feature>/spec.md)
- **API Specification**: [Link to API Spec](../../specs/<feature>/api/<feature>-api.md)
- **Architecture Decisions (ADRs)**: [Link to ADRs](../../docs/adr/README.md)
