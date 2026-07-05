---
layer: agentic
---

# e2e-testing

## Overview

End-to-end testing function for the `hy-home.docker` workspace. Validates the composed stack
at runtime through health checks and smoke tests across service boundaries.

## Purpose

Confirm that composed services start, become healthy, and satisfy cross-service smoke paths
before a change is considered done.

## Scope

**Covers:**

- Compose stack bring-up validation (config, dependency order, health)
- Service health-endpoint and smoke-path checks
- Read-only runtime inspection (`docker compose ps`, `docker inspect`, logs)

**Excludes:**

- Unit/integration tooling checks (see `test-automator`)
- Destructive or stateful test operations

## Structure

- Compose config validate → bring-up → health wait → smoke checks → evidence capture

## Agents

- **qa-engineer** — primary caller

## Skills

- Runtime mirror: `.claude/skills/e2e-testing/skill.md`

## Usage

- Trigger when validating end-to-end runtime behavior of the stack.
- **Inputs:** target compose project, smoke-path list
- **Outputs:** e2e evidence in `_workspace/repo-support/` and task docs

## Artifacts

- `_workspace/repo-support/e2e_<date>.md`

## Related Documents

- `../../scopes/common.md`
- `../../scopes/qa.md`
- `../functions/test-automator.md`
- `../README.md`
