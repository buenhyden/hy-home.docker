---
layer: agentic
---

# CLAUDE.md

@AGENTS.md
@.claude/CLAUDE.md
@docs/00.agent-governance/providers/agents-md.md
@docs/00.agent-governance/providers/claude.md

<!-- Runtime bootstrap: .claude/CLAUDE.md -->
<!-- Agents: .claude/agents/(7 total; workflow-supervisor=opus, workers=sonnet) -->
<!-- Harness catalog: docs/00.agent-governance/agents (agents + functions) -->
<!-- settings.json=team(tracked) · settings.local=personal(ignored) · no duplication -->
<!-- Skills: .claude/skills/<skill>/skill.md -->
<!-- Models: workflow-supervisor=opus · all domain/task agents=sonnet -->
<!-- Infra: validate→change→verify · Security: cross-validate after infra changes -->
<!-- .pre-commit-config.yaml: lint/format (never manually) -->

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
