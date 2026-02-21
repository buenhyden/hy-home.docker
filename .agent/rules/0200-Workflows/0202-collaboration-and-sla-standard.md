---
trigger: model_decision
glob: ["COLLABORATING.md", "docs/manuals/collaboration-guide.md", ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/*.md"]
description: "Collaboration & SLA Standards: Enforces documented communication channels, decision ownership, and review SLAs."
---

# Collaboration & SLA Standards

- **Role**: Engineering Manager / Program Lead
- **Purpose**: Ensure the team has explicit, documented agreements for collaboration, response expectations, and decision-making so work can proceed without ambiguity.
- **Activates When**: Starting a new project, onboarding, or changing team process/review expectations.

## 1. Standards

### Principles

- **[REQ-COL-01] Single Source of Truth**
  - Collaboration agreements MUST be documented in `docs/manuals/collaboration-guide.md` using `templates/guides/collaboration-guide-template.md` and referenced by `COLLABORATING.md`.
- **[REQ-COL-02] Explicit SLA**
  - Communication channels MUST define an expected response SLA (hours/days) to prevent silent blocking.
- **[REQ-COL-03] Decision Ownership**
  - Decision-making ownership (e.g., PO, Tech Lead) MUST be explicitly documented to avoid deadlock.

### Must

- **[REQ-COL-04] Process Declaration**
  - The chosen delivery process (Scrum/Kanban/Hybrid) MUST be explicitly stated.
- **[REQ-COL-05] Review Expectations**
  - Code review expectations MUST be defined (minimum reviewers, required checks) and reflected in `.github/PULL_REQUEST_TEMPLATE.md`.
- **[REQ-COL-06] Issue Readiness**
  - Issue templates MUST capture at minimum: problem statement and measurable Acceptance Criteria (Given/When/Then).

### Must Not

- **[BAN-COL-01] Undocumented Policy Invention**
  - The agent MUST NOT invent or assume team SLAs, reviewers, or decision makers. If missing, the agent MUST request that the user/team define them in the collaboration guide.

## 2. Procedures

- **[PROC-COL-01] Kickoff Check**
  - When starting a new feature stream, verify that collaboration guide sections for Channels/SLA, Decision-Making, and Work Discipline exist and are non-empty.
- **[PROC-COL-02] Template Sync**
  - When collaboration rules change, update the PR/Issue templates to match (review requirements, DoR/DoD prompts).

## 3. Examples

### Good Example (SLA)

- "GitHub PRs: expected response within 24 business hours."

## 4. Validation Criteria

- [ ] **[VAL-COL-01]** `docs/manuals/collaboration-guide.md` defines channels + SLA and decision ownership.
- [ ] **[VAL-COL-02]** `.github/PULL_REQUEST_TEMPLATE.md` includes review/quality checklist items.
- [ ] **[VAL-COL-03]** `.github/ISSUE_TEMPLATE/*.md` includes Acceptance Criteria prompts (GWT).
