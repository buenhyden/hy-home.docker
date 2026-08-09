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
| Subagents          | `agents/agents/*.md`                                       | `.claude/agents/*.md` (adapter)                | `.codex/agents/*.toml` (adapter)            | `.gemini/agents/*.md` (adapter)         |
| Skills / Functions | `agents/functions/*.md`                                    | `.claude/skills/*/SKILL.md`                    | `.agents/skills/*/SKILL.md` (shared)        | `.agents/skills/*/SKILL.md` (shared)    |
| Rules              | `rules/*.md` + `docs/00.agent-governance/rules/hooks/hookify.*.md` | canonical Hookify rules + `settings.json`; local projection not tracked | governance + `.codex/hooks.json`            | governance + `.gemini/settings.json`    |
| Hooks              | `contracts/provider-models.yaml` semantic events           | `.claude/hooks/*.sh` + `settings.json`         | `.codex/hooks.json`                         | `.gemini/settings.json` + one native event adapter |
| Output style       | `rules/output-style.md`                                    | `.claude/output-styles/*.md` + `settings.json` | behavioral contract                         | behavioral contract                     |
| Workflows          | `rules/workflows.md` (+ `rules/stage-authoring-matrix.md`) | orchestration skills / commands                | orchestration skills (mirror)               | orchestration skills (pointer)          |
| Memory             | `memory/README.md` + `memory/current.md`                   | shared bounded handoff                         | shared bounded handoff                      | shared bounded handoff                  |
| Models             | `contracts/provider-models.yaml` work profiles             | `claude-opus-5` / `claude-sonnet-5` / `claude-haiku-4-5-20251001` | `gpt-5.6-sol` / `gpt-5.6-terra` + reasoning effort | `gemini-3.6-flash` / `gemini-3.5-flash-lite` |
| Templates          | `docs/99.templates/` via `rules/documentation-protocol.md` | shared                                         | shared                                      | shared                                  |
| Harness layers     | `contracts/provider-models.yaml` `harness_layers`          | shared typed controls                          | shared typed controls                       | shared typed controls                    |
| Workflow states    | `contracts/provider-models.yaml` `workflow_states`         | shared discover-to-handoff lifecycle           | shared discover-to-handoff lifecycle        | shared discover-to-handoff lifecycle     |
| Harness loops      | `contracts/provider-models.yaml` `harness_loops`           | bounded controls referencing states; native event where configured | bounded controls referencing states; `SessionEnd` unsupported | bounded controls referencing states; native event adapter where configured |

## 2. Rules

1. A capability's behavior is defined once in its Governance SSOT; provider rows
   describe only the surface and mechanism, never divergent policy.
2. Where a runtime lacks a primitive (Codex/Gemini output style or Codex
   `SessionEnd`), the runtime follows the governance contract as a behavioral
   obligation and the gap remains explicit. Provider support, tracked adoption,
   entitlement, and live runtime acceptance are separate facts.
3. Stage 00 is the canonical runtime catalog. Claude, Codex, and Gemini expose
   provider adapters and must not redefine governance. See the Stage 00
   Canonical Adapter Model for enforcement details.
4. Memory is shared: every runtime reviews `memory/README.md` and
   `memory/current.md` before mutating the repository. Progress, verification,
   and final evidence belong in the applicable co-located Task; the bounded
   current handoff is refreshed after verified changes, while
   `memory/progress.md` remains append-preserved historical navigation.
5. Capability, tracked adoption, and runtime depth are independent facts.
   `configured-not-executed` records a tracked native binding without claiming
   live execution; only authenticated runtime evidence can establish execution.
6. The dated `agent-catalog.yaml` capability intake compares upstream
   deliverable patterns as `merge`, `defer`, or `reject`. Provider model QA
   routes to `provider-model-evaluation`, knowledge continuity routes to
   `project-memory-stewardship`, and upstream personality prose never creates a
   repository role.

## 3. Supported / Unsupported / Deferred

| Capability                        | Claude                                        | Codex / GPT                       | Gemini                               |
| --------------------------------- | --------------------------------------------- | --------------------------------- | ------------------------------------ |
| Custom subagents                  | Supported and adopted (`.claude/agents`)      | Supported and adopted (`.codex/agents/*.toml`) | Supported and adopted (`.gemini/agents/*.md`) |
| Skills                            | Supported (`.claude/skills`)                  | Supported through `.agents/skills` | Supported through `.agents/skills`  |
| Programmatic hooks                | Supported (`settings.json` + `.claude/hooks`) | Supported with explicit `SessionEnd` gap (`.codex/hooks.json`) | Supported (`.gemini/settings.json` + thin adapter) |
| Per-agent model                   | Supported model ID and native `effort`; Haiku omits unsupported effort | Supported (model ID + reasoning effort) | Supported model field plus scoped `modelConfigs.overrides` thinking level |
| Native output style               | Supported (`.claude/output-styles`)           | Unsupported → behavioral contract | Unsupported → behavioral contract    |
| Per-subagent tools/permissionMode | Supported (frontmatter)                       | Supported sandbox mode; parent runtime remains authoritative | Supported tool allowlist; sandbox remains runtime-level |

- **Deferred:** anything a runtime cannot honor natively is recorded here and followed as a
  behavioral contract rather than implemented divergently. Do not add provider-specific
  primitives that have no governance contract behind them.
- Native event capability and tracked repository behavior are independent.
  Advisory dispatcher outputs must not be labeled blocking. Claude uses a
  conditional blocking Stop, Codex uses one bounded continuation retry, and
  Gemini uses deny/retry only where each generated adapter emits the exact
  provider-native schema.

## 4. Shared Development-Harness Gates

All provider adapters preserve the same lifecycle contract:
`discover -> design/plan -> approval -> implement -> validate ->
independent-review -> evidence -> handoff`. The eight typed harness layers
apply canonical contract, routing, permission, model, event, QA, CI, and
evidence controls to those states; they do not create another lifecycle.
Provider-specific hook or reminder mechanics do not change these gates:

- For changed or new target Markdown, run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with a safe comparison base supplied by the execution surface.
- Direct agent execution of all-files pre-commit remains prohibited. At an
  approved final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` and record the reviewed
  Git-visible, non-ignored repository paths in co-located Task evidence.
- A provider reminder, pointer, or hook reports the obligation; it does not
  create policy or prove that a provider-native interception occurred.
- All providers use the same four bounded bootstrap, implementation, review,
  and approved all-files controls. Each loop references its applicable
  `workflow_states`; provider event names and native support may differ, but
  retry, stop, escalation, least-privilege tool, and sanitized evidence rules
  do not.

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
