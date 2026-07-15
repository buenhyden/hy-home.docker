---
layer: agentic
---

# Provider Capability Matrix

Single source of truth for how each agent capability maps from governance to each
runtime surface. Governance owns the contract; each provider exposes it through
its own native mechanism per the Stage 00 Canonical Adapter Model
(`providers/agents-md.md` §5).

## 1. Matrix

| Capability         | Governance SSOT                                            | Claude (`.claude/`)                            | Codex / GPT (`.codex/`)                     | Gemini (`.gemini/`)                     |
| ------------------ | ---------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------- | --------------------------------------- |
| Subagents          | `agents/agents/*.md`                                       | `.claude/agents/*.md` (adapter)                | `.codex/agents/*.toml` (adapter)            | `.gemini/agents/*.md` when rendered     |
| Skills / Functions | `agents/functions/*.md`                                    | `.claude/skills/*/SKILL.md`                    | `.agents/skills/*/SKILL.md` (shared)        | `.agents/skills/*/SKILL.md` (shared)    |
| Rules              | `rules/*.md`                                               | `.claude/hookify.*.md` + `settings.json`       | governance + `.codex/hooks.json`            | governance + `.gemini/settings.json` when rendered |
| Hooks              | `providers/*.md` Hook Parity Contract                      | `.claude/hooks/*.sh` + `settings.json`         | `.codex/hooks.json`                         | provider-native support; no tracked `.gemini` adapter until the projection task |
| Output style       | `rules/output-style.md`                                    | `.claude/output-styles/*.md` + `settings.json` | behavioral contract                         | behavioral contract                     |
| Workflows          | `rules/workflows.md` (+ `rules/stage-authoring-matrix.md`) | orchestration skills / commands                | orchestration skills (mirror)               | orchestration skills (pointer)          |
| Memory             | `memory/` (`progress.md`, notes)                           | read/write `memory/progress.md` + notes        | read/write `memory/progress.md` + notes     | read/write `memory/progress.md` + notes |
| Models             | `subagent-protocol.md` Model Policy                        | `opus-4.8` / `sonnet-4.6`                      | `gpt-5.5` / `gpt-5.4-mini` + reasoning effort | `gemini-3.1-pro` / `gemini-3.5-flash` |
| Templates          | `docs/99.templates/` via `rules/documentation-protocol.md` | shared                                         | shared                                      | shared                                  |

## 2. Rules

1. A capability's behavior is defined once in its Governance SSOT; provider rows
   describe only the surface and mechanism, never divergent policy.
2. Where the workspace has no tracked provider-native adapter (Gemini hooks) or
   the runtime lacks the primitive (Codex/Gemini output style), the runtime
   follows the governance contract as a behavioral obligation. Provider support
   does not prove workspace adoption.
3. Stage 00 is the canonical runtime catalog. Claude, Codex, and Gemini expose
   provider adapters and must not redefine governance. See the Stage 00
   Canonical Adapter Model for enforcement details.
4. Memory is shared: every runtime reads `memory/progress.md` before mutating the
   repository and appends progress after completing repository-modifying work.

## 3. Supported / Unsupported / Deferred

| Capability                        | Claude                                        | Codex / GPT                       | Gemini                               |
| --------------------------------- | --------------------------------------------- | --------------------------------- | ------------------------------------ |
| Custom subagents                  | Supported (`.claude/agents`)                  | Supported (`.codex/agents/*.toml`) | Provider-supported; workspace projection pending |
| Skills                            | Supported (`.claude/skills`)                  | Supported through `.agents/skills` | Supported through `.agents/skills`  |
| Programmatic hooks                | Supported (`settings.json` + `.claude/hooks`) | Supported (`.codex/hooks.json`)   | Provider-supported, not tracked here → behavioral reminder |
| Per-agent model                   | Supported (alias)                             | Supported (model id + effort)     | Supported (pointer frontmatter)      |
| Native output style               | Supported (`.claude/output-styles`)           | Unsupported → behavioral contract | Unsupported → behavioral contract    |
| Per-subagent tools/permissionMode | Supported (frontmatter)                       | Mirror (advisory)                 | Pointer (advisory)                   |

- **Deferred:** anything a runtime cannot honor natively is recorded here and followed as a
  behavioral contract rather than implemented divergently. Do not add provider-specific
  primitives that have no governance contract behind them.

## 4. Shared Development-Harness Gates

All provider adapters preserve the same lifecycle contract:
`discovery -> applicability -> provider loading -> canonical artifact -> validation evidence`.
Provider-specific hook or reminder mechanics do not change these gates:

- For changed or new target Markdown, run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with a safe comparison base supplied by the execution surface.
- Direct agent execution of all-files pre-commit remains prohibited. At an
  approved final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` and record the reviewed
  Git-visible, non-ignored repository paths in Stage 04 evidence.
- A provider reminder, pointer, or hook reports the obligation; it does not
  create policy or prove that a provider-native interception occurred.

## 5. Output-Style Placement

- **Global contract** (all runtimes): `rules/output-style.md` — the workspace-wide style.
- **Claude-native binding**: `.claude/output-styles/hy-home.md`, registered via
  `settings.json` `outputStyle`. Codex and Gemini follow the contract behaviorally.
- **Skill/subagent-specific formatting** stays inside that skill's or subagent's prompt
  (e.g. a report layout for one agent), not in the global contract.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/rules/output-style.md`
- `docs/00.agent-governance/rules/workflows.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/memory/README.md`
