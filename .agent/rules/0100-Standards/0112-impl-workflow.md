---
trigger: always
glob: ["specs/**/plan.md", "specs/**/plan/**/*.md", "**/plan/**/*.md"]
description: "Structured Autonomy Workflow: enforces the 3-phase (Plan/Generate/Implement) lifecycle for deterministic implementation planning and execution."
---

# Implementation Plan: Structured Autonomy Workflow

- **Role**: Workflow Optimization Architect
- **Purpose**: Define the 3-phase lifecycle for implementation plans to separate planning, generation, and execution concerns.
- **Activates When**: Managing the lifecycle of implementation plans in `specs/**/plan.md` and `**/plan/**/*.md`.

**Trigger**: always — Apply this workflow to every implementation plan from inception to completion.

## 1. Standards

### Principles

- **[REQ-IMPL_WF-01] Phase Separation**
  - Planning, code generation, and implementation MUST be treated as distinct phases.
- **[REQ-IMPL_WF-02] Research-First Strategy**
  - Detailed research MUST precede code generation to ensure architectural alignment.
- **[REQ-IMPL_WF-03] Incremental Execution**
  - Implementation MUST be performed in small, testable increments with explicit stop/commit points.

### Scope

- **In-Scope**: Plan/Generate/Implement phases, research workflow, and status management.
- **Out-of-Scope**: Task specification details (see `0111-impl-task-spec.md`) and estimation.

### Outputs

- **Plan Phase Output**: `plan.md` in `specs/<feature-name>/`.
- **Generate Phase Output**: `implementation.md` in `specs/<feature-name>/`.
- **Implement Phase Output**: Checked-off items in `implementation.md`.

### Must

- **[REQ-IMPL_WF-04] User Approval Gate**
  - Phase 1 (Plan) MUST conclude with a mandatory pause for user feedback and approval.
- **[REQ-IMPL_WF-05] Copy-Paste Readiness**
  - Phase 2 (Generate) MUST produce complete, tested code snippets with ZERO placeholders.
- **[REQ-IMPL_WF-06] Status Tracking**
  - Plan status MUST be updated daily to reflect current progress (`Planned`, `In progress`, `Completed`).

### Must Not

- **[BAN-IMPL_WF-01] Out-of-Order Execution**
  - Implementation MUST NOT begin before the generation phase is completed and approved.
- **[BAN-IMPL_WF-02] Placeholder Completion**
  - Tasks MUST NOT be marked complete until all verification criteria are met.

### Failure Handling

- **Stop Condition**: If any step in the Implement phase fails verification, stop and report.
- **Retry Limit**: Max 2 retries per subtask before escalating to a research revision.

### Style

- Use mermaid diagrams for lifecycle visualization.
- Use explicit "STOP & COMMIT" markers in implementation steps.

## 2. Procedures

- **[PROC-IMPL_WF-01] Phase 1 - Plan**
  - Research codebase, define implementation steps, and obtain user approval.
- **[PROC-IMPL_WF-02] Phase 2 - Generate**
  - Conduct project-wide analysis and generate copy-paste ready documentation.
- **[PROC-IMPL_WF-03] Phase 3 - Implement**
  - Execute steps exactly as specified, running validation at each increment.

## 3. Examples

### Phase Transition Example

- 🔄 `Phase 1 Approval` -> `Phase 2 Generation` -> `Phase 3 Start`.

## 4. Validation Criteria

- **[VAL-IMPL_WF-01] Phase Completion**
  - [ ] Every phase has produced its required artifact before moving to the next.
- **[VAL-IMPL_WF-02] Approval Evidence**
  - [ ] User approval is documented before Phase 2 begins.
- **[VAL-IMPL_WF-03] Status Accuracy**
  - [ ] The plan's YAML status matches the current physical state of the implementation.
