---
status: active
---

<!-- Target: docs/03.specs/122-agentic-research-pack-consolidation/spec.md -->

# Agentic Research Pack Consolidation Technical Specification

## Overview

This specification defines the design and implementation contract for
consolidating the workspace's agentic engineering research into the existing
`docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`
canonical pack. It requires fresh repo-local discovery, primary-source external
research, category-by-category comparison, correction of stale claims, and
supersession of the duplicate 2026-07-07 pack.

The consolidated pack covers workspace purpose and roles; CI/CD; QA;
formatting, linting, and syntax checks; automation, pipelines, and workflows;
operating contracts; templates; scripts; integration guides; spec-driven
development and the SDLC; governance, rules, security, Docker Compose,
infrastructure, AI agents, harness engineering, loop engineering, document-type
roles, and task-characteristic model selection.

Claude, OpenAI/Codex, and Gemini model facts use an evidence cutoff of
2026-07-10 10:00 KST (01:00 UTC). The model landscape distinguishes
`stable`, `preview`, and `deprecated` states and records model IDs,
availability surfaces, reasoning controls, tool and agent characteristics,
coding suitability, task fit, and evidence limitations.

## Strategic Boundaries & Non-goals

- This is documentation-only Stage 03/04/90 work plus the mandatory Stage 00
  progress log.
- Stage 90 remains advisory reference context. It does not replace active
  policy, plans, task evidence, operations procedures, incidents, or runtime
  truth.
- The 2026-07-05 research pack remains the only active canonical pack. No new
  dated parallel pack is created.
- Verified unique material from the 2026-07-07 pack is merged into the
  canonical pack. The duplicate pack is then marked `superseded`, removed
  from current-reading routes, and given explicit canonical mappings.
- Completed Stage 03/04 specifications, plans, tasks, and audit records remain
  historical evidence. Their relevant conclusions are linked, not copied or
  deleted.
- No runtime Compose, provider adapter, model policy, CI workflow, hook,
  automation behavior, secret, credential, remote GitHub, or branch-protection
  state changes are authorized.
- External recommendations are analyzed but are not adopted as workspace
  policy in this workstream.

## Related Inputs

- **PRD**: No dedicated PRD is required; this is a source-backed consolidation
  of an existing Stage 90 reference pack approved by the user.
- **ARD**: No dedicated ARD is required; no runtime or architecture behavior is
  changed.
- **Related ADRs**: No new architecture decision is introduced.
- **Previous Spec**:
  [../104-agentic-research-pack-refresh/spec.md](../104-agentic-research-pack-refresh/spec.md)
- **Canonical Pack**:
  [../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Duplicate Pack**:
  [../../90.references/research/2026-07-07-agentic-research-pack-update/README.md](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)
- **Reference Template**:
  [../../99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md)
- **Stage Authoring Matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Contracts

| Contract | Required Behavior |
| --- | --- |
| Canonical target | Refresh the existing 2026-07-05 research pack in place; do not create a 2026-07-10 replacement pack. |
| Workspace evidence | Derive current implementation claims from tracked source, Stage 00 governance, active stage documents, workflows, scripts, templates, and runtime configuration. Treat Graphify as advisory and corroborate it against tracked files. |
| External research | Compare every workspace category with primary external sources: official vendor documentation, standards bodies, original papers, and official repositories. |
| Comparative analysis | For each category, document workspace current state, external research, comparison, implementation status, gap, recommendation, canonical owner, and evidence. |
| Status vocabulary | Classify workspace coverage as `Implemented`, `Partially Implemented`, `Missing`, or `Not Applicable`. |
| Provider model cutoff | Include official Claude, OpenAI/Codex, and Gemini models documented as available or lifecycle-relevant at 2026-07-10 10:00 KST; exclude later announcements from the cutoff comparison. |
| Provider model lifecycle | Preserve each provider's official lifecycle term, then map it to `stable`, `preview`, or `deprecated` only when the source supports that mapping. If the historical state cannot be proven, label it `historical state unverified` rather than infer it. |
| Provider parity | Do not infer feature or quality parity from similar names, benchmarks, or marketing categories. Each claim needs provider-specific official evidence. |
| Consolidation | Merge verified unique 2026-07-07 content into the responsible canonical document; remove unsupported claims and duplicate explanations. |
| Supersession | Mark the 2026-07-07 pack and its reference documents `status: superseded`, add canonical mappings and current-truth warnings, and remove the pack from active reading order. |
| Historical evidence | Preserve completed Stage 03/04 and audit artifacts. Link them as evidence without copying their full bodies into Stage 90. |
| Language | Keep non-README Stage 03, Stage 04, and Stage 90 research documents in English; README files follow their stage contract. |
| Commit boundary | Commit design, research domains, supersession/index work, and review fixes as separate logical units. |
| Mutation boundary | Record policy, runtime, CI, provider, security, or operations changes as follow-up gaps only. |

## Core Design

### Canonical Research Structure

```text
docs/90.references/research/2026-07-05-agentic-research-pack-refresh/
├── README.md
├── workspace-baseline.md
├── harness-engineering.md
├── loop-engineering.md
├── provider-implementation-comparison.md
├── provider-model-landscape.md
├── agent-model-selection.md
├── ai-agent-catalogs.md
├── spec-driven-sdlc.md
├── sdlc-document-roles.md
├── quality-ci-formatting.md
├── docker-compose-infrastructure.md
├── security-governance.md
└── automation-pipeline-workflow.md
```

`provider-model-landscape.md` is the only new research document. A complete
provider model catalog would overload `agent-model-selection.md` and obscure
its task-to-configuration responsibility.

### Document Responsibilities

| Document | Responsibility |
| --- | --- |
| `workspace-baseline.md` | Workspace purpose, roles, overview, implementation surfaces, contracts, templates, scripts, integration guidance, stage topology, and category-level current-state summary. |
| `harness-engineering.md` | Harness components, isolation, context, tools, permissions, runtime/test/eval/governance harnesses, and workspace application requirements. |
| `loop-engineering.md` | Inner agent, validation, CI, eval, memory, approval, automation, security-review, and human-feedback loops. |
| `provider-implementation-comparison.md` | Claude, Codex, and Gemini harness, loop, subagent, hook, context, sandbox, and approval implementation comparison. |
| `provider-model-landscape.md` | Cutoff-bound official model catalogs, lifecycle status, model IDs, availability, reasoning, tools, agent/coding fit, and evidence caveats. |
| `agent-model-selection.md` | Task-characteristic selection matrix, provider-specific configuration mechanisms, workspace policy comparison, and approved-change boundary. |
| `ai-agent-catalogs.md` | Official or community agent catalog patterns, `msitarzewski/agency-agents` comparison, import boundary, and curated workspace-role implications. |
| `spec-driven-sdlc.md` | Spec-driven development, traceability, stage gates, secure SDLC, Compose lifecycle, evidence flow, and feedback integration. |
| `sdlc-document-roles.md` | Purpose, timing, ownership, inputs, outputs, and lifecycle relationships for PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, Release, and supporting records. |
| `quality-ci-formatting.md` | CI/CD, QA, formatting, linting, syntax, type, build, coverage, security, local/CI/remote evidence boundaries, and gate ordering. |
| `docker-compose-infrastructure.md` | Compose topology, includes, profiles, networks, secrets, volumes, healthchecks, validation, hardening, operations, and infrastructure harness. |
| `security-governance.md` | Secure SDLC, approval boundaries, redaction, secrets, action security, container hardening, dependency controls, supply-chain gaps, and human escalation. |
| `automation-pipeline-workflow.md` | Local automation, CI pipelines, provider hooks, workflow orchestration, action authority, evidence capture, and rollback boundaries. |

### Workspace-to-External Comparison Flow

Each research document follows this flow:

1. Identify canonical repo-local sources and state the current implementation.
2. Gather primary external sources for the same category.
3. Normalize facts without changing provider-native terminology.
4. Compare current state with external practice.
5. Classify implementation status and confidence.
6. Record gaps, risks, prerequisites, and the canonical stage owner.
7. Keep recommendations advisory until separately approved active-stage work
   exists.

### Duplicate-Pack Consolidation Map

| 2026-07-07 document | Canonical destination |
| --- | --- |
| `workspace-baseline.md` | `workspace-baseline.md`, with domain detail routed to the responsible quality, Docker, security, automation, or SDLC document. |
| `harness-engineering.md` | `harness-engineering.md`; provider-specific facts route to `provider-implementation-comparison.md`. |
| `loop-engineering.md` | `loop-engineering.md`; CI and automation details route to `automation-pipeline-workflow.md`. |
| `provider-implementation-comparison.md` | `provider-implementation-comparison.md`; model inventory routes to `provider-model-landscape.md`; task fit routes to `agent-model-selection.md`. |
| `ai-agent-catalogs.md` | `ai-agent-catalogs.md`. |
| `README.md` | Canonical pack README reading order plus the parent research README supersession ledger. |

Unsupported claims are removed rather than carried forward. Superseded files
retain a concise mapping and warning so links remain traceable without
presenting stale text as current truth.

## Data Modeling & Storage Strategy

- Research facts are stored in Markdown tables and prose under the canonical
  Stage 90 pack.
- Every external fact records a direct URL and a short support note.
- Time-sensitive provider facts record provider, model name, model ID, lifecycle
  status, surface, source publication or update date when available, cutoff
  eligibility, verification timestamp, and caveat.
- Repo-local claims use target-relative links to tracked files or active stage
  documents.
- No database, runtime cache, downloaded corpus, raw web capture, secret value,
  or diagnostic log is persisted.
- The 2026-07-07 pack remains at its current path with superseded metadata and
  canonical mappings; it is not copied to a third location.

## Interfaces & Data Structures

### Research Comparison Record

| Field | Meaning |
| --- | --- |
| Category | Requested topic or focused subtopic. |
| Workspace evidence | Current tracked implementation source and observed behavior. |
| External evidence | Primary source and supported practice or capability. |
| Status | `Implemented`, `Partially Implemented`, `Missing`, or `Not Applicable`. |
| Gap or risk | Concrete difference, uncertainty, or stale claim. |
| Recommendation | Advisory next step with prerequisites and trade-offs. |
| Canonical owner | Stage and document type that would own an approved change. |
| Confidence | High, Medium, or Low based on evidence directness and freshness. |

### Provider Model Record

| Field | Meaning |
| --- | --- |
| Provider | Anthropic, OpenAI, or Google. |
| Display name / model ID | Official human name and selectable identifier when documented. |
| Provider-native status | The official lifecycle or availability term exactly as the provider documents it. |
| Normalized lifecycle | `stable`, `preview`, `deprecated`, or `historical state unverified`, with the mapping basis stated. |
| Cutoff evidence | Official release, model, API, CLI, or deprecation source dated at or before the cutoff when available. |
| Availability surface | API, provider CLI, coding agent, IDE, or other documented surface. |
| Reasoning control | Supported effort, thinking, or model-selection control without cross-provider normalization. |
| Agent and coding fit | Officially supported tools, coding surfaces, agent features, and evidence-backed task suitability. |
| Workspace relation | Current Stage 00 model-policy mapping, difference, and whether follow-up approval is required. |

Task-fit recommendations are analysis, not vendor facts. Each recommendation
must be labeled as an inference from officially documented capabilities and the
workspace task taxonomy, and it must state material uncertainty or missing
comparative evidence.

## API Contract (If Applicable)

Not applicable. This work creates documentation contracts and exposes no API.

## Agent Role & IO Contract (If Applicable)

| Role | Inputs | Outputs | Success Definition |
| --- | --- | --- | --- |
| Workflow supervisor | Approved specification, task briefs, global constraints | Sequenced work, review routing, final synthesis | Every task stays within its document ownership and mutation boundary. |
| Documentation implementer | One task brief, templates, repo-local sources, official external sources | Focused document changes, tests, logical commit, report | Requested coverage is accurate, sourced, and template-compliant. |
| Task reviewer | Task brief, implementation report, review package | Spec-compliance and document-quality verdicts | Both verdicts approve or findings return to a fixer. |
| Final reviewer | Whole-branch review package and open minor findings | Cross-document consistency and completion verdict | No unresolved critical or important findings remain. |

Subagent-driven execution is sequential by task to avoid file conflicts.
Independent source discovery may be parallelized, but only the assigned
implementer mutates a task's files.

## Tools & Tool Contract (If Applicable)

- Use `rg`, `rg --files`, and read-only Git commands for repo discovery.
- Use current web retrieval for official external sources and cite direct pages.
- Use `apply_patch` for document edits.
- Use repository scripts for link, template, traceability, implementation
  alignment, provider-surface, and index verification.
- Use Superpowers task briefs, reports, review packages, and durable progress
  ledger during implementation.
- Do not persist raw web pages, shell history, raw diagnostics, or secret
  material.

## Prompt / Policy Contract (If Applicable)

- The approved design is authoritative for scope and document ownership.
- The user-approved external evidence cutoff is
  2026-07-10 10:00 KST (01:00 UTC).
- Current official provider documentation is required for fast-changing facts.
- If a mutable page cannot prove its historical cutoff state, state the
  uncertainty explicitly.
- User approval to research and document a gap does not authorize active policy,
  provider adapter, model, CI, hook, runtime, secret, or remote mutation.
- The repository's active Model Policy remains the SSoT even when provider
  catalogs contain newer models.

## Memory & Context Strategy (If Applicable)

- The Stage 04 task document records source inventory, cutoff evidence,
  validation commands, commits, review outcomes, and deviations.
- `docs/00.agent-governance/memory/progress.md` records material milestones and
  final verification evidence.
- The Superpowers SDD ledger records per-task completion and commit ranges.
- Source research and review artifacts use non-secret scratch handoffs and are
  promoted only when durable evidence belongs in Stage 04 or Stage 90.
- Graphify remains a navigation aid and must not override tracked source.

## Guardrails (If Applicable)

- Do not change active governance, model policy, provider adapters, hooks,
  workflows, scripts, runtime Compose, infrastructure, operations procedures,
  secrets, credentials, remote settings, or branch protection.
- Do not create a third dated research pack.
- Do not delete historical Stage 03/04 evidence or audit reports.
- Do not copy prior documents wholesale; merge verified facts into the
  responsible canonical document and remove duplication.
- Do not label a model or capability `stable`, `preview`, or `deprecated`
  without official evidence.
- Do not turn benchmarks or marketing language into task-fit guarantees.
- Do not claim local behavior from Graphify, generated indexes, or old research
  documents without corroborating tracked current truth.
- Do not leave placeholders, stale canonical links, or active routes to the
  superseded pack.

## Evaluation (If Applicable)

- **Coverage evaluation**: Every user-requested category and subcategory maps to
  exactly one primary canonical document.
- **Evidence evaluation**: Every time-sensitive provider/model claim has an
  official source and cutoff disposition.
- **Workspace evaluation**: Repo-local claims match tracked current
  implementation.
- **Consolidation evaluation**: Unique valid prior content is preserved once;
  unsupported and duplicated content is not carried forward.
- **Lifecycle evaluation**: The 2026-07-05 pack is active, the 2026-07-07 pack
  is superseded, and parent indexes route readers correctly.
- **Quality evaluation**: Templates, frontmatter, language, links, indexes,
  traceability, implementation alignment, and repository contracts pass.

## Edge Cases & Error Handling

- **Mutable official page lacks cutoff history**: Use an official release note
  or archived official source when available; otherwise record
  `historical state unverified`.
- **Source published after cutoff**: Exclude the model or capability from the
  cutoff comparison and note it outside the comparison only if needed to avoid
  reader confusion.
- **Official sources conflict**: Record both sources, dates, surfaces, and the
  narrower supported conclusion; do not silently choose the stronger claim.
- **Repo research conflicts with tracked implementation**: Treat tracked
  implementation and active governance as current workspace truth, correct the
  research document, and record the drift.
- **External recommendation belongs to active policy or runtime**: Record a
  follow-up gap with canonical owner; do not implement it.
- **Prior document contains unique but unverifiable content**: Preserve only a
  supersession mapping and state that the claim was not carried forward.
- **Reference document becomes too broad**: Add a focused document only when the
  responsibility cannot fit an existing canonical boundary. The approved model
  landscape document is the sole pre-authorized addition.
- **Validation exposes unrelated failure**: Record exact out-of-scope evidence
  and do not patch unrelated surfaces.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback | Human Escalation |
| --- | --- | --- |
| Provider cutoff cannot be established | Publish only proven facts and mark the historical state unverified. | Required before asserting an inferred lifecycle or availability state. |
| Consolidation would erase unique historical evidence | Preserve the original as superseded and link the canonical destination. | Required before deletion or archive migration. |
| Reviewer finds a plan-mandated quality defect | Stop the affected task and present the conflicting plan and finding. | User decides which contract governs. |
| Critical or important review finding remains open | Dispatch one scoped fixer, rerun covering checks, and re-review. | Required if the finding conflicts with approved scope. |
| Repository checks fail repeatedly | Narrow the check, diagnose, and stop after the skill-defined blocker threshold. | Required when no safe in-scope resolution remains. |

## Verification

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Also perform targeted checks for:

- unresolved placeholders such as `TBD`, `TODO`, `FIXME`, or template
  braces;
- direct and target-relative link correctness;
- cutoff timestamps and model lifecycle labels;
- requested-category coverage and single-document ownership;
- stale active references to the superseded pack;
- unsupported provider parity or local implementation claims.

## Success Criteria & Verification Plan

- **VAL-ARC-001**: The 2026-07-05 research pack is the only active canonical
  agentic engineering research pack.
- **VAL-ARC-002**: Every requested workspace category contains repo-local
  evidence, external primary-source research, comparative analysis, status,
  gap, recommendation, canonical owner, and confidence.
- **VAL-ARC-003**: Claude, OpenAI/Codex, and Gemini official model catalogs are
  represented at the approved cutoff with lifecycle, ID, availability,
  reasoning, agent/coding fit, task fit, and uncertainty fields.
- **VAL-ARC-004**: The model landscape and task-selection responsibilities are
  separated between `provider-model-landscape.md` and
  `agent-model-selection.md`.
- **VAL-ARC-005**: Verified unique 2026-07-07 content exists once in the
  responsible canonical document; unsupported and duplicated claims are
  removed.
- **VAL-ARC-006**: The 2026-07-07 pack is consistently marked superseded and
  every child maps to a canonical destination.
- **VAL-ARC-007**: Completed related Stage 03/04 and audit evidence remains
  preserved and linked without full-body duplication.
- **VAL-ARC-008**: No active policy, runtime, CI, provider, model, hook, script,
  secret, remote, or branch-protection behavior changes.
- **VAL-ARC-009**: Logical commits and per-task reviews provide auditable
  implementation evidence.
- **VAL-ARC-010**: All specified documentation and repository checks pass, or
  unrelated failures are explicitly recorded.

## Related Documents

- [Spec folder README](./README.md)
- [Implementation plan](../../04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md)
- [Task evidence](../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md)
- [Previous research refresh specification](../104-agentic-research-pack-refresh/spec.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Duplicate research pack to supersede](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)
- [Research category README](../../90.references/research/README.md)
- [Agent governance hub](../../00.agent-governance/README.md)
- [Harness implementation map](../../00.agent-governance/harness-implementation-map.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
- [Reference template](../../99.templates/templates/common/reference.template.md)
