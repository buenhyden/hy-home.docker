---
description: AI Planner Agent logic for driving the Pre-Development phase.
---

# Workflow: Agent Pre-Development

This workflow defines the execution loop for the **Planner Agent** during the Pre-Development phase. Its goal is to translate human requests into rigid specifications.

## 1. Requirement Analysis & PRD Generation

When starting a new feature request:

1. Ensure the user provides a clear goal. If the request is vague, ask for clarification.
2. Draft the Product Requirements Document (PRD) mapped to `docs/prd/[feature].md`.
3. **Template Enforcement**: You MUST use `templates/product/prd-template.md`.
4. **NFR Quantification**: Explicitly define quantifiable Non-Functional Requirements (NFRs) such as Latency < 200ms or Target TPS.
5. **QA Constraint**: Define quantifiable success metrics and write all Acceptance Criteria using the **Given-When-Then** (GWT) format.

## 2. Architecture Evaluation

1. Cross-reference the features requested against the **Architecture & Tech Stack Checklist** in `ARCHITECTURE.md`.
2. Ensure you have explicitly defined the Tech Stack, DB engine, Domain Model, and NFRs (Latency/Availability).
3. Check if the PRD requires a new database, external service, or breaks constraints in `ARCHITECTURE.md`.
4. If yes, generate an Architecture Decision Record in `docs/adr/` using `templates/architecture/adr-template.md`. **Risk Mitigation**: You MUST include Threat Modeling, Risk Assessment, and SPOF mitigation strategies.
5. For structural diagrams or complex system bounds, draft an Architecture Reference Document using `templates/architecture/ard-template.md` and save to `docs/ard/`. **CRITICAL**: The Planner Agent MUST explicitly answer all 12 items of the Architecture & Tech Stack Checklist (from `ARCHITECTURE.md`) in the drafted ARD.

## 3. Specification Generation

Once the PRD and ADRs are agreed upon by the human:

1. Generate the absolute source of truth: the Implementation Spec.
2. **Template Enforcement**: You MUST use `templates/engineering/spec-template.md`.
3. Save it to `specs/<feature>/spec.md`.
4. **QA Constraint**: Define what Unit Tests and Integration Tests MUST be written by the Coder agents to satisfy the PRD's GWT criteria.

## 4. End State

Halt execution and inform the human that the Pre-Development phase is complete. Await their manual approval of the Spec before triggering the Coder Agents.
