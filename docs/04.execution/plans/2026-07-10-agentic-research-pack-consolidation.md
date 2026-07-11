---
status: active
---

<!-- Target: docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md -->

# Agentic Research Pack Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate the workspace's agentic engineering research into one current Stage 90 pack with source-backed workspace comparisons and a provider-model landscape fixed at 2026-07-10 10:00 KST.

**Architecture:** Refresh the existing 2026-07-05 pack in place, split research by one-document ownership, and add only `provider-model-landscape.md` for the full Claude/OpenAI-Codex/Gemini lifecycle inventory. Merge verified unique material from the 2026-07-07 duplicate, replace that pack with supersession mappings, and preserve completed Stage 03/04 and audit artifacts as linked historical evidence.

**Tech Stack:** Markdown, Stage 03/04/90 templates, tracked repository evidence, official vendor and standards documentation, Superpowers task briefs/review packages, Git, and repository documentation validators.

## Global Constraints

- The 2026-07-05 research pack is the only active canonical pack; do not create a 2026-07-10 replacement pack.
- Provider model evidence is fixed at 2026-07-10 10:00 KST (01:00 UTC).
- Cover the official Claude, OpenAI/Codex, and Gemini model catalogs, preserving provider-native status and mapping to `stable`, `preview`, or `deprecated` only when supported.
- Use `historical state unverified` when a mutable official page cannot prove the cutoff state.
- Every research category includes workspace current state, external primary-source research, comparison, `Implemented` / `Partially Implemented` / `Missing` / `Not Applicable` status, gap, recommendation, canonical owner, evidence, and confidence.
- Repo-local claims come from tracked source and active stage documents; Graphify is advisory and must be corroborated.
- Preserve completed Stage 03/04 and audit artifacts as linked history; do not copy or delete their full bodies.
- Merge verified unique 2026-07-07 material once, remove unsupported claims, and mark the duplicate pack and its leaf references `status: superseded`.
- Do not change active policy, runtime Compose, infrastructure, CI workflows, provider adapters, model policy, hooks, scripts, operations procedures, secrets, credentials, remote GitHub state, or branch protection.
- Non-README Stage 03, Stage 04, and Stage 90 research documents remain English.
- Use logical commits and a clean spec-compliance plus document-quality review gate after every task.

---

## Overview

This plan implements
[Spec 122](../../03.specs/122-agentic-research-pack-consolidation/spec.md).
The specification covers one cohesive documentation product rather than
independent runtime subsystems: every research domain feeds the same canonical
pack, cutoff contract, status vocabulary, source rules, index, and supersession
boundary. The plan therefore keeps one workstream but gives each domain a
self-contained mutation, validation, review, and commit cycle.

## Context

The canonical 2026-07-05 pack already contains thirteen focused references.
The 2026-07-07 update duplicates five of them and includes claims that conflict
with current tracked evidence, including Codex adapter allowlists, shared
Prettier execution, network isolation, CI job naming, execution-artifact paths,
and provider-adapter generation. The user approved consolidating all verified
research into the canonical pack, superseding the duplicate, and adding the
official provider-model landscape at an exact cutoff.

Current tracked implementation and active governance remain the source of truth
for the workspace. External sources supply comparison criteria and current
provider capabilities, not authorization to mutate active policy or runtime
surfaces.

## Goals & In-Scope

- **Goals**:
  - Revalidate every requested workspace category against current tracked
    implementation and external primary sources.
  - Add a cutoff-bound provider model inventory without overloading the existing
    task-selection reference.
  - Correct stale or unsupported research claims.
  - Consolidate unique prior material once and supersede the duplicate pack.
  - Preserve traceability through Stage 04 evidence, logical commits, and
    reviewer gates.
- **In Scope**:
  - Spec 122 lifecycle and Stage 03 index status.
  - The canonical 2026-07-05 Stage 90 research pack.
  - The duplicate 2026-07-07 Stage 90 research pack's supersession records.
  - Research-category indexes, generated LLM Wiki index when required, Stage 04
    plan/task evidence, and Stage 00 progress memory.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Adopting external practices as active policy.
  - Updating workspace model values to match vendor catalogs.
  - Implementing research gaps.
  - Redesigning unrelated reference, audit, operations, or provider surfaces.
- **Out of Scope**:
  - Runtime Compose, infrastructure, workflows, scripts, hooks, provider
    adapters, model policy, secrets, credentials, remote settings, branch
    protection, and operations procedures.
  - Deleting completed specifications, plans, tasks, or audit reports.
  - Persisting raw web pages, diagnostics, shell history, logs, or secret
    material.

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md` | Source ledger, task states, commit ranges, review outcomes, deviations, and verification evidence. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md` | Workspace-wide current-state and category routing. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md` | Spec-driven lifecycle and feedback chain. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md` | PRD/ARD/ADR/Spec/Plan/Task/Guide/Policy/Runbook/Incident/Postmortem/Release roles. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md` | New cutoff-bound provider model inventory. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md` | Task-to-model/effort analysis and workspace-policy comparison. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md` | Harness components and workspace requirements. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md` | Agent, eval, validation, CI, approval, and human loops. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md` | Provider harness/loop/subagent/hook/sandbox comparison. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md` | Curated agent catalogs and `agency-agents` comparison. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md` | CI/CD, QA, formatting, linting, syntax, build, coverage, and security gates. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md` | Local/CI/provider automation and authority loops. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md` | Compose/infrastructure harness and validation. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md` | Secure SDLC, approvals, secrets, hardening, and supply-chain analysis. |
| `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md` | Canonical pack structure, ownership, and reading order. |
| `docs/90.references/research/2026-07-07-agentic-research-pack-update/*.md` | Superseded mappings after verified content migration. |
| `docs/90.references/research/README.md` | Current versus superseded pack routing. |
| `docs/90.references/llm-wiki/llm-wiki-index.md` | Generated path index, updated only through its generator when stale. |
| `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` | Generated stage/category coverage snapshot, updated only through its generator when stale. |
| `docs/03.specs/122-agentic-research-pack-consolidation/{README.md,spec.md}` | Approved design lifecycle, completed only after implementation closes. |
| `docs/{03.specs,04.execution/plans,04.execution/tasks}/README.md` | Canonical stage indexes. |
| `docs/00.agent-governance/memory/progress.md` | Material milestone and final verification log. |

## Source Entry Points

Use these direct primary-source entry points and follow only official links
needed for the assigned task:

- Anthropic models and lifecycle:
  - <https://platform.claude.com/docs/en/about-claude/models/overview>
  - <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>
  - <https://platform.claude.com/docs/en/about-claude/model-deprecations>
  - <https://platform.claude.com/docs/en/release-notes/overview>
- Claude Code:
  - <https://code.claude.com/docs/en/overview>
  - <https://code.claude.com/docs/en/sub-agents>
  - <https://code.claude.com/docs/en/hooks>
  - <https://code.claude.com/docs/en/configuration>
- OpenAI models and lifecycle:
  - <https://developers.openai.com/api/docs/models/all>
  - <https://developers.openai.com/api/docs/deprecations>
- Codex:
  - <https://developers.openai.com/codex/subagents>
  - <https://developers.openai.com/codex/hooks>
  - <https://developers.openai.com/codex/security>
  - <https://developers.openai.com/codex/config-reference>
  - <https://developers.openai.com/codex/guides/agents-md>
- Gemini models and lifecycle:
  - <https://ai.google.dev/gemini-api/docs/models>
  - <https://ai.google.dev/gemini-api/docs/deprecations>
  - <https://ai.google.dev/gemini-api/docs/changelog>
- Gemini CLI:
  - <https://google-gemini.github.io/gemini-cli/docs/>
  - <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html>
  - <https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html>
- Docker Compose:
  - <https://docs.docker.com/compose/>
  - <https://docs.docker.com/compose/how-tos/profiles/>
  - <https://docs.docker.com/compose/how-tos/networking/>
  - <https://docs.docker.com/compose/how-tos/use-secrets/>
  - <https://docs.docker.com/compose/how-tos/production/>
  - <https://docs.docker.com/compose/trust-model/>
- CI/CD and security:
  - <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
  - <https://docs.github.com/en/actions/reference/security/secure-use>
  - <https://pre-commit.com/>
  - <https://csrc.nist.gov/pubs/sp/800/218/final>
  - <https://owasp.org/www-project-samm/>
  - <https://slsa.dev/>
- Spec-driven SDLC and document roles:
  - <https://github.github.com/spec-kit/>
  - <https://github.com/github/spec-kit/blob/main/spec-driven.md>
  - <https://www.iso.org/standard/63712.html>
  - <https://www.iso.org/standard/72089.html>
  - <https://www.iso.org/standard/74393.html>
  - <https://adr.github.io/>
  - <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
  - <https://sre.google/sre-book/managing-incidents/>
  - <https://sre.google/sre-book/postmortem-culture/>
  - <https://csrc.nist.gov/pubs/sp/800/61/r3/final>
  - <https://www.pagerduty.com/resources/learn/what-is-a-runbook/>
  - <https://keepachangelog.com/en/1.1.0/>
  - <https://semver.org/>
- Agent and loop foundations:
  - <https://arxiv.org/abs/2210.03629>
  - <https://arxiv.org/abs/2303.11366>
  - <https://github.com/msitarzewski/agency-agents>

Every implementation task must confirm that a mutable source is current at
retrieval time and separately decide whether it proves the approved cutoff.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-ARC-001 | Refresh workspace baseline, spec-driven SDLC, document roles, and execution evidence | Task evidence plus three canonical research references | VAL-ARC-002, VAL-ARC-007, VAL-ARC-009 | All requested workspace/SDLC/document categories have repo-local and external comparison records. |
| PLN-ARC-002 | Add provider model landscape and refresh task-characteristic selection | New model landscape, model selection, task evidence | VAL-ARC-003, VAL-ARC-004 | Every official cutoff model has lifecycle/evidence fields; task-fit analysis is labeled as inference. |
| PLN-ARC-003 | Consolidate harness, loop, provider, and agent-catalog research | Four canonical research references plus task evidence | VAL-ARC-002, VAL-ARC-005 | Provider capabilities match official sources and current adapters; duplicate valid content exists once. |
| PLN-ARC-004 | Refresh QA/CI/formatting and automation/pipeline/workflow research | Two canonical research references plus task evidence | VAL-ARC-002, VAL-ARC-008 | Local/CI/remote boundaries and actual gate names match tracked implementation. |
| PLN-ARC-005 | Refresh Docker Compose/infrastructure and security governance research | Two canonical research references plus task evidence | VAL-ARC-002, VAL-ARC-008 | Compose/security claims match tracked files and primary guidance; policy conflicts remain advisory gaps. |
| PLN-ARC-006 | Finalize canonical indexes and supersede duplicate pack, then close lifecycle after broad review | Pack/index/supersession files, Stage 03/04 status, generated outputs if needed, progress memory | VAL-ARC-001, VAL-ARC-005, VAL-ARC-006, VAL-ARC-007, VAL-ARC-008, VAL-ARC-009, VAL-ARC-010 | Only one active pack remains; Task 6 review passes; a later closure commit records clean broad review and all final checks. |

## Task Details

### Task 1: Workspace Baseline, SDLC, Document Roles, and Evidence

**Files:**

- Modify: `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md`

**Interfaces:**

- Consumes: Spec 122 global constraints, Stage 00 governance, root and stage
  READMEs, templates, workflows, scripts, Compose inventory, existing research,
  and primary SDLC/document sources.
- Produces: The shared workspace category map, comparison-record vocabulary,
  canonical document-role matrix, and source ledger used by later tasks.

- [ ] **Step 1: Establish the tracked workspace evidence inventory**

Run:

```bash
rg -n "^(#|##|###) |purpose|CI/CD|QA|Formatting|Lint|Automation|SDLC|Security|Agent" README.md AGENTS.md docs/README.md docs/00.agent-governance/README.md docs/00.agent-governance/rules docs/00.agent-governance/providers scripts/README.md infra/README.md .github/workflows/ci-quality.yml
```

Expected: paths and headings for workspace purpose, stages, provider rules,
quality gates, automation, infrastructure, and security are visible; no claim
is taken from Graphify without a tracked-file match.

- [ ] **Step 2: Revalidate external SDLC and document-role sources**

Open every URL under `Spec-driven SDLC and document roles` in
`## Source Entry Points`, plus the GitHub Actions workflow syntax and NIST
SSDF URLs in the preceding source groups. Record in the task evidence: direct
URL, source owner, supported claim, publication/update date when shown,
retrieval date `2026-07-10`, and caveat.

Expected: PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
Postmortem, and Release each have an external or repo-template basis; no source
is treated as adopted policy.

- [ ] **Step 3: Normalize the workspace comparison map**

Update `workspace-baseline.md` so each requested category has these exact
columns:

```markdown
| Category | Workspace evidence | External evidence | Status | Gap / risk | Recommendation | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Required category rows: purpose, overview, roles, CI/CD, QA, formatting,
linting, syntax/type checks, automation, pipeline, workflow, operating
contracts, templates, scripts, integration guides, SDLC, governance, system
structure, rules, security, Docker Compose/infrastructure, AI agents, harness
engineering, loop engineering, and task-characteristic model selection.

- [ ] **Step 4: Refresh spec-driven lifecycle analysis**

Update `spec-driven-sdlc.md` with one evidence-backed flow:

```text
intent → PRD → ARD/ADR → Spec → Plan → Task/Evidence → Operations/Release
       ↖ incident/postmortem learning + eval/QA/security feedback ↙
```

For each transition, state the repo-local owner, entry/exit evidence, validation
gate, feedback loop, and external comparison. Keep Compose, CI, and secure SDLC
as lifecycle participants, not replacements for stage documents.

- [ ] **Step 5: Refresh the document-role matrix**

Update `sdlc-document-roles.md` with these exact columns:

```markdown
| Document | Primary question | Authoring trigger | Owner | Inputs | Outputs / consumers | Lifecycle status | Workspace template / path | External basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Include separate rows for PRD, ARD, ADR, Spec, API/agent/data/test supporting
contracts, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, Release
notes/changelog, Reference, Audit, and Archive tombstone.

- [ ] **Step 6: Record task evidence**

In the Stage 04 task document, mark `T-ARC-001` Done only after recording:
source inventory, changed files, the workspace category count, document-role
row count, exact verification commands, results, commit range, and reviewer
verdicts. Do not paste raw web or shell output.

- [ ] **Step 7: Run covering documentation checks**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: all commands exit 0; repository validators report `failures=0`.

- [ ] **Step 8: Commit Task 1**

```bash
git add docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md
git commit -m "docs(research): refresh workspace and SDLC references"
```

### Task 2: Provider Model Landscape and Task Selection

**Files:**

- Create: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md`
- Modify: `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`

**Interfaces:**

- Consumes: Provider model/lifecycle source entry points, cutoff contract,
  `subagent-protocol.md` Model Policy, provider adapters, and Task 1 status
  vocabulary.
- Produces: The complete cutoff inventory and task-fit matrix referenced by the
  provider, agent-catalog, and pack-index tasks.

- [ ] **Step 1: Build the cutoff evidence ledger**

For Anthropic, OpenAI, and Google, inspect the official model list, model ID,
release-note/changelog, deprecation, and CLI configuration pages in
`## Source Entry Points`. Record every model that is active, preview,
experimental/latest, legacy/deprecated, or otherwise lifecycle-relevant at
`2026-07-10 10:00 KST (01:00 UTC)`.

Expected: the ledger distinguishes page retrieval state from cutoff proof; any
post-cutoff announcement is excluded from the comparison and any mutable page
without historical proof is labeled `historical state unverified`.

- [ ] **Step 2: Create the provider model reference from the Stage 90 template**

Create `provider-model-landscape.md` with all reference-template sections and
this exact provider table schema:

```markdown
| Provider | Official name | Model ID / alias | Provider-native status | Normalized lifecycle | Release / cutoff evidence | Availability surfaces | Context / modalities | Reasoning control | Tool / agent / coding characteristics | Cutoff disposition | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Add separate provider subsections, a cross-provider terminology map, a
workspace-policy comparison, source rules, maintenance date, and direct source
notes. Do not normalize provider-native reasoning or maturity terms into false
parity.

- [ ] **Step 3: Separate fact from task-fit inference**

For every task-fit recommendation, add:

```markdown
| Task characteristic | Required capabilities | Claude option | OpenAI/Codex option | Gemini option | Latency/cost consideration | Evidence basis | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Label the table as analysis inferred from official capability descriptions plus
the workspace task taxonomy. Do not present benchmark rank, marketing language,
or provider recommendation as a guaranteed workspace result.

- [ ] **Step 4: Refresh workspace model-selection analysis**

Update `agent-model-selection.md` so it:

- links the full catalog to `provider-model-landscape.md`;
- treats the Stage 00 Model Policy as current workspace SSoT;
- compares, but does not change, supervisor/worker model values and reasoning
  effort;
- documents exact approved-change surfaces: Model Policy, adapter generator,
  generated adapters, validators, Stage 04 evidence, and provider sync;
- records stale values or unsupported availability as gaps.

- [ ] **Step 5: Record model evidence and coverage**

In the task document, record per-provider model-row totals, lifecycle totals,
cutoff exceptions, source URLs, mutable-page caveats, changed files, commands,
commit range, and reviewer verdicts. Mark `T-ARC-002` Done only when no model
row lacks a lifecycle and cutoff disposition.

- [ ] **Step 6: Run covering checks**

Run:

```bash
git diff --check
rg -n "2026-07-10 10:00 KST|stable|preview|deprecated|historical state unverified|Provider-native status|Normalized lifecycle" docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-repo-contracts.sh
```

Expected: the targeted scan finds the cutoff and lifecycle contract; all scripts
exit 0; provider sync reports no drift; repo contracts report `failures=0`.

- [ ] **Step 7: Commit Task 2**

```bash
git add docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md
git commit -m "docs(research): add provider model landscape"
```

### Task 3: Harness, Loop, Provider, and AI Agent Catalogs

**Files:**

- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`
- Modify: `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`

**Interfaces:**

- Consumes: Task 1 workspace vocabulary, Task 2 model catalog, local Stage 00
  provider/agent/hook evidence, official Claude/Codex/Gemini CLI sources,
  ReAct/Reflexion papers, and `agency-agents`.
- Produces: Current harness/loop/provider matrices and the curated external-agent
  import boundary.

- [ ] **Step 1: Inventory current provider implementation**

Read:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
docs/00.agent-governance/providers/
docs/00.agent-governance/subagent-protocol.md
docs/00.agent-governance/harness-implementation-map.md
.claude/
.codex/
.agents/
scripts/hooks/
scripts/operations/sync-provider-surfaces.sh
```

Record only tracked facts: adapter fields, context discovery, hooks, subagents,
sandbox/approval, tool permissions, model selection, lifecycle events, and
provider sync/generation behavior.

- [ ] **Step 2: Revalidate provider capabilities**

Use only the official Claude Code, Codex, Gemini CLI, and Gemini API entry
points in this plan. For every capability row, record provider, surface,
official URL, documented maturity, cutoff relevance, workspace adapter, and
confidence.

Expected: lack of evidence is recorded as unknown or missing, not provider
parity.

- [ ] **Step 3: Refresh the harness matrix**

In `harness-engineering.md`, use:

```markdown
| Harness element | Workspace implementation | External/provider pattern | Status | Required environment/rule | Gap / risk | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Include isolation, filesystem/network boundaries, tool routing, context/JIT
loading, agent catalog, model routing, hooks, approvals, test/eval harnesses,
Compose/infrastructure harness, security harness, observability/evidence,
rollback, and human escalation.

- [ ] **Step 4: Refresh the loop matrix**

In `loop-engineering.md`, describe exact inputs, actions, evidence, exit
conditions, retry limits, and escalation for:

- inner reason/action/tool loop;
- validation/format/lint loop;
- CI gate loop;
- eval/regression loop;
- memory/context loop;
- plan/task/review loop;
- security/approval loop;
- automation/pipeline loop;
- incident/postmortem learning loop;
- human-in-the-loop pause/resume loop.

Use ReAct and Reflexion as research foundations, not product-policy authority.

- [ ] **Step 5: Refresh provider implementation comparison**

In `provider-implementation-comparison.md`, use:

```markdown
| Capability | Claude | Codex | Gemini | Common workspace substrate | Gap / normalization rule | Evidence date |
| --- | --- | --- | --- | --- | --- | --- |
```

Explicitly prevent these stale claims from being carried forward:

- Codex agent TOMLs contain strict tool/path allowlists;
- the shared post-tool runner executes `prettier --check`;
- adapter auto-scaffolding is absent;
- all workspace networks block external bridges;
- canonical execution artifacts are `implementation_plan.md` and
  `walkthrough.md`.

- [ ] **Step 6: Refresh AI agent catalog analysis**

Compare `msitarzewski/agency-agents` with the curated local catalog using:

```markdown
| Catalog concern | agency-agents pattern | Workspace pattern | Importability | Required wrapper/control | Recommendation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
```

Cover persona breadth, role boundaries, prompt portability, scope imports,
tools/permissions, model tier, lifecycle, handoffs, evidence, security, evals,
and direct-import risks. Do not vendor external agent identities or prompts.

- [ ] **Step 7: Record evidence and review**

Update `T-ARC-003` with source URLs, current adapter paths, corrected stale
claims, changed files, commands, commit range, and reviewer verdicts. Mark Done
only when every provider capability row has a direct official source or an
explicit evidence gap.

- [ ] **Step 8: Run covering checks**

```bash
git diff --check
rg -n "implementation_plan\.md|walkthrough\.md|prettier --check|strict tool|auto-scaffolding|all.*networks" docs/90.references/research/2026-07-05-agentic-research-pack-refresh/{harness-engineering,loop-engineering,provider-implementation-comparison,ai-agent-catalogs}.md
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: targeted output contains no unsupported current-state assertion; all
scripts exit 0 and repo contracts report `failures=0`.

- [ ] **Step 9: Commit Task 3**

```bash
git add docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md
git commit -m "docs(research): consolidate harness and agent research"
```

### Task 4: QA, CI/CD, Formatting, Automation, Pipelines, and Workflows

**Files:**

- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md`
- Modify: `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`

**Interfaces:**

- Consumes: `.github/workflows/`, pre-commit/tool configuration,
  `scripts/validation/`, `scripts/hooks/`, GitHub Actions and quality-tool
  primary sources, and Task 1 workspace categories.
- Produces: Accurate local/CI/remote gate taxonomy and automation-loop mapping.

- [ ] **Step 1: Inventory actual local and CI gates**

Run:

```bash
rg -n "^  [a-z0-9_-]+:|name:|run:|uses:" .github/workflows/*.yml
rg -n "entry:|id:|language:|files:|exclude:" .pre-commit-config.yaml
rg -n "^(#|##|###) |run-local-qa-gates|recommend-qa-gates|post-tool|provider" scripts/README.md scripts/validation scripts/hooks
```

Expected: actual workflow job IDs, local gates, format/lint/syntax/type/build/
coverage/security tools, and provider hook entrypoints are enumerated.

- [ ] **Step 2: Revalidate external quality and workflow sources**

Use these exact sources: GitHub Actions workflow syntax and secure-use URLs
from `## Source Entry Points`, <https://pre-commit.com/>,
<https://editorconfig.org/>, <https://spec.editorconfig.org/>,
<https://prettier.io/docs>, <https://prettier.io/docs/cli>,
<https://dora.dev/guides/dora-metrics/>, and
<https://martinfowler.com/bliki/ContinuousDelivery.html>. Record what each
source supports and which checks are local, CI-only, or remote-only.

- [ ] **Step 3: Refresh the quality-gate matrix**

Use:

```markdown
| Gate | Purpose | Local command / tool | CI job | Evidence class | Blocking behavior | External basis | Gap / recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Include whitespace/diff, Markdown/YAML/JSON/TOML, shell syntax, ShellCheck,
actionlint, Hadolint, secret scanning, ESLint, TypeScript, build, coverage,
Compose validation, hardening, docs traceability/alignment, agent-output eval
fixtures, dependency vulnerability audit, provider drift, generated-data
freshness, and remote branch protection.

- [ ] **Step 4: Correct known QA drift**

Ensure the document:

- uses CI job ID `zizmor`, not `zizmor-security`;
- includes current tracked jobs such as `docs-implementation-alignment`,
  `agent-output-eval-fixture-gate`, and
  `dependency-vulnerability-audit`;
- states that `run-local-qa-gates.sh` separates local from CI/remote-only
  responsibility rather than fully replicating CI;
- does not claim the shared post-tool hook runs Prettier;
- distinguishes formatting, linting, syntax, type, test, build, coverage, and
  security evidence.

- [ ] **Step 5: Refresh automation and workflow loops**

Use:

```markdown
| Automation | Trigger | Authority | Inputs | Actions | Evidence | Failure / retry | Rollback / escalation | External boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Cover local validation scripts, post-tool hooks, provider-surface sync,
generated-reference checks, CI workflows, changelog verification, version sync,
PR labeling/stale automation, task/subagent orchestration, and remote approval
boundaries. State that `generate-changelog.yml` verifies pushed-tag coverage
rather than generating the changelog when that matches tracked workflow.

- [ ] **Step 6: Record task evidence**

Update `T-ARC-004` with workflow job count, local gate count, evidence-class
mapping, corrected claims, sources, changed files, commands, commit range, and
reviewer verdicts.

- [ ] **Step 7: Run covering checks**

```bash
git diff --check
rg -n "zizmor-security|prettier --check|fully replicates CI|signed rationale" docs/90.references/research/2026-07-05-agentic-research-pack-refresh/{quality-ci-formatting,automation-pipeline-workflow}.md
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: no unsupported stale phrase remains; validators exit 0 with
`failures=0`.

- [ ] **Step 8: Commit Task 4**

```bash
git add docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md
git commit -m "docs(research): refresh QA and automation references"
```

### Task 5: Docker Compose, Infrastructure, and Security Governance

**Files:**

- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md`
- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md`
- Modify: `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`

**Interfaces:**

- Consumes: root Compose, `infra/`, generated Compose coverage, hardening and
  validation scripts, Stage 00 security/approval rules, Docker/GitHub/NIST/
  OWASP/SLSA sources, and Task 1 vocabulary.
- Produces: Current infrastructure-harness and security-governance comparisons
  with advisory gap ownership.

- [ ] **Step 1: Revalidate tracked Compose and infrastructure truth**

Run:

```bash
rg -n "^include:|^  - path:|^networks:|external:|internal:|profiles:|secrets:|healthcheck:|restart:" docker-compose.yml infra -g 'docker-compose*.yml' -g 'compose*.yml'
rg -n "variant|service|profile|include|network" docs/90.references/data/docker/compose-profile-service-coverage.md infra/README.md
```

Expected: root includes, variants, service directories, profiles, networks,
secrets, healthchecks, and validation surfaces are derived from tracked files.
Recheck all counts instead of copying the prior 17/48/40 observations.

- [ ] **Step 2: Revalidate Docker guidance**

Use the Compose overview, profiles, networking, secrets, production, and trust
model pages. Record which recommendation applies to local development,
single-host production, multi-project networking, secret delivery, or untrusted
Compose execution. Do not treat a Docker example as a workspace mandate.

- [ ] **Step 3: Refresh the infrastructure comparison**

Use:

```markdown
| Infrastructure concern | Workspace evidence | Docker/external basis | Status | Risk / limitation | Required harness/control | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Cover root includes, variants, profiles, project names, internal/external
networks, service discovery, ports, volumes, secrets, healthchecks,
dependencies, restart behavior, production overlays, hardening, validation,
observability, backup/restore handoff, rollback, and runbook linkage.

- [ ] **Step 4: Revalidate security sources and controls**

Read Stage 00 approval boundaries/security scope, `.github/SECURITY.md`,
workflow security, pre-commit secret scanning, hardening scripts, dependency
audit gate, NIST SSDF, OWASP SAMM, SLSA, GitHub Actions secure use, Docker
secrets, and Compose trust model.

Expected: active control, reference framework, implementation gap, and remote
or human approval are distinct.

- [ ] **Step 5: Refresh the security comparison**

Use:

```markdown
| Security concern | Workspace control / evidence | External basis | Status | Gap / conflict | Recommendation | Canonical owner | Approval boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Cover threat boundaries, least privilege, sandbox/approval, secret redaction,
Compose secrets, action pinning, workflow permissions, dependency scanning,
container hardening, SBOM, signing/attestation, provenance, Scorecard,
incident/response handoff, and model/provider change approval.

Record, but do not resolve, the current tension between an unconditional ban on
secret-value reads in `approval-boundaries.md` and approved scoped reads
described by `scopes/security.md`.

- [ ] **Step 6: Record task evidence**

Update `T-ARC-005` with rechecked Compose counts, source inventory, security
control/gap totals, explicit out-of-scope policy conflict, changed files,
commands, commit range, and reviewer verdicts.

- [ ] **Step 7: Run covering checks**

```bash
git diff --check
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: documentation-only changes do not alter Compose; all applicable checks
exit 0 and repo contracts report `failures=0`.

- [ ] **Step 8: Commit Task 5**

```bash
git add docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md
git commit -m "docs(research): refresh infrastructure and security references"
```

### Task 6: Canonical Index, Supersession, and Closure

**Files:**

- Modify: `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/research/2026-07-07-agentic-research-pack-update/README.md`
- Modify: `docs/90.references/research/2026-07-07-agentic-research-pack-update/workspace-baseline.md`
- Modify: `docs/90.references/research/2026-07-07-agentic-research-pack-update/harness-engineering.md`
- Modify: `docs/90.references/research/2026-07-07-agentic-research-pack-update/loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md`
- Modify: `docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md`
- Modify if stale: `docs/90.references/llm-wiki/llm-wiki-index.md`
- Modify if stale: `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`
- Modify: `docs/03.specs/122-agentic-research-pack-consolidation/README.md`
- Modify: `docs/03.specs/122-agentic-research-pack-consolidation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md`
- Modify: `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: Approved outputs and clean task reviews from Tasks 1-5.
- Produces in Steps 1-9: one active canonical pack, a complete supersession
  ledger, and provisional validation evidence for Task 6 review. Closed Stage
  03/04 lifecycle and whole-branch review packages are deferred to Steps 10-12.

**Provisional implementation state:** Tasks 1-5 have final PASS/APPROVED
reviews. Task 6 Steps 1-8 prepare a 35-row category/criterion ownership audit,
a 30-family duplicate-claim disposition ledger, canonical/superseded routing,
and the required gate evidence. Step 9 is the logical implementation commit.
T-ARC-006, all Completion Criteria, the Task 6 reviewer verdict, Steps 10-12,
and lifecycle completion remain open.

- [ ] **Step 1: Run the requested-category coverage audit**

Build a task-evidence matrix mapping every original user category and Spec 122
success criterion to one canonical document and section. Reject:

- an uncovered category;
- the same rule or fact owned by multiple canonical documents;
- a provider/model claim without primary evidence;
- a 2026-07-07 unique claim not dispositioned as merged, unsupported, duplicate,
  or historical-only.

Expected: every item has exactly one primary owner and an evidence link.

- [ ] **Step 2: Update the canonical pack README**

Add `provider-model-landscape.md` to Structure, Current References, and Reading
Order. Add a consolidation note stating:

- 2026-07-05 is the only active canonical pack;
- verified 2026-07-07 content has been merged;
- the duplicate pack is superseded;
- completed Stage 03/04 and audits remain historical evidence;
- current policy/runtime truth remains outside Stage 90.

- [ ] **Step 3: Replace duplicate leaf bodies with supersession records**

For each 2026-07-07 non-README reference:

1. set frontmatter to `status: superseded`;
2. retain its original H1 title;
3. replace current analysis with template-compliant sections:
   `Overview`, `Purpose`, `Repository Role`, `Scope`,
   `Definitions / Facts`, `Source Rules`, `Sources`, `Maintenance`,
   and `Related Documents`;
4. state the exact canonical destination(s);
5. state that unsupported claims were not carried forward;
6. preserve no stale claim as current workspace truth.

Expected: old links remain resolvable while the body cannot be mistaken for
current research.

- [ ] **Step 4: Supersede the duplicate pack README and update parent routing**

Set the duplicate README to `status: superseded`, replace Current References
and reading guidance with a canonical mapping table, and remove active-work
language. In the parent research README:

- list the 2026-07-05 pack as the only current agentic research pack;
- list 2026-07-07 under a `Superseded References` section;
- explain that readers must use the canonical pack for current facts.

- [ ] **Step 5: Prepare provisional closure evidence**

After Tasks 1-5 reviews are clean and the Task 6 coverage audit passes:

- record Tasks 1-5 commit ranges and task-review verdicts;
- keep Spec 122, this Plan, and task evidence `status: active`;
- keep `T-ARC-006` and the final Completion Criteria open;
- record source cutoff caveats, deviations, generated-output state, and the
  exact broad-review command that will follow Task 6 review;
- leave the progress entry In Progress.

Lifecycle completion is intentionally deferred until the post-task broad review
and closure sequence below. This avoids claiming completion before the review
that proves it.

- [ ] **Step 6: Regenerate LLM Wiki outputs only when stale**

Run:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

If either check fails only because tracked documentation paths/status changed,
run the corresponding canonical generator and recheck both outputs:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

Expected: both final checks exit 0. Do not edit either generated file by hand.

- [ ] **Step 7: Run final verification**

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected: all commands exit 0; sync reports no drift; repository validators
report `failures=0`.

- [ ] **Step 8: Run targeted closure scans**

```bash
rg -n "status: active" docs/90.references/research/2026-07-07-agentic-research-pack-update
rg -n "2026-07-07-agentic-research-pack-update" docs/90.references/research docs/03.specs/122-agentic-research-pack-consolidation docs/04.execution
rg -n "TBD|TODO|FIXME|implementation_plan\.md|walkthrough\.md|zizmor-security|Codex.*strict tool/path|post-tool.*prettier --check|auto-scaffolding is absent|all workspace networks" docs/90.references/research/2026-07-05-agentic-research-pack-refresh docs/90.references/research/2026-07-07-agentic-research-pack-update
```

Expected:

- the first command returns no matches;
- the second returns only supersession, traceability, and historical-evidence
  links;
- the third returns no unresolved placeholder or unsupported stale claim.

- [ ] **Step 9: Commit Task 6**

```bash
git add docs/00.agent-governance/memory/progress.md docs/03.specs/122-agentic-research-pack-consolidation docs/03.specs/README.md docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md docs/90.references/research/README.md docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md docs/90.references/research/2026-07-07-agentic-research-pack-update docs/90.references/llm-wiki/llm-wiki-index.md docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git commit -m "docs(research): supersede duplicate research pack"
```

- [ ] **Step 10: Run the first whole-branch review**

After the Task 6 task-scoped reviewer approves both spec compliance and document
quality, generate a review package from the branch merge base through current
HEAD and dispatch the final whole-branch reviewer.

Expected: no open Critical or Important finding. If findings exist, dispatch
one fix subagent with the complete finding list, rerun covering checks, and
repeat the broad review before lifecycle closure.

- [ ] **Step 11: Record closure in a separate logical commit**

After the first whole-branch review is clean, dispatch one closure subagent to:

- set Spec 122 `spec.md` and folder README to `status: completed`;
- change the Stage 03 index description from Active to Completed;
- set this Plan and its task evidence to `status: completed`;
- mark every task-table and phase-view entry Done;
- check every Completion Criteria item;
- record all task commit ranges, task-review verdicts, the clean broad-review
  package/verdict, final validation results, source cutoff caveats, and
  deviations;
- update the progress entry from In Progress to Done;
- run the complete final verification command set.

Commit:

```bash
git add docs/00.agent-governance/memory/progress.md docs/03.specs/122-agentic-research-pack-consolidation docs/03.specs/README.md docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md
git commit -m "docs(task): close agentic research consolidation"
```

- [ ] **Step 12: Re-run the whole-branch review after closure**

Generate a new whole-branch package that includes the closure commit and
dispatch the final reviewer again. If it returns findings, dispatch one fix
subagent for the complete list, require covering test evidence, and re-review
until the branch is clean.

Expected: final reviewer reports the branch ready to merge with no open
Critical or Important finding.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-ARC-001 | Patch | Whitespace and conflict hygiene | `git diff --check` | Exit 0, no output. |
| VAL-PLN-ARC-002 | Coverage | User request and Spec 122 mapping | Task evidence coverage matrix | Every category and VAL-ARC item has one canonical owner and evidence. |
| VAL-PLN-ARC-003 | Provider cutoff | Model lifecycle and cutoff completeness | Targeted model-document scan plus source ledger | Every model row has native status, normalized lifecycle, cutoff disposition, and source caveat. |
| VAL-PLN-ARC-004 | Supersession | Duplicate lifecycle and routing | Targeted `rg` scans | No active 2026-07-07 file; links are supersession or history only. |
| VAL-PLN-ARC-005 | LLM Wiki | Generated index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Exit 0. |
| VAL-PLN-ARC-006 | LLM Wiki coverage | Generated stage/category snapshot freshness | `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | Exit 0. |
| VAL-PLN-ARC-007 | Provider | Provider adapter drift | `bash scripts/operations/sync-provider-surfaces.sh --check` | Exit 0 and `no drift`. |
| VAL-PLN-ARC-008 | Traceability | Stage chain and links | `bash scripts/validation/check-doc-traceability.sh` | Exit 0 and `failures=0`. |
| VAL-PLN-ARC-009 | Implementation | Tracked implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | Exit 0 and `failures=0`. |
| VAL-PLN-ARC-010 | Infrastructure | Compose remains valid | `bash scripts/validation/validate-docker-compose.sh` | Exit 0. |
| VAL-PLN-ARC-011 | Security | Hardening contracts remain valid | `bash scripts/hardening/check-all-hardening.sh` | Exit 0. |
| VAL-PLN-ARC-012 | Repository | Full documentation/runtime contracts | `bash scripts/validation/check-repo-contracts.sh` | Exit 0 and `failures=0`. |
| VAL-PLN-ARC-013 | Review | Task and whole-branch quality | Superpowers review packages | Each task has clean spec/quality verdicts; final review has no open Critical/Important finding. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Mutable provider pages no longer expose the cutoff state | High | Use release/deprecation pages; mark `historical state unverified` rather than infer. |
| “All official models” expands into irrelevant historical catalog noise | High | Include only models lifecycle-relevant at the cutoff and keep provider-native state plus cutoff disposition. |
| Task-fit analysis becomes unsupported ranking | High | Label recommendations as inference; cite capability and workspace-task evidence; state confidence. |
| Duplicate pack content is deleted before migration | High | Complete Tasks 1-5 first; use Task 6 coverage/disposition matrix before supersession. |
| Stage 90 advice is mistaken for adopted policy | High | Repeat repository-role and out-of-scope boundaries; route each recommendation to a canonical owner. |
| Broad research tasks create conflicting edits | Medium | One sequential implementer per task; task-scoped reviewer; no parallel mutation. |
| Generated LLM Wiki index becomes stale | Medium | Run check first; regenerate only through the canonical generator. |
| Current Graphify snapshot is stale/advisory | Medium | Use it only for navigation and corroborate with tracked sources and stage docs. |
| Existing policy conflict tempts out-of-scope remediation | Medium | Record the conflict in research/task evidence; do not edit active policy. |
| External source is unavailable | Medium | Use another official source or record the evidence gap; do not downgrade to unsupported secondary claims. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Repository document validators, targeted cutoff/status
  scans, and task coverage matrix must pass before each task review.
- **Sandbox / Canary Rollout**: Documentation-only branch; no runtime or remote
  mutation. Each task commit is the rollback boundary.
- **Human Approval Gate**: Required if a source conflict would force inference,
  a reviewer finding conflicts with this plan, or any active policy/runtime
  change becomes necessary.
- **Rollback Trigger**: Revert the affected logical task commit if it introduces
  unsupported claims, broken traceability, lifecycle ambiguity, or validator
  failure that cannot be fixed in scope.
- **Prompt / Model Promotion Criteria**: No provider model promotion is
  authorized. Model differences are research gaps until a separate approved
  Model Policy change updates every coupled surface.

## Completion Criteria

- [ ] All six tasks have clean spec-compliance and document-quality reviews.
- [ ] Every requested category and subcategory has one canonical owner and
      workspace/external comparison.
- [ ] Provider model catalog satisfies the exact cutoff and lifecycle contract.
- [ ] Task-fit recommendations are labeled evidence-backed analysis.
- [ ] Verified duplicate content is merged once; unsupported content is removed.
- [ ] The 2026-07-07 pack and all leaf references are superseded and mapped.
- [ ] Completed historical Stage 03/04 and audit evidence remains linked.
- [ ] No out-of-scope active policy, runtime, CI, provider, model, hook, script,
      secret, remote, or branch-protection change occurred.
- [ ] The first whole-branch review is clean before lifecycle closure.
- [ ] A separate closure commit completes Stage 03/04 lifecycle, task evidence,
      indexes, and progress memory.
- [ ] Final validation and post-closure whole-branch review pass with no open
      Critical/Important finding.

## Related Documents

- **Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Task**:
  [Agentic Research Pack Consolidation Task](../tasks/2026-07-10-agentic-research-pack-consolidation.md)
- **Previous Spec**:
  [Agentic Research Pack Refresh](../../03.specs/104-agentic-research-pack-refresh/spec.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Duplicate Pack**:
  [2026-07-07 Update](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)
- **Research Category**:
  [Research References](../../90.references/research/README.md)
- **Stage Authoring Matrix**:
  [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
