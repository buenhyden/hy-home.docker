# Technical Specifications Hub (`specs/`)

This directory is the absolute **Source of Truth** for the During-Development phase. It forms the primary bridge between Human Intent and AI Execution.

## Golden Rule for AI Agents

**NO SPEC, NO CODE.**
Coder Agents (Backend/Frontend) are governed by `.agent/workflows/` to explicitly refuse writing executable code unless a corresponding, human-approved specification exists in this folder.

## Purpose

- Translate high-level Product Requirements (PRDs) and Architecture Designs (ARDs) into concrete, deterministic coding instructions.
- Provide a rigid, unchanging target for AI Coder Agents to implement against, establishing exactly what Unit and Integration tests must be created.
- Prevent AI hallucination by removing the need for agents to guess at edge cases, error handling, or API signatures.

## Creation & Execution Rules

- **Owner**: The Planner Agent creates these files.
- **Template**: All specs MUST be generated using `templates/engineering/spec-template.md`.
- **Locations**:
  - **Spec** MUST be stored at `specs/<feature>/spec.md`.
  - **Plan** MUST be stored at `specs/<feature>/plan.md`.
  - **API contracts** (if any) MUST be stored under `specs/<feature>/api/`.
- **Approval Gate**: Specs MUST be explicitly approved by a Human Developer. The gate MUST be validated against `ARCHITECTURE.md` checklist items with Priority `**필수**`.

## Example Feature Layout

```text
specs/user-auth/
  spec.md
  plan.md
  api/
    openapi.yaml
```

## Relation to Other Ecosystems

- `docs/prd/`: The **What** (Human-readable Features, Success Metrics).
- `docs/ard/`: The **How** (System Architecture, Data Models).
- `.agent/workflows/`: The **Behaviors** (AI Agent Prompt logic and runtime loops).
- `specs/`: The **Exact Instructions** (File paths, function signatures, QA layer test requirements).
- `.agent/rules/`: Specifically `.agent/rules/0250-implementation-lifecycle-standard.md` which mandates the overarching Plan -> Implement -> QA -> Document cycle, alongside the **6 Core Engineering Pillars** (Security, Performance, Observability, Compliance, Documentation, Localization). All specs must adhere to rigid standards like GWT Acceptance Criteria and Machine-Readable IDs (defined in `0120-requirements-and-specifications-standard.md`).
