---
status: active
artifact_id: plan:2026-07-26-agent-governance-canonical-convergence
artifact_type: plan
parent_ids:
  - spec:134-agent-governance-canonical-convergence
---

# Agent Governance Canonical Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` for task-by-task implementation and
> independent review. Use `superpowers:executing-plans` for controller tracking.
> Every executable step uses checkbox (`- [ ]`) syntax.

**Goal:** Converge the repository's active agent-governance control plane on
current provider models, one bounded project-memory route, a typed harness and
loop, and locally enforceable CI/QA contracts without changing remote GitHub or
provider runtime state.

**Architecture:** Stage 00 remains the sole active authority for agents,
functions, provider models, permissions, events, memory, harness layers, and
loop states. Existing validators load duplicate-safe typed contracts; the
provider renderer projects them deterministically into `.agents`, `.claude`,
`.codex`, and `.gemini`. Stage 90 owns historical retirement and remote
observation evidence. Stage 04 owns execution and review evidence.

**Tech Stack:** YAML contracts, Python 3.12, PyYAML, markdown-it-py, html5lib,
unittest, Markdown/CommonMark, JSON, TOML, Bash, Claude Code project agents,
Codex project agents, Gemini CLI project agents, GitHub Actions, zizmor 1.28.0,
pre-commit, and Git.

## Global Constraints

- Work only in
  `.worktrees/agent-governance-canonical-convergence` on
  `feat/agent-governance-canonical-convergence`; keep the root checkout on
  `main`.
- Stage 00 is the only active policy/catalog owner. Root files are thin entry
  adapters, provider directories are native or compatibility projections,
  Stage 90 is evidence, and Stage 04 is execution state.
- Keep 14 roles. Add exactly two functions, for a final active count of 24.
- Active contracts may not contain lifecycle values `deprecated` or `retired`,
  historical fallback approvals, or retired role-transfer records.
- Historical retirement evidence must identify the former exact ID,
  replacement, dates, source, reason, and immutable Git commit/blob.
- Provider lifecycle, repository disposition, runtime acceptance, entitlement,
  configured-default eligibility, and runtime activation eligibility are
  independent axes. Official catalog presence proves only provider lifecycle.
- Do not perform paid/live provider calls, mutate provider-global configuration,
  inspect private provider memory, or claim runtime acceptance/entitlement
  without direct evidence.
- Do not push, dispatch workflows, mutate remote GitHub settings, authenticate
  GitHub, or read secret values or raw authenticated logs.
- Preserve the local 16-job CI contract. GitHub-managed workflows remain
  dated observations rather than locally recreated workflow files.
- README files remain profile-specific routing and inventory surfaces. Do not
  copy contract or governance prose into them.
- Use TDD for contract, validator, renderer, memory, evaluator, or workflow
  behavior. Record the initial expected RED before making the minimal GREEN
  implementation.
- Each task receives a fresh implementation agent and a distinct fresh
  reviewer. Critical and Important findings are fixed and re-reviewed before
  advancing.
- Each task ends in at least one independently revertible Conventional Commit.
  Generated-owner fallout belongs to the same task or an immediately following
  generated-evidence commit.
- Never execute `pre-commit run --all-files` directly. T-AGCC-006 may invoke
  `scripts/validation/run-agent-precommit-all-files.sh` only after separate
  explicit user approval for that exact run and from a clean committed
  worktree.
- Never persist credentials, tokens, secret values, auth files, shell history,
  raw logs, or unbounded provider output.
- The dependency-locked validator and renderer baseline is environment-blocked
  because the sandbox cannot fetch PyPI and bare Python lacks `html5lib`.
  Re-run in the canonical locked runtime when available; otherwise record the
  exact environment block without claiming product pass or failure.

## Overview

This Plan implements
[Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
through six serial logical tasks:

1. normalize active contracts and move retirement history to Stage 90;
2. update current provider facts, work profiles, and generated projections;
3. establish one bounded project-memory route;
4. add two functions and type harness, loop, and deterministic evaluations;
5. reconcile local GitHub Actions/QA controls and remote observation;
6. refresh canonical research/audits, close cross-links, run final QA, and
   complete whole-branch review.

The sibling
[Task ledger](../tasks/2026-07-26-agent-governance-canonical-convergence.md)
records actual commands, results, commits, deviations, and review verdicts. It
does not duplicate this implementation design.

## Context and Inputs

### Approved Inputs

- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Spec 132](../../98.archive/03.specs/132-agent-governance-harness-convergence/spec.md)
- [Spec 133](../../98.archive/03.specs/133-target-surface-contract-convergence/spec.md)
- [Stage 00 bootstrap](../../00.agent-governance/rules/bootstrap.md)
- [Agent catalog](../../00.agent-governance/contracts/agent-catalog.yaml)
- [Provider model contract](../../00.agent-governance/contracts/provider-models.yaml)
- [Artifact contract](../../00.agent-governance/contracts/agent-governance-artifacts.yaml)
- [Memory contract](../../00.agent-governance/memory/README.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Canonical research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)

### Current External Sources

The implementation must retain source and retrieval time beside every
fast-moving claim:

- Anthropic model overview, model ID/versioning, effort, and Claude Code
  subagent documentation:
  <https://platform.claude.com/docs/en/about-claude/models/overview>,
  <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>,
  <https://platform.claude.com/docs/en/build-with-claude/effort>,
  <https://code.claude.com/docs/en/sub-agents>
- OpenAI model catalog and latest-model guidance:
  <https://developers.openai.com/api/docs/models>,
  <https://developers.openai.com/api/docs/guides/latest-model>,
  <https://openai.com/index/introducing-gpt-5-3-codex-spark/>
- Gemini latest model, Gemini 3.6 Flash, subagent, generation setting, and
  memory documentation:
  <https://ai.google.dev/gemini-api/docs/latest-model>,
  <https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash>,
  <https://geminicli.com/docs/core/subagents/>,
  <https://geminicli.com/docs/cli/generation-settings/>,
  <https://geminicli.com/docs/cli/tutorials/memory-management/>
- GitHub Actions secure-use and monitoring documentation:
  <https://docs.github.com/en/actions/reference/security/secure-use>,
  <https://docs.github.com/en/actions/how-tos/monitor-workflows>
- zizmor immutable v1.28.0 security release:
  <https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0>
- `agency-agents` capability catalog and pre-commit behavior:
  <https://github.com/msitarzewski/agency-agents/blob/main/README.md>,
  <https://pre-commit.com/>

### Baseline and Provenance

- Feature base:
  `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee`.
- Agent catalog baseline blob:
  `9f6a0fba4df6d37ab5f1a3390dc57d0dd99e8034`.
- Provider model baseline blob:
  `58ee9b29cb0e519a34ff919e1e29791171c458a4`.
- Artifact contract baseline blob:
  `8f083195e998ae6435d39d408bf35850c4b3ebf1`.
- GitHub CI memory memo baseline blob:
  `7bf6427ad8f29ab8b0d7c001cf330e29b941cdfe`.
- At feature-base activation, the catalog was duplicate-key clean. A nested
  duplicate `scope` remains a required negative regression fixture.
- At feature-base activation, active counts were 14 roles and 22 functions,
  and the semantic evaluator had 8 fixtures and 10 deterministic regressions.
  The current post-T-AGCC-004 contract is separately 14 roles / 24 functions
  and 11 fixtures / 16 regressions; Task 6 closure evidence must use the
  current values without rewriting the activation baseline.
- Local `ci-quality.yml` owns 16 jobs. The public remote observation exposed 15
  jobs in the last failed run and three GitHub-managed workflows; authenticated
  control-plane state remains unverified.
- Local zizmor was 1.25.2 at baseline. The initially planned 1.27.0 package was
  yanked for `GHSA-f42p-wjw5-97qh` because it could log configured GitHub
  credentials in cleartext. The official immutable current security release
  observed on 2026-07-26 is 1.28.0. CI must use the explicit 1.28.0 package
  version and must reject 1.27.0.

## Goals and Non-goals

### Goals

- Make all active model, role, function, memory, harness, loop, workflow, and
  projection claims current and machine-checkable.
- Remove legacy/deprecated active state without erasing historical evidence.
- Select exact provider model and reasoning values by one role work profile.
- Give every provider entry point the same bounded repository memory.
- Close model-evaluation and memory-stewardship gaps as functions, not roles.
- Keep provider projections deterministic and native-schema compliant.
- Enforce local CI/QA consistency and record remote state honestly.
- Refresh canonical research/audit evidence and complete independent reviews.

### Non-goals

- Remote GitHub mutation, push, merge, or workflow dispatch.
- Live provider model calls, comparative quality/cost/latency benchmarking, or
  entitlement testing.
- Provider-global memory synchronization.
- Runtime, Docker Compose, infrastructure, deployment, release, or secret
  changes.
- Rewriting unrelated SDLC documents or historical Stage 90 evidence.
- Replacing community workflows solely to equalize local and remote counts.

## Requirement Coverage

| Spec requirement | Owning task | Completion evidence |
| --- | --- | --- |
| AGCC-001, AGCC-002 | T-AGCC-001, T-AGCC-003 | authority/profile validation and root-shim parity |
| AGCC-003, AGCC-004 | T-AGCC-001 | duplicate regression, zero active retired/deprecated state, retirement ledger |
| AGCC-005, AGCC-006, AGCC-011 | T-AGCC-002 | sourced model catalog, exact profiles, native projection drift zero |
| AGCC-007 | T-AGCC-003 | bounded `current.md`, exact shared import parity |
| AGCC-008, AGCC-009, AGCC-010 | T-AGCC-004 | 14/24 cardinality, two functions, typed layers/states/evals |
| AGCC-012, AGCC-013 | T-AGCC-005 | 16-job contract, pinned tools, dated remote inventory |
| AGCC-014 | T-AGCC-005, T-AGCC-006 | exact consumer/provenance/rollback decision for every deletion |
| AGCC-015, AGCC-016 | T-AGCC-006 | fresh research/audit/generated evidence and whole-branch review |

## Task Interfaces

| Task | Inputs | Outputs consumed by |
| --- | --- | --- |
| T-AGCC-001 | Spec 134, baseline contracts/blobs | T-AGCC-002, T-AGCC-004, T-AGCC-006 |
| T-AGCC-002 | normalized active contract, current official provider sources | T-AGCC-003, T-AGCC-004, T-AGCC-006 |
| T-AGCC-003 | artifact contract and renderer-stable root/provider routes | T-AGCC-004, T-AGCC-006 |
| T-AGCC-004 | model profiles, shared memory, existing eval runner | T-AGCC-005, T-AGCC-006 |
| T-AGCC-005 | current harness/loop and local workflow contract | T-AGCC-006 |
| T-AGCC-006 | exact commits/reviews from Tasks 1-5 | final branch review and handoff |

## Work Breakdown

### Task 1: Normalize Active Contracts and Retirement Evidence

**Task ID:** `T-AGCC-001`

**Files:**

- Modify
  `docs/00.agent-governance/contracts/agent-catalog.yaml`.
- Modify
  `docs/00.agent-governance/contracts/provider-models.yaml`.
- Modify
  `scripts/validation/agent_governance_contract.py`.
- Modify
  `tests/validation/test_agent_governance_contract.py`.
- Modify
  `tests/validation/test_provider_native_surfaces.py`.
- Create
  `docs/90.references/data/governance/agent-governance-retirement-ledger.yaml`.
- Modify
  `docs/90.references/data/governance/README.md`.
- Modify the sibling Task ledger.

**Historical ledger shape:**

```yaml
schema_version: 1
authority: historical-evidence
baseline_commit: e65bb18fa2f6e3fb6235725750c7c57cbe0227ee
records:
  - record_id: role:style-enforcer
    record_kind: retired-role
    former_id: style-enforcer
    replacement_ids: [qa-engineer, rules-engineer]
    retired_at: 2026-07-15
    source_url: docs/03.specs/132-agent-governance-harness-convergence/spec.md
    source_commit: e65bb18fa2f6e3fb6235725750c7c57cbe0227ee
    source_blob: 9f6a0fba4df6d37ab5f1a3390dc57d0dd99e8034
```

**Interfaces:**

```python
RETIREMENT_LEDGER_PATH = pathlib.PurePosixPath(
    "docs/90.references/data/governance/agent-governance-retirement-ledger.yaml"
)

def validate_retirement_ledger(
    root: pathlib.Path, bundle: ContractBundle
) -> list[Finding]: ...
```

The Task 1 output contract is a duplicate-safe active bundle with no historical
state plus one Stage 90 ledger whose findings join the existing deterministic
`Finding` sequence. T-AGCC-002 consumes the normalized active model/candidate
records; T-AGCC-006 consumes the ledger provenance.

- [ ] Add RED
  `ContractLoadingTests.test_duplicate_agent_entry_key_fails_closed_without_values`
  by injecting a second `scope` under `skill-creator`; assert
  `AGC-YAML-DUPLICATE-KEY` and no duplicated values in diagnostics.
- [ ] Add RED
  `CatalogContractTests.test_active_catalog_forbids_role_transfers_and_retired_status`
  by reintroducing `role_transfers` and a role with `status: retired`; assert
  `AGC-CATALOG-HISTORICAL-STATE-ACTIVE`.
- [ ] Add RED
  `ProviderContractTests.test_active_provider_contract_forbids_deprecated_models`
  by injecting `provider_lifecycle: deprecated` and then `retired`; assert
  `AGC-MODEL-HISTORICAL-STATE-ACTIVE`.
- [ ] Add RED
  `RetirementLedgerTests.test_retirement_ledger_has_exact_replacement_and_git_provenance`
  for `style-enforcer`, `wiki-curator`, and the three explicitly deprecated
  baseline model IDs.
- [ ] Run the four focused tests and record their expected failures before
  production edits.
- [ ] Remove active `role_transfers` and every fallback approval/edge that
  references an explicitly deprecated model.
- [ ] Move role transfers and explicitly deprecated model records into the
  Stage 90 ledger with exact replacement, dates, official/local source, reason,
  baseline commit, and baseline blob.
- [ ] Make active catalog/provider top-level schemas reject historical fields
  and lifecycle values rather than silently ignoring them.
- [ ] Preserve negative fixtures only in tests; do not use historical IDs as
  active defaults, fallbacks, projections, or examples.
- [ ] Run:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_contract.ContractLoadingTests.test_duplicate_agent_entry_key_fails_closed_without_values \
  tests.validation.test_agent_governance_contract.CatalogContractTests.test_active_catalog_forbids_role_transfers_and_retired_status \
  tests.validation.test_agent_governance_contract.ProviderContractTests.test_active_provider_contract_forbids_deprecated_models \
  tests.validation.test_agent_governance_contract.RetirementLedgerTests.test_retirement_ledger_has_exact_replacement_and_git_provenance \
  -v
python3 -m unittest tests.validation.test_agent_governance_contract -v
python3 -m unittest tests.validation.test_provider_native_surfaces -v
python3 scripts/validation/check-agent-governance-contract.py --mode contract
git diff --check
```

- [ ] Expect the focused and full suites to pass; contract mode must report
  3 contracts, 14 agents, 22 functions, 3 providers, and zero failures.
- [ ] Update Task evidence and commit
  `refactor(governance): normalize active agent contracts`.
- [ ] Dispatch a fresh read-only specification reviewer and a separate quality
  reviewer for the exact Task 1 range; remediate and re-review C/I findings.

### Task 2: Update Provider Models, Work Profiles, and Projections

**Task ID:** `T-AGCC-002`

**Files:**

- Modify
  `docs/00.agent-governance/contracts/provider-models.yaml`.
- Modify
  `docs/00.agent-governance/contracts/agent-catalog.yaml`.
- Modify
  `scripts/validation/agent_governance_contract.py`.
- Modify
  `scripts/operations/provider_surface_renderer.py`.
- Modify
  `tests/validation/test_agent_governance_contract.py`.
- Modify
  `tests/validation/test_provider_surface_renderer.py`.
- Modify
  `tests/validation/test_provider_native_surfaces.py`.
- Regenerate the 14 role files in each of
  `.agents/agents/`, `.claude/agents/`, `.codex/agents/`, and
  `.gemini/agents/`.
- Regenerate `.claude/settings.json`, `.codex/hooks.json`, and
  `.gemini/settings.json` only through the renderer.
- Update the Stage 90 retirement ledger for legacy models displaced by the
  current catalog.
- Modify the sibling Task ledger.

**Independent status axes:**

```yaml
provider_lifecycle: stable
repository_disposition: default
runtime_acceptance: needs_revalidation
entitlement: needs_revalidation
repository_default_eligible: true
runtime_activation_eligible: false
```

`repository_default_eligible` means the stable, schema-compatible model may be
written as the repository's configured work-profile default.
`runtime_activation_eligible` remains false until runtime acceptance and
entitlement evidence exist. Rendering configuration does not manufacture those
observations. This wave creates no automatic model fallback graph.

**Exact work-profile defaults:**

| Profile | Claude | Codex | Gemini |
| --- | --- | --- | --- |
| `long-horizon-supervision` | `claude-opus-5`, `xhigh` | `gpt-5.6-sol`, `xhigh` | `gemini-3.6-flash`, `high` |
| `complex-implementation` | `claude-sonnet-5`, `high` | `gpt-5.6-sol`, `high` | `gemini-3.6-flash`, `high` |
| `adversarial-review` | `claude-opus-5`, `high` | `gpt-5.6-sol`, `xhigh` | `gemini-3.6-flash`, `high` |
| `evidence-research` | `claude-sonnet-5`, `low` | `gpt-5.6-terra`, `medium` | `gemini-3.5-flash-lite`, `medium` |
| `routine-validation` | `claude-haiku-4-5-20251001`, no unsupported effort field | `gpt-5.6-terra`, `low` | `gemini-3.5-flash-lite`, `minimal` |

**Exact role assignment:**

| Role | Work profile |
| --- | --- |
| `workflow-supervisor` | `long-horizon-supervision` |
| `code-reviewer`, `eval-engineer`, `iac-reviewer`, `rules-engineer`, `security-auditor` | `adversarial-review` |
| `ci-cd-engineer`, `hook-developer`, `incident-responder`, `infra-implementer`, `qa-engineer`, `skill-creator` | `complex-implementation` |
| `doc-writer` | `evidence-research` |
| `drift-detector` | `routine-validation` |

**Active current catalog:**

- Claude: Fable 5 stable candidate/non-default, Opus 5 stable default,
  Sonnet 5 stable default, Haiku 4.5 stable default, Mythos 5 limited
  availability/catalog-only.
- Codex/OpenAI: GPT-5.6 Sol stable default, GPT-5.6 Terra stable default,
  GPT-5.6 Luna stable catalog-only until runtime acceptance, GPT-5.3 Codex
  Spark preview/catalog-only.
- Gemini: Gemini 3.6 Flash stable default and Gemini 3.5 Flash-Lite stable
  default.

**Interfaces:**

```python
@dataclass(frozen=True)
class ProviderSelection:
    model_id: str
    control_kind: str
    control_value: str | None

def _provider_selections(
    provider_contract: Mapping[str, object],
) -> dict[tuple[str, str], ProviderSelection]: ...
```

T-AGCC-002 replaces renderer use of tuple-valued `_provider_defaults()` with
the typed selection interface. The key is `(work_profile, provider_id)`.
Claude emits `effort`; Codex emits `model_reasoning_effort`; Gemini maps
`minimal|medium|high` to
`modelConfigs.overrides[].modelConfig.generateContentConfig.thinkingConfig.thinkingLevel`
as `MINIMAL|MEDIUM|HIGH`, matched by `overrideScope`.

- [ ] Add RED
  `ProviderModelConvergenceTests.test_model_catalog_matches_2026_07_26_official_set`
  with the exact current IDs and six independent status/eligibility axes.
- [ ] Add RED
  `ProviderModelConvergenceTests.test_work_profiles_and_role_assignments_are_exact`
  with the five profile IDs and fourteen-role table above.
- [ ] Add RED
  `ProviderModelConvergenceTests.test_no_automatic_fallback_or_legacy_model_is_active`.
- [ ] Add RED
  `ProviderNativeSurfaceTests.test_gemini_reasoning_uses_scoped_model_configs_without_sampling_parameters`
  and reject `temperature`, `top_p`, `top_k`, `topP`, or `topK`.
- [ ] Add RED renderer assertions for Claude `effort`, Codex
  `model_reasoning_effort`, Gemini scoped `modelConfigs.overrides`, and exact
  current model IDs.
- [ ] Run the focused provider tests and record the expected old-model/profile
  failures.
- [ ] Rebuild the active model records from the official sources retrieved on
  2026-07-26; retain lifecycle, disposition, source, retrieval time, task fit,
  supported reasoning, runtime acceptance, entitlement,
  configured-default eligibility, and runtime activation eligibility as
  separate fields.
- [ ] Move Claude Opus 4.8 and any other displaced legacy active record to the
  Stage 90 retirement ledger with immutable provenance; do not classify a
  current catalog-only model as deprecated merely because it is not selected.
- [ ] Replace the three old profiles with the five exact profiles and assign
  every role exactly once.
- [ ] Teach the renderer to emit only provider-native fields and deterministic
  Gemini scoped reasoning overrides.
- [ ] Run `python3 scripts/operations/provider_surface_renderer.py --write`.
- [ ] Inspect every renderer-managed changed/deleted path. Stop if a stale-file
  deletion is not confined to a known generated owner.
- [ ] Run:

```bash
python3 -m unittest tests.validation.test_provider_native_surfaces -v
python3 -m unittest tests.validation.test_provider_surface_renderer -v
python3 -m unittest tests.validation.test_agent_governance_contract -v
python3 scripts/operations/provider_surface_renderer.py --check
bash scripts/operations/sync-provider-surfaces.sh --check
python3 scripts/validation/check-agent-governance-contract.py --mode contract
python3 scripts/validation/check-agent-governance-contract.py \
  --mode repository --section providers
git diff --check
```

- [ ] Expect exact five-profile/14-role resolution, zero projection drift, and
  no unsupported provider fields.
- [ ] Update Task evidence and commit
  `feat(providers): update model policy and projections`.
- [ ] Dispatch fresh specification and quality reviewers for the exact Task 2
  range; remediate and re-review C/I findings.

### Task 3: Establish Shared Bounded Project Memory

**Task ID:** `T-AGCC-003`

**Files:**

- Create
  `docs/00.agent-governance/memory/current.md`.
- Modify
  `docs/00.agent-governance/memory/README.md`.
- Modify
  `docs/00.agent-governance/memory/progress.md` only for historical-navigation
  semantics or a compacted pointer; do not rewrite historical rows.
- Modify
  `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml`.
- Modify root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
- Modify provider overlays under
  `docs/00.agent-governance/providers/` only where their bootstrap route names
  the old active memory file.
- Modify
  `scripts/validation/agent_governance_contract.py`.
- Modify
  `tests/validation/test_agent_governance_contract.py`.
- Modify the sibling Task ledger.

**Memory validator constants:**

```python
CURRENT_MEMORY_PATH = "docs/00.agent-governance/memory/current.md"
CURRENT_MEMORY_MAX_BYTES = 32 * 1024
CURRENT_MEMORY_MAX_LINES = 400
CURRENT_MEMORY_SECTIONS = (
    "Current objective",
    "Approved decisions",
    "Active boundary",
    "Verified state",
    "Blockers and unverified facts",
    "Evidence links",
    "Next handoff",
)
```

**Interfaces:**

```python
def _validate_current_memory(
    root: pathlib.Path, bundle: ContractBundle
) -> list[Finding]: ...
```

`current.md` also carries exact value-free labels for `Current task`,
`Verified commit`, and `Verified at`. Stale state means the referenced Task is
missing or not `draft|active`, or the verified commit does not resolve to an
ancestor of `HEAD`; no wall-clock age heuristic is used. T-AGCC-004 consumes
the bounded memory contract for its stewardship function and memory eval.

- [ ] Add RED
  `Task3SharedProjectMemoryTests.test_root_shims_import_current_memory_with_exact_parity`.
- [ ] Add RED
  `Task3SharedProjectMemoryTests.test_current_memory_profile_is_registered_and_required`.
- [ ] Add RED
  `Task3SharedProjectMemoryTests.test_current_memory_enforces_fixed_section_envelope`.
- [ ] Add RED
  `Task3SharedProjectMemoryTests.test_current_memory_rejects_size_line_secret_and_stale_state`.
- [ ] Run the focused class and record missing-file/import/profile failures.
- [ ] Register one `governance-current-memory` artifact profile with fixed
  sections, ordering, bounds, and Stage 00 authority classification.
- [ ] Author `current.md` for this branch using only current objective, approved
  decisions, active boundary, verified state, blockers/unverified facts,
  durable evidence links, and next handoff.
- [ ] Make `progress.md` historical navigation. Keep durable rows; do not use it
  as the bootstrap current-state payload.
- [ ] Make all three root shims import the same memory README and exact
  `current.md` path. Provider overlays may explain native loading but may not
  fork memory content.
- [ ] Add fail-closed validation codes
  `AGC-MEMORY-BOUNDS`, `AGC-MEMORY-FORBIDDEN-MATERIAL`, and
  `AGC-MEMORY-STALE-STATE`, with value-free diagnostics.
- [ ] Validate that memory contains no policy body, raw command log, credential,
  token, secret, auth file, shell history, or provider-global state.
- [ ] Run:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_contract.Task3SharedProjectMemoryTests \
  -v
python3 -m unittest tests.validation.test_agent_governance_contract -v
python3 scripts/validation/check-agent-governance-contract.py \
  --mode repository --section harness
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

- [ ] Expect exact root import parity, all seven sections, no bounds/secret/stale
  finding, and zero documentation failures.
- [ ] Update Task evidence and commit
  `feat(governance): establish shared project memory`.
- [ ] Dispatch fresh specification and quality reviewers for the exact Task 3
  range; remediate and re-review C/I findings.

### Task 4: Converge Capability Functions, Harness, Loop, and Evals

**Task ID:** `T-AGCC-004`

**Files:**

- Create
  `docs/00.agent-governance/agents/functions/provider-model-evaluation.md`.
- Create
  `docs/00.agent-governance/agents/functions/project-memory-stewardship.md`.
- Modify
  `docs/00.agent-governance/contracts/agent-catalog.yaml`.
- Modify
  `docs/00.agent-governance/contracts/provider-models.yaml`.
- Modify
  `docs/00.agent-governance/rules/agentic.md`.
- Modify
  `docs/00.agent-governance/subagent-protocol.md`.
- Modify
  `docs/00.agent-governance/rules/provider-capability-matrix.md`.
- Modify
  `scripts/validation/agent_governance_contract.py`.
- Modify
  `scripts/operations/provider_surface_renderer.py` only if the two new
  functions expose an unhandled native projection shape.
- Modify
  `scripts/validation/agent_output_eval.py`.
- Modify
  `docs/90.references/data/governance/agent-output-eval-fixtures.md`.
- Modify
  `tests/validation/test_agent_governance_contract.py`.
- Modify
  `tests/validation/test_provider_surface_renderer.py`.
- Modify
  `tests/validation/test_agent_output_eval_fixtures.py`.
- Regenerate
  `.agents/skills/provider-model-evaluation/SKILL.md`,
  `.agents/skills/project-memory-stewardship/SKILL.md`,
  `.claude/skills/provider-model-evaluation/SKILL.md`, and
  `.claude/skills/project-memory-stewardship/SKILL.md`.
- Modify the sibling Task ledger.

**Function ownership:**

```yaml
- function_id: provider-model-evaluation
  owner_agent: eval-engineer
  reviewer_agents: [code-reviewer, rules-engineer]
  outputs: [sourced-model-disposition, native-acceptance-verdict, regression-comparison]
- function_id: project-memory-stewardship
  owner_agent: doc-writer
  reviewer_agents: [rules-engineer, eval-engineer]
  outputs: [bounded-current-state-update, durable-evidence-links, policy-duplication-check]
```

**Typed control separation:**

- `harness_layers` owns the eight control-plane layers.
- `workflow_states` owns the ordered
  `discover -> design/plan -> approval -> implement -> validate ->
  independent-review -> evidence -> handoff` lifecycle.
- Existing `harness_loops` remain bounded retry/event controls and must
  reference applicable workflow states. They do not become a second lifecycle.

Each workflow state requires `state_id`, `owner_agent`, `required_inputs`,
`mutation_authority`, `entry_condition`, `exit_gate`, `max_attempts`,
`failure_return`, `evidence_fields`, and `handoff_target`. `failure_return` may
be another state or `stop`; `handoff_target` may be another state or `complete`.

**Interfaces:**

```python
def _validate_harness_layers(
    layers: Sequence[Mapping[str, object]], agent_ids: frozenset[str]
) -> list[Finding]: ...

def _validate_workflow_states(
    states: Sequence[Mapping[str, object]], agent_ids: frozenset[str]
) -> list[Finding]: ...
```

Both functions return the same deterministic, value-free `Finding` type as the
existing contract validator. The provider renderer consumes only catalog
function projections; the eval runner consumes the two new function IDs and
eight workflow-state IDs through exact fixture context.

**Evaluation cardinality:**

- Add `AOE-MODEL-001`, `AOE-MEMORY-001`, and `AOE-LOOP-001`.
- Add `AOE-REG-011` through `AOE-REG-016`, one pass and one fail case per new
  fixture.
- Final exact counts: 11 fixtures and 16 regressions.

- [ ] Add RED function cardinality/ownership/projection tests for 14 roles and
  24 functions.
- [ ] Add RED capability-intake tests that map provider model QA and knowledge
  stewardship to the two new functions without adding roles.
- [ ] Add RED
  `Task4HarnessLoopTests.test_harness_declares_eight_typed_layers_and_discover_to_handoff_states`.
- [ ] Add RED fixture/catalog/cardinality tests for exact 11/16 counts.
- [ ] Run focused RED commands and record the expected 22-to-24, missing
  function, missing layer/state, and 8/10-to-11/16 failures.
- [ ] Add both canonical function documents with the registered function
  frontmatter order and topic-specific content.
- [ ] Assign `provider-model-evaluation` to `eval-engineer` and
  `project-memory-stewardship` to `doc-writer`; update reviewers, capability
  intake, outputs, gates, and projection targets.
- [ ] Keep the active role set at 14; record every `agency-agents` comparison
  decision as merge, defer, or reject with local owner and source.
- [ ] Add eight typed harness layers and eight workflow states with bounded
  retries, failure return, evidence, and handoff semantics.
- [ ] Add the three fixtures and six regressions with exact thresholds,
  value-free block codes, bounded catalog limits, and no live-model claim.
- [ ] Run the provider renderer write path and inspect only the four expected
  new skill projections plus any deterministic owner updates.
- [ ] Run:

```bash
python3 -m unittest \
  tests.validation.test_agent_governance_contract.Task4CapabilityFunctionTests \
  tests.validation.test_agent_governance_contract.Task4HarnessLoopTests \
  -v
python3 -m unittest tests.validation.test_provider_surface_renderer -v
python3 -m unittest tests.validation.test_agent_output_eval_fixtures -v
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/run-agent-output-eval-fixtures.sh \
  --check-fixtures --check-regressions
python3 scripts/validation/check-agent-governance-contract.py --mode contract
python3 scripts/validation/check-agent-governance-contract.py \
  --mode repository --section all
git diff --check
```

- [ ] Expect 14 roles, 24 functions, 8 layers, 8 states, 11/11 fixtures,
  16/16 regressions, and zero provider drift/findings.
- [ ] Update Task evidence and commit
  `feat(harness): converge agent functions and loops`.
- [ ] Dispatch fresh specification and quality reviewers for the exact Task 4
  range; remediate and re-review C/I findings.

### Task 5: Reconcile Local Actions, QA, and Remote Observation

**Task ID:** `T-AGCC-005`

**Files:**

- Create `.github/INDEX.md` as the navigation-only entrypoint for the tracked
  GitHub control surface. Do not create `.github/README.md`.
- Modify `.github/workflows/ci-quality.yml`.
- Preserve `.github/workflows/greetings.yml`; its welcome purpose remains
  current and non-gating.
- Modify `.github/rulesets/main-protection.md`.
- Modify `docs/00.agent-governance/rules/github-governance.md`.
- Modify
  `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml` to
  register the non-canonical GitHub navigation index and remove the deleted
  memo's active artifact registration.
- Delete
  `docs/00.agent-governance/memory/github-ci-contract-audit.md` after its
  current local contract routes and historical provenance are preserved.
- Modify `docs/00.agent-governance/memory/README.md`.
- Modify `scripts/validation/check-repo-contracts.sh`.
- Modify `tests/validation/test_agent_governance_ci_routing.py`.
- Create
  `docs/90.references/data/governance/github-actions-control-plane-observation.yaml`.
- Modify
  `docs/90.references/data/governance/README.md`.
- Regenerate
  `docs/90.references/llm-wiki/llm-wiki-index.md`,
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`, and
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`
  as direct generated-owner fallout.
- Modify the sibling Task ledger.

**Pinned CI command:**

```bash
uvx --from 'zizmor==1.28.0' zizmor . --format sarif . > results.sarif
```

**Remote observation record:**

```yaml
schema_version: 1
observed_at: 2026-07-26T18:22:32+09:00
repository: buenhyden/hy-home.docker
authority: non-authoritative-observation
remote_default_commit: a897978f
local_base_commit: e65bb18fa2f6e3fb6235725750c7c57cbe0227ee
latest_ci_run_id: 29777690571
latest_ci_conclusion: failure
observed_ci_jobs: 15
root_cause: unverified
managed_workflows:
  - {id: 222509952, name: Dependabot Updates}
  - {id: 223086017, name: CodeQL}
  - {id: 282786058, name: Dependency Graph}
control_plane_verification: unverified
```

**Interfaces:**

The GitHub entrypoint contract is:

```yaml
path: .github/INDEX.md
authority: navigation-only
canonical: false
frontmatter: forbidden
required_sections:
  - Purpose
  - Surface Map
  - Authority and Change Routes
  - Verification
  - Related Documents
```

`INDEX.md` links to the tracked GitHub surfaces and to the canonical Stage 00
GitHub governance, proposed ruleset, local QA runner, and dated Stage 90 remote
observation. It may describe how to find those authorities, but it may not
duplicate normative policy, the 16-job contract, secret or variable names, or
remote enforcement claims. The artifact registry uses empty frontmatter keys
for this non-SDLC navigation surface, and focused tests require
`.github/README.md` to remain absent.

The embedded duplicate-safe workflow checker in
`scripts/validation/check-repo-contracts.sh` consumes the tracked workflow,
ruleset proposal, Stage 00 GitHub policy, and Stage 90 observation as one
read-only comparison. New failures are rendered as
`unpinned dynamic tool package`, `stale active remote-state claim`, or
`invalid remote observation field` without including raw remote payloads.
T-AGCC-006 consumes the dated observation and exact 16-job local contract.

The implementation must retain this observation time, add the public source
URLs used for each record, and avoid credentials, secret names, raw logs, or
inferred branch protection.

- [ ] Add RED
  `AgentGovernanceRoutingTests.test_zizmor_dynamic_tool_is_exactly_pinned`
  requiring package `zizmor==1.28.0` and rejecting the yanked 1.27.0 release.
- [ ] Add RED
  `AgentGovernanceRoutingTests.test_github_index_is_navigation_only_and_not_readme`
  requiring the exact path, section envelope, canonical links, absent
  frontmatter, and no `.github/README.md`.
- [ ] Add RED remote-inventory schema tests for management class, retrieval
  time, source visibility, run conclusion, job count, and explicit unverified
  control-plane/root-cause state.
- [ ] Add RED stale-claim tests rejecting the July 4 remote enforcement claims
  from active local proposal/policy surfaces.
- [ ] Run focused RED tests and record the unpinned command, missing inventory,
  and stale remote-state failures.
- [ ] Pin zizmor 1.28.0 while retaining full-SHA action pins, least privilege,
  timeout, SARIF upload, and the existing 16 job IDs.
- [ ] Create `.github/INDEX.md`, register it as a non-canonical
  `github-navigation-index`, and keep policy, job identities, and observed
  remote state in their existing canonical owners.
- [ ] Extend `check-repo-contracts.sh` to fail on an unpinned `uvx` package,
  duplicate workflow keys, unsafe triggers/interpolation, job drift,
  permission/timeout drift, or ruleset/job mismatch.
- [ ] Write the dated Stage 90 remote observation and replace active stale
  remote claims with a link and `unverified` boundary.
- [ ] Remove `github-ci-contract-audit.md` only after:
  `agent-governance-artifacts.yaml`, `memory/README.md`, and
  `github-governance.md` no longer consume it; Stage 90 owns the dated remote
  observation; all three registered generated owners are refreshed; and the
  Task records source commit/blob plus the exact rollback command.
- [ ] Run:

```bash
python3 -m unittest tests.validation.test_agent_governance_ci_routing -v
bash scripts/validation/run-local-qa-gates.sh --list
bash scripts/validation/run-local-qa-gates.sh --harness
bash scripts/validation/check-repo-contracts.sh
python3 scripts/validation/check-agent-governance-contract.py \
  --mode repository --section harness
pre-commit run actionlint --files \
  .github/workflows/ci-quality.yml \
  .github/workflows/document-corpus-lifecycle.yml
git diff --check
```

- [ ] Expect exact 16-job parity, pinned zizmor 1.28.0, one navigation-only
  `.github/INDEX.md`, no `.github/README.md`, static workflow policy pass, and
  remote state still explicitly unverified.
- [ ] If local zizmor 1.28.0 cannot be fetched in the restricted environment,
  record `environment_blocked`; do not substitute local 1.25.2 as a pass.
- [ ] Update Task evidence and commit
  `ci(governance): reconcile agent quality controls`.
- [ ] Dispatch fresh specification and security-focused quality reviewers for
  the exact Task 5 range; remediate and re-review C/I findings.

### Task 6: Refresh Canonical Evidence and Close the Branch

**Task ID:** `T-AGCC-006`

**Files:**

- Modify canonical research:
  `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md`,
  `agent-model-selection.md`, `provider-model-landscape.md`,
  `provider-implementation-comparison.md`, `ai-agent-catalogs.md`,
  `harness-engineering.md`, `loop-engineering.md`, and
  `quality-ci-formatting.md`; also modify the directly affected siblings
  `agent-instructions-vibe-coding.md`, `automation-pipeline-workflow.md`,
  `security-governance.md`, and `workspace-baseline.md` so the canonical pack
  does not retain displaced 14-role/22-function/seven-intake, 8/10 semantic
  evaluation, or 15-job local-CI summaries.
- Modify canonical audit:
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`,
  `implementation-overview.md`,
  `agent-instructions-catalog-vibe-models.md`,
  `harness-engineering-implementation.md`,
  `loop-engineering-implementation.md`,
  `provider-harness-loop-implementation.md`,
  `automation-candidates.md`,
  `sdlc-quality-formatting-implementation.md`,
  `security-framework-maturity.md`, and
  `workspace-rules-environment-implementation.md`.
- Regenerate
  `docs/90.references/data/governance/audit-implementation-matrix.md`,
  `docs/90.references/data/security/security-automation-readiness.md`,
  `docs/90.references/llm-wiki/llm-wiki-index.md`, and
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`.
- Regenerate
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`
  only through its registered owner.
- Modify the two active Stage 00 direct-impact consumers discovered by the
  closure RED scan:
  `docs/00.agent-governance/providers/codex.md` and
  `docs/00.agent-governance/rules/postflight-checklist.md`; add only the narrow
  regression assertions required in
  `tests/validation/test_agent_governance_contract.py`.
- Modify Stage 03/04 README indexes when Spec/Plan/Task lifecycle transitions
  require them.
- Modify `docs/00.agent-governance/memory/current.md` and historical progress
  navigation with compact closure evidence.
- Modify the sibling Task ledger and this Plan for final lifecycle state.

**Interfaces:**

T-AGCC-006 consumes the exact Task 1-5 commit ranges and review verdicts. The
criterion parser must still return 11 reports and 161 ten-column rows; each
registered generator must produce byte-identical output on its immediate
`--check`. The closure output is an active-to-completed lifecycle transition,
not a new policy or runtime interface.

- [ ] Scan all target and direct-impact paths for stale model IDs, old profile
  IDs, retired role-transfer claims, 22-function claims, 8/10 eval counts,
  15-job local claims, stale remote enforcement claims, and any active link to
  the deleted GitHub CI memory memo. T-AGCC-005 owns the deletion and immediate
  consumer/generated cleanup; this step verifies that no later change
  reintroduced drift.
- [ ] Bind the closure RED findings before editing their consumers: the Codex
  overlay must select the five exact work-profile mappings with
  `gpt-5.6-sol` or `gpt-5.6-terra`, provider lifecycle `stable`, and separate
  unverified runtime acceptance/entitlement; the postflight checklist must
  require exactly 11 fixtures and 16 regressions.
- [ ] Update the canonical July 5 research with official 2026-07-26 sources and
  the implemented workspace comparison. Do not revive or rewrite the
  superseded July 7 pack.
- [ ] Update only affected canonical audit criterion rows from observed tracked
  evidence; preserve the exact 11-report/161-row schema and do not promote
  live provider, remote enforcement, or deployment state.
- [ ] Regenerate the audit matrix, security readiness, LLM index/coverage, and
  semantic inventory through their owners; inspect generated diffs.
- [ ] Record every deletion or no-deletion decision. No additional one-time
  file may be removed without exact consumer, owner, provenance, rollback, and
  reviewer evidence.
- [ ] Run focused audit tests:

```bash
python3 -m unittest \
  tests.validation.test_audit_criterion_contract \
  tests.validation.test_agentic_audit_semantic_freshness \
  -v
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/report-audit-pack-coverage.sh --check
```

- [ ] Run the full relevant dependency-locked ladder when available:

```bash
uv run --with-requirements scripts/requirements.txt \
  python -m unittest \
  tests.validation.test_agent_governance_contract \
  tests.validation.test_provider_surface_renderer \
  tests.validation.test_provider_native_surfaces \
  tests.validation.test_agent_output_eval_fixtures \
  tests.validation.test_agent_governance_ci_routing \
  tests.validation.test_audit_criterion_contract \
  tests.validation.test_agentic_audit_semantic_freshness \
  -v
uv run --with-requirements scripts/requirements.txt \
  python scripts/validation/check-agent-governance-contract.py \
  --mode repository --section all
```

- [ ] Run aggregate documentation, owner, and repository gates:

```bash
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/report-provider-hook-parity.sh --check
bash scripts/validation/run-agent-output-eval-fixtures.sh \
  --check-fixtures --check-regressions
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --check
git diff --check
```

- [ ] Record exact pass counts or environment-blocked rerun routes in the Task
  ledger; never convert an unavailable dependency or external capability into
  a pass.
- [ ] Update Task evidence and commit
  `docs(governance): close canonical convergence evidence`.
- [x] Dispatch fresh Task 6 specification and quality reviewers; remediate and
  re-review C/I findings.
- [ ] Ask the user for explicit approval for the exact controlled all-files
  wrapper run. Do not infer approval from this Plan.
- [ ] After approval and from a clean committed worktree, run only:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md \
  --allow-prefix AGENTS.md \
  --allow-prefix CLAUDE.md \
  --allow-prefix GEMINI.md \
  --allow-prefix .agents \
  --allow-prefix .claude \
  --allow-prefix .codex \
  --allow-prefix .gemini \
  --allow-prefix .github \
  --allow-prefix docs/00.agent-governance \
  --allow-prefix docs/03.specs/134-agent-governance-canonical-convergence \
  --allow-prefix docs/04.execution \
  --allow-prefix docs/90.references \
  --allow-prefix scripts \
  --allow-prefix tests
```

- [ ] Record only sanitized wrapper markers, exit status, snapshot result, and
  before/after/changed/unexpected path sets.

#### T-AGCC-006-QA-R1: Value-free Wrapper Failure Diagnostic

The user approved this bounded remediation on 2026-07-28 after the separately
recorded one-attempt wrapper failure. This approval authorizes sanitizer
implementation, focused tests, documentation synchronization, and independent
review only. It does not authorize another all-files wrapper execution.

**Files:**

- Modify
  `scripts/validation/run-agent-precommit-all-files.sh`.
- Modify
  `tests/validation/test_run_agent_precommit_all_files.sh`.
- Modify `scripts/README.md` only to describe the new value-free result.
- Modify this Plan, the sibling Task ledger, and
  `docs/00.agent-governance/memory/current.md` for bounded approval and
  evidence synchronization.

**Interfaces and safety bounds:**

- Preserve the exact inner command
  `pre-commit run --all-files --show-diff-on-failure`, all existing wrapper
  arguments, worktree/task/prefix validation, snapshot semantics, exit
  propagation, exit `20` precedence, signal handling, cleanup, and observation
  boundary.
- On a nonzero hook exit, emit at most one first-failure tuple derived from the
  first pre-commit-owned failure metadata block. A reported hook ID must match
  both the strict token grammar
  `[A-Za-z0-9][A-Za-z0-9._-]{0,63}` and an exact hook ID in the tracked
  `.pre-commit-config.yaml`.
- The tuple may contain only a hook ID plus one bounded class:
  numeric exit `0..255`, files modified, or unavailable. Do not emit hook
  names, messages, durations, command output, file content, configuration
  values, environment values, paths from hook output, or subsequent metadata
  that could have been forged by raw hook output.
- If the first metadata record is absent, malformed, unregistered, ambiguous,
  or not followed by a recognized bounded detail, emit `unavailable`. A
  successful hook run emits `not_applicable`.
- Keep raw stdout/stderr ephemeral and delete it through the existing wrapper
  cleanup. Never persist or print credentials, tokens, secret values, auth
  files, shell history, or raw logs.

**TDD and verification:**

- [ ] Add failing fake-hook tests for a registered first failing hook with a
  numeric exit and for the confidentiality boundary before implementation.
- [ ] Add coverage for files-modified, absent metadata, malformed or
  unregistered IDs, duplicate or ambiguous registered-ID metadata, raw-output
  spoof attempts, successful runs, after-snapshot failure, unchanged exit
  propagation, and temporary-file cleanup.
- [ ] Run the focused fake-hook suite, Bash syntax, ShellCheck for the wrapper
  and test, repository wrapper-contract checks when dependencies are
  available, and `git diff --check`.
- [ ] Record environment-blocked checks without converting them to pass.
- [ ] Commit the remediation as one logical wrapper/test/docs unit, then
  dispatch fresh specification and quality/security reviewers and remediate
  every Critical or Important finding.
- [ ] Do not run the controlled wrapper during this remediation. After clean
  reviews, request a new exact user approval that explicitly authorizes one
  exceptional second attempt from a named clean commit.

#### T-AGCC-006-QA-D2: Post-pass Discrepancy Disposition

The exceptional second attempt approved by the user passed from clean commit
`d4bbc3c47cabcfae3c3b8e3f620939acab8d3fce`. A whole-branch correctness
reviewer later violated its read-only assignment and the consumed approval
boundary by executing the same wrapper at
`6c6a153058fb7d1511d57fd90b0f3f18555a1540`. That unauthorized execution
returned hook exit 3, `first_failure=unavailable`, a passing snapshot, and zero
observed Git-visible path changes. Its review and closure verdict are
disqualified, but the observed failure remains discrepancy evidence and cannot
be ignored.

**Facts and bounds:**

- The only tracked delta from the passing checkpoint to the unauthorized
  execution checkpoint is the Task ledger and bounded current-memory evidence.
- `.pre-commit-config.yaml` and the wrapper are unchanged across that delta.
  Default-stage candidates are basic file hooks, YAML/Markdown/Shell/Actions
  linters, Dependabot validation, Hadolint, Gitleaks, and the applicable
  Next.js lint hook. The local repository-contract and document gates are
  `pre-push` only and are not attributed as the wrapper root cause.
- The sanitized evidence cannot identify a hook or distinguish a hook exit 3
  from a pre-commit internal failure. No raw cache log, hook output, secret,
  auth file, token, or shell history may be inspected or retained.
- Whole-branch security review independently found a stale `29/0` wrapper-test
  oracle in `check-repo-contracts.sh`. Commit
  `b493aa32b7e8ee9428ca8010331732592c977bdb` replaces it with a positive
  zero-failure summary and exact critical-case markers. That pre-push-only
  defect is remediated and reviewed but is not claimed as the default-stage
  wrapper failure root cause.

**Disposition sequence:**

- [ ] Correct the committed discrepancy evidence to attribute the unauthorized
  execution to `/root/whole_branch_correctness_review`, not the Controller,
  while preserving its exact sanitized result and commit provenance.
- [x] Record the disqualified correctness review, the whole-branch security
  C0/I1 result, the `b493aa32` remediation, and its independent C0/I0 re-review.
- [ ] Validate the Plan/Task/current-memory update with an explicit-base
  metadata check, traceability, implementation alignment, and diff hygiene.
- [x] Obtain a fresh independent read-only review of this discrepancy plan.
- [ ] Do not run the wrapper or `pre-commit` while preparing or reviewing this
  disposition.
- [ ] After a clean committed checkpoint and clean plan review, ask the user
  for a new exact approval for one recovery wrapper attempt. The approval must
  name the checkpoint and exact existing command and must acknowledge the
  unauthorized intervening attempt.
- [x] If the recovery attempt passes, record its exact sanitized evidence and
  dispatch entirely fresh whole-branch correctness and security reviewers over
  the then-current range. If it fails, record and stop; do not request or infer
  another run in this task.

- [x] Dispatch a fresh whole-branch correctness reviewer and a separate fresh
  whole-branch security reviewer for
  `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee..HEAD`.
- [x] Remediate and re-review every Critical or Important finding.
- [ ] Transition Spec, Plan, Task, memory current state, and Stage 03/04 indexes
  only after both whole-branch reviewers authorize closure.
- [ ] Run post-lifecycle metadata, traceability, alignment, generated-owner,
  repository-contract, and diff-hygiene checks.
- [x] Present local branch completion options through
  `superpowers:finishing-a-development-branch`; the user selected option 1 and
  the feature branch was merged into local `main`. No push or remote mutation
  was performed.

## Verification Plan

### Per-task Gate

Every task must produce:

- an observed RED for each new behavior;
- focused GREEN tests;
- contract/renderer/owner checks relevant to its files;
- `git diff --check`;
- one logical commit;
- fresh independent review with Critical 0 and Important 0.

### Final Expected State

| Contract | Expected |
| --- | --- |
| Active roles/functions/providers | 14 / 24 / 3 |
| Work profiles | 5 exact profiles; one per role |
| Active historical lifecycle records | 0 |
| Shared current memory | one file, at most 32 KiB and 400 lines |
| Harness/workflow | 8 typed layers and 8 ordered states |
| Semantic eval | 11 fixtures and 16 regressions |
| Provider drift | 0 across four provider surfaces |
| Local CI jobs | 16 exact jobs |
| Dynamic zizmor package | exact 1.28.0; yanked 1.27.0 rejected |
| Canonical audit | 11 criterion reports, 161 exact rows |
| Remote GitHub | read-only dated observation; control plane unverified |
| Task/branch review | each task plus whole branch C0/I0 |

## Risks and Rollback

| Risk | Control | Rollback |
| --- | --- | --- |
| Model ID accepted by API but not CLI/account | separate lifecycle, acceptance, entitlement, and eligibility; no live claim | revert Task 2 commit and restore prior projections |
| Generated provider drift or unsupported field | native-schema RED tests and renderer-only writes | revert Task 2/4 commit; rerun renderer check |
| Current memory becomes policy/log store | fixed sections, byte/line bounds, secret/stale scanners | revert Task 3; root shims fall back to prior bootstrap commit |
| Function or loop authority duplicates existing role policy | 14-role invariant and typed owner/reference checks | revert Task 4 and regenerated projections |
| Workflow hardening changes required job identity | exact 16-job validator/ruleset/tests | revert Task 5; no remote state was changed |
| Historical evidence erased | Stage 90 ledger plus exact commit/blob provenance | restore the exact ledger path from its `source_commit`; the planned authored deletion uses `git restore --source=e65bb18f -- docs/00.agent-governance/memory/github-ci-contract-audit.md` |
| Restricted dependency/network blocks validation | fail closed and record exact rerun route | no product rollback; rerun in canonical locked environment |
| Audit status overpromotion | criterion contract, semantic freshness, independent review | revert Task 6 audit commit and regenerate from prior rows |

## Approval Gates

- Spec 134 is approved and active.
- The user approved this exact Plan on 2026-07-26. This Plan and its sibling
  Task are active; the six local implementation tasks, protected local targets,
  and deletion gates defined here are authorized.
- Remote GitHub remains read-only; any mutation requires a new exact approval.
- Provider live calls, paid jobs, entitlement probes, and provider-global
  configuration remain unapproved.
- The controlled all-files wrapper requires separate per-run approval at
  T-AGCC-006.
- Push, remote merge, and remote branch cleanup require separate approval.

## Completion Criteria

- [ ] All AGCC-001 through AGCC-016 requirements have Task evidence.
- [ ] Active contracts contain 14 roles, 24 functions, 3 providers, 5 profiles,
  and no retired/deprecated lifecycle state.
- [ ] Model sources and retrieval times are current as of 2026-07-26 KST.
- [ ] All provider projections are deterministic and native-schema valid.
- [ ] All root shims load one bounded current project memory.
- [ ] Eight harness layers, eight workflow states, and bounded retry/approval
  semantics validate.
- [ ] Exact 11/16 semantic fixture/regression gates pass.
- [ ] Local 16-job CI/QA contract and zizmor 1.28.0 pin validate.
- [ ] Remote observations are dated, source-linked, non-authoritative, and
  explicitly unverified where authentication was unavailable.
- [ ] Canonical research/audit and registered generated owners are fresh.
- [ ] Every deletion has consumer, provenance, rollback, and reviewer evidence.
- [ ] Six logical tasks have fresh implementation and independent review
  evidence with C0/I0.
- [ ] Whole-branch correctness and security reviews both authorize closure.
- [ ] Controlled wrapper evidence is recorded only after exact user approval.
- [ ] Branch remains local unless the user separately requests finish actions.

## Related Documents

- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Task ledger](../tasks/2026-07-26-agent-governance-canonical-convergence.md)
- [Agent governance overview](../../00.agent-governance/README.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [Quality scope](../../00.agent-governance/scopes/qa.md)
- [Canonical research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
