---
status: completed
---

<!-- Target: docs/03.specs/120-agent-output-eval-ci-gate/README.md -->

# Agent Output Eval CI Gate

## Overview

This spec folder defines the lightweight CI adoption layer for the existing
agent-output eval fixture catalog and local advisory runner.

The gate checks fixture catalog and runner ID alignment in GitHub Actions. It
does not score arbitrary agent outputs, call models, inspect protected runtime
state, or make heuristic eval results authoritative.

## Audience

- QA engineers
- AI agents
- Documentation maintainers
- Repository governance maintainers

## Scope

### In Scope

- CI job for deterministic fixture catalog freshness.
- Stage 03/04 evidence for the CI gate adoption boundary.
- Audit-pack status synchronization for the former eval CI gate gap.

### Out of Scope

- Model-based evals.
- Required scoring gates for every agent response.
- Runtime, provider, Compose, credential, secret, raw-log, shell-history, or
  `.env` mutation.

## Structure

```text
docs/03.specs/120-agent-output-eval-ci-gate/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Keep this folder focused on the fixture freshness CI gate.
2. Use [spec.md](./spec.md) for the technical contract.
3. Record execution evidence in the paired Stage 04 task document.
4. Add a separate Stage 03/04 design before introducing required semantic
   scoring, model-based evals, or remote eval jobs.

## Related Documents

- **Spec**: [spec.md](./spec.md)
- **Parent Runner Spec**: [../116-agent-output-eval-runner/spec.md](../116-agent-output-eval-runner/spec.md)
- **Plan**: [../../04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md](../../04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md)
- **Task**: [../../04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md](../../04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md)
- **Fixture Reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
