---
layer: agentic
---

# GEMINI.md

Antigravity 2.0 IDE & Gemini native root shim. Shared policy lives in `docs/00.agent-governance/`.

## 1. Quick Reference

- **Antigravity Governance:** `docs/00.agent-governance/`
- **Agent Catalog:** `docs/00.agent-governance/agents/`
- **Memory Log:** `docs/00.agent-governance/memory/progress.md`

## 2. Detailed Instructions

For specific guidelines, see:
- [Universal Entry Shim](AGENTS.md)
- [Gemini/Antigravity Provider Notes](docs/00.agent-governance/providers/gemini.md)
- [Agentic Rules](docs/00.agent-governance/rules/agentic.md)
- [Environment Constraints](docs/00.agent-governance/rules/environment-constraints.md)

## 3. IDE Integration

Antigravity natively supports Workspace Rules, Skills, and Workflows.
This repository defines them centrally in `docs/00.agent-governance/`. Agents running via Antigravity MUST directly consult the central governance rather than relying on legacy proxy folders like `.agents/`.

## Related Documents

- `AGENTS.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/providers/gemini.md`
- `RTK.md`
