---
trigger: model_decision
glob: ["**/*"]
description: "Technical Debt Management Standard: Enforces systematic identification, metrics-based prioritization, and actionable remediation of technical debt."
---

# Technical Debt Management Standard

- **Role**: Software Engineering Manager / Architect
- **Purpose**: Define standards for identifying, tracking, and paying down technical debt to ensure long-term codebase health and developer velocity.
- **Activates When**: Identifying code rot, refactoring legacy components, or planning technical debt remediation sprints.

**Trigger**: model_decision — Apply during the identification and remediation of technical inconsistencies and shortcuts.

## 1. Standards

### Principles

- **[REQ-DEBT-01] Conscious Accumulation**
  - Technical debt incurred deliberately (e.g., for speed-to-market) MUST be documented immediately with a target remediation date.
- **[REQ-DEBT-02] Metrics-Driven Prioritization**
  - Every identified debt item MUST be assessed using three core metrics: Ease (1-5), Impact (1-5), and Risk (1-5).
- **[REQ-DEBT-03] Debt Visibility**
  - All confirmed technical debt MUST be tracked as a primary work item (e.g., GitHub Issue with `tech-debt` label).

### Assessment Matrix

| Metric | 🔴 5 (Critical) | 🟡 3 (Medium) | 🟢 1 (Minimal) |
| --- | --- | --- | --- |
| Impact | Blocks features / 🔴 | Noticeable drag / 🟡 | Negligible drag / ⚪ |
| Risk | Security/Data loss / 🔴 | Performance jank / 🟡 | Style nitpick / ⚪ |
| Ease | Weeks/Months / 🔴 | 1-2 Days / 🟡 | < 1 Hour / ⚪ |

### Must

- **[REQ-DEBT-04] Remediation Phasing**
  - Remediation plans MUST include 5 sections: Overview, Explanation (Current vs Desired), Requirements, Implementation Steps, and Testing.
- **[REQ-DEBT-05] Capacity Allocation**
  - Engineering teams SHOULD allocate 10-20% of every sprint cycle to technical debt remediation.
- **[REQ-DEBT-06] "Definitions of Done" Alignment**
  - Debt items are only considered "Resolved" when they pass all associated unit and integration tests as defined in the remediation plan.

### Must Not

- **[BAN-DEBT-01] Silent Debt Accrual**
  - Code reviewers MUST NOT approve "Quick Hacks" or TODO markers without an accompanying tracking ticket.
- **[BAN-DEBT-02] Placeholder Remediation**
  - Remediation plans MUST NOT be generic; they must contain specific, actionable commit-level instructions.

### Failure Handling

- **Stop Condition**: Stop feature development if the "Accumulation Rate" (Debt in vs Debt out) shows a sustained negative trend that threatens system stability.

## 2. Procedures

- **[PROC-DEBT-01] Quarterly Debt Audit**
  - IF a new quarter begins THEN MUST perform a full inventory review of all open `tech-debt` issues to re-prioritize based on current product goals.
- **[PROC-DEBT-02] Issue Conversion**
  - Convert all long-standing `TODO` / `FIXME` comments in the codebase into formal tracking issues within one week of discovery.

## 3. Examples

### Debt Summary (Good)

```markdown
| Item | Component | Type | Ease | Impact | Risk | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Missing Auth Tests | Auth Svc | Testing | 3 🟡 | 5 🔴 | 4 🔴 | Critical |
```

## 4. Validation Criteria

- **[VAL-DEBT-01] Tracking Health**
  - [ ] 100% of open `tech-debt` issues contain an Ease/Impact/Risk assessment.
- **[VAL-DEBT-02] Paydown Velocity**
  - [ ] Sprint reports confirm that a portion of story points was consistently dedicated to debt resolution.
- **[VAL-DEBT-03] Resolution Quality**
  - [ ] audit of resolved items confirms that remediation actually matched the "Desired State" documented in the plan.
