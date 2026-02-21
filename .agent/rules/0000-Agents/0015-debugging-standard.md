---
trigger: model_decision
glob: ["**/*"]
description: "Debugging Agent Standards: Enforces systematic defect isolation, hypothesis-driven investigation, and regression-proof verification."
---

# Debugging Agent Standards

- **Role**: Systematic Debugging Specialist
- **Purpose**: Define standards for identifying, isolating, and resolving software defects using rigorous abductive reasoning and binary search methodologies.
- **Activates When**: The user reports unexpected behavior, runtime crashes, or logic regressions in any part of the software ecosystem.

**Trigger**: model_decision — Apply during all defect investigation and remediation phases.

## 1. Standards

### Principles

- **[REQ-DBG-01] Systematic Root Cause Isolation**
  - Debugging MUST proceed via binary search or logical deduction. "Trial-and-error" or random patching is STRICTLY PROHIBITED.
- **[REQ-DBG-02] Hypothesis-Driven Investigation**
  - Every investigation MUST begin by generating a ranked list of hypotheses based on symptoms and evidence gathered from logs and code inspection.
- **[REQ-DBG-03] Mandatory minimal Reproduction**
  - Before applying a fix, the agent MUST create or identify a minimal reproduction case (test or script) that definitively demonstrates the defect.

### Investigation Baseline

| Step | Requirement ID | Critical Action |
| --- | --- | --- |
| Symptom | [REQ-DBG-04] | Capture exact error messages and logs |
| Hypothesis| [REQ-DBG-05] | Rank causes by likelihood and impact |
| Isolation | [REQ-DBG-06] | Bisect codebase to locate the regression |
| Fix | [REQ-DBG-07] | Apply minimal, focused patch |

### Must

- **[REQ-DBG-08] Verified Regression Prevention**
  - Every fix MUST be accompanied by a regression test that fails without the fix and passes with it.
- **[REQ-DBG-09] Explicit State Inspection**
  - IF the cause is opaque THEN the agent MUST add temporary, strategic logging or use debugger tools to inspect the program state.
- **[REQ-DBG-10] Documentation of Residual Risks**
  - Post-fix summaries MUST explicitly document any side-effects or residual risks introduced by the remediation.

### Must Not

- **[BAN-DBG-01] Assumption of Component Integrity**
  - DO NOT assume any component works as documented without verifying its state or output.
- **[BAN-DBG-02] Opaque "Magic" Fixes**
  - avoid applying broad, complex changes to "hide" symptoms rather than resolving the root cause.

### Failure Handling

- **Stop Condition**: Stop investigation if the reproduction case cannot be established or if the error appears to stem from an unmodifiable upstream dependency.

## 2. Procedures

- **[PROC-DBG-01] The RCA Loop**
  - IF a fix fails verification THEN MUST discard the previous hypothesis and generate a new investigative path based on the new evidence.
- **[PROC-DBG-02] Logging Cleanup**
  - UPON resolution THEN MUST remove all temporary debugging logs and ensure the final patch aligns with the project's "Clean Code" standards.

## 3. Examples

### Ranked Hypotheses (Good)

1. **DB Timeout**: High (Recent network drift).
2. **Race Condition**: Medium (Concurrent worker load).
3. **Logic Flaw**: Low (Unchanged module).

## 4. Validation Criteria

- **[VAL-DBG-01] Reproduction Success**
  - [ ] audit confirms that a failing test case was established before the fix was implemented.
- **[VAL-DBG-02] Fix Precision**
  - [ ] peer review confirms that the patch addresses only the root cause without unnecessary churn.
- **[VAL-DBG-03] Zero-Regression Pass**
  - [ ] build logs confirm that the new test and all existing tests pass after the fix.
