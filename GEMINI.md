# Gemini Project Context

Gemini-specific root only. Shared repository policy lives in [AGENTS.md](AGENTS.md) and the linked `.claude/*.md` guides.

## Shared References

- [AGENTS.md](AGENTS.md) — Canonical cross-agent entrypoint (load this first)
- [.claude/core-governance.md](.claude/core-governance.md) — Persona matrix, rule-loading, lazy-loading policy, template contracts
- [.claude/workflow.md](.claude/workflow.md) — Execution loop, validation commands, doc usage rules
- [docs/agent-instructions.md](docs/agent-instructions.md) — Agent-specific lazy-loading gateway for all doc families

## Gemini-Specific Deltas

- `GEMINI.md` is the repository's Gemini delta file; keep it additive, not duplicative.
- If Gemini CLI is configured with `contextFileName: "AGENTS.md"`, treat this file as a provider-specific overlay only.
- Prefer explicit linked context over relying on implicit file reads.
- Cross-check conclusions against repository evidence: commands, docs, rules, and tests from the current session.
- Move shared durable policy into `.claude/*.md` instead of expanding this root file.

## Gemini Execution Notes

- Load [AGENTS.md](AGENTS.md) for the full persona matrix and infrastructure lifecycle.
- Load [docs/agent-instructions.md](docs/agent-instructions.md) at session start to discover relevant documentation families.
- Use `[LOAD:*]` markers from the agent-instructions gateway to identify which doc families to read.
- Validate all infrastructure changes with `docker compose config` before proposing `up` operations.
- For complex tasks, activate Reasoner persona before specialist personas.
