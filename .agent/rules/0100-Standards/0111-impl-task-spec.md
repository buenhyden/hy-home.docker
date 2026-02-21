---
trigger: always
glob: ["specs/**/plan.md", "specs/**/plan/**/*.md", "**/plan/**/*.md"]
description: "Task specification and validation standards: enforces variable definition, exact command sequences, and measurable compliance for implementation plans."
---

# Implementation Plan Task Specification & Validation

- **Role**: Intelligence Verification Engineer
- **Purpose**: Define the standards for specifying tasks, variables, and validation criteria within implementation plans.
- **Activates When**: Writing or reviewing implementation tasks and validation criteria in `specs/**/plan.md` and `**/plan/**/*.md`.

**Trigger**: always — Apply these standards consistently for all task specifications.

## 1. Standards

### Principles

- **[REQ-IMPL_TSPC-01] Variable Grounding**
  - All configuration values and constants MUST be explicitly defined.
- **[REQ-IMPL_TSPC-02] Command Exactness**
  - All execution commands MUST include exact flags and version-specific arguments.
- **[REQ-IMPL_TSPC-03] Binary Validation**
  - Validation criteria MUST be binary (Pass/Fail) and measurable.

### Scope

- **In-Scope**: Task descriptions, environment variables, command sequences, and acceptance criteria.
- **Out-of-Scope**: High-level workflow, project hierarchy, and estimation.

### Outputs

- Task lists in implementation plans MUST use the specified table format with a "Validation Criteria" column.

### Must

- **[REQ-IMPL_TSPC-04] Exact File Paths**
  - Every task MUST reference a specific file path or range.
- **[REQ-IMPL_TSPC-05] Command Isolation**
  - Commands MUST be isolated into clear, runnable snippets.
- **[REQ-IMPL_TSPC-06] Success Evidence**
  - Every task MUST define what evidence constitutes success (e.g., "output includes X").

### Must Not

- **[BAN-IMPL_TSPC-01] Placeholder Tasks**
  - Tasks MUST NOT use "TBD" or "rest of the logic" placeholders.
- **[BAN-IMPL_TSPC-02] Implicit Versions**
  - Commands MUST NOT rely on default versions if a specific version is required.

### Failure Handling

- **Stop Condition**: Stop execution if a command sequence fails the validation criteria.
- **Escalation**: Report the exact error output and the failed validation check to the user.

### Style

- Use `TASK-NNN` and `TEST-NNN` identifiers.
- Provide examples for complex command sequences.

## 2. Procedures

- **[PROC-IMPL_TSPC-01] Variable Extraction**
  - Identify all secret keys and environment variables during the planning phase.
- **[PROC-IMPL_TSPC-02] Criteria Mapping**
  - Map every requirement (REQ) to at least one validation check (VAL).

## 3. Examples

### Good Example (Exact Command)

- ✅ `npm install @aws-sdk/client-s3@^3.400.0`

### Bad Example (Vague Criteria)

- ❌ "Ensure the upload functionality works correctly."

## 4. Validation Criteria

- **[VAL-IMPL_TSPC-01] Command Runnability**
  - [ ] All specified commands are syntactically correct and includes necessary flags.
- **[VAL-IMPL_TSPC-02] Criteria Measurability**
  - [ ] Every validation criteria is objectively measurable without human interpretation.
- **[VAL-IMPL_TSPC-03] Context Completeness**
  - [ ] All required variables for the task are defined in the context or plan.
