# [Feature or Component] Plan

> Use this template for `docs/<category>/plans/YYYY-MM-DD-<feature-name>.md`.
>
> Repository-derived contract:
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Allowed plan status values: `Planned | In Progress | Completed | Superseded | Deprecated`.
> - Allowed scope values where your doc set uses them: `master | domain | historical`.
> - Every active plan must include explicit verification criteria.
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.
>
> Shape guidance:
> - Use the extended task-and-verification form for `content/` and `vault/`.
> - Use the compact implementation form when the plan is mainly a phased task ledger, as in the active `docs/web` V2 chain.

## Optional Frontmatter

```yaml
---
goal: '[One-sentence implementation goal]'
version: '1.0'
date_created: 'YYYY-MM-DD'
last_updated: 'YYYY-MM-DD'
owner: '[Repository Owner]'
status: '[Planned | In Progress | Completed | Superseded | Deprecated]'
scope: '[master | domain | historical]'
tags: ['implementation', 'planning']
stack: '[nextjs | node | python | go | rust | java]'
---
```

## H1 and Metadata

# [Feature or Component] Plan

> **Status**: [Planned | In Progress | Completed | Superseded | Deprecated]
> **Scope**: [master | domain | historical]
> **Parent Master Plan**: `[./YYYY-MM-DD-system-master-plan.md]` (Optional for `domain`)

**Overview (KR):** [Write a 1-2 sentence Korean summary of why this work exists, where it sits in the document hierarchy, and what this plan is trying to complete.]

## Required Core Sections

## Context & Introduction

[Explain why this work exists, where it sits in the document hierarchy, and whether it is an active implementation plan or a historical record.]

## Tasks

Use either a phase list or a traceability table.

### Phase-style task list

1. [Phase 1]
2. [Phase 2]
3. [Phase 3]

### Traceability-style task table

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | [Action] | `path/to/file` | REQ-001 | [Pass/fail evidence] |
| TASK-002 | [Action] | `path/to/file` | REQ-002 | [Pass/fail evidence] |

## Verification

List the commands, manual checks, or evidence collection steps required before the work can be considered complete.

- `[VAL-001]` [Verification step]
- `[VAL-002]` [Verification step]

## References

- `[../prd/feature-or-system-prd.md]`
- `[../specs/YYYY-MM-DD-feature.md]`
- `[../ard/system-or-domain-ard.md]`
- `[../adr/NNNN-decision.md]`

## Optional Extended Sections

## 2. Goals & In-Scope

- **Goals:**
  - [Goal 1]
  - [Goal 2]
- **In-Scope (Scope of this Plan):**
  - [File, document, or system 1]
  - [File, document, or system 2]

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - [Non-goal 1]
- **Out-of-Scope:**
  - [Out-of-scope item 1]

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-001]`: [Requirement 1]
  - `[REQ-002]`: [Requirement 2]
- **Constraints:**
  - [Constraint 1]
  - [Constraint 2]

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | [Action] | `path/to/file` | REQ-001 | [Pass/fail evidence] |
| TASK-002 | [Action] | `path/to/file` | REQ-002 | [Pass/fail evidence] |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | [Document or architecture check] | [Manual or command] | [Pass condition] |
| VAL-PLN-002 | Build / Test / Link | [What is being verified] | [Command] | [Pass condition] |
| VAL-PLN-003 | Manual / Operational | [Manual validation or walkthrough] | [How to inspect] | [Pass condition] |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| [Risk title] | [High | Medium | Low] | [Mitigation] |

## 8. Completion Criteria

- [ ] All scoped tasks completed
- [ ] Verification checks passed or failures documented
- [ ] Documentation and indexes updated where needed
