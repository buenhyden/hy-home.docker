---
name: "test-authoring"
description: "Use when a behavioral contract or reproducible defect needs a witnessed RED test, minimal correction, GREEN result, and regression coverage."
metadata:
  title: "test-authoring"
  version: "1.3.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-13"
  function_id: "test-authoring"
  scope: "qa"
  owner_agent: "qa-engineer"
---

# test-authoring

## Purpose and Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

A behavioral contract and reproducible failure or not-yet-implemented expectation must be available before production edits.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Write one minimal test that demonstrates the required behavior and run it to witness the expected RED failure.
2. Implement or coordinate the smallest production change, then run the focused test to GREEN before refactoring.
3. Add boundary/regression cases, run the affected suite, and record exact commands and observed outcomes.

#### Gates

- The test is witnessed failing for the intended reason before implementation.
- Regression coverage includes the discovered boundary and keeps existing tests green.

### Failure Handling

If the failure cannot be reproduced or the fixture is nondeterministic, stop and isolate the environment rather than weakening assertions.

Separate a regression from an environment artifact before reporting either. A
suite invoked differently from the way its gate invokes it can fail on
import path, working directory, or a missing descriptor while the code under
test is correct. Reproduce the failure the way the contract runs it, and if the
two disagree, the disagreement is the finding.

## Inputs and Outputs

### Inputs

- Behavioral contract and failure reproduction.
- Existing test framework, fixtures, environment boundary, and acceptance criteria.
- The registered suites and how they are invoked, owned by the typed gate DAG in
  `.github/workflow-contract.yml`. A suite run outside that contract can fail for
  reasons the contract prevents, so a standalone invocation proves less than it
  appears to.

### Outputs

- Deterministic tests and RED/GREEN/regression evidence.

## Verification

### Checks

- The new test was run and failed for the intended reason before the implementation.
- The focused test then passes, and the affected suite stays green.
- The Task records the exact commands and observed outcomes.

### Completion and Handoff

Owning role and policies:

- [QA engineer](../../roles/qa-engineer.md)
- [E2E testing](../e2e-testing/SKILL.md)
- [QA scope](../../governance/quality-standards.md)
