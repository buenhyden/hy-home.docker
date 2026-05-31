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

## 5. Stage 00 Canonical Adapter Model

All runtimes (Claude, Codex, Gemini) expose the same agent and function catalog
through provider-specific adapters. Stage 00 is the only canonical catalog and
policy source; provider overlays describe runtime mechanics but must not redefine
agent roles, model tiers, QA rules, template rules, or workflow policy.

### Tier 1 — Stage 00 Canonical Catalog

- `docs/00.agent-governance/agents/agents/` defines which agents exist, their
  roles, scopes, inputs/outputs, and governing links.
- `docs/00.agent-governance/agents/functions/` defines reusable functions and
  skill contracts.
- `subagent-protocol.md` defines provider-equivalent model tiers and Codex
  reasoning-effort requirements.
- The agent and function name sets defined in Stage 00 are authoritative. Every
  provider adapter MUST expose exactly those name sets.

### Tier 2 — Provider Runtime Adapters

- **Claude (`.claude/`)** exposes Claude-native Markdown agents and skills. These
  files are provider adapters for the Stage 00 catalog, not the canonical source.
- **Codex (`.codex/`)** exposes Codex-native TOML agent definitions under
  `.codex/agents/*.toml`, plus Codex-compatible skills and hooks. TOML files
  carry provider-native `model` and `model_reasoning_effort` fields from the
  Model Policy.
- **Gemini (`.agents/`)** exposes reference-index agents and skills pointing to
  Stage 00 catalog entries, plus native `rules/` and `workflows/` directories
  where Antigravity IDE supports them.

### Adapter Rules

- **Name-set parity:** agent and function name sets MUST be identical across
  Stage 00, `.claude/`, `.codex/`, and `.agents/`.
- **Role parity:** provider adapters MUST point back to the Stage 00 catalog
  entry and preserve the same scope and role intent.
- **Policy parity:** provider adapters may adapt syntax, frontmatter, or hook
  mechanics, but may not introduce separate governance, QA/CI/CD, Template
  Contract, Model Policy, or workflow rules.
- **Model parity:** provider adapters MUST use only model identifiers and
  reasoning-effort values allowed by `subagent-protocol.md`.
- **Validation parity:** `scripts/validation/check-repo-contracts.sh` and
  `scripts/operations/sync-provider-surfaces.sh` enforce or report drift from
  this model.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/providers/codex.md`

## References

- <https://openai.com/index/introducing-codex/>
- <https://agents.md/>
