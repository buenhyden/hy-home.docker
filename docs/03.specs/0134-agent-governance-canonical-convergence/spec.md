---
profile_id: spec
status: active
artifact_id: SPEC-0134
artifact_type: spec
parent_ids:
  - SPEC-0132
  - SPEC-0133
created: 2026-07-26
updated: 2026-08-11
---
# Agent Governance Canonical Convergence Specification

**Date:** 2026-07-26 (Asia/Seoul)

**Status:** Active

## Overview

This specification defines the successor convergence wave for the repository's
agent-governance control plane. It retains the architecture completed by Spec
132: Stage 00 is the only policy and catalog authority, root provider files are
thin entry adapters, and provider-native agent surfaces are deterministic
projections. The wave updates that architecture for current provider models,
removes retired and deprecated entries from active contracts, routes execution
state to the active owning Task, reconciles harness and loop
semantics, and improves local GitHub Actions and QA governance without mutating
the remote GitHub control plane.

The current targets are `AGENTS.md`, `CLAUDE.md`, `.agents/**`, `.claude/**`,
`.codex/**`, `.github/**`, and `docs/00.agent-governance/**`. Only Claude and
Codex remain supported. Stage 99 owns document shapes and lifecycle; the current
owning Task owns progress and handoff, with Git providing historical recovery.

Read-only discovery at local baseline `e65bb18f` found a sound generated
foundation: 14 role identities are present in Stage 00 and in every provider
agent projection, and 22 function identities are present in Stage 00,
`.agents/skills`, and `.claude/skills`. Root entry files are thin. Generated
hook parity is fresh. The active model contract, however, has a
2026-07-10 cutoff and a 2026-07-16 retrieval time and is already stale against
current official model catalogs. Duplicate-safe parsing confirms that the
current `agent-catalog.yaml` contains no duplicate key; the previously reported
`skill-creator.scope` duplicate therefore becomes a negative regression case
rather than a live cleanup claim. Active contracts still carry retired role
transfers and deprecated model records that belong in historical evidence
instead.

The public remote GitHub observation is deliberately separate from local
truth. On 2026-07-26 the remote default branch was at `a897978f`, while the
local `main` was 92 commits ahead. The latest observed remote CI Quality Gates
run failed and exposed 15 jobs, while the local tracked contract defines 16.
Three active remote workflows are GitHub-managed rather than tracked in this
repository. Current rulesets, required checks, workflow logs, Actions policy,
environments, secrets, and variables could not be authenticated and remain
`unverified`. This wave may improve local definitions and evidence, but it may
not claim or change remote enforcement.

## Boundaries and Inputs

### Approved Scope

- Keep Stage 00 as the only canonical agent-policy, role, function, model,
  event, loop, and permission authority.
- Normalize Stage 00 governance frontmatter, section envelopes, key order,
  value domains, and duplicate-key rejection without forcing provider-native
  files into the document metadata schema.
- Remove retired and deprecated models, role-transfer records, fallback edges,
  adapter references, and unsupported parameters from active contracts and
  projections.
- Preserve retirement date, replacement, rationale, and immutable historical
  references in Stage 90 evidence.
- Revalidate current Claude and Codex model catalogs and assign model
  and reasoning settings by work profile.
- Keep API catalog availability distinct from provider CLI/runtime acceptance
  and account entitlement.
- Route supported-provider entry points to the active Spec and current owning
  Task without a separate shared state document.
- Update the agent capability intake against `agency-agents` without importing
  its personas or creating duplicate role authorities.
- Add only capabilities that pass the role/function admission contract.
- Reconcile harness layers, loop states, approval boundaries, stop gates,
  independent review, evidence, retry, and handoff semantics.
- Improve local workflow security, tool pinning, local CI contract checks,
  controlled QA evidence, and remote Actions inventory.
- Remove verified one-time, obsolete, duplicated, or generated-drift files
  only after ownership, consumer, provenance, and rollback checks.
- Update direct-impact renderers, validators, tests, canonical audits,
  generated evidence, and Stage 04 execution artifacts.
- Execute implementation through logical commits, fresh implementation agents,
  independent task reviewers, and a fresh whole-branch review.

### Direct-Impact Exception

The primary target list authorizes direct-impact changes outside those roots
when they are necessary to keep an approved target truthful and executable.
The allowed direct-impact set is limited to:

- the provider-surface renderer and sync entry point;
- agent-governance, provider, memory, hook, workflow, and QA validators;
- focused unit, regression, fixture, and static-analysis tests;
- the controlled agent QA wrapper and its evidence sanitizer;
- the canonical 2026-07-05 audit pack and generated governance evidence;
- this Spec's Plan, Task ledger, and sanitized execution evidence;
- generated indexes whose owner declares an affected target as input.

Every direct-impact mutation must be linked to an approved requirement in the
Task ledger. Adjacency alone is not authorization.

### Non-goals

- Pushing a branch, merging remotely, dispatching a workflow, changing a
  ruleset, changing branch protection, changing required checks, or editing
  any other GitHub control-plane setting.
- Authenticating GitHub, repairing credentials, reading secret values, or
  persisting raw workflow logs.
- Claiming a provider model is accepted by a local CLI, entitled account, or
  live API solely because it appears in an official API catalog.
- Synchronizing provider-global or user-private memories, credentials, tokens,
  shell history, or local authentication state.
- Rewriting the full SDLC document corpus or resolving the known broad
  metadata migration debt outside the approved target and direct-impact set.
- Adding a deployment target, environment, promotion, release, or rollback
  workflow without a separately approved runtime and release contract.
- Copying the `agency-agents` roster, personas, prompt bodies, colors, or
  organization structure into the repository.
- Erasing historically accurate references to retired models, roles, or
  workflow states from research, audits, Task evidence, or Git history.
- Adding arbitrary policy or contract prose to README files.
- Running the all-files pre-commit command directly rather than through the
  approved wrapper.

### Canonical Inputs

- [Spec 132: Agent Governance Harness Convergence](../0132-agent-governance-harness-convergence/spec.md)
- [Spec 133: Target Surface Contract Convergence](../0133-target-surface-contract-convergence/spec.md)
- [Stage 00 bootstrap](../../00.agent-governance/policies/bootstrap.md)
- [Provider-neutral adapter contract](../../00.agent-governance/providers/README.md)
- [Agent catalog](../../00.agent-governance/providers/registry.yaml)
- [Provider model contract](../../00.agent-governance/providers/registry.yaml)
- [Agent-governance artifact contract](../../99.templates/registry.json)
- [Current bootstrap and Task routing](../../00.agent-governance/README.md)
- [Subagent protocol](../../00.agent-governance/policies/agentic.md)
- [Provider capability matrix](../../00.agent-governance/policies/provider-capability-matrix.md)
- [Canonical agentic implementation audit](../../90.references/audits/0019-readme/README.md)
- [Document metadata registry](../../99.templates/registry.json)

### External Source Basis

The rolling source check was performed on 2026-07-26 KST. Official provider
documentation owns provider model IDs, native agent fields, reasoning controls,
and memory behavior. It does not own this repository's role names, lifecycle,
approval policy, path layout, or evidence vocabulary.

<!-- Historical evidence table (not current authority; source: Git history). -->
| Primary source | Local design consequence |
| --- | --- |
| [Anthropic model overview](https://platform.claude.com/docs/en/about-claude/models/overview), [model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions), and [effort](https://platform.claude.com/docs/en/build-with-claude/effort) | Treat dateless 4.6+ identifiers as pinned releases; retain current Fable 5, Opus 5, Sonnet 5, and Haiku 4.5 plus explicitly limited-access Mythos records; and select supported effort by work profile rather than assuming an evergreen alias. |
| [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | Keep native `model`, `effort`, tools, permission, memory, isolation, and turn controls provider-specific; rely on the project entry hierarchy for common repository memory. |
| [OpenAI models](https://developers.openai.com/api/docs/models), [latest model guidance](https://developers.openai.com/api/docs/guides/latest-model), and [GPT-5.3 Codex Spark research preview](https://openai.com/index/introducing-gpt-5-3-codex-spark/) | Use Sol for frontier work and Terra for balanced work; keep Luna catalog-only until Codex runtime acceptance is observed; retain Spark as preview/catalog-only while its official preview remains current; make reasoning effort measurable by profile. |
| [Latest Gemini models](https://ai.google.dev/gemini-api/docs/latest-model) and [Gemini 3.6 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash) | Migrate defaults to Gemini 3.6 Flash and 3.5 Flash-Lite, remove deprecated sampling parameters, and use thinking levels appropriate to autonomous or high-volume work. |
| [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/), [model configuration](https://geminicli.com/docs/cli/generation-settings/), and [memory management](https://geminicli.com/docs/cli/tutorials/memory-management/) | Keep `.gemini/agents/*.md` native, express unsupported per-agent reasoning through scoped model configuration, and load common project context through the repository hierarchy. |
| [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) and [workflow monitoring](https://docs.github.com/en/actions/how-tos/monitor-workflows) | Preserve full-commit action pins, explicit least privilege and timeouts, and separate tracked workflow definitions from observed run logs and remote enforcement. |
| [agency-agents](https://github.com/msitarzewski/agency-agents/blob/main/README.md) | Use the roster as a capability-gap input with identity, mission, workflow, and success-metric evidence; merge capabilities into local roles/functions rather than importing personas. |
| [pre-commit](https://pre-commit.com/) | Treat all-files execution as repository-wide and potentially mutating; route agents through the approved clean-worktree wrapper and record sanitized evidence. |

### Baseline Verification State

| Check | Result | Interpretation |
| --- | --- | --- |
| `report-provider-hook-parity.sh --check` | Pass | Generated hook matrix is fresh at the baseline. |
| Dependency-locked contract validator | Environment blocked | The sandbox could not resolve PyPI and the local runtime lacks `html5lib`; no product failure or pass is claimed. |
| Dependency-locked provider renderer check | Environment blocked | It shares the same dependency boundary; projection freshness must be rerun when the locked environment is available. |
| Working tree before isolation | Clean | Feature work starts from local `main` at `e65bb18f`. |

## Contracts

### Requirement and Acceptance Matrix

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| AGCC-001 | Preserve one canonical authority. | Stage 00 owns policy and catalogs; every root/provider surface is classified as entry, native projection, runtime adapter, or compatibility projection, with no parallel policy body. |
| AGCC-002 | Normalize metadata by consumer. | Stage 00 documents, README profiles, Claude Markdown, Codex TOML, JSON, YAML, and shell files validate against distinct consumer contracts. |
| AGCC-003 | Reject duplicate and legacy keys. | Duplicate YAML keys fail closed; a nested `skill-creator.scope` duplicate is rejected by regression coverage; active target metadata contains no unregistered legacy aliases. |
| AGCC-004 | Remove deprecated active state. | Active contracts and projections contain no `deprecated`, `retired`, or expired fallback record; historical retirement evidence remains immutable and linked. |
| AGCC-005 | Use current model facts. | Every default model maps to an official current ID and every non-default catalog entry separately records provider lifecycle, repository disposition, source, retrieval time, runtime acceptance, and entitlement. |
| AGCC-006 | Optimize by work profile. | Every agent resolves to exactly one work profile with provider model and supported reasoning/effort settings; unsupported native fields are not emitted. |
| AGCC-007 | Resolve current execution state. | Claude and Codex bootstrap resolves the active Spec and its current owning Task; no fixed shared Task or separate state file is introduced. |
| AGCC-008 | Keep the role catalog minimal. | The catalog remains 14 roles unless the admission rule proves a distinct output, permission boundary, and non-mergeable responsibility. |
| AGCC-009 | Close capability gaps as functions. | `provider-model-evaluation` and the retained Stage 00 skills are typed, owned, reviewed, projected, and evaluated; the current catalog determines the exact set. |
| AGCC-010 | Type the harness and loop. | Eight harness layers and the approved loop states have owners, inputs, mutation authority, gates, failure return, evidence, and handoff rules. |
| AGCC-011 | Keep provider projections deterministic. | Renderer write followed by check produces zero drift across `.agents`, `.claude`, and `.codex`; native schema checks pass. |
| AGCC-012 | Govern CI and QA locally. | Local workflow checks enforce job-set consistency, pinned dependencies, permissions, timeouts, safe triggers and interpolation, and controlled QA evidence. |
| AGCC-013 | Represent remote Actions honestly. | Remote-managed workflows and observed runs have dated inventory records; unverified settings remain unverified; no local result is promoted as remote enforcement. |
| AGCC-014 | Remove one-time and obsolete files safely. | Every deletion has a consumer scan, canonical replacement or reason, provenance, rollback, and review evidence. |
| AGCC-015 | Refresh audits and cross-links. | Canonical audit claims, counts, model cutoff, provider parity, CI job count, and remote observation match current tracked evidence. |
| AGCC-016 | Close through independent evidence. | Six logical implementation tasks pass focused validation and independent review, followed by whole-branch correctness and security approval. |

### Authority and Surface Contract

| Surface | Authority or role |
| --- | --- |
| `docs/00.agent-governance/providers/registry.yaml` and canonical roles/skills | Provider model, event, loop, permission, role, skill, and projection authority |
| `docs/99.templates/registry.json` | Sole document profile, shape, identity, template, and lifecycle authority |
| `docs/00.agent-governance/policies/**` | Human-readable policy and workflow authority |
| `docs/00.agent-governance/roles/**` and `skills/**` | Canonical role and function definitions |
| Current owning Stage 03 Task | Bounded execution state and evidence; never policy authority |
| Root `AGENTS.md`, `CLAUDE.md` | Thin bootstrap and active Spec/Task entry adapters |
| `.agents/**` | Provider-neutral compatibility agents and shared skills |
| `.claude/**` | Claude-native generated agents, skills, hooks, and settings |
| `.codex/**` | Codex-native generated TOML agents, hooks, roles, and project config |
| `.github/**` | Tracked desired workflow and repository-governance definitions, not proof of remote enforcement |
| Stage 90 | Source-backed research, retirement history, remote observation, and generated audit evidence |
| Owning Stage 03 Spec package | Approved execution plan, Tasks, sanitized verification, deviations, and review evidence |

README files retain only profile-specific routing, local inventory, setup, and
troubleshooting context. A README may link to a contract or policy but must not
become its second owner.

### Metadata Contract

Stage 00 canonical role and function Markdown use registered document metadata
in fixed order:

1. `layer`
2. `artifact_type`
3. `agent_id` or `function_id`
4. `scope`
5. `tier` when the artifact is a role
6. `status`

The Stage 00 artifact contract owns required, optional, forbidden, ordered, and
conditional keys. Global document aliases such as `title`, `type`,
`document_type`, `template_type`, `owner`, `updated`, and `links` are not added
to these artifacts.

Provider-native metadata stays distinct:

- Claude uses only fields supported by its native agent schema.
- Codex uses the supported TOML agent schema.
- Root shims and README files follow their registered profiles.
- JSON, YAML, TOML, and shell files do not receive Markdown frontmatter.
- Template-source placeholder semantics do not apply to provider-native agent
  definitions.

Duplicate-key-safe parsing precedes semantic validation. A parser dependency
failure is a closed validation failure with an environment code, not a fallback
to permissive parsing.

### Model Status and Acceptance Contract

The active provider model contract keeps independent status axes. A value on
one axis must never satisfy a gate on another axis:

- `provider_lifecycle`: `stable`, `preview`, or `limited_availability`, derived
  only from the current official provider source;
- `repository_disposition`: `default`, `candidate`, or `catalog_only`, derived
  from task fit, local policy, and measured evaluation;
- `runtime_acceptance`: `accepted`, `rejected`, `unavailable`, or
  `needs_revalidation`, derived from the exact provider CLI or runtime;
- `entitlement`: `available`, `unavailable`, `not_applicable`, or
  `needs_revalidation`, derived from the observed account boundary;
- `repository_default_eligible`: a boolean that may be true only for a stable,
  native-schema-compatible model with approved repository task fit; it means
  the model may be written as a configured work-profile default and does not
  prove that a runtime or account can execute it;
- `runtime_activation_eligible`: a boolean that may be true only when
  `runtime_acceptance` is `accepted`, `entitlement` is `available` or
  `not_applicable`, and `repository_default_eligible` is true.

Official catalog presence therefore proves only `provider_lifecycle`. It does
not prove runtime acceptance, entitlement, repository disposition, or default
or activation eligibility. A renderer may write an approved configured default
while activation remains unverified, but neither the contract nor Task evidence
may report the model as runnable until `runtime_activation_eligible` is true.

The active contract does not permit a provider lifecycle of `deprecated` or
`retired`. Historical model records move to a Stage 90 retirement ledger with
provider, exact ID, former lifecycle and disposition, deprecation or shutdown
date, replacement, rationale, source, retrieval time, and immutable repository
provenance. Negative fixtures may retain retired IDs solely to prove rejection.

Dateless IDs are not assumed to be evergreen. Fallback graphs may reference
only active non-expired nodes and must not silently cross provider or work
profile boundaries.

### Historical Work Profile Selection

This July 2026 table records the earlier selection, not current configuration.
Current supported-provider models and reasoning controls are owned solely by
`docs/00.agent-governance/providers/registry.yaml`.

<!-- Historical evidence table (not current authority; source: Git history). -->
| Work profile | Claude | Codex | Gemini |
| --- | --- | --- | --- |
| `long-horizon-supervision` | `claude-opus-5`, `high` or `xhigh` | `gpt-5.6-sol`, `xhigh` | `gemini-3.6-flash`, `high` |
| `complex-implementation` | `claude-sonnet-5`, `high` | `gpt-5.6-sol`, `high` | `gemini-3.6-flash`, `high` |
| `adversarial-review` | `claude-opus-5`, `high` | `gpt-5.6-sol`, `xhigh` | `gemini-3.6-flash`, `high` |
| `evidence-research` | `claude-haiku-4-5-20251001` or `claude-sonnet-5`, `low` | `gpt-5.6-terra`, `low` or `medium` | `gemini-3.5-flash-lite`, `minimal` or `medium` |
| `routine-validation` | `claude-haiku-4-5-20251001` | `gpt-5.6-terra`, `low` | `gemini-3.5-flash-lite`, `minimal` |

The implementation selects one exact configured value per agent rather than
emitting the alternatives shown in this design table. The choice must follow
the agent's mutation authority, risk, tool autonomy, expected horizon, and
measured fixture behavior. A configured value is not a live activation claim.
`gpt-5.6-luna` remains `catalog_only` until Codex accepts it. The contract must
not claim that API availability establishes CLI acceptance.

`claude-fable-5` remains a current stable, exceptional-capability,
non-default catalog candidate and receives a sourced evaluation disposition
even though it is not assigned to a routine work profile. Current
limited-access Claude Mythos entries remain explicit
`limited_availability`/`catalog_only` records unless entitlement and runtime
acceptance are separately observed. This prevents the default table from being
misread as the complete Claude catalog.

Claude effort is emitted only for a model and surface that support it.
Codex uses the supported
`model_reasoning_effort` field.

## Core Design

### Current Task State

The repository provides one provider-neutral current-state route:

- The Stage 00 bootstrap resolves the active Spec and its current owning Task.
- That Task records approved decisions, current blockers, verified checks,
  direct evidence links, and the next handoff; no fixed task number is shared
  across unrelated work.
- Completed execution evidence follows the Stage 99 lifecycle and is recovered
  from Git after approved cleanup.

Entries must be source-linked and value-free. Policy text, full command logs, raw output,
secrets, credentials, tokens, shell history, and private provider memory are
forbidden.

`AGENTS.md` and `CLAUDE.md` use the same bootstrap policy and resolve the owning
Task for the current request. Provider adapters may translate syntax but may not
fork state or define a second lifecycle. Registered metadata, lifecycle, and
governance validators enforce their respective current contracts.

### Agent Catalog and Capability Intake

The current 14 role identities remain. A new role may be admitted only when all
three conditions hold:

1. it owns an output that no current role owns;
2. it requires a distinct permission or approval boundary;
3. adding a function to an existing role cannot preserve accountability.

The retained evaluation capability is:

| Function | Owner | Reviewers | Output |
| --- | --- | --- | --- |
| `provider-model-evaluation` | `eval-engineer` | `code-reviewer`, `rules-engineer` | sourced model disposition, native acceptance verdict, and regression comparison |

The registered Stage 00 roles and skills determine the active catalog and
generated set. Codex uses the shared `.agents/skills` projection; current Task
maintenance does not create a separate state authority or a retired skill.

The `agency-agents` comparison is maintained as a capability matrix:

- Model QA maps to `eval-engineer`.
- Agent identity and trust map to `security-auditor` and `rules-engineer`.
- MCP building maps to `hook-developer` and `skill-creator`.
- Knowledge stewardship maps to `doc-writer`.
- DevOps and release design map to `ci-cd-engineer`.
- Incident and SRE map to `incident-responder`.
- Compliance maps to `security-auditor`.

Each decision is `merge`, `defer`, or `reject`, with local owner, function,
rationale, and evidence. No source persona becomes an active identity merely
because it exists upstream.

### Harness and Loop

The harness has eight typed layers:

1. canonical contract;
2. role and function routing;
3. permission and mutation boundary;
4. provider model and reasoning policy;
5. semantic event hooks;
6. controlled QA and validation;
7. tracked CI;
8. sanitized evidence and handoff.

The common loop is:

`discover -> design/plan -> approval -> implement -> validate -> independent-review -> evidence -> handoff`

Each state declares required input, responsible role, permitted mutation,
entry condition, exit gate, retry budget, failure return state, evidence
record, and handoff target. Approval cannot be inferred from movement between
provider tools. Failed validation returns to `implement`; rejected design
returns to `design/plan`; missing authority returns to `approval`; an exhausted
retry budget stops rather than self-expanding scope.

Provider event adapters map native events to the common states without claiming
event parity that the runtime does not expose. Missing native events are
documented as instruction- or CI-enforced gaps. Tracked hooks do not prove that
a provider loaded or executed them.

### Provider Projection

The typed contract and renderer remain the sole write path for generated role,
function, model, and event projections:

1. load duplicate-safe contracts;
2. validate catalog identities, counts, ownership, profiles, and model graph;
3. resolve one work profile per role;
4. render native provider fields only;
5. render compatibility/shared skill projections;
6. validate native schema and semantic parity;
7. compare generated bytes with tracked files;
8. write only through explicit `--write`.

Manual edits to generated projections fail drift checks. Provider-specific
files may contain a generated header or source link but may not carry copied
contract prose that can diverge.

### CI, QA, and Remote Actions

Local CI remains a 16-job tracked quality contract unless implementation
evidence proves a current canonical owner has changed it. Workflow validation
checks:

- exact expected job identities and dependencies;
- explicit least-privilege permissions;
- bounded timeouts;
- full 40-character action commit pins;
- pinned versions for dynamically executed tools such as `zizmor`;
- rejection of a pinned release that is yanked for a published security defect;
- no unsafe `pull_request_target`;
- no direct untrusted GitHub-context interpolation into shell;
- deterministic wrapper and validator routes;
- consistency among workflow source, local ruleset proposal, and repository
  validator.

The three observed GitHub-managed workflows remain external-control-plane
objects. A Stage 90 inventory records public workflow ID, name, management
class, observed state, last run, source visibility, review owner, retrieval
time, and verification limitations. Local equivalent workflow files are not
created merely to make the inventory counts equal.

The latest remote CI failure is a dated observation, not a defect cause.
Without authenticated logs, the repository may record the failing job and step
but not invent a root cause. No expansion of required remote checks is
recommended until the default branch is observed green and the control plane is
authenticated under separate approval.

Agent QA follows this order:

1. focused parser and validator tests;
2. contract validation;
3. provider renderer check;
4. native schema, hook, memory, and catalog parity;
5. workflow `actionlint` and pinned `zizmor`;
6. changed-document metadata, traceability, and cross-links;
7. relevant regression and aggregate checks;
8. approved controlled all-files wrapper;
9. sanitized Stage 04 evidence.

Direct `pre-commit run --all-files` remains prohibited. The wrapper requires an
explicit approval for the specific run, a clean committed candidate, bounded
environment metadata, sanitized output, and Task-owned evidence.

### Destructive and One-Time Cleanup

A deletion or consolidation requires:

- exact path and surface classification;
- current consumer and cross-link scan;
- canonical replacement or reason no replacement is needed;
- generated-owner check;
- provenance commit and blob when history is the preservation route;
- rollback command;
- specification and quality review.

Historical audits, retirement ledgers, negative fixtures, and durable task
evidence are not one-time files. Scratch reports, dry-run output, duplicated
generated projections, temporary migration ledgers, and obsolete provider
artifacts may be deleted only when the criteria above pass.

## Interfaces and Data

The implementation extends existing typed contracts rather than introducing a
parallel configuration owner.

### Agent Catalog Changes

- remove duplicate YAML keys;
- remove active `role_transfers` after moving history to Stage 90;
- increase active function count from 22 to 24;
- add function inputs, outputs, gates, owner, reviewers, scope, status, and
  projection targets;
- expand work-profile identities and assign every role exactly once;
- update capability-intake decisions and provenance.

### Provider Model Changes

Each model record contains:

- provider;
- exact model ID;
- official provider lifecycle;
- repository disposition, configured-default eligibility, and runtime
  activation eligibility;
- official source and retrieval time;
- capability and task-fit summary;
- supported reasoning or effort levels;
- agent/coding suitability;
- provider-native schema acceptance;
- local runtime or CLI acceptance state;
- entitlement state;
- replacement or fallback edges limited to active nodes.

Retirement records use the Stage 90 evidence schema, not the active provider
contract.

### Current Task State Changes

The active owning Task uses its Stage 99 registered section envelope for
objective, decisions, scope, verification, blockers, evidence, and handoff.
Template prose must not remain in an instantiated Task. Stale execution state
is closed through registered lifecycle, not duplicated in a shared state file.

### Remote Actions Observation

Remote observation data is non-authoritative, date-stamped evidence. It carries
no credentials, secret names, raw logs, or inferred protection settings.
Tracked desired state remains in `.github/**`; observed remote state remains in
Stage 90; applied remote state remains unverified until separately authorized
and read back.

## Failure Modes and Guardrails

- An unavailable dependency produces an environment-blocked result and an
  exact rerun route; it does not downgrade strict parsing.
- An official model absent from a provider CLI remains `catalog_only` or
  `needs_revalidation`; it does not become a default.
- A provider-native field absent from official schema is omitted rather than
  emitted as a hoped-for setting.
- A live provider call, paid job, remote workflow dispatch, push, or control
  plane mutation stops for separate approval.
- An authenticated or raw remote log is never persisted without an approved,
  sanitized evidence route.
- A provider memory feature may not create policy precedence over Stage 00 or a
  second shared-current-state file.
- A capability gap does not create a role until the admission contract passes.
- A generated projection is never hand-edited to bypass a renderer defect.
- A duplicate YAML key fails before semantic validation.
- A historical deprecation reference is preserved when it is evidence, even
  though the active contract rejects deprecated state.
- A deletion without consumer, provenance, rollback, and independent review
  evidence stops.
- A failed task receives bounded remediation and re-review; scope does not
  silently expand.
- Local workflow success does not establish remote branch protection,
  required-check, environment, or execution success.
- Direct all-files pre-commit execution remains prohibited.

## Verification

### Per Logical Task

- exact parser, validator, renderer, or fixture tests;
- changed-document metadata with an explicit safe base;
- generated-owner freshness where applicable;
- `git diff --check`;
- scoped pre-commit hooks where allowed;
- independent specification and quality review;
- one independently revertible logical commit or an explicitly coupled commit
  set recorded in the Task ledger.

### Contract and Projection Gates

- zero duplicate keys in active YAML contracts;
- exactly the registered active roles and skills;
- exactly one work profile per role;
- provider lifecycle, repository disposition, runtime acceptance, entitlement,
  configured-default eligibility, and runtime activation eligibility validate
  as independent axes;
- zero active deprecated or retired model/role records;
- all fallback edges resolve to eligible active nodes;
- provider-native metadata uses supported fields;
- `.agents`, `.claude`, and `.codex` projection drift is zero;
- shared skill counts and provider capability routes are exact;
- root shims resolve the same active Spec and its current owning Task;
- current Task content satisfies its Stage 99 profile without a shared state file;
- hook semantic mapping and generated parity are fresh;
- agent-output evaluation fixtures and regression controls pass.

### CI and Documentation Gates

- local 16-job source and validator contract agree;
- `actionlint` passes;
- pinned `zizmor` reports no actionable finding and is not the yanked 1.27.0
  credential-logging release;
- action pins, permissions, timeouts, triggers, and untrusted-input checks pass;
- remote inventory is current, source-linked, and explicitly non-authoritative;
- canonical audit counts and claims are generated from current criterion rows;
- model cutoff and source retrieval times are current;
- document traceability and cross-links pass;
- no arbitrary README policy duplication is introduced.

### Final Closure

- dependency-locked full relevant suite passes, or every unavailable external
  capability remains explicitly unverified without a closure claim;
- all six tasks have independent review approval;
- a fresh whole-branch correctness reviewer reports no Critical or Important
  finding;
- a fresh whole-branch security reviewer reports no Critical or Important
  finding;
- the user explicitly approves the controlled all-files wrapper run;
- wrapper evidence is sanitized and recorded under the Stage 04 Task;
- the branch remains local and unpushed unless the user separately requests a
  finish action.

## Agent Role and IO Contract

Implementation uses an isolated worktree at
`.worktrees/agent-governance-canonical-convergence` on
`feat/agent-governance-canonical-convergence`.

<!-- Historical evidence table (not current authority; source: Git history). -->
| Task | Boundary | Primary owners | Commit intent |
| --- | --- | --- | --- |
| T-AGCC-001 | Metadata, active contracts, duplicate keys, and retirement evidence | `rules-engineer`, reviewed by `code-reviewer` | Normalize canonical contracts and remove deprecated active state |
| T-AGCC-002 | Model sources, work profiles, renderer, and provider projections | `hook-developer`, reviewed by `eval-engineer` | Update model policy and deterministic provider adapters |
| T-AGCC-003 | Shared project memory, root shims, and memory validation | `doc-writer`, reviewed by `rules-engineer` | Establish one bounded project-memory route |
| T-AGCC-004 | Agent capability intake, functions, harness, loop, and evals | `workflow-supervisor`, reviewed by `code-reviewer` | Close capability and loop-contract gaps |
| T-AGCC-005 | Local Actions, QA, remote observation, and static security | `ci-cd-engineer`, reviewed by `security-auditor` | Reconcile local CI/QA and external-control-plane evidence |
| T-AGCC-006 | Canonical audit, cross-links, cleanup, final QA, and branch review | `eval-engineer`, reviewed by fresh correctness and security reviewers | Close evidence without remote or runtime overclaim |

Each task receives a fresh implementation subagent with an explicit model,
reasoning effort, owned files, forbidden actions, and verification commands.
The implementation agent is not its reviewer. Critical and Important findings
must be fixed and re-reviewed before the next task. Shared-worktree mutations
are sequential; read-only research and review may run in parallel. A fresh
whole-branch review follows all task reviews.

Model assignment follows the same work-profile contract being implemented:
frontier/high reasoning for contracts, security, and cross-provider changes;
balanced/low or medium reasoning for bounded inventory and repetitive
normalization. Dispatch evidence records the actual available runtime model
without claiming that a requested provider model was used when the harness
substituted another model.

## Related Documents

- [Agent governance overview](../../00.agent-governance/README.md)
- [Agentic rules](../../00.agent-governance/policies/agentic.md)
- [Agentic scope](../../00.agent-governance/roles/agentic.md)
- [GitHub governance](../../00.agent-governance/policies/github-governance.md)
- [Task checklists](../../00.agent-governance/policies/task-checklists.md)
- [Stage authoring matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/registry.json)
- [Canonical audit implementation overview](../../90.references/audits/0026-implementation-overview/README.md)
- [Provider harness and loop audit](../../90.references/audits/0028-provider-harness-loop-implementation/README.md)
- [SDLC quality and CI audit](../../90.references/audits/0030-sdlc-quality-formatting-implementation/README.md)

## Behavior Contract

The behaviors and invariants already specified above remain the package behavior contract.

## Technical Approach

The implementation and component design recorded above remain the technical approach.

## Acceptance Contract

The verification and success conditions above remain the acceptance contract.

## Traceability

The requirement, architecture, operations, and evidence links above provide traceability.
