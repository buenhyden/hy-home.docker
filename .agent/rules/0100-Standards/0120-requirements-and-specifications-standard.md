---
trigger: always_on
glob: ["**/docs/prd/**/*", "**/specs/**/*", "**/*-prd.md", "**/*-spec.md"]
description: "Requirements & Specifications Standards: Enforces PRD metric grounding, INVEST user stories, and machine-readable technical specifications with coded identifiers."
---

# Requirements & Specifications Standards

- **Role**: Principal Requirements & Systems Analyst
- **Purpose**: Define standards for capturing, refining, and documenting product requirements and technical specifications to ensure unified business-engineering alignment and AI-optimized readability.
- **Activates When**: Drafting Product Requirements Documents (PRDs), refining user stories, or creating technical specifications for system components.

**Trigger**: always_on — Apply during all phases of the requirements gathering and specification lifecycle.

## 1. Standards

### Principles

- **[REQ-SPT-01] Explicit Success Metric Grounding**
  - All requirements MUST be grounded in quantifiable metrics. Vague qualitative terms (e.g., "fast", "better") MUST NOT be used without a measurable baseline.
- **[REQ-SPT-02] INVEST-Compliant Storytelling**
  - User stories MUST adhere to the INVEST framework (Independent, Negotiable, Valuable, Estimable, Small, Testable) to ensure they are actionable for development.
- **[REQ-SPT-03] Machine-Readable Identifier System**
  - Specifications MUST utilize a coded identifier system (e.g., `REQ-NNN`, `SEC-NNN`) to enable programmatic traceability and automated validation.

### Documentation Baseline

| Type | Requirement ID | Critical Component |
| --- | --- | --- |
| PRD | [REQ-SPT-04] | Vision, Personas, Success Metrics, Use Cases, Scope/Out-of-Scope, Milestones, Risks, Compliance |
| Spec | [REQ-SPT-05] | NFR, Storage Strategy, Interfaces, Verification (Tests/Coverage), Security, Ops & Observability |
| AC | [REQ-SPT-06] | Given-When-Then (GWT) scenarios |
| Traceability| [REQ-SPT-07] | Requirement-to-Issue mapping matrix |

### Must

- **[REQ-SPT-08] Mandatory Persona Framing**
  - Feature requirements MUST be framed from the perspective of an identified user persona to provide context for implementation.
- **[REQ-SPT-09] Deterministic Language Enforcement**
  - Specifications MUST utilize deterministic language (SHALL, MUST, PROHIBITED). Optionality MUST be explicitly marked with SHOULD or MAY.
- **[REQ-SPT-10] Verifiable Acceptance Criteria (AC)**
  - Every requirement MUST be accompanied by at least three testable ACs that define the success state for verification.

### Must Not

- **[BAN-SPT-01] Technical Prescription in PRDs**
  - PRDs MUST NOT dictate technical implementation details; the "How" belongs exclusively to Technical Specifications or Architecture Blueprints.
- **[BAN-SPT-02] Hidden Assumption Sprawl**
  - Do NOT leave implicit assumptions in requirements; document all dependencies, constraints, and out-of-scope items explicitly.

### Failure Handling

- **Stop Condition**: Stop the requirements refinement loop if the proposed feature lacks a clear, measurable success metric or a primary user persona.

## 2. Procedures

- **[PROC-SPT-01] Requirement Refinement Flow**
  - IF a requirement is identified as "Ambiguous" THEN MUST return it to the `needs-refinement` state until GWT acceptance criteria are added.
- **[PROC-SPT-02] Specification Lifecycle Audit**
  - Quarterly, audit the `/specs/` directory to ensure that implemented features have their corresponding "Approved" or "Retired" status correctly reflected.

## 3. Examples

### Measurable Success Metric (Good)

- **Objective**: "Reduce API response latency from 500ms to < 200ms (p95) over a 30-day window."

## 4. Validation Criteria

- **[VAL-SPT-01] Metric Compliance**
  - [ ] audit confirms that 100% of "Released" features possess an associated, measurable success metric in their original PRD.
- **[VAL-SPT-02] Traceability Integrity**
  - [ ] Traceability matrix correctly identifies the mapping between 100% of system requirements and their unit test counterparts.
- **[VAL-SPT-03] GWT Scenario Validation**
  - [ ] Manual review confirms that all user stories possess at least one Given-When-Then scenario for QA testing.
