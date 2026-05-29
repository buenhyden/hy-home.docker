---
layer: agentic
---

# AGENTS.md Provider-Neutral Notes

Provider-neutral guidance for `AGENTS.md` style files.

## 1. Purpose

- Define shared entry behavior that can be consumed by multiple runtimes.
- Keep root instruction files short and reusable.
- Establish `docs/00.agent-governance/` as the single authoritative source of truth (SSOT).

## 2. Baseline Rules

- Root `AGENTS.md` (or platform specific root like `GEMINI.md` / `CLAUDE.md`) should act as an entry shim, not a monolithic policy dump.
- Prefer modular delegation to governance files.
- Use deterministic loading order and clear precedence rules.
- When path-level instruction files coexist, prefer the most specific in-scope file.

## 3. This Repository Policy

- Shared policy source of truth: `docs/00.agent-governance/`.
- Root shim files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- All runtime specific directories (`.agents/`, `.claude/`, `.codex/`) act ONLY as adapters to implement the common governance for their respective platforms.
- Stage docs `docs/01` to `docs/99`: read-only by default.

## 4. Instruction File Hierarchy and Precedence

This repository keeps agent instruction authority inside repo-local files only. Precedence order (highest first):

1. **Direct user / system instructions** — always win.
2. **Repo-local governance** (`docs/00.agent-governance/`) — authoritative for all policy matters.
3. **Root shim files** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) — entry points routing into governance.
4. **Provider overlays** (`providers/claude.md`, `providers/gemini.md`, `providers/codex.md`) — provider-specific behavior within governance bounds.
5. **Runtime controls** — executable enforcement and local agent behavior in `.claude/`, Codex hook support in `.codex/`, and Antigravity workspace settings/rules.

GitHub-native instruction files are not part of this repository's active instruction hierarchy.
If such files ever appear, they must not be treated as authoritative until governance explicitly adopts them.

## 5. Adapter Model (Formerly Provider Parity Model)

The agent catalog, functions, hooks, and workflows are centrally managed. Runtimes (Antigravity/Gemini, Claude, Codex) are adapters that map the central SSOT to their specific execution environments.

### Tier 1 — Universal SSOT (Canonical)

- `docs/00.agent-governance/agents/agents/` (role docs) and `docs/00.agent-governance/agents/functions/` (function entries) are the absolute source of truth for _which_ agents and functions exist, their roles, inputs/outputs, and governing links.
- `docs/00.agent-governance/rules/hooks/` contains the universal definitions of repository guardrails.
- Every runtime surface MUST align with these name sets and rules.

### Tier 2 — Platform Adapters

- **Antigravity / Gemini (`.agents/`, `.gemini/`)**: Maps SSOT to Antigravity's native `Rules`, `Skills`, and `Workflows`. The `.agents/` directory is maintained for legacy references if needed, but the primary logic resides in Antigravity's workspace configuration reading from governance.
- **Claude (`.claude/`)**: Maps SSOT to Claude Code's native `settings.json`, `.claude/agents/`, and local scripts. It reads hooks from the common rules rather than maintaining local isolated logic.
- **Codex (`.codex/`)**: Maps SSOT to Codex's `hooks.json` and agent directory.

### Parity Rules (enforced by `scripts/validation/check-repo-contracts.sh`)

- **Name-set parity:** The agent set and the function set MUST be identical across Tier 1, `.claude/`, `.codex/`, and Antigravity representations.
- **Rule alignment:** No platform may invent a rule or hook that bypasses or conflicts with the central `docs/00.agent-governance/rules/`.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/providers/codex.md`

## References

- <https://openai.com/index/introducing-codex/>
- <https://agents.md/>
