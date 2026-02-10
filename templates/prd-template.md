# [Feature/Epic Name] PRD

- **Status**: [Draft | Review | Approved | Deprecated]
- **Owner**: [Name]
- **Stakeholders**: [Project Manager, Lead Engineer, Designer, etc.]
- **Parent Epic**: [Link to Epic PRD] (Optional)

---

## 0. Executive Summary

[Provide a 2-3 sentence overview of what this feature is, why it's being built,
and who it's for. This should be a high-level summary for busy readers.]

## 0. Business / Product Checklist (Fill Before Review)

> This PRD is the single source of truth for the business/product checklist.
> Complete the PRD sections referenced below and capture alignment notes.

| Item | Check Question | Required | Alignment Notes (Agreement) | PRD Section |
| --- | --- | --- | --- | --- |
| Vision & Goal | Is the problem + business goal defined in one paragraph? | Must |  | Section 1 |
| Success Metrics | Are the key success/failure metrics defined with quantitative targets? | Must |  | Section 3 |
| Target Users | Are specific primary personas and their pain points defined? | Must |  | Section 2 |
| Use Case (GWT) | Are acceptance criteria written in Given-When-Then format? | Must |  | Section 4 |
| Scope (In) | Is the feature list included in this release clearly defined? | Must |  | Section 5 |
| Not in Scope | Is what we will NOT build in this release explicitly listed? | Must |  | Section 6 |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated? | Must |  | Section 7 |
| Business Risks | Are major business risks listed with mitigation strategy? | Optional |  | Section 8 |
| Compliance / Privacy | Have privacy/regulatory constraints been reviewed and documented? | Optional |  | Section 8 |

## 1. Vision & Problem Statement

- **Vision**: [Provide a one-paragraph vision statement of what this feature
  aims to achieve and its business value.]
- **Problem Statement**: Provide a clear, concise description of the problem
  being solved. What is the pain point?

## 2. Target Personas (Primary & Secondary)

> [!IMPORTANT]
> You MUST link every core requirement to a specific persona defined here.

- **Persona 1 ([Name/Role])**: [e.g., "Sarah the Data Scientist"]
  - **Pain Point**: [Describe a specific frustration they face today]
  - **Goal**: [What does this persona want to achieve with this feature?]
- **Persona 2 ([Name/Role])**: [e.g., "Bob the DevOps Engineer"]
  - **Pain Point**: [Specific frustration]
  - **Goal**: [Desired outcome]

## 3. Success Metrics (Quantitative)

> [!IMPORTANT]
> Metrics MUST be measurable and time-bound. Avoid vague terms like "improve" without a target.

| ID | Metric Name | Baseline (Current) | Target (Success) | Measurement Period |
| --- | --- | --- | --- | --- |
| **REQ-PRD-MET-01** | [e.g., Latency] | 500ms | < 200ms | 30 days post-launch |
| **REQ-PRD-MET-02** | [e.g., Conversion] | 2% | > 5% | First 1,000 users |

## 4. Key Use Cases & Acceptance Criteria (GWT)

> [!IMPORTANT]
> Acceptance criteria MUST follow the **Given-When-Then** format for testability.

| ID | User Story (INVEST) | Acceptance Criteria (Given-When-Then) |
| --- | --- | --- |
| **STORY-01** | **As a** [Persona Name],<br>**I want** [action/feature],<br>**So that** [value/benefit]. | **Given** [initial context/precondition],<br>**When** [the user performs an action],<br>**Then** [the system produces this outcome]. |
| **STORY-02** | **As a** [Persona Name],<br>**I want** [action],<br>**So that** [value]. | **Given** [context],<br>**When** [action],<br>**Then** [outcome]. |
| **STORY-03** | **As a** [Persona Name],<br>**I want** [action],<br>**So that** [value]. | **Given** [context],<br>**When** [action],<br>**Then** [outcome]. |

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]** [Requirement Description linked to STORY-XX]
- **[REQ-PRD-FUN-02]** [Requirement Description]

## 6. Out of Scope

- [Items that will NOT be built in this phase]

## 7. Milestones & Roadmap

- **PoC**: [Target Date] - [Key deliverables]
- **MVP**: [Target Date] - [Core functionality]
- **Beta**: [Target Date] - [External validation / limited release]
- **v1.0**: [Target Date] - [Full release]

## 8. Risks, Security & Compliance

- **Risks & Mitigation**: [Market, Technical, or Operational risks and blockers]
- **Compliance & Privacy**: [Personal data, GDPR/CCPA, industry regulations]
- **Security Protocols**: [Specific security requirements for this feature]

## 9. Assumptions & Dependencies

- **Assumptions**: [What are we assuming to be true? (e.g., Users have X device)]
- **External Dependencies**: [Does this rely on external APIs or other teams?]

## 10. Q&A / Open Issues

- **[ISSUE-01]**: [Describe open question] - **Update**: [Resolution]
- **[ISSUE-02]**: [Describe open question]

## 11. Change Log

| Version | Date | Author | Description |
| --- | --- | --- | --- |
| v0.1 | [YYYY-MM-DD] | [Name] | Initial Draft |
