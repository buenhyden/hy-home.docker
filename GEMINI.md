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

Antigravity natively supports Workspace Rules, Skills, and Workflows within the `.agents/` directory.
While the agent catalog (`.agents/agents/`) and skill references (`.agents/skills/`) remain as pointers to the central governance in `docs/00.agent-governance/`, workspace-specific rules and workflows can be directly defined in `.agents/rules/` and `.agents/workflows/` respectively.

**Model Policy (Reasoning Effort)**
Antigravity IDE relies strictly on model selection for reasoning effort:
- **`gemini-3.1-pro`**: High reasoning tasks (Planning, Architecture, Refactor).
- **`gemini-3.5-flash`**: Standard/low reasoning tasks (Iteration, Documentation, Summarization).

## Related Documents

- `AGENTS.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/providers/gemini.md`
- `RTK.md`
