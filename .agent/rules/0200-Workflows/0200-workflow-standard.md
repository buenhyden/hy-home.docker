---
trigger: model_decision
glob: [".git/**", "**/CONTRIBUTING.md", "**/PULL_REQUEST_TEMPLATE.md", "src/**"]
description: "Workflow & Project Management Standards: Enforces Git branching (Conventional), issue refinement (AC/JTBD), and automated PR quality gates."
---

# Workflow & Project Management Standards

- **Role**: Lead Project Manager / DevOps Governance
- **Purpose**: Define standards for the software development lifecycle (SDLC), project management workflows, and version control protocols to ensure traceability, consistency, and high-quality delivery.
- **Activates When**: Creating project work items (Issues/Epics), performing sprint refinement, or managing Git branches and Pull Requests.

**Trigger**: model_decision — Apply during all project planning and execution phases.

## 1. Standards

### Principles

- **[REQ-WRK-01] Traceable SDLC Identity**
  - Every code change MUST be traceable to a specific, refined project work item (Issue/Task). Ad-hoc changes without a parent issue are PROHIBITED.
- **[REQ-WRK-02] Conventional Branch & Commit Discipline**
  - Continuous Delivery MUST be supported by a linear Git history. Branches MUST follow `<type>/<id>-<desc>` and commits MUST follow the "Conventional Commits" standard.
  - **Technical Implementation**: Refer to [.agent/skills/git-commit/SKILL.md](../../.agent/skills/git-commit/SKILL.md) for enforcement logic.
- **[REQ-WRK-03] Acceptance-Driven Refinement**
  - Project items MUST NOT be marked "Ready for Development" until they possess explicit, measurable Acceptance Criteria (AC) and a linked technical specification.
- **[REQ-WRK-11] QA-Ready Spec Gate**
  - Work MUST NOT start until the Spec defines QA requirements:
    - `templates/engineering/spec-template.md` Section 0 (Quality/Testing/Security checklist)
    - Spec Section 7 (Verification Plan: Unit/Integration/E2E/Load + coverage targets, with `N/A (reason: ...)` where applicable)
  - See `.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md` for minimum QA standards.

### Workflow Baseline

| Phase | Requirement ID | Mandatory Standard |
| --- | --- | --- |
| Intake | [REQ-WRK-04] | PRD/Spec alignment before Issue creation |
| Refinement | [REQ-WRK-05] | Given-When-Then (GWT) formats for AC |
| Branching| [REQ-WRK-06] | Feature branching with `<type>/<id>-desc` |
| Review | [REQ-WRK-07] | Max 500 LOC per PR / Peer Approval |

### Must

- **[REQ-WRK-08] Explicit Priority Classification**
  - All project issues MUST be classified by priority (Critical, High, Medium, Low) based on business value and blocking status.
- **[REQ-WRK-09] Automated Quality Gate Pass**
  - Pull Requests MUST pass all automated CI/CD checks (Lint, Test, Security) before being eligible for peer review or merge.
- **[REQ-WRK-10] Blameless Release Logic**
  - Use feature flags and phased rollouts for high-risk changes to separate "Deployment" (code move) from "Release" (user activation).

### Must Not

- **[BAN-WRK-01] Silent Merge Adoption**
  - DO NOT merge code that lacks an associated PR description or one that bypasses the project's standardized review templates.
- **[BAN-WRK-02] Indefinite 'Draft' Retention**
  - DO NOT keep PRs in "Draft" state for more than 48 hours without a status update or conversion to a "Wait" state.

### Failure Handling

- **Stop Condition**: Stop refinement if an issue is identified as being too broad (Epic masquerading as Task) or lacking verifiable success metrics.

## 2. Procedures

- **[PROC-WRK-01] The Refinement Loop**
  - IF an issue is ambiguous THEN MUST apply the `needs-clarification` label and return it to the refinement queue for AC enrichment.
- **[PROC-WRK-02] Conflict Resolution Flow**
  - IF a merge conflict arises THEN MUST resolve it in the feature branch and re-verify through local tests before resubmitting for review.

## 3. Examples

### Clean Issue Breakdown (Good)

```markdown
## Feature: User Authentication
**Problem**: Users cannot login via JWT.
**Acceptance Criteria**:
- Given a valid email/pass, When I login, Then I receive a JWT.
- Given an expired token, When I access /api, Then I receive a 401.
```

## 4. Validation Criteria

- **[VAL-WRK-01] Traceability success rate**
  - [ ] audit confirms that 100% of commits in the main branch map to a closed project issue.
- **[VAL-WRK-02] CI/CD Gate Compliance**
  - [ ] GitHub project logs confirm that zero PRs were merged with failing status checks.
- **[VAL-WRK-03] Lead Time Accuracy**
  - [ ] Sprint reports confirm that "Ready for Dev" items align with the team's capacity and definition of "Ready".
