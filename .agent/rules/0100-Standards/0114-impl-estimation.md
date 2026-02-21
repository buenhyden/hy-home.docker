---
trigger: always
glob: ["**/plan/**/*.md"]
description: "Implementation plan estimation and work item hierarchy: enforces Fibonacci-based story points and T-shirt sizing for features and epics."
---

# Implementation Plan Estimation & Work Hierarchy

- **Role**: Technical Program Manager
- **Purpose**: Define the standards for estimating work effort and organizing the hierarchy of implementation work items.
- **Activates When**: Estimating or scoping work items in `**/plan/**/*.md`.

**Trigger**: always — Apply these estimation standards consistently to ensure predictable delivery timelines.

## 1. Standards

### Principles

- **[REQ-IMPL_EST-01] Relative Sizing**
  - Estimation MUST be done relatively using a Fibonacci scale.
- **[REQ-IMPL_EST-02] INVEST Compliance**
  - All stories MUST meet the INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable) criteria.
- **[REQ-IMPL_EST-03] Hierarchical Alignment**
  - Work items MUST be assigned to the appropriate level of the hierarchy (Epic > Feature > Story > Task).

### Scope

- **In-Scope**: Fibonacci scale, T-shirt sizing, work item hierarchy, and priority matrix.
- **Out-of-Scope**: Real-time tracking and individual developer capacity planning.

### Outputs

- Implementation plans MUST include estimates (points or sizes) for all major work items.

### Must

- **[REQ-IMPL_EST-04] Fibonacci points**
  - Stories MUST be estimated using: 1, 2, 3, 5, 8.
- **[REQ-IMPL_EST-05] Breakdown Threshold**
  - Stories estimated at 13+ points MUST be broken down into smaller stories.
- **[REQ-IMPL_EST-06] Priority Assignment**
  - Every feature/story MUST have a priority (P0 to P3) based on value and impact.

### Must Not

- **[BAN-IMPL_EST-01] Absolute Time Estimation**
  - Level 1-3 work items MUST NOT be estimated in absolute hours (use points instead).
- **[BAN-IMPL_EST-02] Over-Scoping**
  - Individual stories MUST NOT span more than 5 days of development time.

### Failure Handling

- **Stop Condition** Stop estimation if a story is too large to be understood.
- **Action**: Break down the story further into atomic units.

### Style

- Use standard Agile terminology.
- Use tables for point-to-complexity comparisons.

## 2. Procedures

- **[PROC-IMPL_EST-01] Story Breakdown**
  - Analyze requirements and identify independent units of user value.
- **[PROC-IMPL_EST-02] Consensus Planning**
  - Establish a shared understanding of 1-point and 5-point "anchor" tasks before estimating new work.

## 3. Examples

### Point Comparison

- **1 Point**: Simple CSS update or text change.
- **5 Points**: Full user workflow with API and DB changes.

## 4. Validation Criteria

- **[VAL-IMPL_EST-01] Estimation Consistency**
  - [ ] All work items follow the Fibonacci or T-shirt scale.
- **[VAL-IMPL_EST-02] Granularity Balance**
  - [ ] No single story exceeds the 8-point limit.
- **[VAL-IMPL_EST-03] Priority Completeness**
  - [ ] All features and stories have assigned priorities.
