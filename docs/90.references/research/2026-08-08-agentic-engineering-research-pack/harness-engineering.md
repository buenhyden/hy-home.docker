---
status: draft
artifact_id: reference:agentic-engineering-research:harness-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Harness Engineering

## Overview

Harness engineering designs the controlled environment around an agent: what
context it receives, which role and model it uses, which tools it can invoke,
where mutation is allowed, how lifecycle events route to checks, and what
evidence is required before handoff. A harness is therefore broader than a
test runner. It joins governance, provider adapters, permissions, validation,
evaluation, and operations without making any one of those surfaces the policy
source for the others.

This reference satisfies REQ-01 and REQ-03 at tracked baseline
`9a6e09ca06d99ae8234199443974c978640f3ae6`. It uses the
[workspace baseline](./workspace-baseline.md) for the corpus inventory and the
[scope matrix](./scope-application-matrix.md) for the normative fourteen-scope
axis.

## Purpose

Define the elements and patterns of an agent harness, measure their current
workspace implementation, and state the environment and rules needed to adopt
or change them without confusing definition, configuration, execution,
enforcement, runtime acceptance, or remote proof.

## Repository Role

This Stage 90 reference is advisory analysis. Stage 00 contracts, provider
adapters, scripts, tests, lifecycle documents, and approved runtime evidence
remain authoritative. Recommendations here do not authorize provider,
security, infrastructure, secret, runtime, or remote mutations.

## Scope

### In scope

- Provider-neutral contracts and Claude/Codex projections.
- Instruction loading, roles, functions, model controls, tools, permissions,
  hooks, validation, evaluation, evidence, and escalation.
- Tracked implementation and validator depth at the Task 3 baseline.
- Adoption environment, ownership, failure boundaries, and all fourteen
  persona-scope implications.

### Out of scope

- Inspecting user-global provider configuration, credentials, private state,
  ignored volumes, transcripts, raw logs, or shell history.
- Starting services or proving live provider, model, hook, CI, or remote state.
- Editing Stage 00 contracts, provider adapters, hooks, scripts, or tests.

## Definitions / Facts

### Evidence depth

| Depth | What it establishes | What it does not establish |
| --- | --- | --- |
| Definition | A typed or prose contract names an element and owner. | That an adapter contains it or a runtime loads it. |
| Configuration | A tracked provider file contains a native setting or binding. | Trust, entitlement, event firing, or successful execution. |
| Local execution | A named local command ran and returned an observed result. | CI, provider service, or remote enforcement. |
| Repository enforcement | A deterministic validator rejects contract drift or a repository gate returns a decision. | Provider acceptance unless the native runtime was observed. |
| Runtime proof | A scoped provider or service run demonstrates behavior. | Other accounts, machines, branches, or future versions. |
| Remote proof | A remote control-plane observation demonstrates enforcement. | Permanent policy or unobserved environments. |

The tracked harness intentionally stops at different depths by element. The
four typed loops are marked `repository-enforced`; semantic event bindings are
configuration records, and provider/model `runtime_acceptance` remains
`needs_revalidation`.

### Harness element model

| Element | Required contract | Current tracked implementation | Evidence depth | Gap or adoption condition |
| --- | --- | --- | --- | --- |
| Canonical authority | One provider-neutral owner for roles, functions, models, events, permissions, and evidence | Stage 00 catalogs and rules | Definition + repository validation | Change the canonical owner before regenerating adapters; never patch policy into one adapter. |
| Context and instructions | Deterministic entry, precedence, scope, and freshness | `AGENTS.md`, `CLAUDE.md`, provider overlays, bootstrap, one primary scope, JIT stage docs | Definition + tracked configuration | Loading remains behavioral context, not hard enforcement. |
| Role/function routing | Registered role, scope, permissions, inputs, outputs, and functions | 14 agents, 24 functions, one supervisor and 13 workers | Definition + generated projection validation | Six normative scopes remain outside the typed scope enum; `architecture` is enum-only. |
| Provider/model routing | Work profile, provider-native model/control, fallback and status axes | Five work profiles over an 11-model registry; native Claude/Codex/Gemini fields | Definition + configuration | Entitlement, runtime acceptance, quality, latency, and cost are unverified. |
| Tools and skills | Least-privilege tool set and canonical reusable function body | Claude role tools and skills; Codex sandbox and full developer instructions; 24 projected skill bodies | Configuration + parity validation | Tool names and skill presence do not prove invocation or filesystem enforcement. |
| Permission and isolation | Explicit authority distinct from technical sandboxing | Read-only/workspace-write profiles, approval rules, Claude permission settings, Codex sandbox fields | Definition + configuration | Active session overrides and user-global modes are private/runtime facts. |
| Lifecycle interception | Semantic event mapped honestly to a native event and shared behavior | Seven semantic events; Claude wires seven, Codex wires six; shared dispatcher | Configuration + repository Stop decision logic | Codex `SessionEnd` is upstream-supported but stale/unsupported in the local contract and absent from `.codex/hooks.json`. |
| Validation and evaluation | Deterministic change-type checks, fixtures, scorers, thresholds, and independent review | Harness wrapper, repository contracts, 11 synthetic fixtures, 16 regressions | Local executable + repository enforcement when run | Synthetic semantics do not prove comparative provider quality. |
| Evidence and handoff | Sanitized fields, exact commands/results, rollback, skips, reviewer independence | Stage 04 Task, four permitted evidence fields, prohibited-sensitive-evidence set | Definition + reviewed task evidence | Raw logs, credentials, tokens, auth files, secret values, and shell history stay excluded. |
| Runtime/remote operations | Explicit target, approval, pre-check, rollback, post-check, and durable outcome | Rules and runbooks describe the boundary | Definition only for this Task | No live provider, Compose, CI, branch-protection, or deployment proof was collected. |

### Measured local construction

The following counts were re-derived from complete tracked owners, not from
Graphify or predecessor prose.

| Surface | Count or state | Tracked owner and derivation |
| --- | ---: | --- |
| Canonical agents | 14 | `contracts/agent-catalog.yaml` `agents` |
| Canonical functions | 24 | `contracts/agent-catalog.yaml` function records |
| Catalog projection memberships | 104 | 14 agents × four targets plus 24 functions × two targets |
| Native role adapters | 14 Claude, 14 Codex, 14 Gemini, 14 compatibility | Complete provider directories and renderer tests |
| Skill projections | 24 Claude-native and 24 shared `.agents` | Complete `SKILL.md` directories and renderer tests |
| Harness layers | 8 | `contracts/provider-models.yaml` `harness_layers` |
| Workflow states | 8 | `discover` through `handoff` |
| Typed harness loops | 4 | `harness_loops`, each `repository-enforced` |
| Semantic events | 7 | `semantic_events` |
| Semantic binding cells | 21 | Seven events × three providers: 20 `configured-not-executed`, one `unsupported` |
| Evaluation corpus | 11 fixtures, 16 regressions | Agent-catalog evaluation contract and tests |
| Tracked hook configuration | 7 Claude, 6 Codex | `.claude/settings.json`, `.codex/hooks.json` |

Graphify was built from `f8a72211` and is stale. Its navigation was
corroborated against the listed tracked owners; it supplied no count or
implementation conclusion.

### Environment and rules for workspace application

1. Start from an approved requirement and specification, then resolve the
   canonical Stage 00 owner before touching an adapter.
2. Load the bootstrap, provider overlay, one primary scope, and only the stage
   documents needed for the task. Record instruction loading as context, not
   enforcement.
3. Select a registered role and its work profile. Translate model, effort,
   permission, sandbox, hook, and instruction fields into the provider's native
   schema through the renderer.
4. Bind every mutation to explicit path ownership and approval. A provider
   sandbox may narrow technical reach but cannot broaden repository authority.
5. Route provider events through semantic behavior. Unsupported or stale
   mappings remain gaps; do not fabricate parity by copying event names.
6. Run the smallest applicable deterministic checks, then the named aggregate
   gate. Record commands, results, rollback, and skipped checks only.
7. Require a reviewer distinct from the implementing loop owner. Completion
   needs current evidence, not a configured hook, generated adapter, or vendor
   capability statement.
8. Keep credentials, secret values, auth material, raw logs, shell history,
   ignored volumes, private provider state, and unapproved runtime/remote
   actions outside the evidence system.

## Scope Implications

Every row uses the disposition and evidence owners in the
[scope application matrix](./scope-application-matrix.md); this table states
the harness-specific implication so no scope is inherited silently.

| Scope | Harness implication | Current disposition / route |
| --- | --- | --- |
| `agentic` | Owns contracts, adapters, hooks, roles, skills, and provider translation. | Implemented as tracked definitions; runtime unverified; route changes through Stage 00 owners. |
| `architecture` | Harness boundaries and provider trade-offs need ARD/ADR/Spec ownership. | Partial; enum-only scope with no typed agent. |
| `backend` | Apply tool, secret, test, and runtime isolation only after a backend surface exists. | Not Applicable now; future product/Spec decision required. |
| `common` | Shared review, diff hygiene, and controlled QA apply across harness changes. | Partial; use `code-reviewer`, never direct all-files pre-commit. |
| `docs` | Stage 90 research, templates, metadata, links, and Task evidence are harness inputs/outputs. | Implemented corpus; route switch remains pending. |
| `entry` | Gateway tooling needs infra ownership, targeted approval, and runtime evidence. | Partial; route through `infra-implementer`; edge state unverified. |
| `frontend` | Frontend-specific harness gates apply only to the tracked Storybook/Next fixture or a future product surface. | Partial; current fixture remains QA/review-owned. |
| `infra` | Compose, filesystem, network, secret-reference, and rollback controls form the infrastructure harness. | Definitions implemented; live state unverified. |
| `meta` | Typed metadata and generated indexes constrain harness evidence and navigation. | Partial; route through docs because the typed meta route is missing. |
| `mobile` | Device, signing, store, and mobile test harnesses need a real surface and approved lifecycle chain. | Not Applicable; no tracked mobile source. |
| `ops` | Observability, incident, deployment, and recovery evidence close operational harness loops. | Partial; definitions exist, outcomes unverified. |
| `product` | Product intent decides whether harness cost, latency, autonomy, and risk are acceptable. | Partial; human approval and Stage 01 ownership remain required. |
| `qa` | Owns deterministic validation, fixture/regression evidence, and independent evaluation. | Partial but extensive; remote gates and live model quality unverified. |
| `security` | Least privilege, approval, redaction, supply-chain, and secret boundaries apply to every element. | Partial; `security-auditor` reviews, secret/runtime/remote state excluded. |

## Sources

External pages below were reopened directly at
`2026-08-08T15:48:51+09:00`. Each returned HTTP 200 without redirect. None
displayed a stable revision identifier, so every vendor observation is
external mutable and valid only at retrieval time.

| Source | Class | Verification |
| --- | --- | --- |
| [Claude hooks](https://code.claude.com/docs/en/hooks) | External mutable, primary | Verified directly: lifecycle events, handler types, decisions, hook locations, and `SessionEnd`. |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents) | External mutable, primary | Verified directly: Markdown/YAML agents, tools, model, effort, permissions, skills, hooks, memory, and isolation. |
| [Claude settings](https://code.claude.com/docs/en/settings) | External mutable, primary | Verified directly: managed/CLI/local/project/user precedence and project settings. |
| [Claude memory](https://code.claude.com/docs/en/memory) | External mutable, primary | Verified directly: instruction and auto-memory separation; context is not enforcement. |
| [Codex hooks](https://learn.chatgpt.com/docs/hooks) | External mutable, primary | Verified directly: 11 events, trust gate, hook locations, and main-thread `SessionEnd`. |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | External mutable, primary | Verified directly: orchestration, required TOML fields, model/reasoning controls, sandbox inheritance. |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | External mutable, primary | Verified directly: global/project discovery, root-to-CWD merge order, and size limit. |
| [Codex config basics](https://learn.chatgpt.com/docs/config-file/config-basic) | External mutable, primary | Verified directly: config precedence and trusted-project boundary. |
| [Codex models](https://learn.chatgpt.com/docs/models) | External mutable, primary | Verified directly: model selection and product reasoning controls; not proof of local entitlement. |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml) | Tracked mutable | Complete registry measured at Task 3 BASE. |
| [Provider/model contract](../../../00.agent-governance/contracts/provider-models.yaml) | Tracked mutable | Complete harness, workflow, loop, event, and model records measured. |
| [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) | Tracked mutable | Corroborated routing map; policy remains in linked owners. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | Tracked stale/advisory | Read first; built from `f8a72211`; no uncorroborated claim retained. |

## Maintenance

Re-measure this leaf when agent/function catalogs, provider models, adapters,
hooks, harness layers, loop/event contracts, eval fixtures, regressions, or
official provider pages change. Record a new baseline and retrieval timestamp,
preserve the evidence-depth distinctions, and route implementation changes to
their canonical Stage 00/03/04 owner.

## Related Documents

- [Loop engineering](./loop-engineering.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
