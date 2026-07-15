---
layer: agentic
runtime: shared
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
- `.agents/` is the provider-neutral compatibility and shared-skill surface.
- Stage docs `docs/01` to `docs/99`: read-only by default.

## 4. Instruction File Hierarchy and Precedence

This repository keeps agent instruction authority inside repo-local files only. Precedence order (highest first):

1. **Direct user / system instructions** — always win.
2. **Repo-local governance** (`docs/00.agent-governance/`) — authoritative for all policy matters.
3. **Root shim files** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) — entry points routing into governance.
4. **Provider overlays** (`providers/claude.md`, `providers/gemini.md`, `providers/codex.md`) — provider-specific behavior within governance bounds.
5. **Runtime controls** — executable provider behavior in `.claude/`, `.codex/`, and `.gemini/` when tracked and validated.
6. **Compatibility surfaces** — `.agents/` exposes shared skills and compatibility projections without becoming a native-provider policy owner.

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
- `contracts/provider-models.yaml` defines typed provider/model/event facts,
  work profiles, reasoning controls, fallbacks, and observation provenance;
  `subagent-protocol.md` supplies the human routing and handoff view.
- The agent and function name sets defined in Stage 00 are authoritative. Every
  provider adapter MUST expose exactly those name sets.

### Tier 2 — Provider Runtime Adapters

- **Claude (`.claude/`)** exposes Claude-native Markdown agents and skills. These
  files are provider adapters for the Stage 00 catalog, not the canonical source.
- **Codex (`.codex/`)** exposes Codex-native TOML agent definitions under
  `.codex/agents/*.toml` and hook compatibility. TOML files
  carry provider-native `model` and `model_reasoning_effort` fields from the
  Model Policy.
- **Gemini (`.gemini/`)** exposes generated native agents, settings, and one
  thin event-name adapter. `.agents/skills/` remains the shared Gemini/Codex
  skill source and `.agents/` remains the compatibility surface.

### Adapter Rules

- **Name-set parity:** agent and function name sets MUST be identical across
  Stage 00 and all active provider/compatibility projections.
- **Role parity:** provider adapters MUST point back to the Stage 00 catalog
  entry and preserve the same scope and role intent.
- **Policy parity:** provider adapters may adapt syntax, frontmatter, or hook
  mechanics, but may not introduce separate governance, QA/CI/CD, Template
  Contract, Model Policy, or workflow rules.
- **Model parity:** provider adapters MUST use only the model identifiers and
  provider-specific controls allowed by `contracts/provider-models.yaml`.
- **Validation parity:** `scripts/validation/check-repo-contracts.sh` and
  `scripts/operations/sync-provider-surfaces.sh` enforce or report drift from
  this model.

### Shared Lifecycle and QA Contract

Every adapter preserves
`discovery -> applicability -> provider loading -> canonical artifact -> validation evidence`.
For changed or new target Markdown, run
`python3 scripts/validation/check-document-metadata.py --mode check-changed`
with a safe base. Direct agent execution of all-files pre-commit is prohibited;
an approved final QA gate uses only
`scripts/validation/run-agent-precommit-all-files.sh` and records reviewed
Git-visible, non-ignored repository paths. Provider-native hooks may route these
obligations, while pointer/reminder surfaces remain behavioral and must not be
described as native interception.

## Related Documents

- `../../01.requirements/024-agent-governance-standardization.md`
- `../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md`
- `../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/providers/codex.md`

## References

- <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- <https://agents.md/>
