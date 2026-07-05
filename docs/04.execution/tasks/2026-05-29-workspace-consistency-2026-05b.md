---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md -->

# Task: Workspace Doc & Governance Consistency (2026-05b)

## Overview

This document is the implementation and verification task list for the workspace governance consistency follow-up work (2026-05b). It records 6 tasks derived from the `workspace-consistency-2026-05b` Spec and Plan in a traceable form. Each task is completed as an independent commit, and validation command results are recorded as Validation Evidence.

## Inputs

- **Parent Spec**: [workspace-consistency-2026-05b spec](../../03.specs/092-workspace-consistency-2026-05b/spec.md)
- **Parent Plan**: [2026-05-29 workspace consistency 2026-05b plan](../plans/2026-05-29-workspace-consistency-2026-05b.md)

## Working Rules

- Perform only structure and format fixes. Do not change document body meaning.
- Check the current state of target files before changes.
- After each change, use validation commands to confirm zero remaining mismatches.
- Commit in Conventional Commits format after validation passes.
- Although this is documentation-only work, every task requires validation evidence.

## Task Table

| Task ID | Description                                          | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                   | Owner | Status |
| ------- | ---------------------------------------------------- | ---- | --------------------- | ------------------- | ------------------------------------------------------- | ----- | ------ |
| T-001   | Add R4+R5 rules to documentation-protocol.md | doc | SPC / §Contracts | PLN-001 | Confirm R4 and R5 sections exist | agent | Done |
| T-002   | Add Section 8 CI/CD taxonomy to github-governance.md | doc | SPC / §Contracts | PLN-002 | Confirm Section 8 CI/CD taxonomy exists | agent | Done |
| T-003   | Strengthen guide profile checks in check-repo-contracts.sh | ops | SPC / §Contracts | PLN-003 | Confirm `## Common Checks` and `## Runbook Handoff` checks are included | agent | Done |
| T-004   | Add template list to docs/99.templates/README.md | doc | SPC / §Interfaces | PLN-004 | Confirm guide.template.md and runbook.template.md entries exist | agent | Done |
| T-005   | Replace example filenames in agent-design.template.md | doc | SPC / §Interfaces | PLN-005 | Confirm no virtual filenames and directory links are used | agent | Done |
| T-006   | Remove duplicate Policy Scope heading from nginx.md | doc | SPC / §Interfaces | PLN-006 | Confirm 0 duplicate headings | agent | Done |

## Phase View

### Phase 1: Governance Rule Additions (completed)

- [x] T-001 Add R4+R5 rules to documentation-protocol.md
- [x] T-002 Add Section 8 CI/CD taxonomy to github-governance.md

### Phase 2: Script Extension (completed)

- [x] T-003 Strengthen guide profile checks in check-repo-contracts.sh

### Phase 3: Template & Doc Fixes (completed)

- [x] T-004 Add template list to docs/99.templates/README.md
- [x] T-005 Replace example filenames in agent-design.template.md
- [x] T-006 Remove duplicate Policy Scope heading from nginx.md

## Verification Summary

- **Test Commands**:

  ```bash
   # R4/R5 rules exist
  grep -c "R4\|R5" docs/00.agent-governance/rules/documentation-protocol.md

   # CI/CD taxonomy section exists
  grep "CI/CD" docs/00.agent-governance/rules/github-governance.md

   # Guide profile checks strengthened
  grep "Common Checks" scripts/validation/check-repo-contracts.sh

  # repo contracts
  bash scripts/validation/check-repo-contracts.sh

  # doc traceability
  bash scripts/validation/check-doc-traceability.sh
  ```

- **Eval Commands**: N/A
- **Logs / Evidence Location**: git log for the `docs/workspace-consistency-2026-05b` branch

## Final Verification Evidence

| Check                                               | Result            |
| --------------------------------------------------- | ----------------- |
| R4/R5 rules exist (documentation-protocol.md) | PASS |
| CI/CD taxonomy section exists (github-governance.md) | PASS |
| Guide profile checks strengthened (check-repo-contracts.sh) | PASS |
| nginx.md duplicate heading removed | PASS |
| `check-repo-contracts.sh`                           | PASS (failures=0) |
| `check-doc-traceability.sh`                         | PASS (failures=0) |

## Related Documents

- **Parent Spec**: [workspace-consistency-2026-05b spec](../../03.specs/092-workspace-consistency-2026-05b/spec.md)
- **Parent Plan**: [2026-05-29 workspace consistency 2026-05b plan](../plans/2026-05-29-workspace-consistency-2026-05b.md)
- **Predecessor Task**: [2026-05-28 workspace doc consistency tasks](./2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
