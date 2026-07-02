---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-02-governance-optimization.md -->

# Task: Governance Optimization (I1+I2)

> Implementation and verification work record for the governance optimization round (I1+I2).

## Overview

This document tracks the task list and verification evidence for the governance
optimization round. It records the changed files for I1 and I2 work derived from
the Parent Plan and the contract-check results that were executed.

## Inputs

- **Parent Plan**: [Execution plan](../plans/2026-06-02-governance-optimization.md)
- **Parent Spec**: N/A -- governance/documentation optimization has no separate `docs/03.specs/` spec chain.

## Working Rules

- Every change must keep contract checks at `failures=0`.
- Documentation-only work also leaves verification evidence (commands and results).
- Stage only task-owned paths. Do not touch unrelated changes.

## Task Table

| Task ID | Description                              | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                       | Owner               | Status |
| ------- | ---------------------------------------- | ---- | --------------------- | ------------------- | ------------------------------------------- | ------------------- | ------ |
| T-001   | Create the security-hardening built-in service seed | impl | N/A                   | PLN-001             | `yaml.safe_load` OK, contract check `failures=0` | workflow-supervisor | Done   |
| T-002   | Register service scaffold template plus 4 files | doc  | N/A                   | PLN-002             | `check-repo-contracts.sh` `failures=0`      | workflow-supervisor | Done   |
| T-003   | Write the new service onboarding guide | doc  | N/A                   | PLN-003             | guide normalization passed, `failures=0`    | workflow-supervisor | Done   |
| T-004   | Codify the code-review request/acceptance loop | doc  | N/A                   | PLN-004             | `check-repo-contracts.sh` `failures=0`      | workflow-supervisor | Done   |
| T-005   | Inject the generated-artifact freshness contract into the QA scope | doc  | N/A                   | PLN-005             | `check-repo-contracts.sh` `failures=0`      | workflow-supervisor | Done   |

## Suggested Types

- `impl`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001 Create service seed
- [x] T-002 Template + registration

### Phase 2

- [x] T-003 Onboarding guide
- [x] T-004 Code-review loop

## Verification Summary

- **Test Commands**: `bash scripts/validation/check-repo-contracts.sh`, `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A -- not a model/agent evaluation target.
- **Logs / Evidence Location**: Both checks reported `failures=0`. The seed compose passed `yaml.safe_load`.

## Related Documents

- **Parent Plan**: [Execution plan](../plans/2026-06-02-governance-optimization.md)
- **Service template**: [Service scaffold template](../../99.templates/templates/spec-contracts/service.template.md)
- **Operations**: [New-service onboarding guide](../../05.operations/guides/00-workspace/new-service-onboarding.md)
