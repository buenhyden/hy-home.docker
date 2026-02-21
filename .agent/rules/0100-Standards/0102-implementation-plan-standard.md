---
trigger: always
glob: ["specs/**/plan.md", "specs/**/plan/**/*.md", "**/plan/**/*.md"]
description: "Master authority for Implementation Plan Standards: workspace-wide orchestration of planning, specification, workflow, and estimation rules."
---

# Implementation Plan Standard (Master Authority)

- **Role**: Intelligence Architecture Strategist
- **Purpose**: Serve as the high-level authority and entry point for all implementation planning standards in the workspace.
- **Activates When**: Any implementation planning activity is initiated.

**Trigger**: always — Apply the modularized planning standards across the entire workspace.

## 1. Standards

### Principles

- **[REQ-IMPL_MASTER-01] Modular Authority**
  - Planning standards are partitioned into focused, composable rules to ensure maintainability and clarity.
- **[REQ-IMPL_MASTER-02] Layering Precedence**
  - Regional or task-specific planning rules MUST NOT override these core standards unless explicitly permitted.

### Scope

- **In-Scope**: Orchestration of planning rules and cross-file references.
- **Out-of-Scope**: Execution details covered by sub-rules.

### Outputs

- A complete set of compliant implementation plan documents.

### Must

- **[REQ-IMPL_MASTER-03] Reference Hierarchy**
  - All implementation planning MUST comply with the following modularized rules:
    - [Core Principles](../0100-Standards/0110-impl-core-principles.md)
    - [Task Specification & Validation](../0100-Standards/0111-impl-task-spec.md)
    - [Structured Autonomy Workflow](../0100-Standards/0112-impl-workflow.md)
    - [Traceability & Verification](../0100-Standards/0113-impl-traceability.md)
    - [Estimation & Work Hierarchy](../0100-Standards/0114-impl-estimation.md)
    - [Templates](../0100-Standards/0115-impl-templates.md)

### Must Not

- **[BAN-IMPL_MASTER-01] Redundant Content**
  - Sub-rules MUST NOT duplicate the master principles defined in this file.

### Failure Handling

- **Stop Condition**: Stop planning if any of the mandatory sub-rules are violated.

## 2. Procedures

- **[PROC-IMPL_MASTER-01] Standard Interpretation**
  - IF a conflict arises between sub-rules THEN refer to the Core Principles (0110) for resolution.

## 3. Examples

### Compliance Map

- Core -> 0110
- Workflow -> 0112
- Tasks -> 0111

## 4. Validation Criteria

- **[VAL-IMPL_MASTER-01] Reference Integrity**
  - [ ] All mandatory sub-rule links are valid and active.
- **[VAL-IMPL_MASTER-02] Modular Coverage**
  - [ ] No unique technical planning concept is left unaddressed across the rule set.
