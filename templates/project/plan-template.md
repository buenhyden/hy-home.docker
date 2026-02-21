---
goal: "[One-sentence implementation goal]"
version: "1.0"
date_created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
owner: "[Team or owner]"
status: "Planned"
tags: ["implementation", "planning"]
stack: "[node | python | react | nextjs | go | rust | java]"
---

# [Feature/Component] Implementation Plan

*Target Directory: `specs/<feature>/plan.md`*

## 1. Context & Introduction

[Brief context and why this work is needed. Link to PRD/Spec if applicable.]

## 2. Goals & In-Scope

- **Goals:**
  - [Goal 1]
- **In-Scope (Scope of this Plan):**
  - [Item 1]

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - [Item 1]
- **Out-of-Scope:**
  - [Item 1]

## 4. Requirements & Constraints

*Note: Use Machine-Readable Identifiers (e.g., `[REQ-001]`) for traceability.*

- **Requirements:**
  - `[REQ-001]`: [Description]
- **Constraints:**

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | [Action] | `path/to/file` | [REQ-001] | [Binary pass/fail condition] |
| TASK-002 | [Action] | `path/to/file` | [REQ-002] | [Binary pass/fail condition] |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Unit | [e.g., test isolated function] | `npm run test:unit` | All pass |
| VAL-PLN-002 | Integration | [e.g., test API endpoint] | `pytest tests/api/` | All pass |
| VAL-PLN-003 | Lint/Build | [e.g., type check] | `npm run build` | Zero errors |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| [Risk Title] | [High/Med/Low] | [Action] |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/<feature>-prd.md` (Optional)
- **Spec**: `specs/<feature>/spec.md` (Optional)
- **ADRs**: `docs/adr/NNNN-...` (Optional)
