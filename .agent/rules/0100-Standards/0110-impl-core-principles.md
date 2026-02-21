---
trigger: always
glob: ["**/plan/**/*.md"]
description: "Core principles for deterministic implementation planning: enforces naming, structural standards, and AI-executable instruction design."
---

# Implementation Plan Core Principles

- **Role**: Intelligence Architecture Strategist
- **Purpose**: Define the fundamental standards for creating implementation plans that are fully executable by AI agents or humans.
- **Activates When**: Creating, refactoring, or reviewing implementation plans in `**/plan/**/*.md`.

**Trigger**: always — Apply these principles at all times during implementation planning.

## 1. Standards

### Principles

- **[REQ-IMPL_CORE-01] Deterministic Communication**
  - Implementation plans MUST use deterministic language with zero ambiguity.
- **[REQ-IMPL_CORE-02] Machine-Parseable Structure**
  - Plans MUST use structured formats (tables, lists) for tasks and validation.
- **[REQ-IMPL_CORE-03] Complete Self-Containment**
  - Plans MUST include all necessary context without external dependencies.
- **[REQ-IMPL_CORE-04] Atomic Phase Architecture**
  - Plans MUST be broken into discrete, atomic phases with clear boundaries.

### Scope

- **In-Scope**: Fundamental planning principles, naming conventions, and file structure.
- **Out-of-Scope**: Task-specific details, workflow procedures, and estimation metrics.

### Outputs

- Implementation plans MUST follow the structure defined in `templates/project/plan-template.md`.

### Must

- **[REQ-IMPL_CORE-05] Naming Convention**
  - File names MUST follow `[purpose]-[component]-[version].md`.
  - Purpose MUST be one of: `upgrade`, `refactor`, `feature`, `data`, `infrastructure`, `process`, `architecture`, `design`.
- **[REQ-IMPL_CORE-06] Front Matter**
  - Every plan MUST include YAML front matter with: `goal`, `version`, `date_created`, `last_updated`, `owner`, `status`, `tags`.
- **[REQ-IMPL_CORE-07] Directory Location**
  - Active plans MUST be stored in `specs/<feature-name>/plan.md`.

### Must Not

- **[BAN-IMPL_CORE-01] Ambiguous Logic**
  - Plans MUST NOT use vague terms like "add logic" or "fix the file".
- **[BAN-IMPL_CORE-02] External Dependencies**
  - Plans MUST NOT rely on implicit knowledge or unreferenced external docs.

### Failure Handling

- **Stop Condition**: Stop planning if requirements are ambiguous.
- **Retry Limit**: Max 3 attempts to clarify requirements with the user.

### Style

- Use MUST/MUST NOT keywords only.
- Prefer tables for task lists.

## 2. Procedures

- **[PROC-IMPL_CORE-01] Initial Plan Creation**
  - IF creating a new plan THEN MUST start from the canonical template.
- **[PROC-IMPL_CORE-02] Phase Breakdown**
  - Break complex features into testable increments.
- **[PROC-IMPL_CORE-03] Validation Setup**
  - Define measurable validation criteria for every phase.

## 3. Examples

### Good Example (Deterministic)

- ✅ "Create file `src/auth.ts` with function `validateToken(token: string): boolean`"

### Bad Example (Ambiguous)

- ❌ "Add some authentication logic to the project."

## 4. Validation Criteria

- **[VAL-IMPL_CORE-01] Skeleton Integrity**
  - [ ] All 8 required sections exist in the implementation plan.
- **[VAL-IMPL_CORE-02] Naming Compliance**
  - [ ] File name follows `[purpose]-[component]-[version].md`.
- **[VAL-IMPL_CORE-03] Deterministic Language**
  - [ ] All tasks use specific, unambiguous instructions.
- **[VAL-IMPL_CORE-04] Front Matter Completeness**
  - [ ] All mandatory YAML fields are present.
