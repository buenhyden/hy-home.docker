---
trigger: always
glob: ["**/plan/**/*.md"]
description: "Implementation plan traceability and verification: enforces AC coverage, constraint compliance, and cross-validation workflows."
---

# Implementation Plan Traceability & Verification

- **Role**: Quality Assurance Architect
- **Purpose**: Define the standards for maintaining traceability between specifications and implementation plans.
- **Activates When**: Verifying requirement coverage or constraint compliance in `**/plan/**/*.md`.

**Trigger**: always — Apply these standards during verification phases to ensure zero requirement leakage.

## 1. Standards

### Principles

- **[REQ-IMPL_TRC-01] Requirement Mapping**
  - Every specification requirement MUST map to at least one implementation task.
- **[REQ-IMPL_TRC-02] AC Coverage**
  - Every acceptance criterion MUST have a corresponding test task.
- **[REQ-IMPL_TRC-03] Constraint Adherence**
  - Every technical constraint MUST be acknowledged and addressed in the implementation tasks.

### Scope

- **In-Scope**: Traceability matrices, gap analysis, and verification protocols.
- **Out-of-Scope**: Task-level execution (see `0111-impl-task-spec.md`) and workflow management.

### Outputs

- **Traceability Matrix**: A table mapping requirements (REQ) and acceptance criteria (AC) to implementation and test tasks.

### Must

- **[REQ-IMPL_TRC-04] Gap Identification**
  - Any specification requirement not addressed in the plan MUST be flagged and documented with rationale.
- **[REQ-IMPL_TRC-05] Verification Checklists**
  - Plans MUST include a final verification checklist covering all requirements and ACs.

### Must Not

- **[BAN-IMPL_TRC-01] Unmapped Requirements**
  - Implementation tasks MUST NOT exist without a parent requirement or clear technical justification.
- **[BAN-IMPL_TRC-02] Blind Assumption**
  - Constraints MUST NOT be assumed to be met without explicit verification evidence.

### Failure Handling

- **Stop Condition**: Stop verification if a requirement-to-task mapping is missing.
- **Resolution**: Prompt the planner to add missing tasks or document the omission.

### Style

- Use `REQ-nnn` and `AC-nnn` referencing.
- Prefer tabular format for matrices.

## 2. Procedures

- **[PROC-IMPL_TRC-01] Coverage Audit**
  - Perform a line-by-line audit of specifications against implementation tasks before final approval.
- **[PROC-IMPL_TRC-02] Evidence Collection**
  - Document the exact evidence (e.g., test logs, screenshots) required to satisfy each traceability link.

## 3. Examples

### Traceability Matrix Example

| Spec Requirement | Implementation Tasks     | Status |
| ---------------- | ------------------------ | ------ |
| `REQ-001`        | `TASK-001`, `TASK-003`   | ✅     |

## 4. Validation Criteria

- **[VAL-IMPL_TRC-01] Coverage Completeness**
  - [ ] All REQ and AC items from the spec are accounted for in the matrix.
- **[VAL-IMPL_TRC-02] Link Validity**
  - [ ] Every link in the traceability matrix points to a valid task or test.
- **[VAL-IMPL_TRC-03] Constraint Verification**
  - [ ] Every constraint (CON) has a documented compliance method.
