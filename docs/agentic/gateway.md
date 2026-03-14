---
layer: agentic
---

# Agent Instructions Gateway

Agent-specific context entrypoint for the `hy-home.docker` infrastructure workspace. Load this file at session start to discover relevant documentation families before doing any work.

**Core Instruction Set**: [instructions.md](instructions.md) - Behavioral standards.

## Discovery Protocol

- `[GATE-AGT-01]` Load this file first in any agent session.
- `[GATE-AGT-02]` Read category indexes via the map below.
- `[GATE-AGT-03]` Follow the consolidated [Behavioral Instructions](instructions.md).

## Lazy-Loading Map (By Category)

| Marker | Entry Point | Load when |
| --- | --- | --- |
| `[LOAD:ADR]` | [../adr/README.md](../adr/README.md) | Reviewing architecture decisions |
| `[LOAD:PRD]` | [../prd/README.md](../prd/README.md) | Reviewing requirements |
| `[LOAD:SPEC]` | [../specs/README.md](../specs/README.md) | Implementing or verifying specs |
| `[LOAD:RUNBOOK]` | [../runbooks/README.md](../runbooks/README.md) | Performing operational procedures |

## Intent-Based Discovery (Load Rule Files)

| Intent | Rule File | Marker |
| --- | --- | --- |
| **Refactoring Docs** | [rules/refactor-rule.md](rules/refactor-rule.md) | `[LOAD:RULES:REFACTOR]` |
| **Maintaining Docs** | [rules/doc-maintenance-rule.md](rules/doc-maintenance-rule.md) | `[LOAD:RULES:DOCS]` |
| **Infra Management** | [rules/lifecycle-rule.md](rules/lifecycle-rule.md) | `[LOAD:RULES:INFRA]` |
| **Persona Selection** | [rules/persona-rule.md](rules/persona-rule.md) | `[LOAD:RULES:PERSONA]` |
| **Incidents/Ops** | [rules/governance-rule.md](rules/governance-rule.md) | `[LOAD:RULES:OPS]` |

## Related Policy

- [../../AGENTS.md](../../AGENTS.md) — Cross-agent entrypoint
- [core-governance.md](core-governance.md) — Persona matrix and template contracts
- [workflow.md](workflow.md) — Execution loop
