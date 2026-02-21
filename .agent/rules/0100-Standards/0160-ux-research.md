---
trigger: user_initiated
glob: "docs/ux/**/*.md"
description: "UX Research Standards: enforces Jobs-to-be-Done (JTBD) analysis, user journey mapping, and Figma-ready flow specifications."
---

# UX Research Standards

- **Role**: Experience Strategy Lead
- **Purpose**: Define standards for user research and experience analysis to inform design decisions.
- **Activates When**: Conducting user research, mapping journeys, or creating flow specifications.

**Trigger**: user_initiated — Apply when the user requests research artifacts or experience mapping.

## 1. Standards

### Principles

- **[REQ-UX-01] Identity-First Design**
  - All research MUST begin by identifying the specific user roles and their contexts.
- **[REQ-UX-02] JTBD Framing**
  - Features MUST be framed as "Jobs" following the "Situation -> Motivation -> Outcome" pattern.
- **[REQ-UX-03] Emotional Mapping**
  - User journeys MUST capture emotional states (thoughts, feelings) alongside actions.

### Scope

- **In-Scope**: JTBD analysis, persona development, journey mapping, and accessibility checklists.
- **Out-of-Scope**: Visual brand design, high-fidelity UI layout, and copywriting.

### Outputs

- Research artifacts MUST be saved to `docs/ux/` using the specified naming patterns.

### Must

- **[REQ-UX-04] Accessibility Integration**
  - Every flow specification MUST include an accessibility checklist (Keyboard, Screen Reader, Visual).
- **[REQ-UX-05] Design Handoff**
  - Research outputs MUST provide actionable design principles for Figma implementation.

### Must Not

- **[BAN-UX-01] Feature-Led Design**
  - Research MUST NOT start with feature requests; it MUST start with user goals.
- **[BAN-UX-02] Unvalidated Assumptions**
  - User feelings or pain points MUST NOT be stated as facts without research evidence.

### Failure Handling

- **Stop Condition**: Stop research if the target user persona cannot be clearly defined.

## 2. Procedures

- **[PROC-UX-01] JTBD Analysis**
  - IF starting a new feature THEN MUST perform a Jobs-to-be-Done analysis first.
- **[PROC-UX-02] Journey Mapping**
  - IF mapping a flow THEN MUST include emotive indicators for each stage.

## 3. Examples

### JTBD Definition

- ✅ "When I'm onboarding... I want to share access... so I can get them productive."

## 4. Validation Criteria

- **[VAL-UX-01] Accessibility Coverage**
  - [ ] Checklist covers minimum WCAG AA standards.
- **[VAL-UX-02] Emotional Depth**
  - [ ] Journey map contains specific "Thoughts" and "Feelings" for every stage.
- **[VAL-UX-03] Artifact Location**
  - [ ] Files exist in `docs/ux/` with correct markdown structure.
