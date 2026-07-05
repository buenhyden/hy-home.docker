---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md -->

# Workspace Doc & Governance Consistency (2026-05b) Implementation Plan

## Overview

This document is the implementation plan for the workspace governance consistency follow-up work (2026-05b). It stages governance rule formalization, validation script expansion, template normalization, and small documentation fixes identified after PR #89, and defines completion criteria.

## Context

PR #89 (`workspace-doc-consistency-2026-05`) completed large-scale structural consistency work. This follow-up targets the following items:

- R4 (Operations Profile Compliance) and R5 (Frontmatter Status), which are already applied in practice, are not codified in `documentation-protocol.md`.
- `github-governance.md` lacks a CI/CD job taxonomy section.
- The `check-repo-contracts.sh` guide profile check verifies only `## Usage` and does not verify `## Common Checks` or `## Runbook Handoff`.
- guide.template.md and runbook.template.md are missing from the template list in `docs/99.templates/README.md`.
- `agent-design.template.md` examples use imaginary filenames.
- `docs/05.operations/policies/01-gateway/nginx.md` contains a duplicate `## Policy Scope` heading.

## Goals & In-Scope

- **Goals**:
  - Add R4 and R5 rules to `documentation-protocol.md`.
  - Add CI/CD job taxonomy section (Section 8) to `github-governance.md`.
  - Strengthen guide profile checks in `check-repo-contracts.sh`.
  - Update the template list in `docs/99.templates/README.md`.
  - Replace example filenames in `agent-design.template.md`.
  - Remove the duplicate heading in `nginx.md`.
- **In Scope**: `docs/00.agent-governance/rules/`, `scripts/validation/`, `docs/99.templates/`, `docs/05.operations/policies/01-gateway/`

## Non-Goals & Out-of-Scope

- **Non-goals**: Revising documentation body content or reflecting new requirements.
- **Out of Scope**: docs/01~04 structural changes, Docker Compose changes, or secret/env changes.

## Work Breakdown

| Task ID | Description                                          | Files / Docs Affected                                      | Target REQ  | Validation Criteria                                |
| ------- | ---------------------------------------------------- | ---------------------------------------------------------- | ----------- | -------------------------------------------------- |
| PLN-001 | Add R4+R5 rules to documentation-protocol.md | `docs/00.agent-governance/rules/documentation-protocol.md` | VAL-SPC-001 | R4 and R5 sections exist |
| PLN-002 | Add Section 8 CI/CD taxonomy to github-governance.md | `docs/00.agent-governance/rules/github-governance.md` | VAL-SPC-002 | Section 8 exists |
| PLN-003 | Strengthen check-repo-contracts.sh guide profile checks | `scripts/validation/check-repo-contracts.sh` | VAL-SPC-003 | `## Common Checks` and `## Runbook Handoff` checks are included |
| PLN-004 | Add docs/99.templates/README.md template list entries | `docs/99.templates/README.md` | VAL-SPC-004 | guide.template.md and runbook.template.md are listed |
| PLN-005 | Replace agent-design.template.md example filenames | `docs/99.templates/templates/spec-contracts/agent-design.template.md` | VAL-SPC-004 | No imaginary filenames; directory links are used |
| PLN-006 | Remove duplicate Policy Scope heading in nginx.md | `docs/05.operations/policies/01-gateway/nginx.md` | VAL-SPC-005 | 0 duplicate headings |

## Verification Plan

| ID          | Level       | Description               | Command / How to Run                                                        | Pass Criteria      |
| ----------- | ----------- | ------------------------- | --------------------------------------------------------------------------- | ------------------ |
| VAL-PLN-001 | Structural  | R4/R5 rules exist | `grep -c "R4\|R5" docs/00.agent-governance/rules/documentation-protocol.md` | >=2 |
| VAL-PLN-002 | Structural  | CI/CD taxonomy section exists | `grep "CI/CD" docs/00.agent-governance/rules/github-governance.md` | Results exist |
| VAL-PLN-003 | Structural  | Guide profile checks are strengthened | `grep "Common Checks" scripts/validation/check-repo-contracts.sh` | Results exist |
| VAL-PLN-004 | Integration | Verify repo contracts | `bash scripts/validation/check-repo-contracts.sh` | exit 0, failures=0 |
| VAL-PLN-005 | Integration | Verify doc traceability | `bash scripts/validation/check-doc-traceability.sh` | exit 0, failures=0 |

## Risks & Mitigations

| Risk                           | Impact | Mitigation                                              |
| ------------------------------ | ------ | ------------------------------------------------------- |
| Script strengthening breaks existing files | Medium | Check affected files before strengthening and edit those files together if needed |
| Rule numbering conflicts after additions | Low | Check the existing rule numbering system and assign the next number |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A
- **Sandbox / Canary Rollout**: N/A
- **Human Approval Gate**: Review git diff after each phase commit.
- **Rollback Trigger**: `git revert <commit>` or `git reset --hard HEAD~N`
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] All tasks PLN-001 through PLN-006 completed
- [x] All checks VAL-PLN-001 through VAL-PLN-005 passed
- [x] `bash scripts/validation/check-repo-contracts.sh` exit 0
- [x] `bash scripts/validation/check-doc-traceability.sh` exit 0
- [x] Each change committed in Conventional Commits format

## Related Documents

- **Spec**: [workspace-consistency-2026-05b spec](../../03.specs/092-workspace-consistency-2026-05b/spec.md)
- **Task**: [2026-05-29 workspace consistency 2026-05b tasks](../tasks/2026-05-29-workspace-consistency-2026-05b.md)
- **Predecessor Plan**: [2026-05-28 workspace doc consistency plan](./2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
- **Operations**: [Operations index](../../05.operations/README.md)
