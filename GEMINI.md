# Gemini Project Context

Gemini-specific root only. Shared repository policy lives in [AGENTS.md](AGENTS.md) and the linked `.claude/*.md` guides.

## Shared References

- [AGENTS.md](AGENTS.md)
- [.claude/README.md](.claude/README.md)
- [.claude/core-governance.md](.claude/core-governance.md)
- [.claude/workflow.md](.claude/workflow.md)

## Gemini-Specific Deltas

- `GEMINI.md` is the repository’s explicit Gemini delta file; keep it additive, not duplicative.
- If Gemini CLI is configured with `contextFileName: "AGENTS.md"`, treat this file as provider-specific overlay only.
- Prefer explicit linked context over relying on implicit file reads.
- Cross-check conclusions against repository evidence: commands, docs, rules, and tests from the current session.
- Move shared durable policy into `.claude/*.md` instead of expanding this root file.
