# Claude Project Memory

Claude-specific deltas only. Shared project policy lives in imported `.claude/*.md` files and in [AGENTS.md](AGENTS.md).

@.claude/core-governance.md
@.claude/workflow.md

## Claude-Specific Notes

- Use imports to keep this file thin; do not restate shared policy here.
- Prefer repo-local commands, paths, and docs over generic examples.
- Keep memory concise and current; use `/memory` or `#` only when the new instruction is durable.
- If a task needs additional subtree-specific context, prefer adding nested docs or imported files instead of bloating this root file.
