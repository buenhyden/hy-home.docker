---
status: active
artifact_id: spec:132-agent-governance-harness-convergence
artifact_type: spec
parent_ids:
  - spec:128-agentic-audit-harness-consolidation
---

# Agent Governance Harness Convergence Design Specification

**Date:** 2026-07-15 (Asia/Seoul)

**Status:** Approved and active

**Scope:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/`, `.claude/`,
`.codex/`, new `.gemini/`, `.github/`, `docs/00.agent-governance/`, and the
supporting generators, validators, tests, Stage 04 evidence, and canonical
Stage 90 audit updates required to keep those surfaces enforceable.

## Overview

The repository intends Stage 00 to be the provider-neutral source of truth for
agent governance. The current implementation has strong structural coverage,
but its effective authority flows in both directions:

- the provider sync script derives skills from `.claude/skills/` even though
  Stage 00 declares the canonical function catalog;
- Codex TOML adapters omit current native required fields such as
  `description` and `developer_instructions`;
- `.agents/` is described partly as Gemini runtime support even though current
  Gemini CLI uses `.gemini/agents/*.md` and `.gemini/settings.json`;
- provider-neutral agent entries and rich provider prompts do not preserve the
  same role semantics;
- several Stage 00 ownership rules overlap or conflict;
- local pre-push routing omits root and provider governance surfaces;
- harness structure exists, but the canonical audit still records every loop
  criterion as Partial and no measured depth-4 closure.

The canonical July 5 audit pack remains the only current status source. The
July 7 pack is a superseded mapping aid and must not supply current counts or
recommendations.

## Boundaries and Inputs

### Approved Decisions

The user approved the following design choices:

1. Use a staged canonical convergence rather than an all-at-once rewrite or a
   validator-only patch.
2. Add `.gemini/**` as the official Gemini CLI runtime adapter surface.
3. Treat `.agents/` as the Antigravity/common compatibility and shared-skill
   surface, not as Gemini CLI native parity.
4. Apply `agency-agents` through capability-gap analysis. Do not wholesale
   import upstream identities, personalities, or the full roster.
5. Revalidate model policy against official sources as of 2026-07-15 KST.
   Separate stable/current, preview, deprecated, entitlement, and local
   availability; do not use moving `latest` aliases as defaults.
6. Use type-specific metadata rather than forcing identical keys across
   governance documents and provider-native formats.
7. Use Subagent-Driven Development with a fresh implementer and a separate
   reviewer for every logical task, followed by whole-branch review.
8. Keep direct agent execution of `pre-commit run --all-files` prohibited. The
   approved final gate uses the controlled repository wrapper and records
   sanitized evidence.

### Goals

- Make Stage 00 the actual, machine-enforced authority for agent roles,
  functions, provider projections, model routing, path authority, and
  harness/loop contracts.
- Normalize frontmatter and sections by artifact type, remove legacy keys and
  duplicated policy, and keep README files profile-specific indexes.
- Generate Claude, Codex, and Gemini runtime adapters from canonical Stage 00
  definitions using each provider's native schema.
- Make provider capability, repository adoption, runtime acceptance, and
  validation depth distinct states.
- Consolidate overlapping agent roles and complete the canonical function
  catalog without copying provider-specific policy into adapters.
- Add deterministic schema/drift checks and representative semantic evals to
  CI and local QA routing.
- Update the canonical audit and task evidence from observed results, without
  promoting unverified runtime claims.

### Non-Goals

- User-global `~/.claude`, `~/.codex`, or `~/.gemini` changes.
- Credential, token, entitlement, or authentication changes.
- Docker Compose, deployment runtime, promotion, or rollback implementation.
- Remote GitHub ruleset, environment, secret, push, PR, or merge actions.
- An always-on orchestrator or wholesale `agency-agents` installation.
- Floating model aliases or preview models as repository defaults.
- Claims of provider runtime acceptance when the provider CLI or entitlement
  cannot be checked.

## Contracts

### Authority Architecture

Authority flows in one direction:

```text
Stage 00 typed contracts, catalog, and model policy
                         |
                         v
              provider surface generator
                 /          |          \
                v           v           v
             Claude       Codex       Gemini
             native       native       native
            adapters     adapters     adapters
                 \          |          /
                  v         v         v
                   validator, CI, QA evidence
```

#### Canonical layers

- `docs/00.agent-governance/` owns normative policy and canonical role/function
  definitions.
- Machine-readable Stage 00 contracts separately own:
  - artifact types, frontmatter, required sections, and README profiles;
  - agent/function responsibilities, scopes, permissions, model profiles, and
    provider projections;
  - provider capability/adoption and model status, checked time, evidence,
    eligibility, and fallback.
- Root shims contain only the minimum bootstrap/import sequence.
- `.claude/`, `.codex/`, and `.gemini/` are generated or validated runtime
  adapters, never independent policy authorities.
- `.agents/` is a compatibility/shared-function projection with explicit
  status and source references.

#### Generator rules

- The generator reads only canonical Stage 00 contracts and source documents.
- Provider adapters use native provider keys and file layouts.
- Generated content has deterministic ordering and an origin marker or
  equivalent manifest record.
- `--check` is read-only and reports semantic drift; the write mode is
  explicit and idempotent.
- Provider-only prose must not create policy absent from the canonical source.

### Typed Metadata and Document Structures

#### Root and governance documents

- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are instruction shims, not lifecycle
  documents. General YAML frontmatter is removed unless a provider formally
  requires it.
- Ordinary Stage 00 governance documents retain minimal `layer: agentic`.
- Provider overlays add only the applicable `runtime` field.
- H1-duplicating `title`, overlapping identifiers, meaningless dates, and
  lifecycle keys without lifecycle semantics are removed.
- Hookify/native rule schemas remain explicit artifact-type exceptions rather
  than receiving unrelated generic keys.

#### Canonical agent metadata

```yaml
layer: agentic
artifact_type: agent-role
agent_id: code-reviewer
scope: common
tier: worker
status: active
```

Required sections are Purpose, Use When, Inputs, Outputs, Permissions, Success
Criteria, Failure and Escalation, and Related Documents.

#### Canonical function metadata

```yaml
layer: agentic
artifact_type: agent-function
function_id: code-review
scope: common
status: active
```

Required sections are Preconditions, Inputs, Procedure, Outputs, Gates,
Failure Handling, and Related Documents. Placeholder or copied template prose
does not satisfy the contract.

#### Provider metadata

- Claude agent Markdown uses only Claude-supported frontmatter fields and an
  executable instruction body.
- Codex TOML includes current native required fields such as `name`,
  `description`, and `developer_instructions`, plus supported model, reasoning,
  sandbox, MCP, and skill settings when justified.
- Gemini agent Markdown uses native fields such as `name`, `description`,
  `kind`, tools, model, turn, and timeout controls.
- Unsupported local metadata such as catalog paths and role scope remains in
  the canonical contract and is not injected into strict provider schemas.

#### README profiles

README files remain navigation and ownership surfaces. Policy, contracts, and
long provider behavior descriptions live in their canonical documents. The
implementation may normalize existing sections but must not invent arbitrary
README sections.

### Path Authority

One machine-readable matrix records the canonical owner, permitted
contributors, mandatory reviewers, protected status, validation, and rollback
for each governed path family.

| Surface | Canonical owner | Mandatory review |
| --- | --- | --- |
| Stage 00 policy/contracts and root shims | `rules-engineer` | `workflow-supervisor` |
| Agent role catalog | domain owner + `rules-engineer` | `workflow-supervisor` |
| Function/skill catalog | `skill-creator` | domain owner |
| Provider adapters and hooks | `hook-developer` | `rules-engineer`, `security-auditor` |
| Validators and QA evidence | `qa-engineer` | `rules-engineer` |
| GitHub workflow | `ci-cd-engineer` | `security-auditor`, `qa-engineer` |

`doc-writer` may implement approved documentation changes but is not the sole
owner of Stage 00 policy. Read-only reviewers do not gain duplicate ownership
of operational, incident, or specification artifacts.

## Core Design

### Provider and Model Projection

#### Approved default profiles

| Work profile | Claude | Codex | Gemini |
| --- | --- | --- | --- |
| Supervision, architecture, complex planning | `claude-opus-4-8` | `gpt-5.6`, `high`/`xhigh` | `gemini-3.5-flash` |
| Complex implementation, security, precision review | `claude-sonnet-5`, with approved Opus escalation | `gpt-5.6`, `medium`/`high` | `gemini-3.5-flash` |
| Exploration, large reads, repetitive organization | `claude-haiku-4-5-20251001` | `gpt-5.6-terra`, `low`/`medium` | `gemini-3.1-flash-lite` |

`claude-fable-5` is a generally available exceptional-capability profile, not
the routine supervisor default. `gpt-5.3-codex-spark`, invitation-only Claude
models, and `gemini-3.1-pro-preview` remain non-default catalog entries.

Each registry entry records provider-reported status, source URL, checked time,
entitlement state, repository default eligibility, supported reasoning or
thinking controls, task fit, and a rollback/fallback value. Provider-reported
availability and local entitlement are never conflated.

### Approved Fallback Edges

An `approved-degraded` fallback is authorized only by a typed
`fallback_approvals` record in the provider-model contract. Each record binds
one provider, source model, target model, exact source work-profile set, and
this resolvable section. A model row references the approval ID; prose-shaped
or nonexistent fragments do not authorize an edge.

| Provider | Source | Target | Authorized work profiles |
| --- | --- | --- | --- |
| Claude | `claude-fable-5` | `claude-opus-4-8` | `complex-implementation`, `supervision` |
| Claude | `claude-haiku-4-5-20251001` | `claude-sonnet-5` | `read-heavy-repetitive` |
| Claude | `claude-mythos-5` | `claude-opus-4-8` | `complex-implementation`, `supervision` |
| Claude | `claude-opus-4-1-20250805` | `claude-opus-4-8` | none; migration-only |
| Claude | `claude-opus-4-8` | `claude-sonnet-5` | `supervision` |
| Claude | `claude-sonnet-5` | `claude-opus-4-8` | `complex-implementation` |
| Codex | `gpt-5.2-codex` | `gpt-5.6-terra` | none; migration-only |
| Codex | `gpt-5.6-terra` | `gpt-5.6` | `read-heavy-repetitive` |
| Codex | `gpt-5.6` | `gpt-5.6-terra` | `complex-implementation`, `supervision` |
| Gemini | `gemini-3.1-flash-lite-preview` | `gemini-3.1-flash-lite` | none; migration-only |
| Gemini | `gemini-3.1-flash-lite` | `gemini-3.5-flash` | `read-heavy-repetitive` |
| Gemini | `gemini-3.5-flash` | `gemini-3.1-flash-lite` | `complex-implementation`, `supervision` |

Cutoff evidence is separate from this current provider-schema authority. A
model can claim `verified-before-cutoff` only by referencing a typed official
evidence record whose publication time is at or before the approved cutoff and
whose observation time equals the contract retrieval time. Current CLI
capability documentation does not retroactively prove historical model state.

#### Claude

- Restore the actual root import sequence.
- Remove fenced literal imports and other prompt constructs that pass substring
  checks but do not load as instructions.
- Use pinned model IDs where supported and least-privilege tool settings.
- Map supported Claude hook events to shared semantic events without making
  unsupported parity claims.

#### Codex

- Regenerate native TOML with required description and developer instructions.
- Remove or relocate unsupported non-native fields.
- Validate current hook events, matcher rules, handler types, blocking
  semantics, and timeouts. Unsupported events are marked as gaps rather than
  counted as native parity.
- Use supported per-agent model, reasoning, and sandbox controls.

#### Gemini

- Add project-native `.gemini/agents/*.md` and `.gemini/settings.json`.
- Add thin project hook wrappers only where needed to dispatch to shared logic.
- Apply role-specific tools, MCP boundaries, turns, timeouts, and recursion
  protection.
- Keep Antigravity/common compatibility in `.agents/` and Gemini CLI runtime
  behavior in `.gemini/`.

### Agent and Function Catalog

#### Role changes

- Retire `style-enforcer` as a standalone agent. Move deterministic formatting,
  output-style, and lint routing to `qa-engineer` and the style-validation
  function.
- Retire `wiki-curator` as a standalone agent. Move generated index and
  freshness work to `doc-writer` and the knowledge-map function.
- Retain `iac-reviewer` for pre-change static IaC/Compose review.
- Retain `drift-detector` for post-change declared-versus-observed read-only
  comparison.
- Add `eval-engineer` for representative datasets, semantic scorers,
  calibration, thresholds, and regression history.

The resulting canonical catalog has 14 agents: one supervisor, seven
implementation/operations roles, and six independent review/evaluation roles.

#### Capability intake

`agency-agents` is evidence, not an install source. A capability intake ledger
maps upstream capability to recurring workspace need, existing owner, uncovered
responsibility, measurable evaluation, and an adopt/merge/reject/defer decision.
Technical writing, code review, DevOps, SRE, incident, reality-checking, and
multi-agent architecture capabilities strengthen existing owners. Product
discovery remains deferred until recurring demand and a representative eval
exist.

#### Function convergence

- Complete all 22 canonical functions with typed inputs, procedures, outputs,
  gates, and failure handling.
- Replace the seven current placeholder entries with canonical content derived
  from approved workspace behavior, not provider-local prompt text.
- Generate provider-native skill projections from the canonical functions.
- Detect provider-local policy additions and semantic drift.

### Harness and Loop Design

The shared harness defines semantic events rather than pretending provider
event names are identical:

```text
session start
  -> context/bootstrap
  -> plan/spec approval
  -> bounded implementation loop
  -> independent review loop
  -> scoped QA
  -> approved all-files wrapper
  -> evidence and closure
```

Every loop has:

- an owner and independent reviewer;
- a maximum retry count and explicit stop condition;
- retry, narrower-scope retry, and escalation behavior;
- least-privilege tools and sandbox;
- deterministic checks plus representative semantic fixtures;
- sanitized evidence recording commands, results, skips, and rollback;
- honest maturity status when native dispatch or local entitlement is not
  observed.

The design does not introduce an always-on issue-tracker orchestrator. It first
improves repository legibility, isolated execution, evaluation, feedback, and
recovery.

## Interfaces and Data

### Validator, CI, and QA

#### Typed validator

A focused validator and unit-test suite own Stage 00 contract semantics. The
existing repository-contract shell calls it as an aggregate gate rather than
absorbing another large inline rule block.

The validator checks:

- artifact inventory and exactly one artifact type per file;
- type-specific keys, order, enum, and required sections;
- root-shim and README profile constraints;
- path authority and protected-surface review requirements;
- canonical agent/function completeness;
- provider-native schema and semantic projection;
- executable imports rather than string-only matches;
- model source, status, date, eligibility, and fallback;
- hook capability versus repository adoption;
- retired references, nonexistent runtime paths, and generator drift;
- semantic fixture catalog, scorers, thresholds, and regression results.

Errors identify file and field/section, expected and actual values, and the
canonical source.

#### CI and local routing

- Keep repository-contract validation within the existing `repo-contracts`
  job.
- Extend the existing agent-output fixture job for representative routing,
  role-boundary, completion-evidence, hook-denial, and adapter-rendering cases.
- Extend pre-push routing to root shims, all four provider/compatibility trees,
  Stage 00, and coupled generator/validator/test files.
- Preserve read-only workflow permissions, SHA-pinned actions, and secret-safe
  output.
- Do not add deployment or runtime mutation.

#### Verification ladder

Per logical commit:

- parser or validator unit tests;
- generator `--check`;
- focused contract tests;
- `git diff --check`.

Per provider batch:

- native schema validation;
- hook semantic mapping;
- adapter/catalog parity;
- model registry checks.

At final closure:

- changed-document metadata with an explicit safe base;
- repository contracts and documentation traceability;
- harness validation and semantic eval fixtures;
- approved controlled all-files pre-commit wrapper;
- sanitized Stage 04 evidence and progress memory;
- Graphify refresh, or an explicit CLI-unavailable record.

## Failure Modes and Guardrails

- Missing provider CLI or entitlement produces `needs_revalidation`, not a
  fabricated pass.
- Generators default to dry-run and use explicit, deterministic write mode.
- Raw logs, tokens, auth data, shell history, and secret values are never
  persisted as evidence.
- A semantic-eval failure receives at most two fix/review attempts before
  narrowing scope and escalating.
- Each task is one independently revertible logical commit or a small group of
  explicitly coupled commits.
- Deleted agents, functions, or paths are removed with their generated adapters
  and cross-links in the same task.
- The canonical audit is updated only after observed validation; superseded
  packs remain non-canonical.

## Agent Role and IO Contract

Work runs in `.worktrees/agent-governance-harness-convergence` on
`codex/agent-governance-harness-convergence`, leaving the root checkout on
`main`.

1. Typed governance foundation: inventory, migration ledger, contracts,
   validator, and tests.
2. Metadata, authority, and root shims: normalize Stage 00 and provider entry
   points; resolve stale Hookify and ownership text.
3. Agent/function catalog: retire two roles, add `eval-engineer`, complete the
   functions, and reverse the skill SSoT dependency.
4. Native providers: converge Claude and Codex and add Gemini native adapters,
   hooks, model registry, and routing.
5. Harness/loop and CI/QA: semantic event mapping, permissions, retry/evidence,
   fixtures, generator drift, and routing.
6. Corpus closure: retire references, refresh the canonical audit, record Stage
   04 evidence and memory, run full QA, and complete whole-branch review.

Every implementation task uses a fresh implementer and a separate reviewer.
Critical and Important review findings must be fixed and re-reviewed. Shared
worktree implementation is sequential; read-only discovery and review may run
in parallel. The SDD ledger and per-task brief, report, review, and review-fix
artifacts are maintained according to the selected skill.

## Verification

The implementation is complete only when every task has focused test evidence,
independent specification and quality approval, and the final exact branch
range passes the full verification ladder defined above. The commit sequence
must remain independently reviewable and revertible:

1. Design document.
2. Implementation plan.
3. Typed contracts and validator.
4. Metadata, authority, and shim normalization.
5. Agent/function catalog convergence.
6. Provider-native adapters and model policy.
7. Harness, loop, CI, QA, and semantic evaluation.
8. Audit, evidence, memory, and closure.

### External Evidence Baseline

Official sources checked on 2026-07-15 KST include:

- OpenAI Codex subagents, hooks, models, configuration, and harness engineering:
  - <https://learn.chatgpt.com/docs/agent-configuration/subagents>
  - <https://learn.chatgpt.com/docs/hooks>
  - <https://openai.com/index/harness-engineering/>
  - <https://openai.com/index/unrolling-the-codex-agent-loop/>
- Anthropic Claude subagents, hooks, models, versioning, and effective-agent
  guidance:
  - <https://code.claude.com/docs/en/sub-agents>
  - <https://code.claude.com/docs/en/hooks>
  - <https://platform.claude.com/docs/en/about-claude/models/overview>
  - <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>
  - <https://www.anthropic.com/engineering/building-effective-agents>
- Gemini CLI native agents, hooks, configuration, model status, and deprecation:
  - <https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md>
  - <https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md>
  - <https://ai.google.dev/gemini-api/docs/models>
  - <https://ai.google.dev/gemini-api/docs/deprecations>
- Capability catalog reference:
  - <https://github.com/msitarzewski/agency-agents>

External facts are recorded with their observed date and must not be treated as
permanent provider guarantees.

## Related Documents

- [Parent audit harness specification](../128-agentic-audit-harness-consolidation/spec.md)
- [Canonical Stage 00 governance hub](../../00.agent-governance/README.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Provider capability matrix](../../00.agent-governance/rules/provider-capability-matrix.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
