---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-26-workspace-audit.md -->

# Workspace Audit 2026-05 Implementation Plan

## Overview

This document is the implementation plan for the May 2026 workspace-wide audit and improvement session. It defines execution order, verification criteria, and completion conditions for low-risk changes.

## Context

This audit is performed as part of the recurring workspace governance cycle. Three parallel Explore agents examined governance, infrastructure, CI/CD, hooks, and skills areas and identified 14 gaps. Low-risk gaps are implemented immediately, while medium/high-risk gaps are recorded as deferred.

## Goals & In-Scope

- **Goals**: Implement low-risk items from the Gap Registry, record medium/high-risk items as deferred, and create session tracking documents.
- **In Scope**: Session Spec/Plan/Task, 7 skill stubs, env/secrets key comparison reports, stage README lifecycle reinforcement, progress.md update, and verification execution.

## Non-Goals & Out-of-Scope

- **Non-goals**: Docker Compose runtime changes, CI/CD deployment behavior changes, or secret value changes.
- **Out of Scope**: GAP-01 (healthcheck), GAP-08 (CI workflow), GAP-11 (OPA).

## Work Breakdown

| Task    | Description                             | Files / Docs Affected                                                                                                         | Risk | Validation Criteria                              |
| ------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------------------ |
| PLN-001 | Create Session Spec/Plan/Task | `docs/03.specs/workspace-audit-2026-05/spec.md`, `plans/2026-05-26-workspace-audit.md`, `tasks/2026-05-26-workspace-audit.md` | Low  | Required template sections included |
| PLN-002 | Create 7 AI Agent skill stubs | `.claude/skills/*/skill.md` (7 files) | Low  | Each skill includes frontmatter and core sections |
| PLN-003 | Create env key comparison report | `docs/05.operations/guides/00-workspace/env-key-comparison.md` | Low  | No secret values, key names only |
| PLN-004 | Create secrets key comparison report | `docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md` | Low  | No secret values, IDs/paths only |
| PLN-005 | Reinforce Stage README lifecycle | `docs/03.specs/README.md`, `docs/04.execution/README.md`, `docs/05.operations/README.md`, `docs/90.references/README.md` | Low  | frontmatter status and Stage Handoff section added |
| PLN-006 | Add Execution/Specs index README links | `docs/04.execution/README.md`, `docs/03.specs/README.md` | Low  | New plan/task/spec file links included |
| PLN-007 | Update progress.md | `docs/00.agent-governance/memory/progress.md` | Low  | Audit session item recorded |

## Verification Plan

| ID          | Level      | Description                     | Command / How to Run                                | Pass Criteria |
| ----------- | ---------- | ------------------------------- | --------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural | Verify docs taxonomy contract | `bash scripts/validation/check-repo-contracts.sh` | exit 0 |
| VAL-PLN-002 | Structural | Verify document traceability | `bash scripts/validation/check-doc-traceability.sh` | exit 0 |
| VAL-PLN-003 | Manual | Confirm skill stubs exist | `ls .claude/skills/*/skill.md` | 7 files exist |
| VAL-PLN-004 | Manual | Confirm key comparison reports contain no secret values | Manual file review | No value column |

## Risks & Mitigations

| Risk                                      | Impact | Mitigation                      |
| ----------------------------------------- | ------ | ------------------------------- |
| Stage README edits break existing links | Medium | Keep existing sections and append only at the end |
| check-repo-contracts.sh fails to detect new files | Low | Verify and manually confirm |

## Completion Criteria

- [x] PLN-001 through PLN-007 completed
- [x] VAL-PLN-001 and VAL-PLN-002 passed
- [x] Medium/high-risk items recorded as deferred

## Related Documents

- **Spec**: [../../03.specs/workspace-audit-2026-05/spec.md](../../03.specs/workspace-audit-2026-05/spec.md)
- **Task**: [../tasks/2026-05-26-workspace-audit.md](../tasks/2026-05-26-workspace-audit.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
