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
- `.agents/` is the shared runtime surface and moderate-shim for Gemini, while maintaining compatibility for generic tools.
- Stage docs `docs/01` to `docs/99`: read-only by default.

## 4. Instruction File Hierarchy and Precedence

This repository keeps agent instruction authority inside repo-local files only. Precedence order (highest first):

1. **Direct user / system instructions** — always win.
2. **Repo-local governance** (`docs/00.agent-governance/`) — authoritative for all policy matters.
3. **Root shim files** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) — entry points routing into governance.
4. **Provider overlays** (`providers/claude.md`, `providers/gemini.md`, `providers/codex.md`) — provider-specific behavior within governance bounds.
5. **Runtime controls** — executable enforcement and local agent behavior in `.claude/`, Codex hook support in `.codex/`, and Gemini runtime skills/agents in `.agents/`.
6. **Compatibility surfaces** — The `.agents/` directory doubles as a cross-provider compatibility layer, though its primary role is the Gemini runtime surface.

GitHub-native instruction files are not part of this repository's active instruction hierarchy.
If such files ever appear, they must not be treated as authoritative until governance explicitly adopts them.

## 5. Provider Parity Model

All three runtimes (Claude, Codex, Gemini) mirror the same agent and function catalog through one shared, three-tier model. This model is the canonical rule for how each provider surface relates to the catalog; provider overlays must not redefine it.

### Tier 1 — Catalog SSOT

- `docs/00.agent-governance/agents/agents/` (role docs) and `docs/00.agent-governance/agents/functions/` (function entries) are the source of truth for _which_ agents and functions exist, their roles, inputs/outputs, and governing links.
- The agent name set and function name set defined here are authoritative. Every runtime surface MUST expose exactly the same name sets.

### Tier 2 — Canonical Runtime Implementation (Claude)

- `.claude/agents/*.md` and `.claude/skills/*/skill.md` hold the full, self-contained runtime content (provider frontmatter plus prompt body).
- This is the canonical _implementation_ mirror that catalog `functions/*.md` entries reference as the runtime mirror.

### Tier 3 — Provider Mirrors and Indexes

- **Codex (`.codex/`)** keeps full runtime copies under `.codex/agents/` and `.codex/skills/` because Codex loads self-contained files. These copies MUST stay content-identical to `.claude/` (provider frontmatter aside) and are kept in sync deliberately.
- **Gemini (`.agents/`)** uses a reference-index model: each `.agents/agents/<name>.md` and `.agents/skills/<name>/skill.md` is a thin pointer that imports the governance catalog entry and names `.claude/` as the canonical implementation. Gemini surfaces carry no full duplication. `.agents/` holds no `rules/` or `workflows/` directories; Gemini-specific policy lives in governance.

### Parity Rules (enforced by `scripts/validation/check-repo-contracts.sh`)

- **Name-set parity:** the agent set and the function set MUST be identical across Tier 1, `.claude/`, `.codex/`, and `.agents/`.
- **Content parity:** `.codex/` runtime content MUST match `.claude/` runtime content.
- **Pointer parity:** every `.agents/` agent and skill file MUST be a reference index pointing to the canonical source and MUST NOT contain divergent full content or reference nonexistent paths.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/providers/codex.md`

## References

- <https://openai.com/index/introducing-codex/>
- <https://agents.md/>
