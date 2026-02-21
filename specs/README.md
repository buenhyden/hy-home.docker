# Technical Specifications Hub (`specs/`)

This directory is the absolute **Source of Truth** for the During-Development phase. It exists explicitly and exclusively for **Spec-Driven Development**.

## 1. Necessity and Purpose

This directory is necessary because it forms the rigid, non-negotiable bridge between Human Intent (defined in `docs/`) and AI Execution.

- **Spec-Driven Development Core**: By forcing all planned changes into concrete specifications here *before* coding begins, we eliminate AI hallucination, scope creep, and untested edge cases.
- **Traceability**: It translates high-level Product Requirements (PRDs) and Architecture Designs (ARDs) into deterministic coding instructions mapping directly to file paths.
- **QA Gateway**: It provides a concrete target for AI Coder Agents to implement against, establishing exactly what Unit and Integration tests *must* be created to pass CI/CD.

## 2. Required Content and Templates

Every specification created in this folder MUST be instantiated from the predefined templates located in `templates/engineering/`.

- **Owner**: The **Planner Agent** creates these files. The **Coder Agent** reads and executes them.
- **Required Files per Feature**:
  - `specs/<feature>/spec.md` — The technical specification detailing exact required code changes, logic flows, and testing constraints. **(Template: `templates/engineering/spec-template.md`)**
  - `specs/<feature>/plan.md` — The step-by-step execution roadmap for the Coder agent.
  - `specs/<feature>/api/` — OpenAPI or GraphQL schemas documenting interface contracts. **(Template: `templates/engineering/api-spec-template.md`)**

## 3. Golden Rules for AI Agents

**NO SPEC, NO CODE.**
Coder Agents (Backend/Frontend) are governed by `.agent/workflows/` to explicitly refuse writing executable code unless a corresponding, human-approved specification exists in this folder.

- **Approval Gate**: Specs MUST be explicitly approved by a Human Developer. The gate MUST validate that all `ARCHITECTURE.md` items with Priority `**필수**` are satisfied.
- **Drift Prevention (Reverse Documentation)**: If during implementation, technical limitations force a deviation from the plan, Coder Agents MUST update the `spec.md` to match reality *before* finalizing the Pull Request.

## 4. Relation to Other Ecosystems (No Overlap)

- `docs/prd/`: The **What** (Human-readable Features, Success Metrics). Do not place implementation rules there.
- `docs/ard/`: The **How** globally (System Architecture). Do not place function-level logic there.
- `specs/`: The **Exact Instructions** (File paths, function signatures, QA layer test requirements). Do not place broad product visions here.
