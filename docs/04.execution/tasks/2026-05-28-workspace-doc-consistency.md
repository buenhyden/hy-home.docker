---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-28-workspace-doc-consistency.md -->

# Task: Workspace Documentation Consistency 2026-05

## Overview

This document is the implementation and verification task list for improving workspace documentation consistency and uniformity. It records 16 tasks derived from the `workspace-doc-consistency-2026-05` Spec and Plan in a traceable form. Each task is completed as an independent commit, and validation command results are recorded as Validation Evidence.

## Inputs

- **Parent Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/091-workspace-doc-consistency-2026-05/spec.md)
- **Parent Plan**: [2026-05-28 workspace doc consistency plan](../plans/2026-05-28-workspace-doc-consistency.md)

## Working Rules

- Perform only structure and format fixes. Do not change document body meaning.
- Before running `sed`, always confirm the current pattern with `grep`.
- After each phase, use validation commands to confirm zero remaining mismatches.
- Commit in Conventional Commits format after validation passes.
- Although this is documentation-only work, every task requires validation evidence.

## Task Table

| Task ID | Description                      | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                    | Owner | Status |
| ------- | -------------------------------- | ---- | --------------------- | ------------------- | -------------------------------------------------------- | ----- | ------ |
| T-000   | Check docs/99.templates baseline | doc | SPC / §Contracts | Phase 0 | Confirm Policy Scope and Agent Role sections exist | agent | Done |
| T-001   | Fix ADR title format (5 files) | doc | SPC / §Interfaces | Phase 1 | Empty result from `grep -v "ADR-[0-9]\{4\}:"` | agent | Done |
| T-002   | Fix ARD title format (5 files) | doc | SPC / §Interfaces | Phase 1 | Empty result from `grep -v "(ARD)"` | agent | Done |
| T-003   | Add missing PRD sections | doc | SPC / §Contracts | Phase 1 | 0 missing Overview(KR) and AI Agent Requirements sections | agent | Done |
| T-004   | Add Spec Agent Role N/A (15 files) | doc | SPC / §Agent Role | Phase 2 | Empty result from `grep -rL "## Agent Role" docs/03.specs/*/spec.md` | agent | Done |
| T-005   | Fix Task file title prefixes (4 files) | doc | SPC / §Interfaces | Phase 2 | 100% `# Task:` prefix coverage | agent | Done |
| T-006   | Unify Policy Scope heading (~50 files) | doc | SPC / §Interfaces | Phase 2 | Empty result from `grep -rl "^## Applies To" policies/` | agent | Done |
| T-007   | Complete Guides frontmatter/sections | doc | SPC / §Contracts | Phase 2 | 0 missing status frontmatter items (already complete) | agent | Done |
| T-008   | Complete Runbooks frontmatter | doc | SPC / §Contracts | Phase 2 | 0 missing status frontmatter items (already complete) | agent | Done |
| T-009   | Complete Incidents README links | doc | SPC / §Contracts | Phase 2 | Confirm template links are included (already complete) | agent | Done |
| T-010   | Fix hardening-lib.sh permissions | ops | SPC / §Tools | Phase 3 | `ls -la` -> `-rwxr-xr-x` | agent | Done |
| T-011   | Check use-qa-ci-tools.sh shebang | ops | SPC / §Tools | Phase 3 | POSIX sh syntax only -- no change required | agent | Done |
| T-012   | Update GitHub Actions SHAs | ops | SPC / §Tools | Phase 3 | zizmor validation passed | agent | Done |
| T-013   | Detect and fix broken links | doc | SPC / §Guardrails | Phase 4 | check-doc-traceability.sh passed -- 0 in scope | agent | Done |
| T-014   | Remove legacy/deprecated items | doc | SPC / §Guardrails | Phase 4 | No deprecated file references (0) | agent | Done |
| T-015   | Synchronize governance files | doc | SPC / §Contracts | Phase 4 | Confirm Policy Scope and ADR/ARD rules are explicit | agent | Done |

## Phase View

### Phase 0: Pre-flight (completed)

- [x] T-000 Check docs/99.templates baseline -- confirmed `## Policy Scope` and `## Agent Role` sections exist, and all status frontmatter is present

### Phase 1: Foundation -- Title and Format Mismatch Fixes (completed)

- [x] T-001 Fix ADR title format (5 files) -- commit `67d8a558`
- [x] T-002 Fix ARD title format (5 files) -- commit `db344d2e`
- [x] T-003 Add missing PRD sections -- commit `499ef652`

### Phase 2: Core Operations -- Bulk Repeated Fixes (completed)

- [x] T-004 Add Spec Agent Role N/A (15 files) -- commit `920300b1`
- [x] T-005 Fix Task file title prefixes (4 files) -- commit `3c7eb8eb`
- [x] T-006 Unify Policy Scope heading (50 files) -- commit `92fad3b7`
- [x] T-007 Complete Guides frontmatter/sections -- already complete (no change)
- [x] T-008 Complete Runbooks frontmatter -- already complete (no change)
- [x] T-009 Complete Incidents README links -- already complete (no change)

### Phase 3: Technical -- Scripts & CI/CD (completed)

- [x] T-010 Fix hardening-lib.sh permissions -- commit `c6bd6157`
- [x] T-011 Check use-qa-ci-tools.sh shebang -- POSIX sh is valid (no change)
- [x] T-012 Update GitHub Actions SHAs -- commit `e41704ab`

### Phase 4: Governance & Cleanup (completed)

- [x] T-013 Detect and fix broken links -- 0 in scope (no change)
- [x] T-014 Remove legacy/deprecated items -- 0 items (no change)
- [x] T-015 Synchronize governance files -- commit `d566ea97`

## Verification Summary

- **Test Commands**:

  ```bash
  # ADR
  grep "^# " docs/02.architecture/decisions/*.md | grep -v "ADR-[0-9]\{4\}:"
  # ARD
  grep "^# " docs/02.architecture/requirements/*.md | grep -v "(ARD)"
  # Spec Agent Role
  grep -rL "## Agent Role" docs/03.specs/*/spec.md
  # Policy Scope
  grep -rl "^## Applies To" docs/05.operations/policies/
  # Operations frontmatter
  find docs/05.operations -name "*.md" ! -name "README.md" | xargs grep -rL "^status:" | wc -l
  ```

- **Eval Commands**: N/A
- **Logs / Evidence Location**: git log for the `docs/workspace-doc-consistency-2026-05` branch

## Final Verification Evidence (2026-05-29)

| Check                             | Result            |
| --------------------------------- | ----------------- |
| ADR title format | PASS |
| ARD (ARD) suffix | PASS |
| Spec Agent Role section | PASS |
| Policy Scope heading | PASS |
| Operations status frontmatter | PASS (0 missing) |
| scripts/lib/hardening-lib.sh permissions | PASS (-rwxr-xr-x) |
| `check-repo-contracts.sh`         | PASS (failures=0) |
| `check-doc-traceability.sh`       | PASS (failures=0) |

## Related Documents

- **Parent Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/091-workspace-doc-consistency-2026-05/spec.md)
- **Parent Plan**: [2026-05-28 workspace doc consistency plan](../plans/2026-05-28-workspace-doc-consistency.md)
- **Upstream Audit**: [workspace-audit-2026-05 spec](../../03.specs/090-workspace-audit-2026-05/spec.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
