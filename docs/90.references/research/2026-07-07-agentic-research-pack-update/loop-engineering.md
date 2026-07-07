---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/loop-engineering.md -->

# Reference: Loop Engineering and Feedback Systems

## Overview

This reference documents the loop engineering framework in `hy-home.docker`, explaining how inner agent execution, outer validation gates, and human approval cycles form automated feedback loops.

## Purpose

Define the iterative cycles that control agent execution, code modification, and user check gates to guarantee repeatable and verifiable outcomes.

## Repository Role

This document provides a conceptual reference for loop systems. It does not replace or modify active CI/CD configurations (`ci-quality.yml`), pre-commit hooks, or local validation scripts.

## Scope

### In Scope

- Concepts of inner agent loop, validation loop, CI loop, and human feedback loop
- Multi-provider (Claude, Codex, Gemini) hook integration and loop parity
- Evaluation of loop execution depth and remaining gaps

### Out of Scope

- Directly updating GitHub Actions workflow definitions
- Altering Git Hook scripts or commit-time hooks
- Ingestion of sensitive system logs or credentials

## Definitions / Facts

- **Loop Engineering**: An iterative system engineering approach where agent outputs are captured, validated by scripts, and fed back to the agent for self-correction (observe -> plan -> execute -> verify).
- **Claude Code Loop**: Utilises deep ReAct loops and automatically runs `agent-event-hook.sh` after tool executions to feed results back into the agent's context window.
- **Codex Loop**: Executes local validators immediately upon tool completion based on configurations in `.codex/hooks.json`, parsing stdout/stderr errors for the agent.
- **Gemini Loop**: Heavily relies on human-in-the-loop validation and prompt-driven self-evaluation, as native post-tool hook integration is less mature in Gemini's standard environment.
- **Implementation Status & Gaps**:
  - *Status*: A strong plan-to-task pipeline (`implementation_plan.md` -> user approval -> execution -> verification evidence) is enforced, backed by remote CI quality check gates.
  - *Gaps*: The workspace lack a semantic agent output evaluation gate in the CI pipeline; only a local advisory runner (`run-agent-output-eval-fixtures.sh`) and a fixture freshness check exist. Also, hook triggers are inconsistent across IDE-based provider runtimes.

## Sources

- [QA scope](../../../00.agent-governance/scopes/qa.md) - QA/CI loop and validation gate policies
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - Remote CI check gates
- [Post tool validate hook](../../../../scripts/hooks/post-tool-validate.sh) - Post-tool normalisation hook
- [Agent event hook dispatcher](../../../../scripts/hooks/agent-event-hook.sh) - Provider-neutral hook dispatcher

## Maintenance

- **Owner**: DevOps & Workflow Specialist
- **Review Cadence**: Review when CI workflows, validation gates, or Git hooks are restructured
- **Update Trigger**: Update when new hook dispatchers are implemented or when automated evaluation gates are introduced

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [harness-engineering.md](./harness-engineering.md)
