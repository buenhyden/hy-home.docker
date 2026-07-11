---
status: completed
artifact_id: plan:2026-07-11-agentic-engineering-audit-remediation
artifact_type: plan
parent_ids:
  - spec:123-agentic-engineering-audit-remediation
---

<!-- Target: docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md -->

# Agentic Engineering Audit and Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate the canonical agentic research and implementation-audit packs, measure repository implementation depth exhaustively, and apply approved typed-metadata, QA-wrapper, provider, validator, and CI governance improvements without mutating runtime infrastructure.

**Architecture:** Extend the existing 2026-07-05 research and audit packs in place, using source-backed criteria and tracked repository evidence. Introduce typed metadata through a profile-driven Python validator and advisory-first rollout, then add a controlled full-repository pre-commit wrapper and synchronized provider/CI contracts. Route Compose, infrastructure, security-runtime, and deployment findings into four independent follow-up specs/plans rather than changing runtime state.

**Tech Stack:** Markdown, YAML, Python 3.12, PyYAML 6.x, Bash, pre-commit 3.7+, GitHub Actions, Claude/Codex/Gemini provider adapters, Docker Compose validators, Stage 03/04/90/99 templates, Git, and Superpowers subagent review packages.

## Global Constraints

- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` remains the only current canonical agentic research pack.
- `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/` becomes the only current canonical agentic implementation audit.
- Merge verified unique 2026-07-07 audit content before converting the 2026-07-07 pack to mapping-only `superseded` records.
- Preserve the 2026-07-03 and 2026-07-04 audit packs as dated historical evidence; their corpus counts are not current implementation facts.
- Keep the official Claude, OpenAI/Codex, and Gemini model catalog fixed at 2026-07-10 10:00 KST. Later announcements may be noted only as later context.
- Use primary external sources and current tracked workspace evidence. Graphify is advisory and must be corroborated against tracked source, Stage 00, and stage documents.
- Every audit criterion records implementation state, enforcement depth, disposition, canonical owner, automation impact, verification, and confidence.
- Typed metadata rolls out advisory-first. Migrate the approved agentic active chain and changed/new documents before considering repository-wide blocking enforcement.
- Direct manual `pre-commit run` remains prohibited. AI agents execute `pre-commit run --all-files` only through the controlled wrapper in an isolated worktree with Stage 04 evidence.
- Do not change model policy without a separate exact provider, model ID, role, reasoning control, adapter, and validator approval.
- Do not start, stop, deploy, or mutate Docker Compose services, infrastructure runtime, secrets, credentials, remote GitHub settings, or branch protection.
- Every implementation task uses a fresh implementer, a separate spec-compliance reviewer, a separate quality/security reviewer, and a clean logical commit. Review fixes use a separate commit.
- Non-README Stage 03, Stage 04, and Stage 90 documents remain English.

---

## Overview

This plan implements
[Spec 123](../../03.specs/123-agentic-engineering-audit-remediation/spec.md).
The umbrella specification contains five ordered workstreams. This plan keeps
one Stage 04 plan for the umbrella spec, while each numbered task below is a
self-contained deliverable with its own tests, commit, and two-stage review.

The future task-evidence document will use the matching path
`docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md`.
It is created only after this plan is approved.

## Context

The research lifecycle is already canonicalized, but the implementation-audit
lifecycle is not. The 2026-07-05 and 2026-07-07 audit packs are both active,
and the latter cites a superseded research source. Existing audit reports also
predate the latest provider-model research and do not provide exhaustive
semantic frontmatter assessment, explicit numbering/status-transition checks,
controlled agent pre-commit execution, or complete vibe-coding and
agent-instruction criteria.

Repository validators currently prove strong syntax, template, link, Compose,
hardening, and provider-name parity. They do not prove valid lifecycle
transitions, stable cross-stage artifact identity, semantic parent coverage,
model availability, or closed-loop agent-output quality. This plan preserves
those distinctions rather than inflating maturity claims.

## Goals & In-Scope

- **Goals**:
  - Revalidate and integrate research for every requested category.
  - Produce one current, category-complete implementation audit with explicit
    retain/fix/improve/add/remove dispositions.
  - Audit frontmatter keys and values for every applicable document through a
    reproducible inventory.
  - Introduce typed metadata and lifecycle transition rules incrementally.
  - Permit full-repository pre-commit execution only through an auditable,
    scope-aware wrapper.
  - Synchronize Stage 00/99, provider adapters, validators, pre-push, and CI
    behavior for approved development-harness changes.
  - Create independent follow-up specs/plans for runtime gaps.
- **In Scope**:
  - Spec 123 and its Stage 04 plan/task lifecycle.
  - Canonical Stage 90 research and audit packs and required indexes/data.
  - Stage 00 documentation, Stage 99 support/templates, provider adapters,
    validation scripts/tests, `.pre-commit-config.yaml`, and `ci-quality.yml`.
  - Documentation-only follow-up specs/plans for Compose, infrastructure,
    security supply chain, and deployment/release engineering.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Replacing evidence rows with a single maturity score.
  - Forcing one numeric identifier format across all SDLC stages.
  - Importing external agent identities wholesale.
  - Treating provider marketing or model names as proof of parity.
  - Making all historical documents satisfy typed metadata immediately.
- **Out of Scope**:
  - Runtime Compose, infrastructure, deployment, secret, credential, remote
    GitHub, and branch-protection mutations.
  - Exact model-policy value changes without a later explicit approval.
  - Raw web captures, raw logs, environment dumps, shell history, or secret
    values in tracked evidence.

## File Structure

### Research and Audit

| Path | Responsibility |
| --- | --- |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md` | New source-backed metadata, artifact identity, numbering, and lifecycle criteria. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md` | New instruction anatomy, generated-code accountability, and vibe-coding criteria. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/*.md` | Existing responsibility-focused research updated in place. |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md` | SDLC flow, document roles, numbering, transitions, and traceability audit. |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md` | Frontmatter, template, and README profile audit. |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md` | Compose, infrastructure, and operations-readiness audit. |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md` | Instruction, catalog, vibe-coding, `agency-agents`, and model-routing audit. |
| `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md` | Generated exhaustive per-document metadata inventory. |
| `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/*.md` | Mapping-only superseded records after verified merge. |

### Metadata and Harness Automation

| Path | Responsibility |
| --- | --- |
| `docs/99.templates/support/document-metadata-profiles.yaml` | Machine-readable required/optional/forbidden key profile by artifact type. |
| `docs/99.templates/support/frontmatter-contract.md` | Human-readable metadata ownership and rollout contract. |
| `docs/99.templates/support/lifecycle-status.md` | Lifecycle state machine and override evidence rules. |
| `scripts/validation/check-document-metadata.py` | Parse metadata, infer profiles, resolve artifact IDs/parents, render inventory, and enforce advisory/changed modes. |
| `tests/validation/test_document_metadata.py` | Standard-library unit tests for parsing, profiles, IDs, transitions, and report output. |
| Directory `scripts/validation/`, file `run-agent-precommit-all-files.sh` | Controlled agent-only wrapper around `pre-commit run --all-files`. |
| `tests/validation/test_run_agent_precommit_all_files.sh` | Argument, worktree, task-evidence, and unexpected-path tests using a fake pre-commit binary. |
| `scripts/validation/check-repo-contracts.sh` | Integration point for metadata and wrapper contract checks. |
| `.pre-commit-config.yaml` | Changed/new metadata pre-push hook; never invokes the full agent wrapper. |
| `.github/workflows/ci-quality.yml` | Explicit changed/new metadata check in the existing `repo-contracts` job. |
| `scripts/operations/sync-provider-surfaces.sh` | Canonical provider adapter regeneration after Stage 00/Claude source updates. |

### Runtime Follow-up Documentation

| Path | Responsibility |
| --- | --- |
| `docs/03.specs/124-compose-runtime-readiness-remediation/` | Follow-up contract for Compose startup, health, recovery, upgrade, and rollback gaps. |
| `docs/03.specs/125-infrastructure-operations-readiness-remediation/` | Follow-up contract for infrastructure operations, backup/restore, and optional-profile gaps. |
| `docs/03.specs/126-security-supply-chain-remediation/` | Follow-up contract for SBOM, provenance, signing, broader SCA/container scanning, and approval gaps. |
| `docs/03.specs/127-deployment-release-engineering-remediation/` | Follow-up contract for CD, promotion, environment approval, rollback, and release records. |
| `docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md` | Independent Compose runtime-readiness plan requiring later runtime approval. |
| `docs/04.execution/plans/2026-07-11-infrastructure-operations-readiness-remediation.md` | Independent infrastructure operations-readiness plan requiring later runtime approval. |
| `docs/04.execution/plans/2026-07-11-security-supply-chain-remediation.md` | Independent security supply-chain plan requiring later runtime approval. |
| `docs/04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md` | Independent deployment and release-engineering plan requiring later runtime approval. |

## Source Entry Points

Use current primary sources and record direct URLs, supported claim, source
owner, publication/update date when available, retrieval date, and
applicability. Required source families include:

- Claude and Claude Code official model, deprecation, hooks, subagent,
  configuration, and permission documentation.
- OpenAI model/deprecation pages and Codex subagent, hook, security,
  configuration, and AGENTS.md documentation.
- Google Gemini model/deprecation/changelog pages and Gemini CLI configuration,
  MCP, and extension documentation.
- GitHub Actions workflow/security documentation and GitHub Spec Kit.
- pre-commit official documentation.
- Docker Compose profiles, networks, secrets, production, and trust-model
  documentation.
- NIST SSDF and incident-response guidance, OWASP SAMM, SLSA, OpenSSF
  Scorecard, and official supply-chain specifications.
- ISO/IEC/IEEE requirements and architecture references, ADR guidance, Google
  SRE incident/postmortem references, PagerDuty runbook guidance, Keep a
  Changelog, and Semantic Versioning.
- Original ReAct and Reflexion papers.
- <https://github.com/msitarzewski/agency-agents> as an external catalog
  pattern source, not an identity source.

## Work Breakdown

| Task | Description | Risk | Primary Files | Validation |
| --- | --- | --- | --- | --- |
| PLN-AER-001 | Research metadata, lifecycle, document roles, agent instructions, and vibe coding. | Low | Canonical research pack | Sources, template contract, repo contracts. |
| PLN-AER-002 | Revalidate harness, loop, provider, model, and agent-catalog research. | Low | Canonical research pack | Provider cutoff ledger, provider sync check, repo contracts. |
| PLN-AER-003 | Revalidate workspace, QA, automation, Compose, infrastructure, security, release, and deployment research. | Low | Canonical research pack | Tracked inventory, primary sources, repo contracts. |
| PLN-AER-004 | Audit SDLC, document roles, numbering, transitions, frontmatter, templates, and README profiles. | Low | Canonical audit pack | Reproducible counts, category matrices, repo contracts. |
| PLN-AER-005 | Audit harness, loop/evals, providers/models, workspace rules, agent instructions, catalogs, and vibe coding. | Low | Canonical audit pack | Criterion coverage and evidence review. |
| PLN-AER-006 | Audit QA/CI/CD, automation, Compose/infrastructure, security; consolidate indexes and supersede 2026-07-07 audit. | Medium | Canonical and duplicate audit packs | One-current-pack scan, generated audit matrices, repo contracts. |
| PLN-AER-007 | Implement typed metadata profiles, parser, advisory inventory, and unit tests. | High | Stage 00/99, Python validator/tests, generated inventory | Unit tests, advisory report, contract integration. |
| PLN-AER-008 | Migrate the approved active chain and enforce metadata for changed/new documents. | High | Templates, active chain, pre-push hook, validator | Before/after inventory, changed-mode tests, repo contracts. |
| PLN-AER-009 | Implement the controlled agent pre-commit wrapper and governance rules. | High | Bash wrapper/tests, Stage 00, scripts README | Fake-binary tests, shellcheck, wrapper contract test. |
| PLN-AER-010 | Synchronize provider adapters and add the metadata check to the existing CI repo-contracts job. | High | Stage 00/providers, `.claude`, generated `.codex`/`.agents`, CI | Provider no-drift, workflow lint/security, repo contracts. |
| PLN-AER-011 | Author four independent runtime-remediation specs/plans without runtime mutation. | Medium | Specs 124-127 and four plans | Template, traceability, rollback/approval gates. |
| PLN-AER-012 | Run full local gates through the wrapper, complete independent reviews, and close lifecycle evidence. | High | Task/plan/spec indexes, generated data, progress | Full verification bundle and clean whole-branch review. |

Plan approval is the explicit local authorization for medium/high tasks on the
named files. It does not authorize model-value changes, runtime mutation,
secret access, remote GitHub mutation, or branch-protection changes.

## Task Details

### Task 1: Metadata, Lifecycle, Document Roles, Instructions, and Vibe-Coding Research

**Files:**

- Create: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md`
- Create: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`

**Interfaces:**

- Consumes: Spec 123 audit record fields, current Stage 00/99 contracts, stage
  READMEs/templates, and the primary SDLC/instruction source families.
- Produces: Metadata/lifecycle and instruction/vibe criteria consumed by Tasks
  4, 5, 7, and 8.

- [ ] **Step 1: Inventory current metadata, lifecycle, document-role, and instruction claims**

Run:

```bash
rg -n "frontmatter|status|transition|number|PRD|ARD|ADR|Release|instruction|vibe|generated code" docs/00.agent-governance docs/01.requirements docs/02.architecture docs/03.specs/README.md docs/04.execution/README.md docs/05.operations/README.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh docs/99.templates
```

Expected: current rules and research gaps are enumerated from tracked files;
the task ledger records conflicting or missing claims.

- [ ] **Step 2: Revalidate primary external sources**

Open the required SDLC, metadata, instruction, incident, postmortem, runbook,
release, and agent-loop sources. Record each claim with retrieval date and
applicability. Expected: no community summary substitutes for an available
official standard, original paper, or official repository.

- [ ] **Step 3: Write the two focused criteria documents**

Each new reference must use this exact criterion shape:

```markdown
| Criterion ID | Practice | Primary source | Workspace applicability | Required evidence | Potential owner |
| --- | --- | --- | --- | --- | --- |
```

`document-metadata-lifecycle.md` must cover artifact identity, type profiles,
parents, supersession, review freshness, numbering, lifecycle transitions,
README exceptions, generated documents, and semantic validation.

`agent-instructions-vibe-coding.md` must cover instruction authority,
scope/context, tools, permissions, verification, generated-code ownership,
review thresholds, debt tracking, escalation, and safe vibe-coding boundaries.

- [ ] **Step 4: Integrate existing responsibility documents**

Update the five existing research files so release/document roles, spec-driven
flow, QA evidence, agent catalogs, and instruction/vibe criteria point to one
canonical owner and do not duplicate the new documents.

- [ ] **Step 5: Validate and commit**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: generated indexes are fresh and repository contracts report
`failures=0`.

Commit:

```bash
git add docs/90.references/research docs/90.references/llm-wiki docs/90.references/data/knowledge docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(research): define metadata and instruction criteria"
```

### Task 2: Harness, Loop, Provider, Model, and Agent-Catalog Research

**Files:**

- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`

**Interfaces:**

- Consumes: Approved 2026-07-10 10:00 KST model cutoff, official provider
  sources, current provider adapters, and Task 1 instruction criteria.
- Produces: Provider-specific harness/loop/model/catalog criteria consumed by
  Task 5 and the exact model-approval gate in Task 10.

- [ ] **Step 1: Inventory tracked provider surfaces**

Run:

```bash
find .claude .codex .agents docs/00.agent-governance/providers docs/00.agent-governance/agents -maxdepth 4 -type f -print | sort
bash scripts/operations/sync-provider-surfaces.sh --check
```

Expected: provider file sets and current no-drift result are recorded without
claiming native capability parity.

- [ ] **Step 2: Revalidate official provider sources and cutoff evidence**

Verify model IDs, provider-native lifecycle states, reasoning controls, coding
and agent surfaces, hooks, subagents, sandbox/permissions, and deprecations.
Later announcements remain outside the cutoff tables. Expected: every changed
model row has direct provider evidence or `historical state unverified`.

- [ ] **Step 3: Refresh harness, loop, and provider criteria**

Use the shared matrix:

```markdown
| Criterion | Claude | Codex | Gemini | Workspace common contract | Gap / caveat |
| --- | --- | --- | --- | --- | --- |
```

Keep Gemini reminder/pointer behavior distinct from native execution. Separate
research facts, workspace policy, and task-fit inference.

- [ ] **Step 4: Refresh agent catalogs and task-model mapping**

Compare the curated workspace roles with `agency-agents` by capability family,
not name count. Cover missing or mergeable product/spec, performance,
reliability, release/deployment, supply-chain, eval, and model-routing roles.

- [ ] **Step 5: Validate and commit**

Run provider sync check, `git diff --check`, LLM Wiki generators, and repository
contracts. Expected: no provider drift and `failures=0`.

```bash
git add docs/90.references/research docs/90.references/llm-wiki docs/90.references/data/knowledge docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(research): revalidate provider harness and models"
```

### Task 3: Workspace, Quality, Automation, Compose, Security, and Release Research

**Files:**

- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md`

**Interfaces:**

- Consumes: Current workflows, pre-commit configuration, validation scripts,
  Compose topology, security controls, Task 1 lifecycle criteria, and primary
  Docker/GitHub/pre-commit/NIST/SLSA/OpenSSF sources.
- Produces: Criteria for Tasks 4 and 6 and scoped runtime follow-ups in Task 11.

- [ ] **Step 1: Capture current workspace and automation inventory**

Run:

```bash
git ls-files '.github/workflows/*' '.pre-commit-config.yaml' 'scripts/**' 'infra/**' 'docker-compose.yml' 'docs/00.agent-governance/**' 'docs/05.operations/**'
rg -n '^  [a-z0-9_-]+:|include:|profiles:|secrets:|healthcheck:' docker-compose.yml infra/**/docker-compose*.yml
rg -n '^  [a-z0-9_-]+:|pre-commit|format|lint|typecheck|build|audit|zizmor' .github/workflows/ci-quality.yml .pre-commit-config.yaml
```

Expected: workflow, hook, script, root-active/optional Compose, operations, and
security surfaces are enumerated from tracked files.

- [ ] **Step 2: Revalidate primary guidance**

Verify local/CI/remote responsibilities, pre-commit semantics, Compose
profiles/networks/secrets/production, secure SDLC, supply chain, release
records, deployment promotion, rollback, and environment approval guidance.

- [ ] **Step 3: Refresh the five research documents**

Every category must state current tracked implementation, external criterion,
implementation status, gap, recommendation, owner, and confidence. Explicitly
distinguish CI from CD and structural Compose validation from runtime smoke,
recovery, migration, backup, and rollback testing.

- [ ] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: documentation and generated outputs are fresh, Compose validation
does not start services, all hardening tiers pass, and contracts report
`failures=0`.

```bash
git add docs/90.references/research docs/90.references/llm-wiki docs/90.references/data/knowledge docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(research): refresh quality infrastructure and security"
```

### Task 4: SDLC, Document Contract, Frontmatter, Template, and README Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md`
- Create: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`

**Interfaces:**

- Consumes: Task 1 criteria, current Stage 01-05/90/98/99 corpus, existing
  2026-07-03/04 audit evidence, templates, and validators.
- Produces: Current pre-remediation criterion rows and semantic inventory
  requirements consumed by Tasks 7 and 8.

- [ ] **Step 1: Reproduce current corpus and status counts**

Run:

```bash
git ls-files 'docs/**/*.md' | wc -l
rg -l '^status: (draft|active|completed|superseded|archived)$' docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references docs/98.archive | wc -l
rg -n '^(artifact_id|artifact_type|parent_ids|supersedes|reviewed_at|review_cycle|type|owner|updated|links|document_type|template_type):' docs
find docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references docs/98.archive docs/99.templates -name README.md -print | sort
find docs/05.operations/incidents -type f -name '*.md' -print | sort
rg -n 'release|changelog|version' docs/05.operations .github/workflows README.md
```

Expected: current counts and exception surfaces are reproducible. Historical
930/948-document counts remain labeled as dated evidence.

- [ ] **Step 2: Audit end-to-end lifecycle and document roles**

Assess PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
Postmortem, Release, README, Reference, Audit, and Archive. Include numbering,
parent coverage, entry/exit gates, status transitions, missing/unnecessary
artifacts, and release-record versus changelog/runbook disposition.

- [ ] **Step 3: Audit metadata and template semantics**

Use one row per criterion with the Spec 123 audit fields. Separate syntax
compliance from semantic correctness, including stale active state,
replacement-free supersession, README exceptions, generated documents, and
type-inappropriate keys.

- [ ] **Step 4: Publish reports and validate**

Update indexes and cross-links, run diff/wiki/traceability/alignment/contracts,
then commit:

```bash
git add docs/90.references/audits docs/90.references/llm-wiki docs/90.references/data/knowledge docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(audit): assess SDLC and document metadata"
```

### Task 5: Harness, Loop, Provider, Workspace, Agent, and Vibe-Coding Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`

**Interfaces:**

- Consumes: Tasks 1-2 research criteria and current Stage 00/provider/runtime
  surfaces.
- Produces: Evidence-backed harness, loop/eval, provider, model-policy,
  instruction, catalog, and vibe-coding dispositions for Tasks 9-10.

- [ ] **Step 1: Build the provider-neutral and provider-specific evidence map**

Run:

```bash
find .claude/agents .agents/agents -maxdepth 1 -type f -print | sort
find .codex/agents -maxdepth 1 -type f -name '*.toml' -print | sort
find .claude/skills .codex/skills .agents/skills -mindepth 2 -maxdepth 2 -type f -print | sort
rg -n 'model|reasoning|permission|sandbox|hook|subagent|memory|approval|eval' docs/00.agent-governance .claude .codex .agents
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures
```

Expected: provider counts, model/reasoning settings, native versus pointer
behavior, eval fixtures, and no-drift state are recorded.

- [ ] **Step 2: Assess every criterion**

Use `Implemented / Partial / Missing / Not Applicable / Needs Revalidation`,
enforcement depth 0-4, and `Retain / Fix / Improve / Add / Remove`. Include
actual model literals and reasoning settings without changing policy.

- [ ] **Step 3: Compare the agent catalog and instruction system**

Map workspace roles to capability families in `agency-agents`, identify roles
to add, merge, or reject, and audit model routing by task risk and evidence
needs. Keep external persona prose out of repo-local runtime identities.

- [ ] **Step 4: Validate and commit**

Run provider no-drift, diff/wiki/traceability/alignment/contracts, then commit:

```bash
git add docs/90.references/audits docs/90.references/llm-wiki docs/90.references/data/knowledge docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(audit): assess agentic harness and providers"
```

### Task 6: Quality, Automation, Compose, Security Audit and Pack Consolidation

**Files:**

- Create: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`
- Modify: `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md`
- Modify: `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/implementation-overview.md`
- Modify: `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md`
- Modify: `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/sdlc-qa-security-audit.md`
- Modify: `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md`
- Modify: `docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md`
- Modify: `docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/README.md`
- Modify: `docs/90.references/README.md`
- Modify: `scripts/validation/generate-audit-implementation-matrix.sh`
- Modify: `scripts/validation/report-audit-pack-coverage.sh`

**Interfaces:**

- Consumes: Tasks 1-5 criteria and reports plus tracked QA, workflow, Compose,
  hardening, security, release, and deployment evidence.
- Produces: One current audit pack, supersession mappings, current generated
  matrices, and prioritized runtime follow-up rows for Task 11.

- [ ] **Step 1: Audit QA, CI/CD, automation, pipeline, and workflow**

Cover formatting, linting, syntax, typecheck, build, coverage, dependency
audit, pre-commit, local/CI/remote boundaries, CI versus CD, skipped-tool
behavior, and automation candidates. The controlled wrapper remains `Missing`
until Task 9.

Run:

```bash
rg -n '^  [a-z0-9_-]+:|name:|run:|uses:|SKIP:' .github/workflows/ci-quality.yml
rg -n 'id:|entry:|stages:|exclude:|files:' .pre-commit-config.yaml
find scripts -maxdepth 2 -type f -print | sort
```

Expected: every claimed gate maps to a tracked job, hook, or script and CI is
not mislabeled as CD.

- [ ] **Step 2: Audit Compose, infrastructure, operations, and security**

Separate structural render/hardening evidence from startup, health, recovery,
upgrade, migration, backup/restore, promotion, rollback, SBOM, provenance,
signing, and broader vulnerability scanning.

Run:

```bash
find infra -type f -name 'docker-compose*.yml' -print | sort
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
rg -n 'SBOM|provenance|attestation|signing|Scorecard|vulnerability|rollback|backup|restore|promotion|deploy' docs scripts .github infra
```

Expected: structural and policy evidence is separated from missing runtime and
supply-chain evidence; no service is started.

- [ ] **Step 3: Merge and supersede the 2026-07-07 audit pack**

For each 2026-07-07 leaf, record canonical destination, verified merged
claims, rejected unsupported claims, and current-truth warning. Set README and
all five leaves to `status: superseded`; remove the pack from current-reading
routes.

- [ ] **Step 4: Preserve dated historical audit boundaries**

Update 2026-07-03/04 READMEs so their unique evidence remains available while
current corpus counts route to the canonical audit.

- [ ] **Step 5: Update generators, regenerate, validate, and commit**

Run:

```bash
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/report-audit-pack-coverage.sh
bash scripts/validation/report-audit-pack-coverage.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: one current audit pack, fresh generated reports, all structural
checks pass, and repository contracts report `failures=0`.

```bash
git add docs/90.references scripts/validation docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(audit): consolidate implementation audit pack"
```

### Task 7: Typed Metadata Profiles, Advisory Validator, and Exhaustive Inventory

**Files:**

- Create: `docs/99.templates/support/document-metadata-profiles.yaml`
- Create: `scripts/validation/check-document-metadata.py`
- Create: `tests/validation/test_document_metadata.py`
- Create: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`
- Modify: `docs/99.templates/support/README.md`
- Modify: `docs/99.templates/support/frontmatter-contract.md`
- Modify: `docs/99.templates/support/lifecycle-status.md`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify: `scripts/validation/check-repo-contracts.sh`
- Modify: `scripts/README.md`

**Interfaces:**

- Consumes: Task 4 audit criteria and current Stage 99 contracts.
- Produces:
  - `parse_frontmatter(path: Path) -> dict[str, object]`
  - `infer_artifact_type(path: Path) -> str`
  - `build_manifest(records: Sequence[Record]) -> dict[str, Path]`
  - `validate_record(record: Record, profiles: dict, manifest: dict) -> list[Finding]`
  - CLI modes `report`, `check-changed`, and `check-active`.

- [ ] **Step 1: Write failing unit tests**

Create tests for valid/invalid YAML frontmatter, README exceptions, duplicate
artifact IDs, unresolved parents, forbidden keys, valid and invalid lifecycle
transitions, generated documents, and deterministic report ordering.

```python
def test_duplicate_artifact_id_is_reported(tmp_path):
    write_doc(tmp_path / "a.md", {"status": "active", "artifact_id": "SPEC-123", "artifact_type": "spec"})
    write_doc(tmp_path / "b.md", {"status": "active", "artifact_id": "SPEC-123", "artifact_type": "spec"})
    result = run_checker(tmp_path, mode="report")
    assert "duplicate-artifact-id" in result.stdout
```

Run:

```bash
python3 -m unittest discover -s tests/validation -p 'test_document_metadata.py' -v
```

Expected: FAIL because the checker module and profile file do not exist.

- [ ] **Step 2: Define the machine-readable profile contract**

Use this top-level YAML shape:

```yaml
schema_version: 1
common:
  allowed_statuses: [draft, active, completed, superseded]
  terminal_statuses: [superseded]
profiles:
  spec:
    required: [status, artifact_id, artifact_type, parent_ids]
    optional: [supersedes, reviewed_at, review_cycle]
    forbidden: [type, document_type, template_type, owner, updated, links]
```

Add explicit profiles for every artifact type in Spec 123, including README,
generated, template-source, governance, and archive exceptions.

- [ ] **Step 3: Implement the minimal validator**

Use PyYAML `safe_load`, `dataclasses`, sorted tracked Markdown paths, and
deterministic findings:

```python
@dataclass(frozen=True, order=True)
class Finding:
    path: str
    code: str
    message: str
    severity: str = "error"

@dataclass(frozen=True)
class Record:
    path: Path
    metadata: dict[str, object]
    artifact_type: str
```

`report` always renders the inventory and exits nonzero only for parser or
configuration failure. `check-changed` fails on new violations in the selected
diff. `check-active` is implemented but remains non-gating in this program.

- [ ] **Step 4: Run tests and generate the pre-migration inventory**

```bash
python3 -m unittest discover -s tests/validation -p 'test_document_metadata.py' -v
python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
```

Expected: all unit tests PASS; inventory rows are sorted by path and record
current pre-migration findings without failing the task.

- [ ] **Step 5: Integrate advisory checks, validate, and commit**

Add a repository-contract check for profile syntax, script/tests presence, and
fresh inventory. Do not activate changed/new blocking yet.

```bash
git add docs/00.agent-governance docs/99.templates scripts tests docs/90.references/audits docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "feat(metadata): add typed document inventory"
```

### Task 8: Active-Chain Metadata Migration and Changed/New Enforcement

**Files:**

- Modify: `docs/99.templates/templates/sdlc/prd.template.md`
- Modify: `docs/99.templates/templates/sdlc/ard.template.md`
- Modify: `docs/99.templates/templates/sdlc/adr.template.md`
- Modify: `docs/99.templates/templates/sdlc/spec.template.md`
- Modify: `docs/99.templates/templates/sdlc/plan.template.md`
- Modify: `docs/99.templates/templates/sdlc/task.template.md`
- Modify: `docs/99.templates/templates/operations/guide.template.md`
- Modify: `docs/99.templates/templates/operations/policy.template.md`
- Modify: `docs/99.templates/templates/operations/runbook.template.md`
- Modify: `docs/99.templates/templates/operations/incident.template.md`
- Modify: `docs/99.templates/templates/operations/postmortem.template.md`
- Modify: `docs/99.templates/templates/common/reference.template.md`
- Modify: `docs/99.templates/templates/common/readme.template.md`
- Modify: `docs/99.templates/templates/common/archive.template.md`
- Modify: `docs/03.specs/123-agentic-engineering-audit-remediation/README.md`
- Modify: `docs/03.specs/123-agentic-engineering-audit-remediation/spec.md`
- Modify: `docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md`
- Modify: `docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md`
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md`
- Modify generated: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`
- Modify: `scripts/validation/check-document-metadata.py`
- Modify: `tests/validation/test_document_metadata.py`
- Modify: `.pre-commit-config.yaml`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/postflight-checklist.md`
- Modify: `docs/00.agent-governance/rules/task-checklists.md`

**Interfaces:**

- Consumes: Task 7 profile schema, manifest, and pre-migration inventory.
- Produces: Typed active agentic chain, changed/new enforcement, and
  post-migration inventory; does not enable repository-wide active blocking.

- [ ] **Step 1: Add failing changed-mode tests**

Test a newly added document without required metadata, a changed legacy
document with a permitted migration exception, a valid parent chain, a
superseded document without a replacement, and a reverse status transition
without override evidence.

Expected: tests fail until changed-mode diff selection and exception handling
are implemented.

- [ ] **Step 2: Update templates and active-chain metadata**

Each changed target gets the type profile's exact keys. Use stable IDs and
real parent IDs; do not copy every `Related Documents` link into `parent_ids`.
Template sources keep `status: draft` and use template-safe placeholders
defined by Stage 99.

- [ ] **Step 3: Implement changed/new enforcement and pre-push hook**

Add the local hook:

```yaml
- id: check-document-metadata
  name: Document metadata changed/new contract
  entry: python3 scripts/validation/check-document-metadata.py --mode check-changed
  language: system
  files: ^docs/.*\.md$
  pass_filenames: false
  stages: [pre-push]
```

The checker determines its base using the same safe local/CI rules as existing
validation scripts and reports an explicit fallback when no base is available.

- [ ] **Step 4: Regenerate and compare inventories**

Run unit tests, changed mode, report mode, and compare pre/post counts. Expected:
the approved active chain has zero typed-profile errors; historical corpus
findings remain advisory and visible.

- [ ] **Step 5: Validate and commit**

Run diff/wiki/traceability/alignment/contracts and commit:

```bash
git add .pre-commit-config.yaml docs scripts tests
git commit -m "feat(metadata): enforce typed metadata on changed docs"
```

### Task 9: Controlled Agent Pre-commit Wrapper and Governance Contract

**Files:**

- Create in `scripts/validation/`: `run-agent-precommit-all-files.sh`
- Create: `tests/validation/test_run_agent_precommit_all_files.sh`
- Modify: `scripts/README.md`
- Modify: `scripts/validation/check-repo-contracts.sh`
- Modify: `docs/00.agent-governance/rules/environment-constraints.md`
- Modify: `docs/00.agent-governance/rules/postflight-checklist.md`
- Modify: `docs/00.agent-governance/rules/task-checklists.md`
- Modify: `docs/00.agent-governance/rules/github-governance.md`
- Modify: `docs/00.agent-governance/rules/workflows.md`
- Modify: `docs/00.agent-governance/scopes/common.md`
- Modify: `docs/00.agent-governance/scopes/qa.md`
- Modify: `docs/99.templates/templates/sdlc/task.template.md`

**Interfaces:**

- Consumes: `--task <tracked-task-path>` and one or more
  `--allow-prefix <repo-relative-prefix>` arguments.
- Produces: pre-commit exit code, concise hook summary, before/after changed
  path sets, and explicit unexpected-path failure. It never writes task
  evidence automatically.

- [ ] **Step 1: Write failing shell tests**

Test missing task path, non-task path, primary-checkout rejection, linked
worktree acceptance, fake pre-commit failure propagation, expected edits, and
unexpected new edits. Use a temporary Git repository and fake `pre-commit` on
`PATH`; do not execute real hooks in unit tests.

```bash
bash tests/validation/test_run_agent_precommit_all_files.sh
```

Expected: FAIL because the wrapper does not exist.

- [ ] **Step 2: Implement argument and safety contract**

The wrapper starts with:

```bash
#!/usr/bin/env bash
set -euo pipefail

TASK_FILE=""
ALLOW_PREFIXES=()
```

It verifies `git rev-parse --git-dir` differs from `--git-common-dir`, the task
file is tracked under `docs/04.execution/tasks/`, every prefix is relative and
non-parent-traversing, and `pre-commit` is available.

- [ ] **Step 3: Implement execution and unexpected-path detection**

Run exactly:

```bash
pre-commit run --all-files --show-diff-on-failure
```

Record status before and after using temporary files removed by `trap`. A path
newly changed by hooks must match an allowed prefix or the wrapper exits with a
distinct unexpected-path code. Never run reset, checkout, clean, or deletion.

- [ ] **Step 4: Update governance and task-evidence template**

Replace blanket manual-pre-commit ambiguity with one rule: direct execution is
prohibited; the wrapper is required at the approved final QA gate. Add task
evidence fields for command, prefixes, exit status, modified paths, review
disposition, and skipped rationale.

- [ ] **Step 5: Test, validate, and commit**

Run shell syntax, shell tests, shellcheck, repository contracts, and diff
hygiene. Do not run the real full-repository wrapper until Task 12.

```bash
git add scripts tests docs/00.agent-governance docs/99.templates docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "feat(qa): add controlled agent precommit wrapper"
```

### Task 10: Provider Adapter and CI Synchronization

**Files:**

- Modify: `docs/00.agent-governance/rules/provider-capability-matrix.md`
- Modify: `docs/00.agent-governance/rules/workflows.md`
- Modify: `docs/00.agent-governance/rules/github-governance.md`
- Modify: `docs/00.agent-governance/providers/claude.md`
- Modify: `docs/00.agent-governance/providers/codex.md`
- Modify: `docs/00.agent-governance/providers/gemini.md`
- Modify: `docs/00.agent-governance/providers/agents-md.md`
- Modify: `.claude/skills/style-validation/skill.md`
- Modify: `.claude/skills/test-automator/skill.md`
- Modify: `.claude/skills/ci-cd-patterns/skill.md`
- Modify: `.claude/CLAUDE.md`
- Modify generated: `.codex/skills/style-validation/skill.md`
- Modify generated: `.codex/skills/test-automator/skill.md`
- Modify generated: `.codex/skills/ci-cd-patterns/skill.md`
- Modify generated: `.agents/skills/style-validation/skill.md`
- Modify generated: `.agents/skills/test-automator/skill.md`
- Modify generated: `.agents/skills/ci-cd-patterns/skill.md`
- Modify generated: `.agents/README.md`
- Modify: `.github/workflows/ci-quality.yml`
- Modify: `scripts/operations/sync-provider-surfaces.sh`
- Modify: `scripts/validation/check-repo-contracts.sh`

**Interfaces:**

- Consumes: Tasks 5, 8, and 9 findings and contracts.
- Produces: Synchronized provider guidance for typed metadata and wrapper use,
  plus an explicit CI metadata step in the existing `repo-contracts` job.

- [ ] **Step 1: Write the expected CI/provider contract as failing checks**

Extend repo contracts to require the metadata command in the existing
`repo-contracts` job and the wrapper/metadata wording on each provider surface.
Expected: repository contracts fail before source adapters and workflow are
updated.

- [ ] **Step 2: Update Stage 00 and Claude canonical adapter sources**

Add provider-neutral lifecycle terms and provider-specific execution notes.
Gemini must remain a behavioral pointer where native hooks are unavailable.
Do not change any model literal or reasoning effort in this task.

- [ ] **Step 3: Regenerate provider surfaces**

```bash
bash scripts/operations/sync-provider-surfaces.sh --write
bash scripts/operations/sync-provider-surfaces.sh --check
```

Expected: write mode updates only generated adapters and check mode reports
`no drift`.

- [ ] **Step 4: Add explicit CI changed/new metadata validation**

In the existing `repo-contracts` job, after installing
`scripts/requirements.txt`, run:

```yaml
- name: Check changed and new document metadata
  run: python3 scripts/validation/check-document-metadata.py --mode check-changed
```

Do not add a new required job or change local/remote branch-protection context
lists.

- [ ] **Step 5: Validate workflow, providers, and commit**

Run provider no-drift, unit tests, actionlint when available, local zizmor when
available, repo contracts, and diff hygiene. Record CI-only rationale for tools
that are unavailable locally.

```bash
git add .claude .codex .agents .github/workflows/ci-quality.yml docs/00.agent-governance scripts docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "ci(governance): synchronize metadata and provider gates"
```

### Task 11: Runtime Follow-up Specifications and Plans

**Files:**

- Create: `docs/03.specs/124-compose-runtime-readiness-remediation/README.md`
- Create: `docs/03.specs/124-compose-runtime-readiness-remediation/spec.md`
- Create: `docs/03.specs/125-infrastructure-operations-readiness-remediation/README.md`
- Create: `docs/03.specs/125-infrastructure-operations-readiness-remediation/spec.md`
- Create: `docs/03.specs/126-security-supply-chain-remediation/README.md`
- Create: `docs/03.specs/126-security-supply-chain-remediation/spec.md`
- Create: `docs/03.specs/127-deployment-release-engineering-remediation/README.md`
- Create: `docs/03.specs/127-deployment-release-engineering-remediation/spec.md`
- Create: `docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md`
- Create: `docs/04.execution/plans/2026-07-11-infrastructure-operations-readiness-remediation.md`
- Create: `docs/04.execution/plans/2026-07-11-security-supply-chain-remediation.md`
- Create: `docs/04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/README.md`

**Interfaces:**

- Consumes: Canonical audit gap IDs from Task 6.
- Produces: Four independent, later-approvable specs/plans with exact audit
  inputs, dependencies, rollback/recovery, validation, and runtime approval
  gates. No task evidence or runtime implementation is created.

- [ ] **Step 1: Route each runtime gap once**

Assign every Compose/infrastructure/security/deployment gap to exactly one
follow-up spec. Cross-links may reference another owner, but duplicate
requirements are prohibited.

- [ ] **Step 2: Author the four specs from the canonical template**

Each spec states current evidence, target behavior, dependencies, migration,
rollback/recovery, verification, and the exact approvals still required.
Architecture-changing gaps explicitly list required PRD/ARD/ADR predecessors.

- [ ] **Step 3: Author one plan per follow-up spec**

Create all four follow-up plans with `status: draft`. Runtime implementation,
upstream architecture decisions, and exact approval evidence are intentionally
unresolved at this stage. None of these plans may claim runtime authorization
from this umbrella plan.

- [ ] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: all follow-up documents satisfy templates and traceability, generated
indexes are fresh, and no runtime file is modified.

Commit:

```bash
git add docs/03.specs docs/04.execution/plans docs/90.references/llm-wiki docs/90.references/data/knowledge docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
git commit -m "docs(plan): route runtime remediation followups"
```

### Task 12: Full Verification, Independent Branch Review, and Lifecycle Closure

**Files:**

- Modify: `docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md`
- Modify: `docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md`
- Modify: `docs/03.specs/123-agentic-engineering-audit-remediation/README.md`
- Modify: `docs/03.specs/123-agentic-engineering-audit-remediation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Regenerate when stale: LLM Wiki, audit implementation matrix, audit coverage,
  metadata inventory, provider surfaces, and other generator-owned outputs.

**Interfaces:**

- Consumes: Tasks 1-11 commits, review verdicts, deviations, and exact allowed
  prefixes for the controlled wrapper.
- Produces: Final verification evidence, whole-branch verdict, closed lifecycle
  statuses, and clean worktree.

- [x] **Step 1: Re-run every generator in write and check mode**

Run:

```bash
bash scripts/operations/sync-provider-surfaces.sh --write
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/report-audit-pack-coverage.sh
bash scripts/validation/report-audit-pack-coverage.sh --check
python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
```

Expected: provider surfaces report `no drift`; LLM Wiki, audit, metadata, and
coverage outputs are fresh.

- [x] **Step 2: Run targeted and repository-wide local checks**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata -v
bash tests/validation/test_run_agent_precommit_all_files.sh
WRAPPER_DIR="scripts/validation"
WRAPPER_NAME="run-agent-precommit-all-files.sh"
bash -n "$WRAPPER_DIR/$WRAPPER_NAME"
shellcheck "$WRAPPER_DIR/$WRAPPER_NAME" tests/validation/test_run_agent_precommit_all_files.sh
actionlint .github/workflows/ci-quality.yml
zizmor .github/workflows/ci-quality.yml
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: every available local check passes. If `actionlint` or `zizmor` is
unavailable, record the missing tool and CI-only verification requirement;
do not report that check as passed. No service is started.

- [x] **Step 3: Run the approved full-repository pre-commit wrapper**

Run:

```bash
WRAPPER_DIR="scripts/validation"
WRAPPER_NAME="run-agent-precommit-all-files.sh"
bash "$WRAPPER_DIR/$WRAPPER_NAME" \
  --task docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md \
  --allow-prefix docs/ \
  --allow-prefix scripts/ \
  --allow-prefix tests/ \
  --allow-prefix .claude/ \
  --allow-prefix .codex/ \
  --allow-prefix .agents/ \
  --allow-prefix .github/ \
  --allow-prefix .pre-commit-config.yaml
```

Expected: all configured hooks pass, no unexpected new path is modified, and
the task evidence records exit status, hook summary, before/after paths, and
review disposition. On unexpected paths, stop without reset and return to the
responsible task.

- [x] **Step 4: Dispatch the new exact-range whole-branch independent review**

The reviewer receives the exact base..HEAD range, Spec 123, this plan, task
evidence, source/cutoff ledger, protected-surface list, test output summary,
and all task-level verdicts. Required result: Spec PASS, Quality APPROVED,
Critical 0, Important 0.

- [x] **Step 5: Apply any new review fixes in a separate commit and re-run affected gates**

Do not close lifecycle while any critical/important finding or unverified
required check remains.

- [x] **Step 6: Close lifecycle only after the new review passes**

Set Spec/Plan/Task statuses to `completed` only after all criteria pass. Update
indexes and progress memory, verify a clean worktree, then commit:

```bash
git add docs scripts .claude .codex .agents .github .pre-commit-config.yaml tests
git commit -m "docs(task): close agentic audit remediation"
```

### Postclosure Remediation and Final Reclosure Evidence

- Tasks 1-11 have task-scoped Spec PASS / Quality APPROVED verdicts with all
  findings resolved to Critical 0, Important 0, Minor 0.
- Task 12 Steps 1-3 and the controlled wrapper's final zero-exit attempt remain
  historical evidence and were not rerun for the focused postclosure fix.
- The exact preclosure whole-branch range
  `3e92b39fa02767dafff612fcfa5b3670998471be..6a73dddb6fe95df2c2cf022d27ab0878d3773213`
  historically returned Spec PASS / Quality APPROVED, Critical 0, Important 0,
  Minor 0, and `READY_FOR_CLOSURE: YES`.
- The first postclosure range
  `3e92b39fa02767dafff612fcfa5b3670998471be..74945d22898b9005d5f5450231c8c45980f6c0d7`
  returned Spec FAIL / Quality CHANGES_REQUESTED, Critical 0, Important 1,
  Minor 0, and `READY_FOR_FINISHING: NO` for deletion-induced relation bypass.
- Commit `52fa67cf` fixed I-01 deletion impact. The next review found I-02,
  in-place identity replacement impact, and commit `746be1be` fixed it across
  unstaged, staged, and explicit-base changes.
- The exact re-review of
  `3e92b39fa02767dafff612fcfa5b3670998471be..746be1be`
  returned Spec PASS / Quality APPROVED, Critical 0, Important 0, Minor 0,
  resolved I-01 and I-02, and `READY_FOR_RECLOSURE: YES`.
- The later final merge-readiness review of
  `3e92b39fa02767dafff612fcfa5b3670998471be..132418a4` found I-03: required
  local Git discovery could fail open as `selected=0 violations=0`. The
  fail-closed implementation landed in `b08d6576`; its postfix review found
  I-03-R1, and `10ffce8f` bounded explicit-base non-UTF-8 path decoding.
- The exact re-review of
  `3e92b39fa02767dafff612fcfa5b3670998471be..10ffce8f`
  returned Spec PASS / Quality APPROVED, Critical 0, Important 0, Minor 0,
  resolved I-01, I-02, I-03, and I-03-R1, and `READY_FOR_RECLOSURE: YES`.
- Specs 124-127 and their plans remain `draft`; no runtime or remote mutation
  is authorized by this lifecycle reclosure.

## Verification Plan

| ID | Level | Command / Evidence | Pass Criteria |
| --- | --- | --- | --- |
| VAL-AER-001 | Unit | `python3 -m unittest discover -s tests/validation -p 'test_document_metadata.py' -v` | All metadata parser/profile/manifest/transition/report tests pass. |
| VAL-AER-002 | Unit | `bash tests/validation/test_run_agent_precommit_all_files.sh` | All wrapper safety and fake-pre-commit tests pass. |
| VAL-AER-003 | Provider | `bash scripts/operations/sync-provider-surfaces.sh --check` | Reports `no drift`. |
| VAL-AER-004 | Metadata | `python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md` | Inventory is deterministic and fresh; approved active chain is clean after migration. |
| VAL-AER-005 | Docs | `bash scripts/validation/check-doc-traceability.sh` | `failures=0`. |
| VAL-AER-006 | Alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0`. |
| VAL-AER-007 | Compose | `bash scripts/validation/validate-docker-compose.sh` | Structural validation passes without service startup. |
| VAL-AER-008 | Hardening | `bash scripts/hardening/check-all-hardening.sh` | All governed tiers pass. |
| VAL-AER-009 | Contracts | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`; generated outputs are fresh. |
| VAL-AER-010 | Full QA | Controlled wrapper with task and minimal allowed prefixes | All configured hooks pass; no unexpected paths. |
| VAL-AER-011 | Review | Task-level and whole-branch independent reports | Spec PASS, Quality APPROVED, Critical 0, Important 0. |
| VAL-AER-012 | Git | `git diff --check` and final `git status --short` | No whitespace errors and clean worktree. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Mutable external sources obscure the approved model cutoff | High | Preserve direct cutoff evidence and use `historical state unverified`; never backdate later facts. |
| Audit reports become policy or runtime truth | High | Keep Stage 90 advisory; route approved changes to Stage 00/99/04 or runtime follow-up specs. |
| Typed metadata causes mass false positives | High | Advisory report first, type-profile tests, active-chain migration, changed/new enforcement only. |
| Artifact IDs or parent links collide | High | Deterministic manifest, duplicate-ID failure, unresolved-parent failure, explicit multi-parent support. |
| Full pre-commit modifies unrelated files | High | Isolated worktree, before/after path sets, minimal allowed prefixes, stop without auto-revert. |
| Provider adapters drift or claim false parity | High | Stage 00/Claude canonical source, generator-only mirrors, no-drift validation, explicit Gemini capability limits. |
| CI change creates a new remote required context | Medium | Add a step to existing `repo-contracts`; do not add a job or mutate branch protection. |
| Runtime follow-up plans are mistaken for authorization | High | State approval boundary in every spec/plan; create no task evidence or runtime changes. |
| Multiple agents edit the same file | Medium | Sequential task execution, explicit ownership, close agents, stop on overlap. |

## Rollback and Recovery

- Research/audit errors: revert only the task's logical commit after preserving
  verified unique content and reviewer evidence.
- Metadata gate errors: disable changed/new invocation while keeping advisory
  report mode and recorded findings.
- Provider drift: regenerate from the corrected canonical source; never patch
  generated adapters independently.
- Wrapper error: remove the wrapper invocation contract but retain direct
  pre-commit prohibition until a corrected wrapper passes tests.
- Workflow error: remove only the added step from the existing repo-contracts
  job; required job taxonomy remains unchanged.
- Runtime follow-up error: keep specs/plans draft or supersede them; runtime is
  untouched and requires no operational rollback.

## Agent Rollout & Evaluation Gates

- **Execution mode:** Subagent-Driven Development, already selected by the
  user. Dispatch one fresh implementer per task, then a spec-compliance reviewer
  and a quality/security reviewer.
- **Task gate:** No next task begins until both reviews pass or a dedicated
  fixer resolves findings and the affected reviewer re-approves.
- **Offline eval gate:** Metadata and wrapper unit tests plus deterministic
  fixture/report checks.
- **Sandbox gate:** All implementation occurs in an isolated linked worktree.
- **Human approval gate:** Approval of this plan authorizes the named local
  medium/high surfaces only. Exact model values, runtime, secrets, remote
  GitHub, and branch protection remain separately gated.
- **Rollback trigger:** Unexpected wrapper paths, broad metadata false
  positives, provider drift, CI syntax/security failure, or a critical/important
  review finding.
- **Promotion criteria:** Full verification bundle passes; whole-branch review
  is PASS/APPROVED; worktree is clean.

## Completion Criteria

- [x] Canonical research includes all requested external criteria and two new focused criteria documents.
- [x] Canonical audit covers every category/subcategory with the shared status/depth/disposition model.
- [x] The 2026-07-07 audit pack is mapping-only superseded history; 2026-07-03/04 boundaries are explicit.
- [x] Exhaustive semantic frontmatter inventory is reproducible and current.
- [x] Typed metadata profiles, lifecycle rules, unit tests, identity-removal handling, and fail-closed Git discovery pass with exact-range re-review approval.
- [x] Approved active agentic chain carries valid typed metadata and parent relations.
- [x] Controlled agent pre-commit wrapper and evidence contract pass tests and final full-repository execution.
- [x] Stage 00/99, provider adapters, validators, pre-push, and CI repo-contracts step are synchronized.
- [x] No model literal changes occur without separate exact approval.
- [x] Four runtime follow-up specs/plans exist with explicit approval and rollback boundaries; runtime remains unchanged.
- [x] Every task has logical commits and independent spec/quality reviews.
- [x] Full affected validation and exact-range whole-branch review pass; lifecycle is reclosed.

## Related Documents

- [Parent specification](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- [Specification folder](../../03.specs/123-agentic-engineering-audit-remediation/README.md)
- [Task evidence](../tasks/2026-07-11-agentic-engineering-audit-remediation.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
