---
name: test-automator
description: >
  Test automation reference for hy-home.docker. Plans and runs unit/integration validation for
  Docker Compose services and repository tooling by reusing existing validation scripts.
  Use for 'test', 'integration test', 'validate service', 'QA check', 'test evidence'.
  Backs the qa-engineer agent. Note: runtime smoke tests live in the e2e-testing skill.
---

# Test Automation — hy-home.docker

## When to Use

Use when validating service or tooling changes before marking work complete.

## Procedure

1. Identify changed services and tooling from the diff.
2. Validate Compose integration:

   ```bash
   bash scripts/validation/validate-docker-compose.sh
   ```

3. Run repository contract checks for changed docs/config:

   ```bash
   bash scripts/validation/check-repo-contracts.sh
   ```

4. Capture results as task evidence under `docs/04.execution/tasks/` (template-first) or
   `_workspace/test_<date>.md` for intermediate runs.

## Rules

- Reuse existing scripts; do not introduce parallel test runners.
- Report failures with the failing command output; never mark complete on red.

## Related Documents

- `docs/00.agent-governance/agents/functions/test-automator.md`
- `docs/00.agent-governance/scopes/qa.md`
- `.claude/skills/e2e-testing/skill.md`
