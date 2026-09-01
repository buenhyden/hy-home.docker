---
status: active
artifact_id: reference:agentic-engineering-research:agent-model-selection
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Reference: Task-Aware Agent Model Selection

## Overview

The workspace selects models by role work profile, not by per-prompt model
shopping. A task first routes to a canonical role; that role declares one of
five profiles; the typed provider contract then supplies the exact native
model and effort/thinking value. This provides deterministic configuration but
does not prove runtime acceptance, entitlement, execution, quality, cost, or
latency.

This 2026-08-14 pass re-derives the routing evidence directly from
`agent-catalog.yaml` and `provider-models.yaml` at repository commit
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`, resolves the exact per-model
effort ladder and subagent thinking-inheritance mechanics from the current
Claude Code references, and compares the workspace's static role-to-profile
routing against current third-party practice for dynamic, complexity-scored
model routing.

## Purpose

Satisfy REQ-29 with task-characteristic selection rules covering role/tier,
model, effort, settings, evaluation, fallback, and atomic change surfaces.

## Repository Role

This Stage 90 analysis explains the existing Model Policy. The policy owners
remain `provider-models.yaml`, `agent-catalog.yaml`, `subagent-protocol.md`, the
renderer, and validators. Recommendations here require a later approved
Stage 03/04 change before they can alter a value.

## Scope

### In scope

- Task characteristics, five work profiles, and provider-native controls.
- Evidence required before selection, fallback, or override changes.
- Evaluation and rollback rules for a proposed model-policy change.

### Out of scope

- Live provider calls, entitlement inspection, price comparison, or benchmarks.
- Direct edits to generated adapters or session-only model overrides.
- Automatic fallback not encoded by the typed contract.

## Definitions / Facts

### Deterministic selection sequence

1. Classify the task by outcome, complexity, reversibility, sensitivity,
   volume, latency tolerance, and required independent challenge.
2. Route to the canonical agent whose scope and permission profile own it.
3. Read that role's single `work_profile` from `agent-catalog.yaml`.
4. Resolve the provider-native exact model/control from
   `provider-models.yaml`; never translate an effort label across providers.
5. Confirm lifecycle, repository disposition, runtime acceptance, entitlement,
   and activation eligibility separately.
6. If acceptance/entitlement evidence is missing, keep `needs_revalidation`;
   do not silently substitute or invent a fallback.
7. Validate repository semantics and, for a policy change, run an approved
   comparative evaluation before updating all coupled surfaces atomically.

### Observable decision inputs

Step 1 of the sequence names seven task characteristics but does not define
how each is observed. This maps every named characteristic to the concrete
workspace signal that stands in for it, since none of these signals is a
live measurement:

| Decision input    | What it means here                                                   | Observable workspace proxy                                                                                                                                                        | Where it is read                                                                           |
| ----------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Task complexity   | How many steps, tools, or ambiguous judgment calls the task needs    | The agent's `tier` (`worker` vs `supervisor`) and `category` in `agent-catalog.yaml`                                                                                              | `agent-catalog.yaml:53-264` (per-agent block)                                              |
| Risk              | Cost of an undetected mistake reaching a protected surface           | `permission_profile` (`read-only` vs `workspace-write`)                                                                                                                           | Same per-agent block; `permissions:` enum at `agent-catalog.yaml:17-24`                    |
| Reversibility     | Whether the action can be cleanly undone                             | Not a typed field; inferred only from `permission_profile` plus the human-owned `mutation_authority` values in `provider-models.yaml`'s `harness_layers`/`workflow_states` blocks | `provider-models.yaml` harness/workflow sections (no dedicated reversibility field exists) |
| Sensitivity       | Whether the domain is security-, policy-, or infrastructure-adjacent | The agent's `scope` value, cross-referenced against `security`/`infra`/`agentic`                                                                                                  | `agent-catalog.yaml` per-agent `scope:` lines                                              |
| Context breadth   | How much source material the task must hold at once                  | `long-horizon-supervision` is reserved for the one `tier: supervisor` role; workers use narrower profiles                                                                         | `agent-catalog.yaml:257-264` (`workflow-supervisor`)                                       |
| Latency tolerance | Whether the task is interactive/blocking or can run longer           | Not a typed field anywhere in either contract; `routine-validation`'s lower effort is the closest proxy, chosen for cost, not measured latency                                    | Absent; named as a gap below                                                               |
| Cost budget       | Acceptable spend for the task                                        | Not a typed field; the profile's registered effort level is a cost proxy, not a budget                                                                                            | Absent; named as a gap below                                                               |

Reversibility, latency tolerance, and cost budget have no dedicated typed
field in either contract today. Routing currently approximates them through
`permission_profile` and the profile's registered effort level. This is
recorded as a gap in "Gaps and revalidation" below rather than treated as an
implemented control.

### Task-characteristic mapping

| Work profile               | Task characteristics                                                      | Claude                                        | Codex                      | Gemini                              | Selection boundary                                                    |
| -------------------------- | ------------------------------------------------------------------------- | --------------------------------------------- | -------------------------- | ----------------------------------- | --------------------------------------------------------------------- |
| `long-horizon-supervision` | Architecture, planning, orchestration, final synthesis, long context      | `claude-opus-5` / `xhigh`                     | `gpt-5.6-sol` / `xhigh`    | `gemini-3.6-flash` / `high`         | Supervisor-only; not a generic escalation for workers.                |
| `complex-implementation`   | Multi-step implementation, tool use, bounded mutation, verification depth | `claude-sonnet-5` / `high`                    | `gpt-5.6-sol` / `high`     | `gemini-3.6-flash` / `high`         | Requires workspace-write role and approved scope.                     |
| `adversarial-review`       | Correctness, policy, security, infrastructure, edge cases                 | `claude-opus-5` / `high`                      | `gpt-5.6-sol` / `xhigh`    | `gemini-3.6-flash` / `high`         | Read-only reviewer distinct from implementer.                         |
| `evidence-research`        | Primary-source retrieval, documentation, bounded synthesis                | `claude-sonnet-5` / `low`                     | `gpt-5.6-terra` / `medium` | `gemini-3.5-flash-lite` / `medium`  | Source quality and claim calibration matter more than model branding. |
| `routine-validation`       | Deterministic checks, drift classification, repetitive bounded work       | `claude-haiku-4-5-20251001` / no effort field | `gpt-5.6-terra` / `low`    | `gemini-3.5-flash-lite` / `minimal` | Use only when completion is decided by deterministic evidence.        |

These are configured repository defaults. The official pages support the
general task-fit hypotheses, but no tracked comparative benchmark establishes
cross-provider equivalence.

### Full role-to-profile registry and the 8-of-14 scope gap

Direct re-read of `agent-catalog.yaml` at commit
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` confirms
exactly 14 `agent_id` entries (`agent-catalog.yaml:53,69,85,103,117,133,147,
162,177,194,211,227,243,257`), matching `EXPECTED_AGENT_COUNT = 14` enforced
in `scripts/lib/agent_governance/agent_governance_contract.py:69`. Every entry's scope,
tier, and work profile:

| `agent_id`            | `scope`    | `tier`       | `work_profile`             |
| --------------------- | ---------- | ------------ | -------------------------- |
| `ci-cd-engineer`      | `ops`      | `worker`     | `complex-implementation`   |
| `code-reviewer`       | `common`   | `worker`     | `adversarial-review`       |
| `doc-writer`          | `docs`     | `worker`     | `evidence-research`        |
| `drift-detector`      | `infra`    | `worker`     | `routine-validation`       |
| `eval-engineer`       | `qa`       | `worker`     | `adversarial-review`       |
| `hook-developer`      | `agentic`  | `worker`     | `complex-implementation`   |
| `iac-reviewer`        | `infra`    | `worker`     | `adversarial-review`       |
| `incident-responder`  | `ops`      | `worker`     | `complex-implementation`   |
| `infra-implementer`   | `infra`    | `worker`     | `complex-implementation`   |
| `qa-engineer`         | `qa`       | `worker`     | `complex-implementation`   |
| `rules-engineer`      | `agentic`  | `worker`     | `adversarial-review`       |
| `security-auditor`    | `security` | `worker`     | `adversarial-review`       |
| `skill-creator`       | `agentic`  | `worker`     | `complex-implementation`   |
| `workflow-supervisor` | `agentic`  | `supervisor` | `long-horizon-supervision` |

The `scopes:` enum at `agent-catalog.yaml:8-16` declares exactly 8 values:
`agentic`, `architecture`, `common`, `docs`, `infra`, `ops`, `qa`, `security`.
This is a strict subset of the pack's fixed 14-scope axis
(`agentic`, `architecture`, `backend`, `common`, `docs`, `entry`, `frontend`,
`infra`, `meta`, `mobile`, `ops`, `product`, `qa`, `security`): 6 axis scopes
— `backend`, `entry`, `frontend`, `meta`, `mobile`, `product` — have no
corresponding value in the catalog's own `scopes:` enum and therefore cannot
be assigned to any agent today, not merely "have zero current agents." Of
the 8 enum scopes, `architecture` is declared but has no agent whose
`scope:` is `architecture` in the table above, so it too is currently unused
even though the catalog's schema permits it. This decomposes what the prior
Scope Implications table stated qualitatively ("no typed X scope") into a
verifiable, file-line-anchored fact: 7 of 14 pack scopes (the 6 missing from
the enum plus `architecture`) route no model-selection decision through any
registered role today.

`code-reviewer` is the sole `common`-scope agent and the only reviewer with
`adversarial-review` outside the `agentic`/`infra`/`qa`/`security` scopes,
which is why the leaf's fallback policy and atomic-change-surface sections
name it as the shared review gate no other scope may bypass.

### Effort and setting rules

- Use the lowest registered effort that meets the profile; never lower a
  review/supervision gate for convenience.
- Claude `effort`, Codex `model_reasoning_effort`, and Gemini scoped
  `thinkingLevel` are different native mechanisms.
- Claude/Codex product-level orchestration modes such as ultracode/Ultra are
  not ordinary per-agent effort values and are not in the local policy.
- A provider default, user setting, organization cap, allowlist, alias,
  resumed session, or safety fallback can change the effective runtime model.
  Repository validation cannot observe that substitution.
- Model configuration is not authorization to access tools, mutate protected
  surfaces, or bypass sandbox/approval controls.

### Subagent model and effort resolution, and the thinking-inheritance gap

The current Claude Code subagents reference documents an exact four-step
resolution order for a subagent's model, from highest to lowest precedence:
(1) the `CLAUDE_CODE_SUBAGENT_MODEL` environment variable, (2) a
per-invocation `model` parameter passed when Claude invokes the subagent,
(3) the subagent definition's `model` frontmatter, (4) the main
conversation's model. `effort` in subagent frontmatter is a separate control
that "overrides the session effort level" and defaults to inheriting from
the session; its allowed values (`low`, `medium`, `high`, `xhigh`, `max`)
are the same five-value Claude ladder documented in
[Provider model landscape](./provider-model-landscape.md#effort-mechanics-per-model-family),
not a distinct subagent-only vocabulary.

Extended thinking is documented as inherited, not independently
configurable: "subagents also inherit the main conversation's extended
thinking configuration: if thinking is on in your session, it's on for the
subagent, and if it's off, it stays off. There is no per-subagent thinking
setting." This directly satisfies the effort/setting rule above that
`effort` and `thinking` are governed separately: a role can override its
own reasoning depth (`effort` in frontmatter) but cannot independently
toggle extended-thinking display or budget; that follows the session. No
tracked generated adapter in this repository sets a `thinking` key, which is
consistent with this provider-native constraint rather than an
independent workspace choice.

The Codex `model_reasoning_effort` field documented by the current
configuration reference (`minimal`/`low`/`medium`/`high`/`xhigh`) does not
match the six-value set recorded in `provider-models.yaml`'s
`supported_reasoning_controls` for the Codex work-profile defaults (adds
`max`/`none`, omits `minimal`). See
[Provider model landscape: Reasoning-control value drift](./provider-model-landscape.md#reasoning-control-value-drift-codex-unverified)
for the full `UNVERIFIED` analysis; the practical selection consequence here
is that `agent-catalog.yaml`'s Codex-routed roles (all `complex-implementation`,
`adversarial-review`, and `long-horizon-supervision` workers) inherit
whichever of `high`/`xhigh`/`low`/`medium` the registry currently configures,
and none of those four configured values falls outside either the old or the
newly observed vendor enumeration, so the drift does not currently invalidate
a configured selection — it only means the registry's stated _supported_
superset should be revalidated before it is used to justify adding a new
Codex-routed default.

### Evaluation gate

The existing 11 synthetic fixtures and 16 regressions check repository
semantics such as routing, closure, model-status honesty, and provider
boundaries. They do not compare live models. A proposed default/profile change
therefore needs versioned representative tasks, the current value as baseline,
an explicit rubric/scorer and threshold, failure cases, privacy boundary,
latency/token observations where permitted, reviewer calibration, and a
rollback literal. Provider prose is a hypothesis, not an acceptance test.

### Fallback policy

The typed workspace contract defines no automatic model fallback graph.
Claude Code can perform provider-native availability or safety fallbacks, but
that capability is external behavior and may substitute a model without a
repository change. Codex product/config sources cited here do not establish a
local automatic fallback. Any desired repository fallback must name trigger,
ordered exact values, entitlement/acceptance evidence, quality floor,
observability, rollback, and coupled changes before adoption.

### Atomic change surface

A model, effort, profile, or fallback change is incomplete unless the same
approved unit updates or verifies all applicable owners:

1. `contracts/provider-models.yaml` and `subagent-protocol.md`;
2. `contracts/agent-catalog.yaml` when role/profile routing changes;
3. provider renderer logic and every generated adapter/config output;
4. validators, deterministic fixtures, and regression expectations;
5. Stage 04 approval, exact source/date, evaluation, validation, and rollback;
6. provider-surface sync and independent specification/quality review.

### External model-routing practice compared to workspace policy

Current third-party practice for agentic-system model routing (2026-08-14
web survey, External mutable, not adopted here) centers on dynamic,
per-request complexity classification: a routing layer scores each request
(commonly using token count, presence of code blocks, and embedding
similarity against labeled examples) and dispatches to the cheapest model
that can handle it, with reported bill reductions in a 40-85% range and
routing overhead from under 1 ms (rule-based) to 50-100 ms (semantic/ML
classifiers) — small relative to typical LLM response latency. Academic
work such as the TRACE-Router line (task-consistent, adaptive online
routing for agentic AI) formalizes this as an online decision problem over
a stream of heterogeneous tasks rather than a static per-role assignment.

This repository's routing is the structural opposite: profile assignment is
static and role-scoped (`agent-catalog.yaml`'s one `work_profile` per
`agent_id`), not per-request or complexity-scored, and there is no typed
classifier, token-count heuristic, or embedding-similarity check anywhere in
either contract. That is a deliberate simplicity/reviewability tradeoff
appropriate to a governance-gated repository — every model selection is
traceable to one static, reviewed table cell rather than a runtime
classifier decision that would itself need evaluation and drift monitoring —
but it also means none of the industry cost-reduction figures above transfer
to this repository's economics, and this leaf makes no claim that they do.
The gap this surfaces is named below rather than treated as a defect: a
future Stage 03 change could add a bounded, typed complexity signal (for
example, a Task-level `estimated_complexity` field) without adopting a live
classifier, but no such field exists today.

### Gaps and revalidation

- No typed field for reversibility, latency tolerance, or cost budget exists
  in `agent-catalog.yaml` or `provider-models.yaml`; both are currently
  approximated through `permission_profile` and registered effort, per
  "Observable decision inputs" above. Closing this needs an approved Stage 03
  schema addition, not a leaf-level recommendation.
- 6 of the pack's 14 scopes (`backend`, `entry`, `frontend`, `meta`,
  `mobile`, `product`) have no value in `agent-catalog.yaml`'s `scopes:`
  enum, so no role in any of those scopes can exist without a prior schema
  change. `architecture` is enumerated but currently has zero assigned
  agents. Observation that would close this: an approved catalog change
  request naming the owning role, permission profile, and work profile for
  any of these scopes before a role is added.
- The Codex `model_reasoning_effort` supported-value drift (`UNVERIFIED`,
  detailed in [Provider model landscape](./provider-model-landscape.md#reasoning-control-value-drift-codex-unverified))
  has not been revalidated against the exact `reasoning_source_url` cited
  per Codex model row; until it is, treat the registry's stated Codex
  reasoning-control superset as unconfirmed even though today's four
  configured Codex defaults are unaffected.
- No workspace evaluation fixture exercises the subagent model-resolution
  precedence order (environment variable, per-invocation parameter,
  frontmatter, inherited) end to end; the 11 fixtures and 16 regressions
  check repository semantics, not this provider-native precedence chain.
  Observation that would close this: a synthetic fixture that asserts which
  of the four sources should win for a given generated adapter.

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **Setting the Claude effort control to its high value is a no-op.** Official guidance states that setting the effort control to `high` produces exactly the same behaviour as omitting the parameter. A profile configured at that value therefore matches the provider default and must not be read as the workspace raising effort. **Identifiers restored 2026-08-19** after a seat found `CVD-` occurred zero times pack-wide while this pack holds naming an identifier to be load-bearing elsewhere, at `agent-instructions-vibe-coding.md` where three criteria are named because an unnamed marker attaches to nothing. The retiring source names the cells: `CVD-01` and `CVD-04` configure the default explicitly, which is defensible as pinning against a future default change but must not be read as the workspace raising effort for adversarial review or complex implementation; only `CVD-07` and `CVD-10` move Claude off its default at all.
- **Gemini thinking is not a per-agent file control.** The Gemini CLI subagent file schema carries no reasoning or thinking field, so configured thinking values are not per-agent file controls; their destination is the model-config `thinkingConfig.thinkingLevel` path. The schema does carry `temperature`, which an earlier description omitted.

### Selection criteria and evaluation

The profile names encode task characteristics, not a live classifier.
`routine-validation` is appropriate only where deterministic evidence decides
completion; `evidence-research` emphasizes source-calibrated synthesis;
`complex-implementation` requires scoped mutation authority; and
`adversarial-review` is a separate challenge role. These are adoption options
based on registry declarations, not assertions that one provider model is
superior to another.

The declared pairs are concrete but static: adversarial review uses Opus/high
or Sol/xhigh; complex implementation Sonnet/high or Sol/high; evidence
research Sonnet/low or Terra/medium; long-horizon supervision Opus/xhigh or
Sol/xhigh; and routine validation Haiku/no Claude effort value or Terra/low.
Each is read from the five registry profiles, so it does not establish provider
entitlement, actual model resolution, or a cross-provider quality ranking.

A proposed promotion needs a frozen representative task set, a baseline,
explicit rubric and threshold, failure cases, permitted latency/cost evidence,
reviewer calibration, and rollback. The local configuration alone cannot show
effective runtime selection because native precedence and account constraints
can intervene. The retained native observation supports that distinction; it
does not evidence that an environment override was set here.

## Scope Implications

| Scope          | Application and disposition                                                                                                                                                                                                                                       |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Owns work profiles, provider mapping, renderer, and change protocol; `hook-developer`, `rules-engineer`, `skill-creator`, and `workflow-supervisor` are its 4 agents (`agent-catalog.yaml:133,211,243,257`); only `workflow-supervisor` uses the supervisor tier. |
| `architecture` | Enumerated in `scopes:` (`agent-catalog.yaml:10`) but assigned to zero agents; route architecture judgment to the supervisor profile only after an approved catalog change adds an owning role.                                                                   |
| `backend`      | Not in `agent-catalog.yaml`'s `scopes:` enum at all; a future backend role/model requires an approved schema addition, Spec, evaluation, and typed route before it can exist.                                                                                     |
| `common`       | `code-reviewer` is the sole `common`-scope agent and uses adversarial review; shared work cannot self-upgrade or bypass independent review.                                                                                                                       |
| `docs`         | `doc-writer` uses evidence research; source traceability and calibration remain mandatory at a lower effort.                                                                                                                                                      |
| `entry`        | Not in the `scopes:` enum; current gateway work routes through `infra` profiles instead, and model choice there does not authorize runtime gateway mutation.                                                                                                      |
| `frontend`     | Not in the `scopes:` enum; use the current `qa`-scope owner for the QA fixture and require an approved schema change before a `frontend` role can exist.                                                                                                          |
| `infra`        | 3 agents — `drift-detector` (routine-validation), `iac-reviewer` (adversarial-review), `infra-implementer` (complex-implementation); runtime evidence stays separate from configured selection.                                                                   |
| `meta`         | Not in the `scopes:` enum; metadata work routes through `docs` until an approved schema change adds it, and deterministic validators still decide completion.                                                                                                     |
| `mobile`       | Not in the `scopes:` enum; no model selection is inferred for a nonexistent mobile role.                                                                                                                                                                          |
| `ops`          | 2 agents — `ci-cd-engineer` and `incident-responder`, both `complex-implementation`; incident/runtime outcomes and rate limits require direct evidence beyond configuration.                                                                                      |
| `product`      | Not in the `scopes:` enum; stakeholder judgment and product approval cannot be delegated to a model tier even if a role is later added.                                                                                                                           |
| `qa`           | 2 agents — `eval-engineer` (adversarial-review) and `qa-engineer` (complex-implementation); owns comparative evaluation design; synthetic scores are not live-model scores.                                                                                       |
| `security`     | `security-auditor` is the sole `security`-scope agent, using adversarial review and read-only permissions; specialized-provider labels never imply entitlement.                                                                                                   |

## Sources

| Source                                                                                                                                                      | Accessed                  | Class             | Verification state                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview)                                                               | 2026-08-08T16:18:04+09:00 | External mutable  | HTTP 200 via canonical redirect; task-fit/lifecycle facts only.                                                                             |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config)                                                                             | 2026-08-08T16:18:04+09:00 | External mutable  | HTTP 200; effort, alias, restriction, and fallback mechanics.                                                                               |
| [Codex models](https://learn.chatgpt.com/docs/models)                                                                                                       | 2026-08-08T16:18:04+09:00 | External mutable  | HTTP 200; task-fit and reasoning guidance.                                                                                                  |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)                                                                | 2026-08-08T16:18:04+09:00 | External mutable  | HTTP 200; `model` and native configuration fields.                                                                                          |
| Provider model contract (retired path: `../../../00.agent-governance/contracts/provider-models.yaml`)                                                                      | 2026-08-08                | Workspace tracked | Five profiles, 11 model rows, and separated status axes at Task 4 baseline.                                                                 |
| Agent catalog contract (retired path: `../../../00.agent-governance/contracts/agent-catalog.yaml`)                                                                         | 2026-08-08                | Workspace tracked | Fourteen role-to-profile assignments and evaluation owner.                                                                                  |
| [Provider model evaluation function](../../../00.agent-governance/skills/provider-model-evaluation.md)                                            | 2026-08-08                | Workspace tracked | Source, native-schema, regression, and `needs_revalidation` gate.                                                                           |
| [Claude Code subagents reference](https://code.claude.com/docs/en/sub-agents)                                                                               | 2026-08-14T13:40:00+09:00 | External mutable  | HTTP 200; subagent model-resolution precedence, `effort` frontmatter, and the explicit no-per-subagent-thinking statement.                  |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)                                                                | 2026-08-14T13:40:00+09:00 | External mutable  | Re-read; HTTP 200; source of the `model_reasoning_effort` five-value drift analysis.                                                        |
| Agent catalog contract (retired path: `../../../00.agent-governance/contracts/agent-catalog.yaml`)                                                                         | 2026-08-14                | Workspace tracked | Re-read at commit `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`; 14 agents, 8-value `scopes:` enum, full role table re-derived line by line.   |
| [Governance contract validator](../../../../scripts/lib/agent_governance/agent_governance_contract.py)                                                                | 2026-08-14                | Workspace tracked | `EXPECTED_AGENT_COUNT = 14` / `EXPECTED_FUNCTION_COUNT = 24` / `EXPECTED_PROVIDER_COUNT = 3` constants at lines 69-71.                      |
| [LLM model routing 2026: cost-quality optimization](https://www.digitalapplied.com/blog/llm-model-routing-2026-cost-quality-optimization-engineering-guide) | 2026-08-14                | External mutable  | Dynamic complexity-scored routing practice and reported cost-reduction figures; not adopted, comparative only.                              |
| [TRACE-Router: task-consistent and adaptive online routing for agentic AI](https://arxiv.org/html/2607.22465v1)                                             | 2026-08-14                | External fixed    | Versioned arXiv preprint; formalizes dynamic routing as an online decision problem, contrasted against this repository's static assignment. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `workflow-supervisor` resolves role/profile from `registry.yaml`. | Check the named profile pair. | Native runtime precedence remains unobserved. |
| architecture | applies | Architecture owner approves changed routing semantics. | Inspect an approved change record. | No routing change is proposed. |
| common | applies | `code-reviewer` confirms implementer/reviewer separation. | Review role and profile mapping. | Role mapping is static only. |
| docs | applies | `doc-writer` records source-backed selection boundaries. | Reconcile README IDs. | This is advisory documentation. |
| infra | applies | `infra-implementer` assesses endpoint compatibility/capacity for a concrete deployment target. | Review a target-specific approval record. | No provider endpoint invoked. |
| ops | applies | `incident-responder` owns any availability or fallback policy for operations. | Inspect an approved runbook or incident record. | No fallback graph exists. |
| qa | applies | `qa-engineer` owns the comparative-evaluation proposal. | Inspect frozen task/rubric before promotion. | No evaluation executed. |
| security | applies | `security-auditor` assesses sensitivity and entitlement evidence. | Review sanitized approval evidence. | No account/organization state read. |

## Maintenance

Revalidate when task taxonomy, roles, profiles, exact IDs, provider reasoning
controls/defaults, evaluation fixtures, fallback capability, renderer, or
validators change. Never update a generated adapter alone.

## Related Documents

- [Provider model landscape](./provider-model-landscape.md)
- [AI agent catalogs](./ai-agent-catalogs.md)
- [Agent instructions](./agent-instructions-vibe-coding.md)
- [Scope application matrix](./scope-application-matrix.md)
- Subagent protocol (retired path: `../../../00.agent-governance/subagent-protocol.md`)
- [SPEC-0158 preservation contract](../../../03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
