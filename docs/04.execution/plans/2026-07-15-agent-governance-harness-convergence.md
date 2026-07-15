---
status: active
artifact_id: plan:2026-07-15-agent-governance-harness-convergence
artifact_type: plan
parent_ids:
  - spec:132-agent-governance-harness-convergence
---

# Agent Governance Harness Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development to implement this plan task-by-task.
> Use superpowers:executing-plans only as the controller's batch-tracking
> discipline. Steps use checkbox (`- [ ]`) syntax for execution tracking.

**Goal:** Make Stage 00 the tested source of truth for agent governance,
provider-native projections, model routing, harness loops, and evidence while
keeping provider surfaces deterministic, least-privilege, and honest about
runtime adoption.

**Architecture:** Three typed Stage 00 contracts own artifact/authority,
agent/function, and provider/model semantics. A focused Python validator loads
those contracts, and a deterministic renderer projects the canonical catalog
into Claude, Codex, Gemini CLI, and `.agents` compatibility surfaces. Existing
repository-contract, semantic-eval, local QA, and CI owners enforce the result;
they do not become additional policy authorities.

**Tech Stack:** YAML 1.2-compatible contracts, Python 3.12, PyYAML, unittest,
Markdown/CommonMark, JSON, TOML, Bash, Claude Code project configuration,
Codex project agents/hooks, Gemini CLI project agents/hooks, GitHub Actions,
pre-commit, Graphify, and Git.

## Global Constraints

- Work only in `.worktrees/agent-governance-harness-convergence` on
  `codex/agent-governance-harness-convergence`; keep the root checkout on
  `main`.
- Stage 00 is the only normative owner. Root shims and `.claude/`, `.codex/`,
  `.gemini/`, and `.agents/` are entry or generated adapter surfaces.
- `.agents/` is the Antigravity/common compatibility and shared-function
  projection. It is not Gemini CLI native configuration.
- Canonical functions project to `.claude/skills/<id>/SKILL.md` and shared
  `.agents/skills/<id>/SKILL.md`. Remove lowercase `skill.md` entrypoints and
  the obsolete `.codex/skills/**` tree; do not recreate them.
- Use provider-native schemas. Do not inject canonical-only fields into strict
  provider formats to imitate parity.
- Separate provider capability, repository adoption, local runtime acceptance,
  entitlement, and validation depth. Missing provider CLIs or entitlement
  produce `needs_revalidation`, never a fabricated pass.
- Model defaults are pinned official IDs checked on 2026-07-15 KST. Preview,
  deprecated, invitation-only, and entitlement-dependent models remain
  catalog-only and are never silent fallbacks.
- Retire `style-enforcer` and `wiki-curator`; transfer their responsibilities
  in the same task. Add `eval-engineer`. The final catalog has 14 roles.
- Complete all 22 canonical functions before treating generated skill parity
  as implemented. Provider skill content may not be the source of Stage 00
  policy.
- Keep README files profile-specific navigation surfaces. Do not add arbitrary
  policy sections or copy contract prose into them.
- Preserve existing historical evidence. Update the canonical July 5 audit
  only from observed results; the superseded July 7 pack remains mapping-only.
- Never persist secrets, credentials, tokens, auth files, shell history, raw
  logs, or unbounded provider output in evidence.
- Do not change user-global provider configuration, credentials, runtime
  Compose, infrastructure, deployment, release, remote GitHub state, branch
  protection, or environments.
- Use TDD for every parser, validator, generator, selector, or semantic-eval
  behavior. Run the RED command and record the expected failure before the
  minimal GREEN change.
- Execute Tasks 1 through 6 serially. Each task receives a fresh implementation
  agent, a fresh specification reviewer, and a separate quality reviewer.
  Critical and Important findings must be fixed and re-reviewed.
- Create at least one logical Conventional Commit per task. Material review
  remediations remain separate logical commits.
- Never run `pre-commit run --all-files` directly. Task 6 uses
  `scripts/validation/run-agent-precommit-all-files.sh` with the tracked Task
  ledger and explicit allowed prefixes.
- After Python, shell, workflow, or validation changes, run `graphify update .`
  when available. Treat its report as advisory and corroborate it against
  tracked source and Stage 00/03/04 contracts.

## Overview

This plan implements Spec 132 in six dependency-ordered logical units. Task 1
creates typed machine owners and a contract-only validator. Task 2 normalizes
artifact metadata, path authority, root shims, and stale governance references.
Task 3 converges the canonical agent and function catalogs and reverses the
current `.claude/skills` source-of-truth inversion. Task 4 renders complete
provider-native Claude, Codex, Gemini CLI, and compatibility projections with
the approved model registry. Task 5 activates repository-wide drift, semantic
loop, QA selector, and CI enforcement. Task 6 reconciles references and the
canonical audit, records evidence, performs controlled all-files QA, and closes
the exact branch range.

The tracked execution ledger is created with this Plan at
`docs/04.execution/tasks/2026-07-15-agent-governance-harness-convergence.md`.
It begins with `not_run` evidence, then records exact commands, exit states,
review verdicts, deviations, commits, and final closure without duplicating the
implementation design.

Because this Plan is a new active consumer of five promoted Foundation sources,
the planning commit also adds this exact Plan path to those five existing
`active_consumers` lists and regenerates the Foundation summary. It changes no
Foundation disposition, review verdict, enforcement level, source identity, or
other consumer row.

## Context and Inputs

At baseline `6cde68dc`, Stage 00 declares canonical ownership but the provider
sync script reads `.claude/skills/*/skill.md` as the source for Codex and
compatibility skills. The 15-role catalog contains two roles approved for
retirement and lacks `eval-engineer`. Seven function entries remain skeletal.
Codex adapters omit current native instruction fields, Gemini CLI has no native
`.gemini/` project surface, several Claude imports are literal fenced text, and
Hookify rules reference nonexistent local files. Root/provider changes are not
fully included in the current pre-push selector.

The canonical July 5 audit measures 161 criteria and records every harness and
loop criterion below full closure. Existing CI, repository contracts,
controlled all-files QA, semantic fixture execution, metadata validation, and
generated indexes are strong reusable owners. This work extends those owners
instead of adding a second CI taxonomy or an always-on orchestrator.

Canonical inputs:

- `docs/03.specs/132-agent-governance-harness-convergence/spec.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/harness-implementation-map.md`
- `docs/00.agent-governance/rules/provider-capability-matrix.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/workflows.md`
- `docs/00.agent-governance/agents/agents/`
- `docs/00.agent-governance/agents/functions/`
- `scripts/operations/sync-provider-surfaces.sh`
- `scripts/validation/check-repo-contracts.sh`
- `scripts/validation/run-agent-output-eval-fixtures.sh`
- `scripts/validation/run-local-qa-gates.sh`
- `scripts/validation/run-agent-precommit-all-files.sh`
- `.pre-commit-config.yaml`
- `.github/workflows/ci-quality.yml`
- `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`

Official provider and external evidence is frozen by observed date in Spec 132:
OpenAI Codex agents/hooks/models and harness engineering; Anthropic Claude
subagents/hooks/models/effective agents; Gemini CLI native subagents/hooks and
Gemini model/deprecation pages; and `agency-agents` as capability-catalog input.

The Graphify report was built from `f8a72211`, predates this branch, and contains
generic communities. It is navigation evidence only. Tracked Stage 00, the
approved Spec, this Plan/Task pair, validation code, and Git history are
authoritative.

## Goals and Non-goals

### Goals

- Define one typed authority and artifact inventory, one canonical role and
  function catalog, and one dated provider/model registry.
- Validate type-specific metadata, section envelopes, root shims, README
  profiles, protected paths, and exact canonical relationships.
- Render provider-native agents, skills, hooks, imports, settings, and model
  choices deterministically from Stage 00.
- Complete the 14-role/22-function operating model with independent evaluation
  ownership and explicit least-privilege boundaries.
- Define semantic harness events, retry/stop/escalation rules, review
  independence, sanitized evidence, and representative regression fixtures.
- Expand existing local and CI gates to all root/provider/Stage 00 coupled
  surfaces without changing runtime or deployment state.
- Reconcile canonical research/audit facts, generated inventories, Task
  evidence, progress memory, and exact logical commits.

### Non-goals

- Install the upstream `agency-agents` roster or preserve its personalities.
- Create an always-running supervisor, issue-tracker integration, or paid/remote
  agent dispatch.
- Add floating model aliases or make preview models repository defaults.
- Assert provider-native hook parity where the provider lacks an event.
- Mutate provider-global settings, credentials, secrets, Compose services,
  deployment runtime, releases, GitHub rulesets, or protected environments.
- Rewrite unrelated Stage 01 through Stage 99 documents or historical evidence.

## File Responsibility Map

| Surface | Responsibility |
| --- | --- |
| `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml` | Artifact types, exact governed-path inventory, root/README profiles, path authority, and protected review rules. |
| `docs/00.agent-governance/contracts/agent-catalog.yaml` | Fourteen roles, twenty-two functions, scopes, permissions, ownership, role transfers, provider projection eligibility, and capability-intake decisions. |
| `docs/00.agent-governance/contracts/provider-models.yaml` | Provider capabilities/adoption, native schemas, semantic-event mapping, model status/evidence/eligibility/fallback, and work profiles. |
| `scripts/validation/agent_governance_contract.py` | Reusable typed loader, finding model, contract checks, repository checks, and deterministic diagnostics. |
| `scripts/validation/check-agent-governance-contract.py` | Thin CLI for `contract` and sectioned `repository` modes. |
| `tests/validation/test_agent_governance_contract.py` | Contract, metadata, model, schema, path-authority, event, and drift RED/GREEN tests. |
| `scripts/operations/provider_surface_renderer.py` | Deterministic native agent/skill/settings/hook renderer with `--check` and explicit `--write`. |
| `scripts/operations/sync-provider-surfaces.sh` | Compatibility wrapper that delegates to the renderer; no embedded catalog/model policy. |
| `docs/00.agent-governance/agents/agents/` | Canonical human-readable role instructions only. |
| `docs/00.agent-governance/agents/functions/` | Canonical human-readable function procedures only. |
| `.claude/`, `.codex/`, `.gemini/`, `.agents/` | Generated native or compatibility projections, never policy authorities. |
| `scripts/validation/run-agent-output-eval-fixtures.sh` | Existing semantic fixture runner extended for role, routing, hook-denial, evidence, and adapter-rendering cases. |
| `docs/90.references/data/governance/agent-output-eval-fixtures.md` | Human-readable representative fixture catalog and observed threshold evidence. |
| `scripts/validation/check-repo-contracts.sh` | Existing aggregate gate that calls the focused validator in repository mode. |
| `.pre-commit-config.yaml`, `scripts/validation/recommend-qa-gates.sh`, `scripts/validation/run-local-qa-gates.sh` | Changed-surface selection and deterministic local execution. |
| `.github/workflows/ci-quality.yml` | Existing read-only quality workflow; reuse `repo-contracts` and agent-output eval jobs. |
| canonical July 5 research/audit pack | Dated source facts, observed implementation state, criteria reconciliation, and recommendations. |
| Stage 04 Task and `memory/progress.md` | Approval, execution, review, commit, QA, and closure evidence. |

## Acceptance Map

| ID | Acceptance |
| --- | --- |
| VAL-132-001 | Three typed contracts parse deterministically, have unique identities, safe exact paths, non-overlapping ownership, dated sources, and valid cross-references. |
| VAL-132-002 | Every governed document and native adapter satisfies its type-specific metadata/schema/section profile; root shims and README profiles contain no copied policy. |
| VAL-132-003 | The canonical catalog contains exactly 14 roles and 22 complete functions; retired roles and stale ownership references are absent. |
| VAL-132-004 | Claude, Codex, Gemini CLI, and compatibility projections are deterministic, native-schema-valid, semantically traceable to Stage 00, and generator-check clean. |
| VAL-132-005 | Provider/model entries separate capability, adoption, runtime acceptance, entitlement, status, dated evidence, default eligibility, and fallback. |
| VAL-132-006 | Semantic events, retry/stop/escalation, least privilege, independent review, sanitized evidence, and representative eval thresholds are executable and fail closed. |
| VAL-132-007 | Existing repo-contract, pre-commit selector, local QA, and CI jobs cover root/provider/Stage 00 coupled changes without deployment or remote mutation. |
| VAL-132-008 | Canonical research/audit, generated artifacts, Task evidence, progress memory, controlled all-files QA, whole-branch reviews, and logical commits agree with observed results. |

## Work Breakdown

| Task | Logical unit | Acceptance | Primary gate |
| --- | --- | --- | --- |
| T-AGHC-001 | Typed contracts and contract-only validator | VAL-132-001 | focused Python unit tests and `--mode contract` |
| T-AGHC-002 | Metadata, authority, root shims, and governance normalization | VAL-132-002 | metadata/profile tests and governed inventory validation |
| T-AGHC-003 | Agent/function catalog and canonical skill source | VAL-132-003 | catalog/function completeness and renderer unit tests |
| T-AGHC-004 | Provider-native adapters and model policy | VAL-132-004/005 | native schema, event/model, and render-drift tests |
| T-AGHC-005 | Harness loops, semantic eval, local QA, and CI | VAL-132-006/007 | eval fixtures, selector tests, repository contracts |
| T-AGHC-006 | Reference/audit/evidence reconciliation and closure | VAL-132-008 | full verification ladder, controlled wrapper, branch reviews |

### Subagent-Driven Commit and Review Protocol

For Tasks 1 through 5, a fresh implementation agent receives only the exact
task brief, current base commit, allowed paths, prohibited paths, RED command,
GREEN command, expected commit message, and evidence fields. The implementer
runs RED/GREEN, self-reviews, updates the Task ledger, and commits. A fresh
specification reviewer examines the exact `BASE..HEAD` range against Spec 132
and this Plan. After specification PASS, a different quality reviewer examines
correctness, maintainability, security, tests, and scope. Findings are fixed in
separate commits and both reviewers re-review the new range.

Task 6 uses fresh closure implementer and review agents, then a whole-branch
specification reviewer and separate quality reviewer over
`6cde68dc..FINAL_HEAD`. The controller does not ask a reviewer to approve
uncommitted changes.

### Generated Owner Order

When a task changes tracked paths, scripts, workflow, or typed documents, run
only the applicable existing owners in this fixed order and inspect their exact
diffs:

```bash
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
python3 scripts/validation/check-document-metadata.py \
  --mode report \
  --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
```

Security readiness and the audit matrix apply when scripts/workflows change.
LLM index/coverage apply when tracked paths change. The semantic inventory
applies when typed document metadata or paths change. Owned fallout belongs to
the same logical task or an immediately following `docs(generated)` commit.

### Task 1: Typed Contracts and Contract-only Validator

**Files:**

- Create `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml`.
- Create `docs/00.agent-governance/contracts/agent-catalog.yaml`.
- Create `docs/00.agent-governance/contracts/provider-models.yaml`.
- Create `scripts/validation/agent_governance_contract.py`.
- Create `scripts/validation/check-agent-governance-contract.py`.
- Create `tests/validation/test_agent_governance_contract.py`.
- Modify `docs/00.agent-governance/README.md` only in existing Structure,
  How-to-work, and Related Documents routing.
- Modify `scripts/README.md` only in existing validation/operations catalogs.
- Modify the Task ledger and `docs/00.agent-governance/memory/progress.md`.

**Contract shape to implement:**

```yaml
schema_version: 1
checked_at: 2026-07-15T10:00:00+09:00
artifacts:
  - artifact_type: agent-role
    path_pattern: docs/00.agent-governance/agents/agents/*.md
    canonical: true
    required_keys: [layer, artifact_type, agent_id, scope, tier, status]
    key_order: [layer, artifact_type, agent_id, scope, tier, status]
    required_sections:
      - Purpose
      - Use When
      - Inputs
      - Outputs
      - Permissions
      - Success Criteria
      - Failure and Escalation
      - Related Documents
```

```python
@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    location: str
    expected: str
    actual: str
    source: str

@dataclass(frozen=True)
class ContractBundle:
    artifacts: Mapping[str, object]
    catalog: Mapping[str, object]
    providers: Mapping[str, object]

def load_contract_bundle(root: Path) -> ContractBundle: ...
def validate_contract_bundle(root: Path, bundle: ContractBundle) -> list[Finding]: ...
def validate_repository(root: Path, bundle: ContractBundle) -> list[Finding]: ...
def render_findings(findings: Sequence[Finding]) -> str: ...
```

- [ ] Write RED tests for duplicate YAML keys, unknown top-level keys,
  traversal/absolute paths, duplicate IDs, invalid cross-references, overlapping
  canonical ownership, invalid provider/model states, missing source URLs or
  checked time, default-ineligible fallback, and nondeterministic findings.
- [ ] Run
  `python3 -m unittest tests.validation.test_agent_governance_contract -v` and
  record the expected import/file failures.
- [ ] Implement and GREEN duplicate-key-safe YAML loading plus immutable
  `Finding`/`ContractBundle` models.
- [ ] Implement and GREEN safe repo-relative path and unknown-key validation.
- [ ] Implement and GREEN artifact ownership/overlap validation.
- [ ] Implement and GREEN catalog identity/cross-reference validation.
- [ ] Implement and GREEN provider/model status/source/fallback validation.
- [ ] Implement and GREEN deterministic sorting and value-free diagnostics.
- [ ] Implement the thin CLI with `--root`, `--mode contract|repository`,
  repository `--section catalog|providers|harness|all`; Task 1 activates only
  `--mode contract`. Provider render drift remains solely in the renderer's
  `--check` mode. Unknown or
  incompatible flag combinations fail closed.
- [ ] Run the focused tests and expect all tests to pass.
- [ ] Run
  `python3 scripts/validation/check-agent-governance-contract.py --mode contract`
  and expect
  `agent_governance_contract: PASS contracts=3 agents=14 functions=22 providers=3 failures=0`.
- [ ] Run `python3 -m py_compile` for both Python files and
  `git diff --check`.
- [ ] Run applicable generated owners, inspect the exact diff, update Task
  evidence, commit `feat(governance): add typed agent governance contracts`,
  and complete fresh specification and quality reviews.

### Task 2: Metadata, Authority, Root Shims, and Governance Normalization

**Files:**

- Modify `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as minimal executable entry
  shims with no generic lifecycle frontmatter.
- Modify `.agents/README.md`, `.claude/CLAUDE.md`, and `.codex/README.md` within
  existing README profile sections only.
- Modify `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml`
  to enumerate every governed Stage 00, root, provider, Hookify, and README
  artifact and its exact type/profile.
- Modify `docs/99.templates/support/document-metadata-profiles.yaml` only for
  the approved typed Stage 00 profiles and their exact validation envelope.
- Modify `docs/99.templates/support/frontmatter-contract.md` only to explain
  the boundary between the generic governance profile and registered Stage 00
  specializations.
- Modify `scripts/validation/check-document-metadata.py` so registered
  `agent-role`, `agent-function`, and provider-governance specializations are
  inferred through the Stage 00 artifact contract rather than rejected as
  mismatched generic governance documents. The focused validator owns the
  exact subtype keys/headings; the generic checker must not duplicate them.
- Modify `tests/validation/test_document_metadata.py` for those profiles.
- Modify exactly these non-role Stage 00 authority files:
  `README.md`, `subagent-protocol.md`, `harness-implementation-map.md`,
  `agents/README.md`, `memory/README.md`, the four files under `providers/`,
  `rules/agentic.md`, `rules/approval-boundaries.md`, `rules/bootstrap.md`,
  `rules/documentation-protocol.md`, and
  `rules/provider-capability-matrix.md`.
- Modify the 13 exact scope documents that currently carry duplicated `title`
  metadata: `scopes/{agentic,architecture,backend,common,entry,frontend,infra,
  meta,mobile,ops,product,qa,security}.md`; preserve each real `layer` value.
  The artifact contract inventories every other Stage 00/Hookify path as
  validate-only in Task 2. The remaining stale reference inside the canonical
  `hook-developer` role is fixed atomically with role generation in Task 3.
- Modify `.github/CODEOWNERS` to keep the valid repository principal
  `@buenhyden` and add missing root shims, `.agents/**`, `.claude/**`,
  `.codex/**`, `.gemini/**`, Stage 00 contracts, and coupled
  validator/renderer paths. Agent-role reviewers such as `rules-engineer`
  exist only in the typed path-authority contract, never as GitHub principals.
- Modify `tests/validation/test_agent_governance_contract.py`, the Task ledger,
  and progress memory.

**Root shim envelope:**

```markdown
# <PROVIDER ENTRY>

1. Load `docs/00.agent-governance/rules/bootstrap.md`.
2. Load the provider overlay in `docs/00.agent-governance/providers/<provider>.md`.
3. Load `docs/00.agent-governance/memory/README.md` and `memory/progress.md`.
```

The implementation uses the provider's real import syntax where one exists;
ordinary Markdown links and fenced literals are not counted as imports.

- [ ] Add RED tests for generic frontmatter on root shims, noncanonical key
  order, missing/extra type-specific keys, duplicate H1/title identity, copied
  policy in README profiles, non-executable imports, nonexistent Hookify local
  references, conflicting path owners, and missing mandatory reviewers.
- [ ] Run the focused governance and document-metadata tests and record the
  expected failures against current shims and metadata.
- [ ] Normalize metadata in deterministic inventory order without changing
  unrelated historical evidence; remove legacy keys and duplicated sections.
- [ ] Preserve artifact exceptions: root shims have no frontmatter; ordinary
  Stage 00 documents retain minimal `layer`; scope documents retain their real
  scope layer; progress retains `layer + status`; Hookify keeps its native
  schema; role/function subtype migration remains atomic with Task 3.
- [ ] Normalize the three root shims and rerun only root-shim fixtures.
- [ ] Normalize the three provider/compatibility README entry surfaces and
  rerun only README-profile fixtures.
- [ ] Normalize the four provider governance documents and rerun their
  metadata/authority fixtures.
- [ ] Normalize the five exact Stage 00 rule owners listed above and rerun
  ownership fixtures.
- [ ] Remove duplicate title metadata from `scopes/agentic.md`.
- [ ] Remove duplicate title metadata from `scopes/architecture.md`.
- [ ] Remove duplicate title metadata from `scopes/backend.md`.
- [ ] Remove duplicate title metadata from `scopes/common.md`.
- [ ] Remove duplicate title metadata from `scopes/entry.md`.
- [ ] Remove duplicate title metadata from `scopes/frontend.md`.
- [ ] Remove duplicate title metadata from `scopes/infra.md`.
- [ ] Remove duplicate title metadata from `scopes/meta.md`.
- [ ] Remove duplicate title metadata from `scopes/mobile.md`.
- [ ] Remove duplicate title metadata from `scopes/ops.md`.
- [ ] Remove duplicate title metadata from `scopes/product.md`.
- [ ] Remove duplicate title metadata from `scopes/qa.md`.
- [ ] Remove duplicate title metadata from `scopes/security.md` and rerun the
  complete scope-profile fixture.
- [ ] Reduce root/provider README surfaces to bootstrap, scope, structure,
  usage, generated-state, and related-document routing already permitted by
  their profiles.
- [ ] Resolve Stage 00 ownership conflicts using the contract path-authority
  matrix and distinguish implementation owner from independent reviewer.
- [ ] Replace literal/fenced imports and stale Hookify references with valid
  execution or explicit capability-gap language.
- [ ] Run focused tests; run explicit-base changed metadata validation against
  Task 1 HEAD; run traceability and documentation alignment; expect zero
  blocking failures.
- [ ] Run contract mode and `git diff --check`; regenerate index, coverage, and
  semantic inventory; commit
  `refactor(governance): normalize agent authority and metadata`; complete
  independent specification and quality reviews.

### Task 3: Agent/Function Catalog and Canonical Skill Source

**Files:**

- Modify `docs/00.agent-governance/contracts/agent-catalog.yaml`.
- Delete canonical and generated `style-enforcer` and `wiki-curator` role files
  from Stage 00, `.claude/agents/`, `.codex/agents/`, and `.agents/agents/`.
- Create `docs/00.agent-governance/agents/agents/eval-engineer.md` and its
  Task-3 compatibility/native projections using the then-current schemas.
- Modify all 22 files under
  `docs/00.agent-governance/agents/functions/*.md` to satisfy the canonical
  function profile with topic-specific procedures.
- Modify the remaining 13 canonical role files only to transfer retired
  responsibilities, remove overlapping ownership, and satisfy the role
  contract.
- Create `scripts/operations/provider_surface_renderer.py`.
- Create `tests/validation/test_provider_surface_renderer.py`.
- Modify `scripts/operations/sync-provider-surfaces.sh` to delegate to the
  renderer and never read provider skill bodies as policy input.
- Delete the entire obsolete `.codex/skills/**` tree. Codex discovers
  repository skills through shared `.agents/skills/<id>/SKILL.md`.
- Replace every lowercase `.claude/skills/*/skill.md` and
  `.agents/skills/*/skill.md` with generated uppercase `SKILL.md` entrypoints.
  Claude reads `.claude/skills/**/SKILL.md`; Codex and Gemini may consume the
  shared `.agents/skills/**/SKILL.md` projection.
- Modify `docs/00.agent-governance/README.md`,
  `docs/00.agent-governance/agents/README.md`,
  `docs/00.agent-governance/subagent-protocol.md`,
  `docs/00.agent-governance/providers/codex.md`,
  `docs/00.agent-governance/rules/workflows.md`,
  `docs/00.agent-governance/scopes/docs.md`,
  `docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md`,
  `docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md`,
  `scripts/README.md`, `scripts/hooks/agent-event-hook.sh`,
  `scripts/knowledge/generate-llm-wiki-index.sh`,
  `scripts/knowledge/generate-llm-wiki-coverage.sh`,
  `tests/validation/test_agent_governance_contract.py`, Task evidence, and
  progress memory.
- Modify `scripts/validation/check-repo-contracts.sh` in the same task: remove
  the obsolete mixed runtime-catalog block plus its
  catalog/function/shared-skill/LLM-Wiki-owner assertions,
  call the focused validator with `--mode repository --section catalog`, and
  leave separable still-current provider/harness blocks in place until Tasks 4
  and 5. Because the mixed block also contains old hardcoded model assertions,
  record their bounded removal in Task evidence; Task 3 may not otherwise
  change provider models, and Task 4 must immediately activate the typed
  provider section.

**Renderer interface:**

```python
def load_catalog(root: Path) -> Catalog: ...
def render_agent(provider: str, agent: AgentRecord) -> bytes: ...
def render_function(provider: str, function: FunctionRecord) -> bytes: ...
def expected_projection(root: Path, provider: str) -> Mapping[Path, bytes]: ...
def find_managed_stale_files(root: Path, expected: Mapping[Path, bytes]) -> set[Path]: ...
def find_projection_drift(root: Path, provider: str) -> list[Finding]: ...
def write_projection(root: Path, provider: str) -> None: ...
```

The catalog fixes the tier membership exactly:

- supervisor: `workflow-supervisor`;
- implementation/operations: `ci-cd-engineer`, `doc-writer`,
  `hook-developer`, `incident-responder`, `infra-implementer`, `qa-engineer`,
  and `skill-creator`;
- independent review/evaluation: `code-reviewer`, `drift-detector`,
  `eval-engineer`, `iac-reviewer`, `rules-engineer`, and `security-auditor`.

Each role/function line below is a separate 2–5 minute authored micro-cycle:
enable the single-ID RED fixture, edit only that canonical file, rerun the
focused fixture, and inspect its diff before moving to the next ID.

- [ ] Normalize role `workflow-supervisor`.
- [ ] Normalize role `ci-cd-engineer`.
- [ ] Normalize role `doc-writer`.
- [ ] Normalize role `hook-developer`.
- [ ] Normalize role `incident-responder`.
- [ ] Normalize role `infra-implementer`.
- [ ] Normalize role `qa-engineer`.
- [ ] Normalize role `skill-creator`.
- [ ] Normalize role `code-reviewer`.
- [ ] Normalize role `drift-detector`.
- [ ] Create and normalize role `eval-engineer`.
- [ ] Normalize role `iac-reviewer`.
- [ ] Normalize role `rules-engineer`.
- [ ] Normalize role `security-auditor`.
- [ ] Normalize function `adr-writing`.
- [ ] Normalize function `ci-cd-patterns`.
- [ ] Normalize function `code-review-dimensions`.
- [ ] Normalize function `code-reviewer`.
- [ ] Replace stub and normalize function `compose-stack-agent`.
- [ ] Normalize function `container-threat-modeling`.
- [ ] Normalize function `deployment-pipeline-design`.
- [ ] Normalize function `docker-compose-patterns`.
- [ ] Normalize function `e2e-testing`.
- [ ] Replace stub and normalize function `execution-plan-agent`.
- [ ] Normalize function `incident-response`.
- [ ] Normalize function `infra-cross-validate`.
- [ ] Normalize function `infra-validate`.
- [ ] Replace stub and normalize function `knowledge-map-agent`.
- [ ] Replace stub and normalize function `ops-runbook-agent`.
- [ ] Replace stub and normalize function `policy-gate-agent`.
- [ ] Replace stub and normalize function `requirements-to-design-agent`.
- [ ] Normalize function `security-audit`.
- [ ] Normalize function `style-validation`.
- [ ] Replace stub and normalize function `task-breakdown-agent`.
- [ ] Normalize function `test-automator`.
- [ ] Normalize function `workspace-audit-revalidation`.

- [ ] Write RED tests that assert exactly 14 unique agents, exactly 22 unique
  functions, one supervisor, seven implementation/operations roles, six
  review/eval roles, no retired IDs/references, complete required sections,
  unique owners, `iac-reviewer`/`drift-detector` separation, and the presence of
  `eval-engineer`. Also assert that no lowercase `skill.md` or `.codex/skills`
  path remains.
- [ ] Add renderer RED tests proving Stage 00-only inputs, deterministic byte
  output, explicit write mode, read-only `--check`, stale-file deletion, and
  idempotence. Mutating `.claude/skills` alone must not change expected output.
- [ ] Run focused tests and record the expected current-catalog and missing
  renderer failures.
- [ ] Implement the catalog role-transfer ledger: formatting/style to
  `qa-engineer` plus `style-validation`; knowledge/index freshness to
  `doc-writer` plus `knowledge-map-agent`; representative evaluation to
  `eval-engineer`.
- [ ] Author topic-specific content for every canonical role/function. Do not
  copy template instructions or provider-local prompts verbatim.
- [ ] Implement deterministic rendering and update the shell wrapper as a thin
  compatibility entry point with `--check` default and explicit `--write`.
  Reject unknown flags. Limit stale deletion to the managed manifest/origin
  marker plus the enumerated one-time legacy migration set.
- [ ] Run renderer write once, inspect exact additions/deletions, then run
  renderer check twice; expect zero drift and no second-write diff.
- [ ] Run catalog tests, changed metadata, traceability, repository contracts,
  and `git diff --check`. Repository contracts must pass through the new
  catalog section while the still-current provider checks remain GREEN; commit
  `refactor(agents): converge role and function catalogs`; complete independent
  reviews.

### Task 4: Provider-native Adapters and Model Policy

**Files:**

- Modify `docs/00.agent-governance/contracts/provider-models.yaml`.
- Modify `scripts/operations/provider_surface_renderer.py` and its focused
  tests for provider-native schemas.
- Create `tests/validation/test_provider_native_surfaces.py`.
- Regenerate `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`,
  `.claude/settings.json`, `.claude/hooks/*.sh`, and `.claude/CLAUDE.md`.
- Regenerate `.codex/agents/*.toml`, `.codex/hooks.json`, and `.codex/README.md`;
  keep `.codex/skills/**` absent and consume shared `.agents/skills/**/SKILL.md`.
- Create `.gemini/README.md`, `.gemini/agents/*.md`,
  `.gemini/settings.json`, and `.gemini/hooks/agent-event-hook.sh` as the only
  thin native event-name/schema adapter admitted by the semantic-event
  contract. Gemini uses the shared `.agents/skills/**/SKILL.md` alias unless a
  future contract justifies a distinct native skill projection.
- Regenerate `.agents/agents/*.md`, `.agents/skills/*/SKILL.md`,
  `.agents/rules/workspace.md`, `.agents/workflows/documentation.md`, and
  `.agents/README.md` as compatibility projections.
- Modify `docs/00.agent-governance/providers/{claude,codex,gemini,agents-md}.md`,
  `docs/00.agent-governance/rules/provider-capability-matrix.md`, root shims,
  `scripts/validation/report-provider-hook-parity.sh`, its generated hook
  parity matrix, Task evidence, and progress memory.
- Modify `scripts/validation/check-repo-contracts.sh` again: remove the old
  hardcoded model/native-provider/`.agents-as-Gemini` blocks, activate
  `--mode repository --section providers`, and retain only the harness/QA
  blocks scheduled for Task 5.

**Provider/model record:**

```yaml
models:
  - provider: codex
    model_id: gpt-5.6
    provider_status: stable
    repository_default_eligible: true
    entitlement: needs_revalidation
    runtime_acceptance: needs_revalidation
    reasoning_controls: [medium, high, xhigh]
    work_profiles: [supervision, complex-implementation, precision-review]
    fallback: gpt-5.6-terra
    checked_at: 2026-07-15T10:00:00+09:00
    source_url: https://learn.chatgpt.com/docs/models
```

- [ ] Add RED tests for Claude supported frontmatter, Codex required
  `name`/`description`/`developer_instructions`, Gemini native
  `name`/`description`/`kind` plus tool/turn/timeout controls, compatibility
  origin markers, strict-schema forbidden keys, and all exact generated paths.
- [ ] Add RED tests for stable/preview/deprecated separation, dated official
  source, entitlement/runtime distinction, no `latest`, eligible defaults,
  reasoning/thinking control validation, fallback compatibility, and the three
  approved work profiles.
- [ ] Run focused tests and record current schema, missing `.gemini`, and model
  drift failures.
- [ ] Implement and GREEN the Claude agent/skill Markdown serializer only.
- [ ] Implement and GREEN the Codex agent TOML serializer only.
- [ ] Implement and GREEN the Gemini agent Markdown serializer only.
- [ ] Implement and GREEN the Gemini settings/hook JSON-plus-shell projection
  only.
- [ ] Implement and GREEN the `.agents` compatibility/shared-skill serializer
  only. Keep canonical-only metadata in Stage 00.
- [ ] Implement the approved defaults: Claude Opus 4.8/Sonnet 5/Haiku 4.5;
  Codex GPT-5.6 and GPT-5.6 Terra with pinned reasoning; Gemini 3.5 Flash and
  3.1 Flash-Lite. Keep Fable, Spark, Mythos/invitation-only, and Gemini Pro
  preview catalog-only according to observed status.
- [ ] Map provider hook names to shared semantic events and mark unsupported
  native events as gaps. Specifically remove unsupported Codex `SessionEnd`
  and ignored matchers; map Claude/Codex `PreCompact` and Gemini `PreCompress`
  to the shared pre-compaction event while preserving Gemini's advisory-only
  semantics; distinguish Gemini millisecond hook timeouts from Claude/Codex
  seconds; and add recursion protection plus least-privilege tools.
- [ ] Enforce read-only sandboxes/tool sets for reviewers, workspace-write only
  for approved implementers, and no wildcard tools for Gemini reviewers.
- [ ] Run explicit renderer write; validate Markdown/YAML, JSON, and TOML with
  local parsers; run renderer check twice and expect no drift.
- [ ] Run focused tests and blocking contract repository sections,
  changed metadata, traceability, repository contracts, and diff hygiene.
  Both catalog and provider sections must now be blocking and GREEN; no old
  model or obsolete provider-path assertion may remain active;
  commit `feat(providers): generate native agent adapters`; complete
  independent reviews.

### Task 5: Harness Loops, Semantic Evaluation, Local QA, and CI

**Files:**

- Modify semantic-event and adoption sections in
  `docs/00.agent-governance/contracts/provider-models.yaml` and role/eval
  sections in `agent-catalog.yaml`.
- Modify `docs/00.agent-governance/harness-implementation-map.md`,
  `subagent-protocol.md`, `rules/approval-boundaries.md`,
  `rules/environment-constraints.md`, `rules/quality-standards.md`,
  `rules/task-checklists.md`, `rules/postflight-checklist.md`,
  `rules/workflows.md`, `rules/provider-capability-matrix.md`,
  `rules/output-style.md`, and `scopes/qa.md`.
- Modify `scripts/validation/agent_governance_contract.py` and activate
  full repository enforcement in
  `scripts/validation/check-agent-governance-contract.py`.
- Modify `scripts/validation/check-repo-contracts.sh` to remove only the
  remaining root-shim/hook/harness inline duplication and call the focused CLI
  with `--mode repository --section all`. Catalog and provider delegation from
  Tasks 3 and 4 must remain intact.
- Modify `scripts/validation/run-agent-output-eval-fixtures.sh` and
  `docs/90.references/data/governance/agent-output-eval-fixtures.md`.
- Create `scripts/validation/agent_output_eval.py` and
  `tests/validation/test_agent_output_eval_fixtures.py`; keep the shell script
  as the stable CLI wrapper.
- Modify `scripts/validation/recommend-qa-gates.sh`,
  `scripts/validation/run-local-qa-gates.sh`, `.pre-commit-config.yaml`, and
  existing tests; create `tests/validation/test_agent_governance_ci_routing.py`
  for isolated selector/workflow tests.
- Modify `scripts/hooks/agent-event-hook.sh`,
  `scripts/hooks/post-tool-validate.sh`,
  `scripts/validation/report-provider-hook-parity.sh`,
  `scripts/validation/validate-harness.sh`, `.github/CODEOWNERS`,
  `.github/labeler.yml`, and `.github/PULL_REQUEST_TEMPLATE.md` for the same
  contract-owned paths and evidence classes.
- Modify `.github/workflows/ci-quality.yml` only in the existing
  `repo-contracts` and agent-output eval jobs and coupled path filters.
- Modify Task evidence and progress memory.

**Semantic event contract:**

```yaml
semantic_events:
  - event_id: context-bootstrap
    max_attempts: 1
    stop_condition: bootstrap-contract-pass
    on_failure: escalate
  - event_id: bounded-implementation-loop
    max_attempts: 2
    stop_condition: focused-checks-pass
    on_failure: narrow_then_escalate
  - event_id: independent-review-loop
    max_attempts: 2
    stop_condition: critical_and_important_zero
    on_failure: escalate
  - event_id: approved-all-files-gate
    max_attempts: 1
    stop_condition: controlled-wrapper-pass
    on_failure: record_and_stop
```

- [ ] Write RED tests for semantic event ownership, independent reviewer
  inequality, positive retry bounds, stop/escalation rules, least-privilege
  tool sets, sanitized evidence fields, capability/adoption/runtime depth, and
  every provider event mapping.
- [ ] Add representative RED fixtures for correct role routing, retired-role
  rejection, boundary escalation, hook denial, bounded retry, completion
  evidence, adapter rendering, model fallback, and evaluation calibration.
  Retain the three existing fixture IDs and add `AOE-ROUTING-001`,
  `AOE-ROLE-001`, `AOE-CLOSURE-001`, `AOE-HOOK-001`, and
  `AOE-ADAPTER-001`; the target is eight fixtures and ten deterministic
  positive/negative regression cases.
- [ ] Add selector RED tests proving that any change under root shims,
  `.agents/**`, `.claude/**`, `.codex/**`, `.gemini/**`, Stage 00, the three
  contracts, renderer, validator, fixture runner, or focused tests selects the
  coupled repository-contract and semantic-eval gates.
- [ ] Run focused tests/fixtures and record the expected missing enforcement and
  selector failures.
- [ ] Implement semantic loop validation and replace the inline shell checks
  with the focused repository-mode CLI while preserving aggregate pass/fail
  behavior.
- [ ] Extend existing semantic fixtures with deterministic scorers, explicit
  thresholds, calibration metadata, and value-free failure output.
- [ ] Change shared prompt/function routing to canonical Stage 00 functions,
  remove the non-runtime `docker ps` action from SessionStart, and run provider
  surface synchronization only through explicit `--check` in validation.
- [ ] Update local selector and existing CI jobs. Preserve read-only
  permissions, SHA-pinned actions, no secrets in command lines, and no
  deployment or remote mutation.
- [ ] Require the existing eval job to pass all eight fixture catalog entries
  and ten semantic regressions, with markers
  `fixtures_check=pass` and `regressions_check=pass`; do not add a new required
  job or make a network model call.
- [ ] Run unit tests, semantic fixtures, selector tests, renderer check,
  repository contracts, actionlint/yamllint when available, changed metadata,
  traceability, documentation alignment, and diff hygiene.
- [ ] Run Graphify, corroborate advisory findings, regenerate applicable
  security/audit/index/inventory owners, commit
  `feat(harness): enforce agent loops and semantic gates`, and complete
  independent reviews.

### Task 6: Reference, Audit, Evidence, and Closure

**Files:**

- Modify dated facts in that research pack's `README.md` and
  `{agent-instructions-vibe-coding,agent-model-selection,ai-agent-catalogs,
  harness-engineering,loop-engineering,provider-implementation-comparison,
  provider-model-landscape,quality-ci-formatting,security-governance,
  workspace-baseline}.md`
  only where Spec 132 implementation or 2026-07-15 official sources change the
  canonical conclusion.
- Modify observed implementation state in the canonical July 5 audit pack,
  especially `README.md`, `implementation-overview.md`,
  `agent-instructions-catalog-vibe-models.md`,
  `harness-engineering-implementation.md`,
  `loop-engineering-implementation.md`,
  `provider-harness-loop-implementation.md`,
  `sdlc-quality-formatting-implementation.md`,
  `security-framework-maturity.md`, and
  `workspace-rules-environment-implementation.md`.
- Review `automation-candidates.md` and
  `frontmatter-template-readme-implementation.md`; review but do not churn
  `sdlc-document-contracts-implementation.md` or
  `compose-infrastructure-operations-readiness.md` absent a factual change.
- Do not revive the superseded July 7 pack or copy its counts as current.
- Modify Spec 132, this Plan, the Task ledger, Stage 03/04 indexes,
  `docs/00.agent-governance/memory/progress.md`, generated Stage 90 owners, and
  any cross-links made stale by the retired roles or new `.gemini/` paths.

- [ ] Run a retired-reference search for `style-enforcer`, `wiki-curator`,
  nonexistent Hookify local paths, `.agents`-as-Gemini-native claims, stale
  model IDs/defaults, literal imports, and provider-local source-of-truth
  language. Classify historical mentions separately from current claims.
- [ ] Revalidate each changed research statement against the dated official
  sources already cited by Spec 132. Record source date and distinguish
  inference from provider fact.
- [ ] Re-run the canonical audit generators and validators. Recalculate the
  161-criterion distribution from the observed matrix; do not choose counts to
  match the design. Promote a criterion only when the matrix evidence and
  validation depth justify it.
- [ ] Preserve hard audit invariants: 11 criterion reports; 161 unique IDs;
  the existing ten-column schema; only `Implemented`, `Partial`, `Missing`,
  `Not Applicable`, or `Needs Revalidation`; and criterion-family counts HAR
  7, LOOP 6, PIC 17, WRE 10, AIV 16, AIC 7, AMS 7, AUT 11, SDLC 22, DML 14,
  QAF 16, CIO 14, and SEC 14. Do not promote runtime acceptance, entitlement,
  remote CI enforcement, CD, or actual model availability from tracked
  definitions alone.
- [ ] Update the Task Work Log, Verification Evidence, Review Evidence, Commit
  Ledger, Deferred Items, and pre-wrapper branch-range evidence with sanitized
  results. Leave wrapper fields `not_run` and lifecycle statuses `active`.
- [ ] Run the full verification ladder below and resolve all blocking failures.
- [ ] Run `graphify update .` when available, inspect the new report, and
  corroborate advisory results against tracked Stage 00/03/04/90 and executable
  owners. Restore unrelated generated graph noise if it is not an intended
  artifact.
- [ ] Commit `docs(governance): reconcile agent harness evidence`; obtain fresh
  Task-6 specification and quality PASS, fix/re-review all blocking findings,
  and commit any remediation. The worktree must then be clean.
- [ ] From that clean linked worktree, obtain one successful final controlled
  wrapper execution with the
  already tracked Task ledger and explicit allowed prefixes. Never edit Task
  evidence before this invocation or the wrapper's dirty-worktree guard will
  stop execution.
- [ ] After the wrapper returns, record its command, exit status, snapshot
  result, observed path sets, and disposition in the Task; never store raw
  logs. Commit this evidence as
  `docs(governance): record controlled agent QA evidence` and restore a clean
  worktree.
- [ ] Obtain separate whole-branch specification and quality PASS over
  `6cde68dc..EVIDENCE_HEAD`; fix and re-review all Critical/Important findings,
  and keep the worktree clean.
- [ ] Transition Spec, Plan, and Task to `completed` only after all acceptance
  rows, commits, wrapper evidence, generated freshness, and whole-branch
  reviews are current. Regenerate the semantic inventory, LLM Wiki index, and
  coverage after the status/index edits; rerun changed metadata, traceability,
  repository contracts, and every generated check before committing
  `docs(execution): close agent governance convergence`.
- [ ] Obtain fresh post-closure specification and quality PASS for the closure
  commit and exact final range. Rerun changed metadata, traceability,
  repository contracts, generated freshness, and `git diff --check` against
  the committed closure. Any fix reopens the statuses until both reviewers
  re-approve. Record candidate-range and evidence-only closure-delta verdicts
  separately to avoid self-referential review claims.
- [ ] Use superpowers:finishing-a-development-branch to present merge options.
  Do not merge, push, create a PR, or delete the worktree without the user's
  separate instruction.

## Verification Plan

### Per-task focused gates

```bash
python3 -m unittest tests.validation.test_agent_governance_contract -v
python3 -m unittest tests.validation.test_document_metadata -q
python3 scripts/validation/check-agent-governance-contract.py --mode contract
python3 scripts/validation/check-agent-governance-contract.py --mode repository
python3 -m unittest tests.validation.test_provider_surface_renderer -v
python3 -m unittest tests.validation.test_provider_native_surfaces -v
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions
git diff --check
```

Expected: focused test suites pass; contract and repository modes report zero
failures; provider projection reports zero drift; semantic fixtures meet every
declared threshold; diff hygiene reports no output.

### Provider batch gates

```bash
python3 -m json.tool .claude/settings.json
python3 -m json.tool .codex/hooks.json
python3 -m json.tool .gemini/settings.json
bash -n scripts/operations/sync-provider-surfaces.sh
bash -n .claude/hooks/session-start.sh
bash -n .gemini/hooks/agent-event-hook.sh
```

The focused Python tests parse every generated Codex TOML and provider
frontmatter using strict contract schemas, so no separate ad hoc parser becomes
an authority. Expected: parsers and shell syntax exit 0.

### Repository and documentation gates

```bash
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --base-ref 6cde68dc
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-harness.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

Expected: changed metadata has zero violations and no undocumented transition
override; traceability/alignment/harness/repository gates report zero failures;
all generated owners are fresh.

### Workflow and local QA gates

```bash
bash -n scripts/validation/recommend-qa-gates.sh
bash -n scripts/validation/run-local-qa-gates.sh
actionlint .github/workflows/ci-quality.yml
yamllint .github/workflows/ci-quality.yml
bash scripts/validation/run-local-qa-gates.sh --harness
```

Expected: syntax and workflow linters exit 0; local routing selects the agent
governance, semantic fixture, metadata, repository contract, and generated
freshness gates and they pass.

### Controlled all-files gate

From a clean linked worktree, confirm the wrapper help has not changed and run:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/04.execution/tasks/2026-07-15-agent-governance-harness-convergence.md \
  --allow-prefix AGENTS.md \
  --allow-prefix CLAUDE.md \
  --allow-prefix GEMINI.md \
  --allow-prefix .agents \
  --allow-prefix .claude \
  --allow-prefix .codex \
  --allow-prefix .gemini \
  --allow-prefix .github/CODEOWNERS \
  --allow-prefix .github/PULL_REQUEST_TEMPLATE.md \
  --allow-prefix .github/labeler.yml \
  --allow-prefix .github/workflows/ci-quality.yml \
  --allow-prefix .pre-commit-config.yaml \
  --allow-prefix docs/00.agent-governance \
  --allow-prefix docs/03.specs/132-agent-governance-harness-convergence \
  --allow-prefix docs/03.specs/README.md \
  --allow-prefix docs/04.execution/plans/2026-07-15-agent-governance-harness-convergence.md \
  --allow-prefix docs/04.execution/plans/README.md \
  --allow-prefix docs/04.execution/tasks/2026-07-15-agent-governance-harness-convergence.md \
  --allow-prefix docs/04.execution/tasks/README.md \
  --allow-prefix docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md \
  --allow-prefix docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md \
  --allow-prefix docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack \
  --allow-prefix docs/90.references/research/2026-07-05-agentic-research-pack-refresh \
  --allow-prefix docs/90.references/data/governance/agent-output-eval-fixtures.md \
  --allow-prefix docs/90.references/data/governance/audit-implementation-matrix.md \
  --allow-prefix docs/90.references/data/governance/document-corpus-lifecycle \
  --allow-prefix docs/90.references/data/governance/provider-hook-parity-matrix.md \
  --allow-prefix docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md \
  --allow-prefix docs/90.references/data/security/security-automation-readiness.md \
  --allow-prefix docs/90.references/llm-wiki/llm-wiki-index.md \
  --allow-prefix docs/99.templates/support/document-metadata-profiles.yaml \
  --allow-prefix docs/99.templates/support/frontmatter-contract.md \
  --allow-prefix scripts/README.md \
  --allow-prefix scripts/hooks/agent-event-hook.sh \
  --allow-prefix scripts/hooks/post-tool-validate.sh \
  --allow-prefix scripts/knowledge/generate-llm-wiki-index.sh \
  --allow-prefix scripts/knowledge/generate-llm-wiki-coverage.sh \
  --allow-prefix scripts/operations/provider_surface_renderer.py \
  --allow-prefix scripts/operations/sync-provider-surfaces.sh \
  --allow-prefix scripts/validation/agent_governance_contract.py \
  --allow-prefix scripts/validation/agent_output_eval.py \
  --allow-prefix scripts/validation/check-agent-governance-contract.py \
  --allow-prefix scripts/validation/check-document-metadata.py \
  --allow-prefix scripts/validation/check-repo-contracts.sh \
  --allow-prefix scripts/validation/recommend-qa-gates.sh \
  --allow-prefix scripts/validation/report-provider-hook-parity.sh \
  --allow-prefix scripts/validation/run-agent-output-eval-fixtures.sh \
  --allow-prefix scripts/validation/run-local-qa-gates.sh \
  --allow-prefix scripts/validation/validate-harness.sh \
  --allow-prefix tests/validation/test_agent_governance_contract.py \
  --allow-prefix tests/validation/test_agent_governance_ci_routing.py \
  --allow-prefix tests/validation/test_agent_output_eval_fixtures.py \
  --allow-prefix tests/validation/test_document_metadata.py \
  --allow-prefix tests/validation/test_provider_native_surfaces.py \
  --allow-prefix tests/validation/test_provider_surface_renderer.py
```

Expected markers are `hook_result=passed hook_exit=0`,
`snapshot_result=passed`, and `unexpected_count=0`. If formatter fallout is
inside the allowlist, inspect and commit it, clean the worktree, and rerun. Exit
20 stops closure without reset, checkout, or cleanup. Record every failed or
mutating attempt; only one clean successful execution is the final gate.

### Final Git and review gates

```bash
git diff --check 6cde68dc..HEAD
git log --oneline 6cde68dc..HEAD
git status --short
```

Expected: no diff hygiene failures; each logical task has an independently
reviewable Conventional Commit; the final worktree is clean; exact whole-branch
specification and quality reviews both report Critical 0 and Important 0.

## Risks and Rollback

| Risk | Mitigation | Rollback |
| --- | --- | --- |
| Provider documentation or model status changes during execution | Keep `checked_at`, official URL, status, entitlement, and runtime acceptance separate; revalidate only affected entries. | Revert the model-registry task and regenerate prior adapters. |
| Strict provider schemas reject canonical-only metadata | Validate native schemas and keep local ownership fields in Stage 00 only. | Revert Task 4 provider projection without reverting canonical role content. |
| Deleting roles leaves stale references or unowned work | Transfer responsibility in the same catalog task and block on retired-reference scans. | Revert the complete Task 3 range, including generated additions/deletions. |
| Generator deletes user-authored provider files | Limit output to exact contract inventory and test stale-file deletion only inside owned paths. | Restore the Task 3/4 commit range; rerun the prior renderer revision. |
| README normalization accidentally becomes policy migration | Limit edits to existing profile sections and validate copied-policy markers. | Revert the affected metadata/shim commit only. |
| Existing CI behavior changes unintentionally | Reuse existing jobs, permissions, and action pins; add focused selector/workflow tests. | Revert Task 5 and retain manual focused validators. |
| Audit counts are promoted by intention rather than evidence | Derive counts from the canonical matrix after all checks and keep runtime gaps explicit. | Revert only the reconciliation commit and regenerate from the previous matrix. |
| Full all-files QA mutates files or exposes diagnostics | Use only the controlled wrapper in a clean worktree and record sanitized summaries. | Stop, restore only wrapper-owned generated changes, document failure, and do not close. |
| Graphify produces unrelated graph noise | Treat it as advisory and corroborate with tracked sources. | Restore unrelated Graphify outputs and record the bounded advisory result. |

Each task is reverted in reverse dependency order with ordinary `git revert` or
an equivalent non-history-rewriting logical rollback. Never use `git reset
--hard`, delete user work, or combine rollback with runtime/provider-global
mutation.

## Approval Gates

- The written Spec 132 and this staged six-task architecture are approved.
- Protected Stage 00, provider adapter, QA, CI, contract, governance, and
  canonical audit edits are authorized within this Plan.
- Runtime Compose/infrastructure/deployment, credentials, provider-global
  configuration, remote GitHub mutation, push, PR, merge, and worktree deletion
  remain outside approval.
- Any newly discovered need for those actions pauses implementation and
  requires separate user approval and, where appropriate, a follow-up Spec.

## Completion Criteria

- VAL-132-001 through VAL-132-008 are backed by exact commands and observed
  pass evidence in the Task ledger.
- Three contracts are the sole machine owners; the focused validator reports
  zero contract and repository failures, and the renderer reports zero
  projection drift.
- The catalog has exactly 14 roles and 22 complete functions; retired roles,
  legacy references, and provider-local policy ownership are absent from
  current surfaces.
- Claude, Codex, Gemini CLI, and compatibility adapters parse under their
  native contracts and regenerate idempotently.
- Model policy is dated, pinned, status-aware, fallback-safe, and honest about
  entitlement/runtime acceptance.
- Semantic harness loops and representative eval fixtures enforce bounded
  retry, independent review, least privilege, stop/escalation, and sanitized
  evidence.
- Existing local QA, repo-contract, and CI job families cover every coupled
  root/provider/Stage 00 change without deployment capability.
- Canonical research/audit, generated inventories, Stage 04 evidence, progress
  memory, and cross-links reflect observed final state.
- Every logical task and material remediation is committed and independently
  reviewed; whole-branch Spec and Quality reviews have Critical 0/Important 0.
- The approved controlled all-files wrapper passes, Graphify is refreshed or
  explicitly unavailable, and the final worktree is clean.
- Spec, Plan, and Task statuses are `completed`; no merge/push/PR/worktree
  deletion occurs until separately instructed.

## Related Documents

- [Spec 132](../../03.specs/132-agent-governance-harness-convergence/spec.md)
- [Execution Task](../tasks/2026-07-15-agent-governance-harness-convergence.md)
- [Stage 00 Governance](../../00.agent-governance/README.md)
- [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- [Canonical Agentic Audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Canonical Agentic Research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Plan Template](../../99.templates/templates/sdlc/plan.template.md)
- [Task Template](../../99.templates/templates/sdlc/task.template.md)
