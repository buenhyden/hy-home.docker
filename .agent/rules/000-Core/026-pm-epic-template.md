---
trigger: always_on
glob: "**/*.md"
description: "PM: Advanced Epic and User Story templates for Agile documentation."
---

# Epic & User Story Standards

## 1. Epic Structure (The "Investment")

Epics represent significant business value and require detailed strategic context.

```markdown
# Epic: [Concise Title]

## Strategic Context
[Why this, why now? Link to company goals.]

## Business Value & Metrics
- **Goal**: [Qualitative Goal]
- **KPIs**: [Quantitative Metrics, e.g., Increase conversion by 5%]

## Target Personas
- **[Role]**: [Impact description]

## Scope (In/Out)
- [x] **In Scope**: [Feature A, Feature B]
- [ ] **Out of Scope**: [Feature C]

## Technical Considerations
- [Architecture changes, Security, Performance constraints]

## Dependencies
- [Internal/External dependencies]

## Roadmap
- **Priority**: [P0/P1]
- **Target**: [Q3 Release]
```

## 2. User Story Structure (The "Deliverable")

Stories must be **INVEST** (Independent, Negotiable, Valuable, Estimable, Small, Testable).

```markdown
# Story: [Action-oriented Title]

## Narrative
**As a** [Persona],
**I want to** [Action],
**So that** [Benefit].

## Acceptance Criteria (AC)
- [ ] **Scenario 1**: [Given/When/Then]
- [ ] **Scenario 2**: [Edge Case]
- [ ] **Scenario 3**: [Error Handling]

## Design & Technical Notes
- [Figma Link]
- [API Spec Link]

## Definition of Done (DoD)
- [ ] Unit Tests passed
- [ ] Accessibility Checked
- [ ] Analytics Events added
```

## 3. Best Practices

- **User-Centric**: Describe the *problem*, not just the solution.
- **Measurable AC**: "Fast" is bad. "Under 200ms" is good.
- **Slicing**: Break down Epics into stories that fit in a sprint.
