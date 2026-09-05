---
name: "e2e-testing"
description: "Use when approved acceptance criteria need reproducible end-to-end scenarios through public interfaces within an authorized runtime boundary."
metadata:
  title: "e2e-testing"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "e2e-testing"
  scope: "qa"
  owner_agent: "qa-engineer"
---

# e2e-testing

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

Acceptance criteria, runnable boundary, deterministic fixture strategy, and runtime authority must be approved.

## Inputs

- Acceptance criteria and runnable system boundary.
- Test data, environment assumptions, health endpoints, and cleanup requirements.

## Procedure

1. Convert each user-visible acceptance criterion into an observable scenario with controlled setup and teardown.
2. Execute through public interfaces, capture only sanitized evidence, and distinguish product failures from environment failures.
3. Re-run the failing scenario to prove reproducibility, then run the focused suite after correction.

## Outputs

- End-to-end evidence with scenario, expected/actual result, and reproduction details.

## Gates

- Fixtures and timing are deterministic enough for repeat execution.
- Every reported defect includes a reproducible failure path.

## Failure Handling

Quarantine no test silently; isolate flaky environment dependencies and escalate with the smallest reproducible scenario.

## Related Documents

- [QA engineer](../../roles/qa-engineer.md)
- [Test authoring](../test-authoring/SKILL.md)
- [QA scope](../../governance/quality-standards.md)
