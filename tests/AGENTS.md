---
title: "Tests Agent Guide"
version: "0.1.0"
type: "governance/agent-guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-03"
---

# Tests Agent Guide

## Overview

`tests/` holds repository-wide tests. `tests/lib/<domain>/` mirrors the
library units in `scripts/lib/<domain>/`, and `tests/validation/` covers
entrypoints and execution context. This guide routes an agent that adds or
changes a test. The human guide is [README.md](README.md).

## Scope

`tests/lib/`, `tests/validation/`, `tests/fixtures/` and
`tests/requirements-integration.txt`. Package-local tests under `projects/`
belong to their package.

## Working Rules

- Check `scripts/` and package scripts for an existing check before adding a
  test.
- Place a library test in the mirroring `tests/lib/<domain>/` module and an
  entrypoint test in `tests/validation/`.
- Register every new test module in its suite in `.github/workflow-contract.yml`.
  The full profile must reach each module exactly once,
  which `tests/lib/test_surface_ownership.py` enforces.
- Build fixtures with `_fixtures.py`-style builders in a temporary directory;
  add `tests/fixtures/` only for input a builder cannot reproduce.
- A RED/GREEN test fails without the change it proves; confirm that before
  recording it.
- Delete a test only when the behavior it checks is removed, and replace a
  removed fail-closed check.
- Opt-in integration tests skip unless `HYHOME_INTEGRATION=1`; report a skip
  as `NOT_RUN`, never as a live pass.

## Canonical References

- [Bootstrap](../.agents/governance/bootstrap.md),
  [quality standards](../.agents/governance/quality-standards.md),
  [task checklists](../.agents/governance/task-checklists.md).
- Role: [`qa-engineer`](../.agents/roles/qa-engineer.md).
- Skills: [`test-authoring`](../.agents/skills/test-authoring/SKILL.md),
  [`e2e-testing`](../.agents/skills/e2e-testing/SKILL.md).
- Prompt: [test design](../.agents/prompts/test-design.md).
- Provider loading: [Claude adapter](../.claude/provider.md),
  [Codex adapter](../.codex/provider.md).

## Verification

- `python3 -m unittest tests.lib.test_surface_ownership`
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
- `python3 scripts/validation/check-script-manifest.py`

## Related Documents

- [Tests README](README.md)
- [Scripts agent guide](../scripts/AGENTS.md)
