# Claude Directive

Use this file for Claude-specific behavior only. Load [AGENTS.md](AGENTS.md) and the shared guides first.

## Claude-Specific Rules

- Execute directly once the path is clear and keep status updates dense.
- Read stderr carefully and retry corrected commands before escalating routine command errors.
- Prefer fast local inspection tools such as `rg`, `find`, `sed`, and `ls`, and use parallel reads when they reduce latency.
- Keep edits compact; rewrite an entire file only when the task is structural.
- Do not rely on tools or artifact paths unless they are confirmed in the current runtime or repository.
- When work needs planning or durable context, use repository-local documents under `docs/specs/` and `docs/plans/`.

## Shared References

- [Shared governance](.claude/agent-instructions/core-governance.md)
- [Shared workflow](.claude/agent-instructions/workflow.md)
