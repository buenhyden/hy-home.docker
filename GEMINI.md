# Gemini Directive

Use this file for Gemini-specific behavior only. Load [AGENTS.md](AGENTS.md) and the shared guides first.

## Gemini-Specific Rules

- Use a dual-pass mindset: build the solution, then challenge it as a skeptic before finalizing.
- For complex investigations, debugging, or multi-step execution, use explicit sequential reasoning before action.
- Anchor conclusions in evidence from the current session by cross-checking specs, code, docs, and tests together.
- If screenshots, mockups, or UI images are involved, perform a visual audit before suggesting changes.
- For long sessions, keep a compressed summary in the active repository plan or handoff artifact instead of relying on unstated memory.
- Do not assume a file, API, environment variable, or path exists unless current session evidence confirms it.

## Shared References

- [Shared governance](.claude/core-governance.md)
- [Shared workflow](.claude/workflow.md)
