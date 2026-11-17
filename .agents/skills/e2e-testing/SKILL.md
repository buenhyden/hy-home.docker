---
name: "e2e-testing"
description: "Use when approved acceptance criteria need reproducible end-to-end scenarios through public interfaces within an authorized runtime boundary."
metadata:
  title: "e2e-testing"
  version: "1.3.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-17"
  function_id: "e2e-testing"
  scope: "qa"
  owner_agent: "qa-engineer"
---

# e2e-testing

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Acceptance criteria, runnable boundary, deterministic fixture strategy, and runtime authority must be approved.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Convert each user-visible acceptance criterion into an observable scenario with controlled setup and teardown.
2. Execute through public interfaces, capture only sanitized evidence, and distinguish product failures from environment failures.
3. Re-run the failing scenario to prove reproducibility, then run the focused suite after correction.

#### Gates

- Fixtures and timing are deterministic enough for repeat execution.
- Every reported defect includes a reproducible failure path.

#### Inputs

- Acceptance criteria and runnable system boundary.
- Test data, environment assumptions, health endpoints, and cleanup requirements.

### Failure Handling

Quarantine no test silently; isolate flaky environment dependencies and escalate with the smallest reproducible scenario.

## Outputs

### Artifacts

- End-to-end evidence with scenario, expected/actual result, and reproduction details.

### Handoff

Owning role, policies and related documents:

- [QA engineer](../../roles/qa-engineer.md)
- [Test authoring](../test-authoring/SKILL.md)
- [QA scope](../../governance/quality-standards.md)

## Verification

### Checks

- Each acceptance criterion maps to a scenario with its expected and actual result.
- A failing scenario fails again on re-run before it is reported as a defect.
- After correction, the focused suite passes and the evidence holds no secret or unsanitized output.

### Limits

This skill records no limit on what its checks prove.
