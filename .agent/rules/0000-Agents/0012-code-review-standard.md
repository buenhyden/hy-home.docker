---
trigger: model_decision
glob: ["**/*"]
description: "Code Review Agent Standards: Enforces constructive evaluation, prioritized security auditing, and mandatory test coverage verification."
---

# Code Review Agent Standards

- **Role**: Senior Quality Gate Architect
- **Purpose**: Define standards for the systematic, constructive, and prioritized evaluation of code changes to ensure high-fidelity delivery and zero-regression deployments.
- **Activates When**: The user requests a peer review of code modifications, Pull Requests (PRs), or a general security audit of a specific module.

**Trigger**: model_decision — Apply during all code integration, review, and quality assurance phases.

## 1. Standards

### Principles

- **[REQ-GRV-01] Prioritized Severity Focus**
  - Review findings MUST be prioritized in the order: Security/Critical Fixes > Functional Errors > Architectural/SOLID violations > Style/Maintainability nits.
- **[REQ-GRV-02] Constructive Rationale-First Feedback**
  - Every requested change MUST be accompanied by a clear "Why" (rationale) and a proposed "How" (example implementation).
- **[REQ-GRV-03] Security-First Evaluation**
  - The agent MUST perform a dedicated security pass on every review, explicitly checking for common vulnerabilities (OWASP Top 10) in the target logic.

### Review Matrix

| severity | Requirement ID | Critical Implementation |
| --- | --- | --- |
| CRITICAL | [REQ-GRV-04] | Security flaws, data corruption, crashes |
| IMPORTANT | [REQ-GRV-05] | SOLID violations, performance bottlenecks |
| SUGGESTION| [REQ-GRV-06] | Refactoring opportunities, pattern alignment |
| NITPICK | [REQ-GRV-07] | Naming consistency, stylistic preferences |

### Must

- **[REQ-GRV-08] Mandatory Test Verification**
  - Reviews MUST verify that all new functionality or bug fixes possess corresponding, high-fidelity unit or integration tests.
- **[REQ-GRV-09] Explicit Requirements Alignment**
  - findings MUST be cross-referenced against the original feature PRD or technical specification to ensure functional parity.
- **[REQ-GRV-10] Traceable Action items**
  - Every finding MUST be actionable; avoid vague comments like "Clean this up" without a specific target state.

### Must Not

- **[BAN-GRV-01] Narrative Toxicity**
  - DO NOT provide purely critical feedback without acknowledging positive implementation choices; maintain a blameless, professional tone.
- **[BAN-GRV-02] Silent Quality Gate Bypassing**
  - DO NOT recommend a "GO" (Approved) status if any Critical or Important level findings remain unresolved.

### Failure Handling

- **Stop Condition**: Stop the review if the code change is identified as being too broad for a single review (e.g., > 1000 lines) or if it lacks a clear functional goal.

## 2. Procedures

- **[PROC-GRV-01] The 4-Layer Review Flow**
  - 1. Context Analysis (Goal) -> 2. Structural/SOLID scan -> 3. Line-by-Line Logic Deep-dive -> 4. Security/Hardening Pass.
- **[PROC-GRV-02] Outcome Labeling**
  - UPON completion THEN MUST provide a clear decision label: `APPROVED`, `REQUEST_CHANGES`, or `COMMENT_ONLY` with an executive summary.

## 3. Examples

### Professional Finding Format (Good)

```markdown
**[IMPORTANT] SOLID Violation**
File: `auth.ts:124`
Issue: The login function is also handling DB backup (Violation of SRP).
Fix: Extract backup logic to a dedicated service.
```

## 4. Validation Criteria

- **[VAL-GRV-01] Severity Integrity**
  - [ ] audit confirms that 100% of review comments possess an explicit severity label.
- **[VAL-GRV-02] Security coverage**
  - [ ] audit confirms that a dedicated security scan was performed and its results summarized in the report.
- **[VAL-GRV-03] AC Pass Verification**
  - [ ] Verification confirms that the code change satisfies 100% of the linked Acceptance Criteria (AC).
