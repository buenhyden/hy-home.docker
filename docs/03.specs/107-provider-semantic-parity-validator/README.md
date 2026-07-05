---
status: active
---

<!-- Target: docs/03.specs/107-provider-semantic-parity-validator/README.md -->

# Provider Semantic Parity Validator

> Stage 00 provider adapter semantic parity contract

## Overview

This folder defines the technical contract for enforcing semantic parity across
Claude, Codex, and Gemini provider adapter surfaces.

The validator closes the gap where provider adapters can be structurally
synchronized while still drifting from the canonical Stage 00 agent role scope.

## Audience

This README is for:

- Agentic Workflow Specialists
- QA Engineers
- Documentation Specialists
- Repository Maintainers

## Scope

### In Scope

- Canonical agent role scope extraction from Stage 00 agent catalog entries.
- Codex TOML adapter generation from the canonical role scope.
- Gemini pointer adapter frontmatter generation from the canonical role scope.
- Repository validation for Claude, Codex, Gemini, and subagent-protocol scope
  parity.

### Out of Scope

- Model policy changes.
- Hook behavior changes.
- Provider runtime configuration changes outside generated adapter files.
- Secret values, credentials, tokens, private keys, raw logs, shell history, or
  `.env` values.

## Structure

```text
107-provider-semantic-parity-validator/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Use [spec.md](./spec.md) as the implementation contract.
2. Keep execution ordering and evidence in the linked Stage 04 plan and task.
3. Treat provider adapters as generated or runtime-facing surfaces; do not
   redefine Stage 00 catalog policy inside provider files.
4. Re-run provider sync and repo contracts after any provider adapter metadata
   change.

## Related Documents

- [Spec](./spec.md)
- [Provider capability matrix](../../00.agent-governance/rules/provider-capability-matrix.md)
- [AGENTS.md provider-neutral notes](../../00.agent-governance/providers/agents-md.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
- [Implementation plan](../../04.execution/plans/2026-07-05-provider-semantic-parity-validator.md)
- [Task evidence](../../04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md)
