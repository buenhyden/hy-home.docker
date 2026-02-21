---
trigger: model_decision
glob: ["specs/**", "src/**", "tests/**"]
description: "Implementation Lifecycle Standards: Enforces the mandatory Plan -> Implement -> QA -> Document cycle for all feature development."
---

# Implementation Lifecycle Standards

- **Role**: Technical Lead & Process Guardian
- **Purpose**: Enforce a strict, distinct lifecycle for feature implementation to prevent "coding without planning" and "merging without verification."
- **Activates When**: The agent is asked to implement code, refactor logic, or fix bugs.

**Trigger**: model_decision — Apply during any coding task.

## 1. Standards

### Principles

- **[REQ-IMP-01] Plan-First Execution**
  - **Rule**: Code modification MUST NOT begin until a `specs/<feature>/plan.md` (or `implementation_plan.md` for refactors) exists and is up-to-date.
  - **Exception**: Trivial one-line fixes (typos) are exempt.
- **[REQ-IMP-02] Doc-Driven Traceability**
  - **Rule**: Every implemented function or module MUST trace back to a specific Requirement ID (`REQ-PRD-xxx` or `REQ-SPC-xxx`) from the approved documentation.
- **[REQ-IMP-03] Verification-First Completion**
  - **Rule**: A task cannot be marked "Complete" until verification (Unit Tests, Manual Verification, or Output Validation) has been performed and logged.
- **[REQ-IMP-04] Spec-Anchored Drift Prevention**
  - **Rule**: If the implementation diverges from the original plan, the `specs/` and `docs/` MUST be updated to reflect the true state of the code before proposing a merge.

### Lifecycle Phases

| Phase | Requirement ID | Mandatory Action |
| --- | --- | --- |
| **1. Planning** | [REQ-IMP-05] | Create/Update `plan.md`. Identify touched files. |
| **2. Coding** | [REQ-IMP-06] | Implement logic. Adhere to Code Style & Architecture standards. |
| **3. Verification** | [REQ-IMP-07] | Run tests. Fix regressions. Capture evidence. |
| **4. Drift Check** | [REQ-IMP-08] | Compare final code to `specs/`. Update specs if drifted. |
| **5. Documentation** | [REQ-IMP-09] | Update `walkthrough.md` with proof of work. |

### Must

- **[REQ-IMP-10] Explicit Context Loading**
  - The agent MUST explicitly `view_file` the PRD and Spec before writing a single line of code to ensure context aligment.
- **[REQ-IMP-11] Incremental Commits**
  - The agent MUST propose commits (or file writes) at logical break points (Plan -> Scaffolding -> Logic -> Tests), not one giant dump at the end.

### Must Not

- **[BAN-IMP-01] "Blind" Coding**
  - DO NOT generate code based solely on the user prompt. ALWAYS cross-reference with the established `specs/` or `docs/`.
- **[BAN-IMP-02] Verification Skipping**
  - DO NOT skip verification "because the change is simple." If it's simple, the test should be simple too.

## 2. Procedures

- **[PROC-IMP-01] The Planning Loop**
  - IF `plan.md` does not exist THEN create it using `templates/project/plan-template.md` (if available) or standard format BEFORE editing `src/`.
- **[PROC-IMP-02] The QA Loop**
  - IF tests fail THEN fix the code OR update the test (if requirements changed). NEVER delete the test to make it pass.
- **[PROC-IMP-03] The Drift Check Loop**
  - IF implementation details diverged from the initial `plan.md` or `spec.md` THEN MUST update the text of those spec files to match reality BEFORE declaring completion.

## 3. Validation Criteria

- **[VAL-IMP-01] Plan Existence**
  - [ ] `plan.md` exists and was updated within the current task window.
- **[VAL-IMP-02] Verification Evidence**
  - [ ] Terminal output or screenshot confirms successful test execution.
- **[VAL-IMP-03] Drift Sync**
  - [ ] Final `git diff` aligns exactly with the logical architecture described in the updated `specs/`.
