---
layer: agentic
---

# Memory: Agentic Harness Contract Hardening

- Date: 2026-05-09
- Layer: agentic
- Tags: #harness #agentic #runtime #governance

## Problem

The workspace already had the main AI Agent-first engineering structure, but
the drift guard was weaker than the runtime contract. Future edits could change
agent models, scope imports, Codex boundaries, or source-leak references without
being caught by the repository contract check.

## Context

- Root shims are intentionally thin: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`
  route agents into `docs/00.agent-governance/`.
- `.claude` is the canonical runtime mirror for delegated agents and functions.
- `.codex` is a Codex-local hook and context surface, not a parallel delegated
  agent catalog.
- Governance policy and runtime catalog live under `docs/00.agent-governance/`.

## Resolution

- Preserved the thin root shim structure.
- Clarified the Codex runtime boundary in `.codex/README.md` and
  `providers/codex.md`.
- Strengthened `scripts/check-repo-contracts.sh` to verify agent/function mirror
  parity, runtime model hierarchy, exact scope imports, subagent protocol
  coverage, Codex boundary references, and stale source-reference prevention.

## Prevention

- Treat `.claude` and `docs/00.agent-governance/agents/` as the canonical
  delegated-agent mirror.
- Keep `.codex` limited to hooks, context wiring, and provider notes unless the
  repository explicitly adopts a separate Codex runtime catalog.
- Do not reintroduce external harness source labels or `H100` references.
- Run `bash scripts/check-repo-contracts.sh` after any runtime, provider, or
  governance edit.
