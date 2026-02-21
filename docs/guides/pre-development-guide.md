# Pre-Development Guide (Human Centric)

This guide outlines how human developers and product owners should manage the **Pre-Development** phase. The heavy lifting is done by the **Planner Agent**, but humans define the success criteria and act as the final approval gate.

## 1. Initiating the Phase

You start the Pre-Development phase by feeding the **Planner Agent** your raw requirements via an issue or chat prompt.

**Goal**: Convert abstract human ideas into rigorous, testable implementation specifications.

## 2. Managing the Planner Agent's Outputs

The Planner Agent will autonomously generate three types of files. Your job is to review them against business, QA, and architectural standards.

### A. The PRD (`docs/prd/`)

You must verify that the generated Product Requirements Document (PRD):

1. **Defines Success Metrics**: Are they quantifiable? (e.g., "Latency < 200ms", NOT "Make it faster").
2. **Acceptance Criteria (GWT)**: Ensure scenarios are strictly in **Given-When-Then** format. No code can be properly QA'd if these are vague.

### B. Architecture Decisions (`docs/adr/` & `docs/ard/`)

If the PRD requires new technical boundaries, the Planner Agent will generate ADRs or ARDs.

- You must verify these decisions do not violate constraints listed in `ARCHITECTURE.md`.

### C. The Implementation Spec (`specs/`)

This is the most critical hurdle. The Spec is what the Coder Agents will blindly follow.

- **Traceability**: Does every API route, component, and database table strictly correspond to a feature in the PRD?
- **Test Requirements**: Has the Planner specified explicit Unit and Integration testing layers for the Coder Agents to implement? Are functional and performance tests defined if applicable?

## 3. Human Approval Gate (Pre-Dev Exit)

Do **NOT** proceed to development or notify Coder Agents until the following QA checklist passes:

- [ ] PRD Success metrics are definitively measurable.
- [ ] PRD Acceptance criteria are in testable Given-When-Then format.
- [ ] The **Architecture & Tech Stack Checklist** (as defined in `ARCHITECTURE.md`) has been fully reviewed and mapped in the ARD/PRD.
- [ ] No new technologies were added without an approved ADR.
- [ ] The generated specification in `specs/` is extremely rigid (exact file names, payload shapes, defined test scopes).

Once the Spec is fully approved, you officially command the AI Coder Agents to begin the **During-Development Phase**.
