---
layer: agentic
---

# AGENTS.md Provider-Neutral Notes

Provider-neutral guidance for `AGENTS.md` style files.

## 1. Purpose

- Define shared entry behavior that can be consumed by multiple runtimes.
- Keep root instruction files short and reusable.

## 2. Baseline Rules

- Root `AGENTS.md` should act as an entry shim, not a monolithic policy dump.
- Prefer modular delegation to governance files.
- Use deterministic loading order and clear precedence rules.
- When path-level instruction files coexist, prefer the most specific in-scope file.

## 3. This Repository Policy

- Shared policy source of truth: `docs/00.agent-governance/`.
- Root shim files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Codex entry: `AGENTS.md` plus `.codex/` runtime hooks.
- `.agents/` compatibility files may exist for tools that read that path, but
  they must not override the governance hub or `.claude` runtime catalog.
- Stage docs `docs/01` to `docs/99`: read-only by default.

## 4. Instruction File Hierarchy and Precedence

This repository keeps agent instruction authority inside repo-local files only. Precedence order (highest first):

1. **Direct user / system instructions** — always win.
2. **Repo-local governance** (`docs/00.agent-governance/`) — authoritative for all policy matters.
3. **Root shim files** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) — entry points routing into governance.
4. **Provider overlays** (`providers/claude.md`, `providers/gemini.md`, `providers/codex.md`) — provider-specific behavior within governance bounds.
5. **Runtime controls** — executable enforcement and local agent behavior in `.claude/` and Codex hook support in `.codex/`.
6. **Compatibility surfaces** — `.agents/` files only mirror or route tooling
   behavior and do not define active policy.

GitHub-native instruction files are not part of this repository's active instruction hierarchy.
If such files ever appear, they must not be treated as authoritative until governance explicitly adopts them.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/providers/codex.md`

## References

- <https://openai.com/index/introducing-codex/>
- <https://agents.md/>
