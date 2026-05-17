---
layer: agentic
---

# CLAUDE.md

@AGENTS.md
@.claude/CLAUDE.md
@docs/00.agent-governance/providers/agents-md.md
@docs/00.agent-governance/providers/claude.md
@RTK.md

## Related Documents

- `AGENTS.md`
- `.claude/CLAUDE.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/providers/claude.md`

<!-- Thin Claude root shim. Shared policy lives in docs/00.agent-governance/. -->
<!-- Claude runtime bootstrap: .claude/CLAUDE.md -->
<!-- Agent/function catalog: docs/00.agent-governance/agents/ -->
<!-- Team runtime controls: .claude/settings.json and .claude/hooks/ -->

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
