---
name: e2e-testing
description: >
  End-to-end runtime testing reference for hy-home.docker. Validates the composed stack via
  config checks, health waits, and cross-service smoke paths using read-only Docker inspection.
  Use for 'e2e', 'smoke test', 'stack health', 'runtime validation', 'compose up check'.
  Backs the qa-engineer agent. Note: unit/integration tooling checks live in the test-automator skill.
---

# End-to-End Testing — hy-home.docker

## When to Use

Use when validating end-to-end runtime behavior of the composed stack.

## Procedure

1. Validate Compose configuration and dependency order:

   ```bash
   docker compose config
   ```

2. Bring the target stack up and wait for health, then inspect read-only:

   ```bash
   docker compose ps
   docker inspect --format '{{.State.Health.Status}}' <container>
   ```

3. Execute smoke paths against healthy service endpoints; record pass/fail per path.
4. Capture evidence in `_workspace/repo-support/e2e_<date>.md`; promote to task docs when closing work.

## Rules

- Read-only inspection only; never run destructive or stateful operations.
- A service that never reaches healthy is a failure — report it, do not wait indefinitely.

## Related Documents

- `docs/00.agent-governance/agents/functions/e2e-testing.md`
- `docs/00.agent-governance/scopes/qa.md`
- `.claude/skills/test-automator/skill.md`
