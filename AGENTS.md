---
layer: agentic
---

# AGENTS.md

Universal entry shim for agent execution and Codex/GPT fallback in `hy-home.docker`.

Workspace purpose: shared harness-engineering and agent-first engineering over modular Docker Compose infrastructure and stage-gated documentation.

## 1. Bootstrap Sequence

- Load `[LOAD:RULES:BOOTSTRAP]` from `docs/00.agent-governance/rules/bootstrap.md`.
- Review `[LOAD:MEMORY]` from `docs/00.agent-governance/memory/README.md` and `docs/00.agent-governance/memory/progress.md`; update `progress.md` during repository work.

## 2. Graphify

- After modifying code files, run `graphify update .` when the CLI is available; if `graphify` is unavailable, report that graph refresh was skipped.

## 3. Quick Reference

- **Governance Hub:** `docs/00.agent-governance/`
- **Agent Catalog:** `docs/00.agent-governance/agents/`
- **Codex Provider Notes:** `docs/00.agent-governance/providers/codex.md`

## 4. Detailed Instructions

For specific guidelines, see:
- [Agentic Rules](docs/00.agent-governance/rules/agentic.md)
- [Task Checklists](docs/00.agent-governance/rules/task-checklists.md)
- [Environment Constraints](docs/00.agent-governance/rules/environment-constraints.md)
- [Subagent Protocol](docs/00.agent-governance/subagent-protocol.md)
- [GitHub Governance](docs/00.agent-governance/rules/github-governance.md)

This file is an entry shim. Shared governance, clarification duty, model policy,
Template Contract rules, QA/CI gates, and Codex harness boundaries live in
Stage 00. Do not add provider-local policy here.

## Related Documents

- `RTK.md`
- `docs/00.agent-governance/README.md`
- `.codex/README.md`
