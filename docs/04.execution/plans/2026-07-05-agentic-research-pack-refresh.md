---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-agentic-research-pack-refresh.md -->

# Agentic Research Pack Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh and extend the Stage 90 agentic engineering research pack with current external source evidence and repo-local analysis.

**Architecture:** Use the existing `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` pack as the canonical research category. Refresh current documents first, add targeted reference documents only where Docker Compose, infrastructure, security, automation, pipeline, or workflow coverage would make the existing files unfocused, and record active-stage improvements as gaps. Preserve Stage 90 as reference context rather than policy, plan, runbook, task evidence, or runtime truth.

**Tech Stack:** Markdown reference documents, Stage 90 reference template, Stage 04 task evidence, repository validation scripts, official vendor/standards web sources, repo-local governance/docs/scripts/CI evidence.

---

## Overview

This document is the implementation plan for `docs/03.specs/104-agentic-research-pack-refresh/spec.md`. It defines source collection, document refresh, targeted document additions, validation, risk control, and completion criteria.

## Context

The user requested a categorized research pack covering workspace purpose, roles, CI/CD, QA, formatting, linting, syntax errors, automation, pipelines, workflows, operating contracts, templates, scripts, integration guides, SDLC, governance, system rules, security, harness engineering, loop engineering, provider implementation status for Claude/Codex/Gemini, Docker Compose, and infrastructure.

An existing Stage 90 research pack already covers much of the requested scope. The approved approach is to refresh the existing pack first and add targeted documents only where needed. The design contract now lives in the canonical Stage 03 path:

- [Agentic Research Pack Refresh Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md)

## Goals & In-Scope

- **Goals**:
  - Revalidate existing research documents against current official sources.
  - Expand coverage for Docker Compose, infrastructure, security, automation, pipeline, workflow, linting, and syntax-check concerns.
  - Preserve source-backed citations and repository-local evidence mapping.
  - Update README indexes and progress memory when structure changes.
  - Commit by logical unit.
- **In Scope**:
  - Stage 90 research documents under `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`.
  - Stage 90 research README indexes.
  - Stage 04 task evidence for this execution.
  - Stage 00 progress memory.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - No runtime Docker Compose changes.
  - No provider runtime config changes.
  - No CI workflow behavior changes.
  - No secret, credential, token, private key, branch protection, or remote GitHub setting changes.
  - No active policy adoption of external frameworks during this research pass.
- **Out of Scope**:
  - Fixing gaps discovered during research outside Stage 90/Stage 04/progress memory.
  - Rewriting unrelated research categories.
  - Creating active operations procedures, policies, runbooks, incidents, or runtime tasks.

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md` | Execution evidence, source list, validation evidence, deviations, and final status. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md` | Repo-local workspace purpose, roles, CI/CD, QA, formatting, linting, automation, scripts, templates, integration guides, SDLC, governance, rules, infrastructure, and security baseline. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md` | Harness engineering concepts, runtime/test/eval/governance harness mapping, and workspace application gaps. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md` | Agent, validation, CI, memory, eval, approval, human-in-the-loop, automation, and workflow loops. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md` | Claude, Codex, Gemini harness/loop implementation status and common provider-neutral environment rules. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md` | Spec-driven development and SDLC mapping, including secure SDLC references. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md` | CI/CD, QA, formatting, linting, syntax checks, and security gate analysis. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md` | Targeted Docker Compose and infrastructure reference if existing docs would become too broad. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md` | Targeted security governance reference if security coverage should be separated from quality and workspace baseline docs. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md` | Targeted automation/pipeline/workflow reference if loop and quality docs become too broad. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md` | Research pack index, structure, reading order, and source-maintenance guidance. |
| `docs/90.references/research/README.md` | Parent research index, updated only if pack structure changes materially. |
| `docs/00.agent-governance/memory/progress.md` | Progress and validation evidence. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Verify and expand Stage 04 task evidence scaffold | `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`, `docs/04.execution/tasks/README.md` if index update is required | VAL-SPC-006 | Task doc exists, links to spec/plan/research pack, and has no placeholder sections. |
| PLN-002 | Revalidate external source set and repo-local baseline | Task evidence source inventory; no research body changes unless source conflict is found | VAL-SPC-002, VAL-SPC-003 | Official sources and repo-local evidence are listed with source roles and revalidation date. |
| PLN-003 | Refresh workspace, harness, loop, provider, SDLC, and quality documents | Existing research pack files | VAL-SPC-002, VAL-SPC-003, VAL-SPC-004 | Existing documents cover requested categories without duplicate SSoT or unsupported provider claims. |
| PLN-004 | Add targeted Docker Compose, infrastructure, security, or automation references if needed | New Stage 90 research files and README indexes | VAL-SPC-003, VAL-SPC-004 | Added documents follow reference template and keep active-stage gaps as follow-up items. |
| PLN-005 | Finalize README indexes, progress memory, and validation evidence | Research README files, progress memory, task evidence | VAL-SPC-006, VAL-SPC-007 | Repo validation gates pass and task evidence records final commands/results. |

## Task Details

### Task 1: Verify and Expand Execution Task Evidence

**Files:**
- Modify: `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`
- Modify if needed: `docs/04.execution/tasks/README.md`

- [x] **Step 1: Read task template**

Run:

```bash
cat docs/99.templates/templates/sdlc/task.template.md
```

Expected: template shows required task evidence sections and `## Verification Summary`.

- [x] **Step 2: Confirm task evidence file**

Confirm `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md` contains this minimum evidence scaffold:

```markdown
---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md -->

# Agentic Research Pack Refresh Task

## Overview

This task records execution evidence for refreshing and extending the Stage 90 agentic engineering research pack.

## Task Scope

- Refresh existing Stage 90 research documents under `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`.
- Add targeted reference documents only when existing documents would become unfocused.
- Update README indexes and progress memory.
- Do not change runtime, provider config, CI workflow behavior, scripts, secrets, or remote GitHub state.

## Work Items

| ID | Description | Status | Evidence |
| --- | --- | --- | --- |
| T-RSRCH-001 | Create task evidence and plan link closure | In Progress | This task document |
| T-RSRCH-002 | Revalidate external source set and repo-local evidence | Pending | Source inventory section |
| T-RSRCH-003 | Refresh existing research pack documents | Pending | Git diff and source-backed notes |
| T-RSRCH-004 | Add targeted references if required | Pending | New reference docs or N/A rationale |
| T-RSRCH-005 | Update indexes, progress memory, and validation evidence | Pending | Final validation summary |

## Source Inventory

| Source Class | Source | Role | Status |
| --- | --- | --- | --- |
| Stage 03 Spec | [Agentic Research Pack Refresh Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md) | Design contract | Active |
| Stage 04 Plan | [Agentic Research Pack Refresh Plan](../plans/2026-07-05-agentic-research-pack-refresh.md) | Execution plan | Active |
| Stage 90 Research Pack | [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md) | Target research category | Active |

## Deviation Log

No deviations recorded yet.

## Verification Summary

Validation runs after research documents and indexes are updated.

## Related Documents

- [Plan](../plans/2026-07-05-agentic-research-pack-refresh.md)
- [Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md)
- [Research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Research references](../../90.references/research/README.md)
```

- [x] **Step 3: Check parent task README**

Run:

```bash
rg -n "agentic-research-pack-refresh|2026-07-05" docs/04.execution/tasks/README.md
```

Expected: if no entry exists, add a single related-document/index entry using the local README pattern.

- [x] **Step 4: Validate task scaffold**

Run:

```bash
git diff --check
bash scripts/validation/check-repo-contracts.sh
```

Expected: `git diff --check` has no output and repo contract reports `failures=0`.

- [x] **Step 5: Commit task evidence updates**

Run:

```bash
git add docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md docs/04.execution/tasks/README.md
git commit -m "docs(tasks): Update agentic research refresh task evidence"
```

Expected: commit succeeds.

### Task 2: Revalidate External Sources and Repo-local Evidence

**Files:**
- Modify: `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`
- Read: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/*.md`
- Read: `docs/00.agent-governance/**`, `scripts/README.md`, `.github/workflows/ci-quality.yml`, `infra/README.md`

- [x] **Step 1: Inventory current research pack**

Run:

```bash
rg --files docs/90.references/research/2026-07-05-agentic-research-pack-refresh | sort
```

Expected: existing research files are listed, including `workspace-baseline.md`, `harness-engineering.md`, `loop-engineering.md`, `spec-driven-sdlc.md`, `quality-ci-formatting.md`, and `provider-implementation-comparison.md`.

- [x] **Step 2: Revalidate official external source set**

Use web verification for these primary sources before editing research text:

```text
Claude Code overview: https://docs.anthropic.com/en/docs/claude-code/overview
Claude Code subagents: https://docs.anthropic.com/en/docs/claude-code/sub-agents
Claude Code hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
OpenAI Codex CLI: https://developers.openai.com/codex/cli
OpenAI Codex subagents: https://developers.openai.com/codex/subagents
OpenAI Codex hooks: https://developers.openai.com/codex/hooks
OpenAI Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
Gemini CLI official docs: https://developers.google.com/gemini-code-assist/docs/gemini-cli
Gemini CLI docs site: https://google-gemini.github.io/gemini-cli/docs/
Docker Compose docs: https://docs.docker.com/compose/
Docker Compose file reference: https://docs.docker.com/reference/compose-file/
Docker Compose production guidance: https://docs.docker.com/compose/how-tos/production/
Docker secrets in Compose: https://docs.docker.com/compose/how-tos/use-secrets/
GitHub Actions workflow syntax: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
GitHub Actions secure use: https://docs.github.com/en/actions/reference/security/secure-use
pre-commit docs: https://pre-commit.com/
EditorConfig: https://editorconfig.org/
Prettier docs: https://prettier.io/docs
NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
OWASP SAMM: https://owasp.org/www-project-samm/
SLSA: https://slsa.dev/
ReAct paper: https://arxiv.org/abs/2210.03629
Reflexion paper: https://arxiv.org/abs/2303.11366
```

Expected: task evidence records each source class and whether it supports provider, Docker Compose, infrastructure, security, quality, loop, or SDLC analysis.

- [x] **Step 3: Inventory repo-local evidence**

Run:

```bash
rg -n "CI/CD|QA|Formatting|Linting|Docker Compose|Security|workflow|pipeline|automation|harness|loop|provider|template|secret|approval" README.md AGENTS.md docs/00.agent-governance docs/03.specs/104-agentic-research-pack-refresh docs/90.references/research/2026-07-05-agentic-research-pack-refresh scripts .github infra -g '*.md' -g '*.yml' -g '*.yaml'
```

Expected: output identifies repo-local sources. Record only summarized source roles in the task evidence, not raw output.

- [x] **Step 4: Update task evidence source inventory**

Modify `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md` so `## Source Inventory` includes rows for:

```markdown
| External Provider Docs | Claude, Codex, Gemini official docs | Provider harness/loop implementation facts | Revalidated 2026-07-05 |
| External Infrastructure Docs | Docker Compose official docs | Compose, profiles, secrets, production and infrastructure reference facts | Revalidated 2026-07-05 |
| External Quality/Security Docs | GitHub Actions, pre-commit, EditorConfig, Prettier, NIST SSDF, OWASP SAMM, SLSA | CI/CD, QA, formatting, linting, secure SDLC, supply-chain analysis | Revalidated 2026-07-05 |
| External Loop/Harness Sources | ReAct, Reflexion, eval framework references | Loop and harness engineering interpretation | Revalidated 2026-07-05 |
| Repo-local Evidence | Stage 00, scripts, CI workflow, infra, Stage 90 research pack | Workspace-specific baseline and gap analysis | Revalidated 2026-07-05 |
```

- [x] **Step 5: Commit source inventory**

Run:

```bash
git add docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md
git commit -m "docs(tasks): Record agentic research source inventory"
```

Expected: commit succeeds.

### Task 3: Refresh Existing Research Pack Documents

**Files:**
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md`
- Modify: `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`

- [x] **Step 1: Refresh workspace baseline coverage**

Update `workspace-baseline.md` so the category map explicitly covers:

```markdown
| Security | `.github/SECURITY.md`, `docs/00.agent-governance/scopes/security.md`, `docs/00.agent-governance/rules/github-governance.md`, `scripts/validation/check-template-security-baseline.sh` | Security is handled through disclosure guidance, scope-level enforcement, GitHub Actions security contracts, template/security baseline checks, secret boundaries, and hardening validation. |
| Linting / Syntax | `.pre-commit-config.yaml`, `scripts/hooks/post-tool-validate.sh`, `.github/workflows/ci-quality.yml` | Style and syntax drift are checked through hook-mediated validation, CI pre-commit, frontend quality gates, YAML/security scans, and `git diff --check`. |
| Docker Compose / Infrastructure | `docker-compose.yml`, `infra/README.md`, `scripts/validation/validate-docker-compose.sh`, `scripts/hardening/check-all-hardening.sh` | Runtime truth remains in Compose and infra files; research docs cite it but do not replace it. |
```

Expected: no duplicate rows with the same role remain.

- [x] **Step 2: Refresh harness engineering**

Update `harness-engineering.md` so `Harness Components` includes Docker Compose/runtime infrastructure, security boundaries, and source freshness caveats:

```markdown
| Infrastructure harness | Compose project, profiles, networks, secrets, health checks | `docker-compose.yml`, `infra/**/docker-compose*.yml`, `validate-docker-compose.sh`, `check-all-hardening.sh` |
| Security harness | sandbox, approvals, secret boundaries, workflow security, supply-chain checks | approval boundaries, `.github/SECURITY.md`, GitHub governance, zizmor, template/security baseline |
```

Expected: Application notes distinguish test/eval harness from infrastructure and security harnesses.

- [x] **Step 3: Refresh loop engineering**

Update `loop-engineering.md` so the loop map includes:

```markdown
| Automation pipeline loop | script, hook, CI, or provider workflow trigger | run local or remote automation | pass/fail logs, SARIF, task evidence, progress memory | scripts, provider hooks, `.github/workflows/ci-quality.yml` |
| Security review loop | protected surface, workflow change, secret boundary, dependency or action risk | inspect against policy and scanners | findings, skipped-check rationale, escalation | security scope, GitHub governance, `.github/SECURITY.md`, zizmor |
```

Expected: analysis explains that automation loops do not authorize external actions without approval.

- [x] **Step 4: Refresh provider comparison**

Update `provider-implementation-comparison.md` only after official provider source revalidation. Required comparison rows:

```markdown
| Docker/infra awareness | tool-driven through shell and project docs | sandboxed local shell plus project docs | tool-driven ReAct/MCP workflow | Stage 00 infra scope and scripts are provider-neutral |
| Security/approval model | permissions, hooks, human approval | sandbox/approval modes, hooks, config | trust/config/tool confirmation surfaces | approval boundaries and protected surface evidence |
| Common rule substrate | root shim and provider docs | `AGENTS.md`, `.codex/`, provider docs | `GEMINI.md`, `.agents/`, provider docs | Stage 00 remains the SSoT |
```

Expected: Gemini first-class subagent parity remains a gap unless official current docs prove otherwise.

- [x] **Step 5: Refresh SDLC and quality documents**

Update `spec-driven-sdlc.md` and `quality-ci-formatting.md` with:

```markdown
- Docker Compose infrastructure work still follows Stage 01-05 when it changes requirements, architecture, implementation contracts, execution evidence, or operations behavior.
- QA covers formatting, linting, syntax checks, documentation contracts, Compose rendering, hardening, security baselines, and CI-only gates as separate evidence classes.
- Secure SDLC frameworks remain references unless adopted through a separate approved policy/spec/task.
```

Expected: no active policy wording says the frameworks are adopted.

- [x] **Step 6: Validate refreshed existing docs**

Run:

```bash
git diff --check
rg -n "TBD|TODO|FIXME|\\[.*\\]|\\{.*\\}|first-class subagent parity" docs/90.references/research/2026-07-05-agentic-research-pack-refresh -g '*.md'
bash scripts/validation/check-repo-contracts.sh
```

Expected: `git diff --check` has no output; placeholder scan has no unresolved template placeholders; repo contract reports `failures=0`. The phrase `first-class subagent parity` may appear only in a caveat/gap context.

- [x] **Step 7: Commit existing research refresh**

Run:

```bash
git add docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md
git commit -m "docs(research): Refresh agentic engineering research pack"
```

Expected: commit succeeds.

### Task 4: Add Targeted Reference Documents If Needed

**Files:**
- Create if needed: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md`
- Create if needed: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md`
- Create if needed: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md`
- Modify if pack structure changes: `docs/90.references/research/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`

- [x] **Step 1: Decide targeted additions**

Use this decision rule:

```text
Create docker-compose-infrastructure.md when Docker Compose, profiles, networking, secrets, infrastructure validation, and runtime boundary analysis would take more than one focused section in workspace-baseline.md or quality-ci-formatting.md.
Create security-governance.md when secure SDLC, secret boundaries, workflow security, container security, supply-chain controls, and provider approvals would take more than one focused section in quality-ci-formatting.md.
Create automation-pipeline-workflow.md when automation, pipeline, provider hooks, GitHub Actions, workflow orchestration, and loop engineering would make loop-engineering.md too broad.
```

Expected: task evidence records `Created` or `N/A - covered by refreshed existing documents` for each targeted file.

- [x] **Step 2: Create Docker Compose / infrastructure reference if needed**

If needed, create `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md` with these exact sections:

```markdown
---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md -->

# Reference: Docker Compose and Infrastructure Harness

## Overview

This reference analyzes Docker Compose and infrastructure as part of the workspace harness. It compares official Docker Compose guidance with repo-local Compose, infra, validation, hardening, network, and secret boundaries.

## Purpose

Explain how Docker Compose and infrastructure evidence support agentic harness engineering without replacing runtime configuration.

## Repository Role

This reference supports Stage 00 governance, infra docs, HAFE documents, and Stage 90 research. It does not define runtime Compose behavior or operations procedures.

## Scope

### In Scope

- Compose project, service, profile, network, volume, secret, and validation concepts
- Repo-local infrastructure evidence and validation scripts
- Infrastructure follow-up gaps

### Out of Scope

- Runtime Compose edits
- Secret values
- Deployment execution
- Active operations runbooks

## Definitions / Facts

Add source-backed facts from Docker Compose official docs and repo-local files.

## Analysis

Map official Compose concepts to `docker-compose.yml`, `infra/`, validation scripts, hardening checks, and Stage 90 reference boundaries.

## Potential Follow-up / Gap

Record only follow-up gaps; do not fix them in this document.

## Source Rules

- Prefer Docker official docs and repo-local canonical files.
- Re-check Docker facts before using them for active runtime decisions.

## Sources

- Docker Compose docs: `https://docs.docker.com/compose/` - Compose product and workflow context
- Compose file reference: `https://docs.docker.com/reference/compose-file/` - service, network, volume, profile, and secret syntax
- Use secrets in Compose: `https://docs.docker.com/compose/how-tos/use-secrets/` - Compose secret handling
- Production guidance: `https://docs.docker.com/compose/how-tos/production/` - production-oriented Compose guidance
- Root Compose file: `../../../../docker-compose.yml` from the target reference document - repo-local root include and profile context
- infra README: `../../../../infra/README.md` from the target reference document - repo-local infrastructure index
- Compose validation script: `../../../../scripts/validation/validate-docker-compose.sh` from the target reference document - repo-local Compose validation gate

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Docker Compose guidance, `infra/`, root Compose, or validation scripts change
- **Update Trigger**: Update when infrastructure harness assumptions or runtime validation boundaries change

## Related Documents

- research pack index: `./README.md`
- workspace baseline: `./workspace-baseline.md`
- quality, CI, and formatting: `./quality-ci-formatting.md`
- HAFE spec: `../../../03.specs/094-harness-agent-first-engineering/spec.md`
```

Then replace "Add source-backed facts..." and "Map official..." paragraphs with actual researched content before commit.

- [x] **Step 3: Create security governance reference if needed**

If needed, create `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md` with the same reference template sections and sources for:

```text
NIST SSDF
OWASP SAMM
SLSA
GitHub Actions secure use
Docker security / secrets
repo-local .github/SECURITY.md
repo-local security scope
repo-local GitHub governance
repo-local template/security baseline
```

Expected: document distinguishes reference frameworks from adopted active policy.

- [x] **Step 4: Create automation/pipeline/workflow reference if needed**

If needed, create `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md` with the same reference template sections and sources for:

```text
GitHub Actions workflow syntax
GitHub Actions jobs
provider hooks and automation docs
repo-local scripts README
repo-local CI workflow
repo-local workflows rule
repo-local provider surfaces
```

Expected: document distinguishes local automation evidence from remote action approval.

- [x] **Step 5: Update research README indexes**

If any targeted document is created, update `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md`:

```markdown
├── docker-compose-infrastructure.md      # Docker Compose and infrastructure harness analysis
├── security-governance.md                # Secure SDLC and security governance analysis
└── automation-pipeline-workflow.md       # Automation, pipeline, and workflow analysis
```

Add matching `Current References` rows and reading-order guidance. Update `docs/90.references/research/README.md` only if the parent pack summary needs to name the expanded structure.

- [x] **Step 6: Validate targeted additions**

Run:

```bash
git diff --check
bash scripts/validation/check-repo-contracts.sh
```

Expected: no whitespace issues and `failures=0`.

- [x] **Step 7: Commit targeted additions**

Run:

```bash
git add docs/90.references/research/2026-07-05-agentic-research-pack-refresh docs/90.references/research/README.md docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md
git commit -m "docs(research): Add targeted agentic engineering references"
```

Expected: commit succeeds if files were added. If no targeted files were needed, commit only task evidence with the N/A rationale using message `docs(tasks): Record targeted research additions rationale`.

### Task 5: Finalize Validation, Progress, and Index Freshness

**Files:**
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`
- Modify if generated: `docs/90.references/llm-wiki/llm-wiki-index.md`

- [x] **Step 1: Run final validation gates**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected:

```text
git diff --check: no output
generate-llm-wiki-index.sh --check: PASS
sync-provider-surfaces.sh --check: no drift
check-doc-traceability.sh: failures=0
check-doc-implementation-alignment.sh: failures=0
check-repo-contracts.sh: failures=0
```

- [x] **Step 2: Regenerate LLM Wiki index if freshness fails**

Run only if `--check` fails:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
```

Expected: `docs/90.references/llm-wiki/llm-wiki-index.md` updates and the subsequent `--check` passes.

- [x] **Step 3: Update task evidence final summary**

In `docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md`, set all work items to `Done` or `N/A` and add validation results:

```markdown
## Verification Summary

| Check | Result | Evidence |
| --- | --- | --- |
| `git diff --check` | Pass | No output |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Pass | LLM Wiki index fresh |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | Pass | no drift |
| `bash scripts/validation/check-doc-traceability.sh` | Pass | failures=0 |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | Pass | failures=0 |
| `bash scripts/validation/check-repo-contracts.sh` | Pass | failures=0 |
```

- [x] **Step 4: Update progress memory**

Add a new English section to `docs/00.agent-governance/memory/progress.md` before `## Open Issues`:

```markdown
## Agentic Research Pack Refresh (2026-07-05)

| Item | Area | Status | Notes |
| ---- | ---- | ------ | ----- |
| Existing research refresh | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/*.md` | ✅ Updated | Revalidated and refreshed source-backed coverage for workspace baseline, harness, loop, provider comparison, SDLC, QA, CI/CD, formatting, linting, syntax checks, automation, pipeline, workflow, Docker Compose, infrastructure, and security. |
| Targeted additions | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` | ✅ Updated | Added targeted reference documents where needed, or recorded N/A rationale in task evidence when existing refreshed documents remained sufficient. |
| Protected surfaces | runtime, Compose, scripts, validators, workflows, secrets | ✅ Preserved | This batch changed research references, task evidence, README indexes, and progress memory only; no runtime config, Compose, validator, workflow behavior, provider runtime, secret material, `.env`, or remote GitHub state changed. |
| Validation | Local documentation contracts | ✅ Pass | Final validation gates passed with `failures=0`. |
```

- [x] **Step 5: Commit final evidence**

Run:

```bash
git add docs/00.agent-governance/memory/progress.md docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md docs/90.references/llm-wiki/llm-wiki-index.md
git commit -m "docs(research): Finalize agentic research refresh evidence"
```

Expected: commit succeeds. If `llm-wiki-index.md` did not change, `git add` safely stages no change for that path.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Whitespace and conflict-marker hygiene | `git diff --check` | No output |
| VAL-PLN-002 | Reference index | LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-003 | Provider parity | Provider surface sync | `bash scripts/operations/sync-provider-surfaces.sh --check` | `no drift` |
| VAL-PLN-004 | Traceability | Execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | `failures=0` |
| VAL-PLN-005 | Implementation alignment | Active docs align with tracked surfaces | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0` |
| VAL-PLN-006 | Repo contracts | Stage, template, language, reference, security, and script contracts | `bash scripts/validation/check-repo-contracts.sh` | `failures=0` |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fast-moving provider documentation changes during the work | Medium | Revalidate official provider docs during Task 2 and avoid version-specific claims unless supported. |
| Research text turns into active policy | High | Keep recommendations in `Potential Follow-up / Gap`; do not edit Stage 00 policy or Stage 05 policy documents. |
| Existing documents become too broad | Medium | Add one targeted reference document rather than overloading existing files. |
| Gemini capability overclaim | High | Treat Gemini first-class subagent parity as a gap unless official current sources prove otherwise. |
| External source unavailable | Medium | Use another official source or record the source gap in task evidence. |
| Validation failure from unrelated drift | Medium | Record exact failure as out of scope and do not patch unrelated surfaces. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: N/A - no model or prompt behavior is promoted.
- **Sandbox / Canary Rollout**: N/A - documentation-only work.
- **Human Approval Gate**: Required before expanding scope into active policy, runtime, CI workflow, provider config, or secrets.
- **Rollback Trigger**: Revert the relevant documentation commit if reference docs introduce unsupported source claims or violate Stage 90 boundaries.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Task evidence exists and links to this plan, the Stage 03 spec, and the research pack.
- [x] External source inventory is revalidated and summarized.
- [x] Existing research documents are refreshed.
- [x] Targeted reference documents are added or N/A rationale is recorded.
- [x] README indexes are updated when structure changes.
- [x] Progress memory is updated.
- [x] Final validation gates pass or unrelated failures are recorded as out of scope.
- [x] Logical commits exist for the plan, task evidence/source inventory, research refresh, targeted additions/rationale, and final evidence.

## Related Documents

- **Spec**: [Agentic Research Pack Refresh Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md)
- **Research Pack**: [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Research References**: [Research References](../../90.references/research/README.md)
- **Task**: [Agentic Research Pack Refresh Task](../tasks/2026-07-05-agentic-research-pack-refresh.md)
- **Reference Template**: [Reference Template](../../99.templates/templates/common/reference.template.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
