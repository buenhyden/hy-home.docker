# graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:

- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- Run `bash scripts/knowledge/report-graphify-health.sh` when graph health matters
- If Graphify health is advisory, corroborate conclusions against tracked source files, `docs/00.agent-governance/`, and active stage docs
- If the graphify MCP server is active and health is clean, utilize tools like `query_graph`, `get_node`, and `shortest_path` for precise architecture navigation
- If the MCP server is not active and health is clean, the CLI equivalents are `graphify query "<question>"`, `graphify path "<A>" "<B>"`, and `graphify explain "<concept>"`
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
