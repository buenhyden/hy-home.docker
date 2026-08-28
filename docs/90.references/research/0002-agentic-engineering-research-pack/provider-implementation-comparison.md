---
status: draft
artifact_id: reference:agentic-engineering-research-draft:provider-implementation-comparison
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Provider Implementation Comparison

## Overview

Claude and Codex offer different native configuration and lifecycle surfaces.
This comparison keeps historical external capability separate from the tracked
local configuration, and does not make entitlement or execution claims.

## Purpose

State a provider-neutral construction: canonical contract, native adapters,
parity checks, irreducible differences, then separately authorized runtime
proof.

## Scope

Only Claude and Codex are in the tracked provider registry. Models are D3
subject matter and no new model capability or availability claim appears here.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `PIC-001` | Claude and Codex are marked supported and adopted in the registry, but each has `runtime_acceptance: needs_revalidation`. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Treat current tracked configuration as adoption intent, not runtime proof. |
| `PIC-002` | Canonical roles and skills are provider-neutral sources; native adapters translate them and may not define policy, lifecycle, templates, model selection, or completion criteria. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/{claude.md,codex.md}` | Change the canonical contract before generating or checking adapters. |
| `PIC-003` | The local semantic-event sets differ: Claude has seven including `SessionEnd`; Codex has six and omits it. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Parity preserves meaning where supported, not identical native event counts. |
| `PIC-004` | Official 2026-08-08 documentation records separate Claude and Codex hook, agent, instruction, and configuration capabilities. | retained official observation | HISTORICAL VERIFIED | Task 0001 source ledger | Native feature descriptions are not evidence of local settings or execution. |
| `PIC-005` | Retained detailed observations record Claude Markdown agents with YAML frontmatter (required name/description and optional tools, model, permissions, skills, hooks, memory, effort, isolation) versus Codex standalone TOML agents (required name, description, developer instructions) used as spawned-session configuration. | retained official observation | HISTORICAL VERIFIED | retained dated provider comparison | Preserve native schemas in adapters while keeping role intent canonical. |
| `PIC-006` | Retained detailed hook observations distinguish Claude's five handler types across 31 events and documented blocking/advisory behavior from Codex command hooks across 11 events, trust-gated project hooks, and advisory main-thread `SessionEnd`. | retained official observation | HISTORICAL VERIFIED | retained dated provider comparison | Map semantic meaning to locally supported events; do not equate event count with parity. |
| `PIC-007` | Retained detailed instruction/configuration observations distinguish Claude hierarchy/imports and managed-to-user settings precedence with merged permissions/deny precedence from Codex global-to-root-to-CWD AGENTS discovery and CLI/project/profile/user/system/built-in configuration precedence with trust. | retained official observation | HISTORICAL VERIFIED | retained dated provider comparison | Preserve native discovery/trust behavior in adapters; bootstrap remains canonical repository authority. |

### Common construction

1. Define roles, skills, permissions, and provider facts in the canonical
   contract. Do not encode shared policy directly in a provider projection.
2. Translate that contract into the native adapter: Claude uses its tracked
   `.claude/` surfaces; Codex uses `.codex/agents/*.toml`, shared skill
   projections, and `.codex/hooks.json` as declared by its adapter.
3. Run the registered parity checks after an authorized canonical change. A
   check can detect drift in tracked surfaces; it cannot prove provider loading.
4. Preserve irreducible differences. Event mapping, native schema, sandbox or
   permission vocabulary, and configuration precedence need adapter-specific
   treatment. `SessionEnd` is the concrete local difference above.
5. Obtain runtime proof only under separate authorization with a concrete
   target, redaction boundary, expected result, rollback, and post-check.

The comparison is therefore capability-to-contract analysis, not a benchmark,
cost comparison, or claim that either provider is presently available.

### Retained historical capability comparison

| Concern | Claude retained observation | Codex retained observation | Provider-neutral handling |
| --- | --- | --- | --- |
| Native role surface | 2026-08-08 source: Markdown body with YAML frontmatter; name/description required, and tools, model, permissions, skills, hooks, memory, effort, and isolation optional. | 2026-08-14 retained detail: standalone TOML requires name, description, and developer instructions; it configures a spawned session. | Define role intent and permission profile once; adapters preserve schema. |
| Hooks and feedback | `PIC-006`: 2026-08-14 retained detail: five handler types across 31 events, with documented blocking/advisory behavior. | `PIC-006`: 2026-08-14 retained detail: command hooks across 11 events; `SessionEnd` is main-thread advisory and project hooks are trust-gated. | Map supported meaning, then inspect local event fields; event count is not parity. |
| Instruction loading | `PIC-007`: 2026-08-14 retained detail: CLAUDE.md hierarchy and imports; settings precedence is managed, CLI, local, project, user, with merged permissions and deny precedence. | `PIC-007`: 2026-08-14 retained detail: `AGENTS.override.md`/`AGENTS.md` discovery proceeds global then project root to CWD, one file per directory; configuration precedence includes CLI, project, profile, user, system, built-in and trust. | Bootstrap owns repository authority; native discovery and trust remain adapter-specific. |
| Configuration boundary | A native settings value is a historical capability/configuration observation. | A native trusted-project setting is a historical capability/configuration observation. | Inspect tracked adapters and registry; require separate runtime proof. |

This table is historical synthesis from retained direct observations, not a
current vendor comparison. The local Codex six-event set is the applicable
tracked configuration even though the historical upstream observation included
`SessionEnd`.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PIC-SRC-001` | `PIC-001`, `PIC-003` | Provider registry / workspace | [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Registry state is not provider acceptance. |
| `PIC-SRC-002` | `PIC-002` | Claude and Codex provider adapters / workspace | [Claude](../../../00.agent-governance/providers/claude.md); [Codex](../../../00.agent-governance/providers/codex.md) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Adapters describe allowed translation only. |
| `PIC-SRC-003` | `PIC-004` | Claude Code hooks, subagents, settings / Anthropic | [hooks](https://code.claude.com/docs/en/hooks); [subagents](https://code.claude.com/docs/en/sub-agents); [settings](https://code.claude.com/docs/en/settings) | retained official observation | retrieval-time pages | 2026-08-08T15:48:51+09:00 | Mutable historical observations; no entitlement or local execution. |
| `PIC-SRC-004` | `PIC-004` | Codex hooks, subagents, AGENTS.md, configuration / OpenAI | [hooks](https://learn.chatgpt.com/docs/hooks); [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents); [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md); [configuration](https://learn.chatgpt.com/docs/config-file/config-basic) | retained official observation | retrieval-time pages | 2026-08-08T15:48:51+09:00 | Historical vendor capability is distinct from current tracked configuration. |
| `PIC-SRC-005` | `PIC-005` | Retained provider comparison evidence / workspace | [dated provider comparison](../2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md) | retained historical synthesis | C-AGENT verified 2026-08-08; C-HOOK/C-SET/O-HOOK/O-AGENT/O-INSTR re-verified 2026-08-14 | 2026-08-08; 2026-08-14 | Retained direct-page detail, not a current vendor or local-runtime observation. |
| `PIC-SRC-006` | `PIC-006` | Claude Code hooks / Anthropic | [official page](https://code.claude.com/docs/en/hooks) | retained official observation | retained dated leaf C-HOOK row; version not recorded | 2026-08-14 | Historical hook mechanics; no local event firing inferred. |
| `PIC-SRC-007` | `PIC-006` | Codex hooks / OpenAI | [official page](https://learn.chatgpt.com/docs/hooks) | retained official observation | retained dated leaf O-HOOK row; version not recorded | 2026-08-14 | Historical main-thread/trust mechanics; no local event firing inferred. |
| `PIC-SRC-008` | `PIC-007` | Claude Code memory and settings / Anthropic | [memory](https://code.claude.com/docs/en/memory); [settings](https://code.claude.com/docs/en/settings) | retained official observation | retained dated leaf C-MEM/C-SET rows; version not recorded | 2026-08-14 | Historical hierarchy/precedence mechanics; no local loading inferred. |
| `PIC-SRC-009` | `PIC-007` | Codex AGENTS.md and configuration / OpenAI | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md); [configuration](https://learn.chatgpt.com/docs/config-file/config-basic) | retained official observation | O-INSTR re-verified 2026-08-14; O-CONFIG verified 2026-08-08; versions not recorded | 2026-08-14; 2026-08-08 | Historical discovery/configuration mechanics; no local trusted-project state inferred. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Translate only canonical contracts. | Inspect registry provider/event fields, then the matching adapter's native surface. | Runtime acceptance unverified. |
| architecture | applies | Record provider decisions in owner artifacts. | Review decision authority. | No choice recommended. |
| common | applies | Preserve native differences in adapters. | Use the adapters' documented parity check after a canonical source change. | No identical-schema assumption. |
| docs | applies | Cite capability with historical date. | Check source rows and caveats. | No current-vendor claim. |
| infra | applies | Authorize environment proof separately. | Require concrete target. | No runtime inspection. |
| ops | applies | Route outage/telemetry proof to ops. | Use approved operational evidence. | No availability claim. |
| qa | applies | Compare tracked contracts first. | Run registered check when authorized. | Static parity is limited. |
| security | applies | Respect native permission boundaries. | Review redacted plan. | No control effectiveness claim. |

## Maintenance

Refresh from retained sources only when a later authorized source observation
exists. Revalidate runtime acceptance separately; do not infer it from adapters.

## Related Documents

- [Harness engineering](./harness-engineering.md)
- [Agent instructions](./agent-instructions-vibe-coding.md)
