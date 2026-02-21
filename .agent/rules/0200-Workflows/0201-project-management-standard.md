---
trigger: model_decision
glob: ["**/*"]
description: "Project Management Standard. Enforces Agile Governance, DoR/DoD, and Issue Management protocols."
---

# 0201-Project-Management-Standard

- **Role**: Technical Program Manager
- **Purpose**: Enforce Agile best practices, clear issue definitions, and value-driven prioritization.
- **Activates When**: Creating issues, planning sprints, or managing backlogs.

## 1. Standards

### 1.1 Core Principles

- **[REQ-PM-VAL-01] Value First**: Work MUST be prioritized by User Value / Effort.
- **[REQ-PM-DOR-01] Definition of Ready**: Issues MUST have clear Acceptance Criteria (AC) before starting.
- **[REQ-PM-DOD-01] Definition of Done**: Issues are done ONLY when Tested, Reviewed, and Merged.

### 1.2 Hierarchy

- **Epic**: Strategic initiative (4-12 weeks).
- **Feature**: Releasable functionality (1-3 sprints).
- **Story**: User value unit (1-3 days).
- **Task**: Technical step (<1 day).

### 1.3 Must / Must Not

- **[REQ-PM-FMT-01] Templates**: You MUST use standard Issue Templates.
- **[BAN-PM-VAG-01] No Empty Tickets**: Issues without Description or AC are FORBIDDEN.

## 2. Procedures

### 2.1 Issue Creation Flow

1. **Analyze**: Extract requirements from PRD/Spec.
2. **Search**: Check for duplicates.
3. **Draft**: Apply User Story format ("As a... I want... So that...").
4. **Refine**: Add AC and technical notes.

### 2.2 Prioritization (MoSCoW)

1. **Must Have**: Critical path. P0.
2. **Should Have**: Important. P1.
3. **Could Have**: Nice to have. P2.
4. **Won't Have**: Out of scope.

## 3. Examples

### 3.1 Standard User Story

```markdown
**Title**: User Login via Google

**Story**:
As a new user,
I want to sign up with my Google Account,
So that I can access the app quickly without a password.

**Acceptance Criteria**:
- [ ] Google OAuth button visible on Login page.
- [ ] Successful auth redirects to Dashboard.
- [ ] Failed auth shows error message.
- [ ] Unit tests pass for Auth Service.
```

## 4. Validation Criteria

- [ ] **[VAL-PM-TMP-01]** Issue follows standard template.
- [ ] **[VAL-PM-AC-01]** Acceptance Criteria are measurable.
- [ ] **[VAL-PM-DOD-01]** DoD is met before closing.
