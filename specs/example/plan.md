---
goal: 'Provide a template-compliant example spec and plan for reference.'
version: '1.0'
date_created: '2026-02-24'
last_updated: '2026-02-24'
owner: 'Example'
status: 'Planned'
tags: ['implementation', 'planning', 'example']
stack: 'python'
---

# Example Spec Implementation Plan

_Target Directory: `specs/example/plan.md`_

## 1. Context & Introduction

This plan exists only as a reference example for how to format specs and plans.

## 2. Goals & In-Scope

- **Goals:**
  - Provide a full template-compliant example spec.
  - Provide a matching example plan.
- **In-Scope (Scope of this Plan):**
  - `specs/example/spec.md`
  - `specs/example/plan.md`

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - No production changes.
- **Out-of-Scope:**
  - No code or infra changes.

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-001]`: Example spec must follow `templates/engineering/spec-template.md`.
  - `[REQ-002]`: Example plan must follow `templates/project/plan-template.md`.
- **Constraints:**
  - Example content only; do not implement.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Write example spec | `specs/example/spec.md` | [REQ-001] | All template sections present |
| TASK-002 | Write example plan | `specs/example/plan.md` | [REQ-002] | Plan template valid |

## 6. Verification Plan

| ID          | Level       | Description | Command / How to Run | Pass Criteria |
| ----------- | ----------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Docs        | Manual review | N/A | All sections present |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Example confused as real spec | Low | Clear example labeling |

## 8. Completion Criteria

- [ ] Example spec/plan created
- [ ] Example clearly labeled

## 9. References

- **Spec Source**: `archive/specs-legacy/example-spec.md`
