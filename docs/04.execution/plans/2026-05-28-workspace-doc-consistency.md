---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-28-workspace-doc-consistency.md -->

# Workspace Documentation Consistency 2026-05 Implementation Plan

## Overview

This document is the implementation plan for improving workspace documentation consistency and uniformity. It fixes inconsistencies identified by the `workspace-audit-2026-05` audit across 5 phases, separating each phase into an independent commit to preserve traceability and rollbackability.

## Context

The `workspace-audit-2026-05` audit found the following inconsistencies across the docs/01 through docs/05 layers and technical infrastructure:

- docs/02.architecture: title-format mismatch in 5 ADRs and 5 ARDs
- docs/03.specs: Agent Role & IO Contract section missing from 15 files
- docs/05.operations/policies: `## Applies To` vs `## Policy Scope` heading mismatch in about 50 files
- docs/05.operations/{guides,policies,runbooks}: frontmatter `status:` field compliance at 60%
- scripts/lib/hardening-lib.sh: executable permission missing (644)
- .github/workflows/: GitHub Actions SHAs pinned to v3/v4-era hashes

The purpose is to remove drift between the documents AI Agents consult during work and the actual files.

## Goals & In-Scope

- **Goals**:
  - Ensure all ADR/ARD titles comply with governance rule format.
  - Ensure all spec files include the Agent Role section.
  - Ensure all policy files use the `## Policy Scope` heading.
  - Bring operations docs frontmatter status compliance to 100%.
  - Refresh GitHub Actions SHAs.
  - Bring governance rule files up to date.
- **In Scope**: docs/01~05, scripts/, .github/workflows/, docs/00.agent-governance/rules/

## Non-Goals & Out-of-Scope

- **Non-goals**: Revising documentation body content or reflecting new requirements.
- **Out of Scope**: Docker Compose changes, secret/env changes, and substantive docs/99.templates edits.

## Work Breakdown

| Task ID | Description                     | Files / Docs Affected                                      | Target REQ  | Validation Criteria                      |
| ------- | ------------------------------- | ---------------------------------------------------------- | ----------- | ---------------------------------------- |
| PLN-000 | Confirm docs/99.templates baseline | 19 template files (read-only) | VAL-SPC-007 | Policy Scope and Agent Role criteria confirmed |
| PLN-001 | Fix ADR title format | decisions/0003, 0009, 0010, 0011, 0026 | VAL-SPC-001 | `grep -v "ADR-[0-9]\{4\}:"` returns empty output |
| PLN-002 | Fix ARD title format | requirements/0002, 0003, 0006, 0012, 0026 | VAL-SPC-002 | `grep -v "(ARD)"` returns empty output |
| PLN-003 | Fill missing PRD sections | selected docs/01.requirements/\*.md files | VAL-SPC-007 | Overview(KR), AI Agent Requirements at 100% |
| PLN-004 | Add Spec Agent Role N/A | 15 docs/03.specs/\*/spec.md files | VAL-SPC-003 | 0 missing Agent Role sections |
| PLN-005 | Fix Task file title prefixes | tasks/2026-03-26-{07,08,09,10}-\*.md | VAL-SPC-007 | `# Task:` prefix at 100% |
| PLN-006 | Standardize Policy Scope headings | about 50 policies/\*_/_.md files | VAL-SPC-004 | 0 remaining `## Applies To` headings |
| PLN-007 | Strengthen Guides frontmatter and sections | selected guides/\*_/_.md files | VAL-SPC-005 | 0 missing status frontmatter entries |
| PLN-008 | Strengthen Runbooks frontmatter | selected runbooks/\*_/_.md files | VAL-SPC-005 | 0 missing status frontmatter entries |
| PLN-009 | Strengthen Incidents README links | incidents/README.md | VAL-SPC-007 | Template links included |
| PLN-010 | Fix hardening-lib.sh permissions | scripts/lib/hardening-lib.sh | VAL-SPC-006 | ls -la shows -rwxr-xr-x |
| PLN-011 | Check use-qa-ci-tools.sh shebang | scripts/operations/use-qa-ci-tools.sh | VAL-SPC-007 | Bash shebang present when bash-only syntax is used |
| PLN-012 | Refresh GitHub Actions SHAs | 5 .github/workflows/\*.yml files | VAL-SPC-007 | zizmor validation passes |
| PLN-013 | Detect and fix broken links | Relative-path links across docs/ | VAL-SPC-008 | check-doc-traceability.sh passes |
| PLN-014 | Remove legacy/deprecated entries | selected files with status: deprecated | VAL-SPC-007 | No deprecated-file references remain |
| PLN-015 | Synchronize governance files | rules/documentation-protocol.md, stage-authoring-matrix.md | VAL-SPC-007 | Policy Scope and ADR/ARD rules documented |

## Verification Plan

| ID          | Level       | Description                   | Command / How to Run                                                                             | Pass Criteria         |
| ----------- | ----------- | ----------------------------- | ------------------------------------------------------------------------------------------------ | --------------------- |
| VAL-PLN-001 | Structural  | ADR title format compliance | `grep "^# " docs/02.architecture/decisions/*.md \| grep -v "ADR-[0-9]\{4\}:"` | Empty result, excluding README |
| VAL-PLN-002 | Structural  | ARD `(ARD)` suffix compliance | `grep "^# " docs/02.architecture/requirements/*.md \| grep -v "(ARD)"` | Empty result, excluding README |
| VAL-PLN-003 | Structural  | Spec Agent Role section | `grep -rL "## Agent Role" docs/03.specs/*/spec.md` | Empty result |
| VAL-PLN-004 | Structural  | Policy Scope heading | `grep -rl "^## Applies To" docs/05.operations/policies/` | Empty result |
| VAL-PLN-005 | Structural  | Operations status frontmatter | `find docs/05.operations -name "*.md" ! -name "README.md" \| xargs grep -rL "^status:" \| wc -l` | 0                     |
| VAL-PLN-006 | Technical   | scripts executable permission | `ls -la scripts/lib/hardening-lib.sh \| grep "^-rwxr-xr-x"`                                      | PASS                  |
| VAL-PLN-007 | Integration | repo contracts                | `bash scripts/validation/check-repo-contracts.sh`                                                | exit 0                |
| VAL-PLN-008 | Integration | doc traceability              | `bash scripts/validation/check-doc-traceability.sh`                                              | exit 0                |

## Risks & Mitigations

| Risk                                     | Impact | Mitigation                                             |
| ---------------------------------------- | ------ | ------------------------------------------------------ |
| sed patterns change unexpected lines | High | Confirm patterns with grep before execution and review git diff afterward |
| Bulk replacement fails across about 50 Policy files | Medium | Split execution by domain folder and validate each stage |
| CI fails after GitHub Actions SHA upgrades | Medium | Run local zizmor validation after SHA replacement and confirm CI in PR |
| frontmatter is inserted at the wrong position | Low | Check frontmatter existence first and handle missing files separately |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A
- **Sandbox / Canary Rollout**: N/A
- **Human Approval Gate**: Review git diff after each Phase commit.
- **Rollback Trigger**: `git revert <commit>` or `git reset --hard HEAD~N`
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [ ] All tasks PLN-000 through PLN-015 completed
- [ ] All checks VAL-PLN-001 through VAL-PLN-008 passed
- [ ] `bash scripts/validation/check-repo-contracts.sh` exit 0
- [ ] `bash scripts/validation/check-doc-traceability.sh` exit 0
- [ ] Each Phase committed in Conventional Commits format

## Related Documents

- **Upstream Audit Spec**: [workspace-audit-2026-05 spec](../../03.specs/workspace-audit-2026-05/spec.md)
- **Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Task**: [2026-05-28 workspace doc consistency tasks](../tasks/2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
- **Operations**: [Operations index](../../05.operations/README.md)
