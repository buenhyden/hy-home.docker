---
layer: agentic
---

# Agent Instructions Gateway

**Overview (KR):** `hy-home.docker` 인프라 워크스페이스의 에이전트 전용 컨텍스트 진입점입니다. 세션 시작 시 이 파일을 로드하여 관련 문서 제품군을 탐색하십시오.

**Core Instruction Set**: [2026-03-15-agent-instructions.md](2026-03-15-agent-instructions.md) - Behavioral standards.

## Discovery Protocol

- `[GATE-AGT-01]` Load this file first in any agent session.
- `[GATE-AGT-02]` Read category indexes via the map below.
- `[GATE-AGT-03]` Follow the consolidated [Behavioral Instructions](2026-03-15-agent-instructions.md).
- `[GATE-AGT-04]` Select intent from the **Intent-Based Discovery** table and load the corresponding rule.

## Lazy-Loading Map (By Category)

| Marker | Entry Point | Load when |
| --- | --- | --- |
| `[LOAD:ADR]` | [../adr/README.md](../adr/README.md) | Reviewing architecture decisions |
| `[LOAD:ARD]` | [../ard/README.md](../ard/README.md) | Reviewing architectural requirements |
| `[LOAD:PRD]` | [../prd/README.md](../prd/README.md) | Reviewing product/system requirements |
| `[LOAD:SPECS]` | [../specs/README.md](../specs/README.md) | Implementing or verifying specs |
| `[LOAD:PLANS]` | [../plans/README.md](../plans/README.md) | Executing or updating implementation plans |
| `[LOAD:RUNBOOKS]` | [../runbooks/README.md](../runbooks/README.md) | Performing operational procedures |
| `[LOAD:OPS]` | [../operations/README.md](../operations/README.md) | Reviewing operational history |

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
- [2026-03-15-agent-workflow.md](2026-03-15-agent-workflow.md) — Execution loop
