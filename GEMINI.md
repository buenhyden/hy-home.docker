# Gemini Project Context

Gemini-specific deltas only. Shared project policy lives in [AGENTS.md](AGENTS.md), [.claude/core-governance.md](.claude/core-governance.md), and [.claude/workflow.md](.claude/workflow.md).

## Shared References

- [AGENTS.md](AGENTS.md)
- [.claude/core-governance.md](.claude/core-governance.md)
- [.claude/workflow.md](.claude/workflow.md)

## Gemini-Specific Notes

- `GEMINI.md` is the repository’s explicit Gemini context file.
- If Gemini CLI is configured with `contextFileName: "AGENTS.md"`, keep this file aligned rather than duplicating full policy here.
- Treat this file as behavior/config context, not as a place to trigger implicit file reads.
- Cross-check conclusions against repo evidence: commands, docs, rules, and tests from the current session.
- Keep provider-specific guidance here and defer shared policy to the linked files.
