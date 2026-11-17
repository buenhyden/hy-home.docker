---
title: "Tests Agent Guide"
version: "0.4.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Tests Agent Guide

## Scope

### Allowed Scope

#### Allowed Surface

`tests/` holds repository-wide tests. `tests/lib/<domain>/` mirrors the
library units in `scripts/lib/<domain>/`, and `tests/validation/` covers
entrypoints and execution context. This guide routes an agent that adds or
changes a test. The human guide is [README.md](README.md).

`tests/lib/`, `tests/validation/`, `tests/fixtures/` and
`tests/requirements-integration.txt`.

#### Non-goals

Package-local tests under `projects/` belong to their package.

### Instruction Precedence

The canonical owners under Intake outrank this guide: when this guide and an
owner disagree, the owner wins and this guide is corrected.
[Bootstrap](../.agents/governance/bootstrap.md#authority-and-precedence)
sets the full precedence order; a folder guide routes only and never overrides
canonical governance or a Stage contract.

## Workflow

### Intake

- [Bootstrap](../.agents/governance/bootstrap.md),
  [quality standards](../.agents/governance/quality-standards.md),
  [task checklists](../.agents/governance/task-checklists.md).
- Role: [`qa-engineer`](../.agents/roles/qa-engineer.md).
- Skills: [`test-authoring`](../.agents/skills/test-authoring/SKILL.md),
  [`e2e-testing`](../.agents/skills/e2e-testing/SKILL.md).
- Prompt: [test design](../.agents/prompts/test-design.md).
- Provider loading: [Claude adapter](../.claude/provider.md),
  [Codex adapter](../.codex/provider.md).

### Execution

#### Inspect and Change

- Check `scripts/` and package scripts for an existing check before adding a
  test.
- Build fixtures with `_fixtures.py`-style builders in a temporary directory;
  add `tests/fixtures/` only for input a builder cannot reproduce.

#### Local Obligations

- Place a library test in the mirroring `tests/lib/<domain>/` module and an
  entrypoint test in `tests/validation/`.
- Register every new test module in its suite in `.github/workflow-contract.yml`.
  The full profile must reach each module exactly once,
  which `tests/lib/test_surface_ownership.py` enforces.
- A RED/GREEN test fails without the change it proves; confirm that before
  recording it.
- Opt-in integration tests skip unless `HYHOME_INTEGRATION=1`; report a skip
  as `NOT_RUN`, never as a live pass.

## Boundaries

### Authority

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../.agents/governance/approval-boundaries.md)
has not granted, or when a required check fails.

### Secrets and External Effects

- Delete a test only when the behavior it checks is removed, and replace a
  removed fail-closed check.

## Verification

### Checks

- `python3 -m unittest tests.lib.test_surface_ownership`
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
- `python3 scripts/validation/check-script-manifest.py`

### Reporting

#### Evidence and Limits

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

#### Handoff

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Tests README](README.md)
- [Scripts agent guide](../scripts/AGENTS.md)
