---
status: active
---

<!-- Target: docs/03.specs/agentic-research-pack-refresh/spec.md -->

# Agentic Research Pack Refresh Technical Specification

## Overview

This document defines the technical design and implementation contract for
refreshing the existing
`docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` research pack. The work uses
a refresh-first strategy, then adds targeted new reference documents only where
the existing pack would become unfocused.

The refreshed pack will analyze workspace purpose, roles, CI/CD, QA,
formatting, linting, syntax checks, automation, pipelines, workflows,
operating contracts, templates, scripts, integration guides, SDLC, governance,
system structure, rules, security, harness engineering, loop engineering,
provider implementation status, Docker Compose, and infrastructure.

## Strategic Boundaries & Non-goals

- This specification covers documentation-only Stage 90 reference work.
- The research pack is source-backed reference context, not active policy,
  execution evidence, operations procedure, or runtime truth.
- The work may identify gaps and automation candidates, but it must not fix
  unrelated active-stage or runtime issues during this pass.
- No runtime Docker Compose, provider adapter, secret, remote GitHub, CI/CD,
  hook, script, model policy, or branch-protection state will be changed.
- No provider capability parity claim may be made unless current official
  sources support it.

## Related Inputs

- **User-approved approach**: 2026-07-05 conversation approval for "refresh
  existing research pack plus targeted additions if needed."
- **PRD**: N/A - this is a documentation research refresh over an existing
  Stage 90 reference pack.
- **ARD**: N/A - no architecture runtime surface changes are proposed.
- **Related ADRs**: N/A - no architecture decision is introduced.
- **Research Pack**:
  [../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Stage 90 Contract**:
  [../../90.references/README.md](../../90.references/README.md)
- **Reference Template**:
  [../../99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md)
- **Stage Authoring Matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Contracts

| Contract | Required Behavior |
| --- | --- |
| Stage boundary | Final research outputs live under `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` and do not replace policy, plans, runbooks, incidents, task evidence, or runtime truth. |
| Refresh-first rule | Existing research documents are updated before adding new files. New files are added only when an existing document would become unfocused. |
| Source priority | External facts prefer official vendor docs, standards, primary papers, official repositories, and canonical framework docs. |
| Repo-local evidence | Workspace claims must cite current Stage 00 governance, provider notes, HAFE docs, scripts, CI workflow, templates, operations docs, and runtime inventory where applicable. |
| Gap handling | Active-stage, runtime, provider, security, or CI changes discovered during research are recorded as follow-up gaps, not implemented in this pass. |
| Language boundary | Human-facing README files may use Korean; non-README Stage 90 reference documents remain English under the closed-surface language contract. |
| Commit boundary | Work is committed by logical unit: spec correction, research refresh, targeted additions, and final index/progress updates. |

## Core Design

### Target Structure

```text
docs/90.references/research/2026-07-05-agentic-research-pack-refresh/
├── README.md
├── workspace-baseline.md
├── harness-engineering.md
├── loop-engineering.md
├── spec-driven-sdlc.md
├── quality-ci-formatting.md
├── provider-implementation-comparison.md
├── docker-compose-infrastructure.md        # add if needed
├── security-governance.md                  # add if needed
└── automation-pipeline-workflow.md         # add if needed
```

### Document Responsibilities

| Document | Responsibility |
| --- | --- |
| `workspace-baseline.md` | Repo-local purpose, roles, CI/CD, QA, formatting, linting, automation, scripts, templates, integration guides, SDLC, governance, rules, and security baseline. |
| `harness-engineering.md` | Harness elements, repo-local harness surfaces, agent/runtime/test/eval harness components, and application gaps. |
| `loop-engineering.md` | Agent, validation, CI, memory, eval, approval, and human-in-the-loop feedback loops. |
| `spec-driven-sdlc.md` | Spec-driven development and stage-gated SDLC mapping. |
| `quality-ci-formatting.md` | CI/CD, QA, formatting, linting, syntax checking, security gate placement, and evidence boundaries. |
| `provider-implementation-comparison.md` | Claude, Codex, Gemini harness and loop implementation status, common environment elements, and gaps. |
| `docker-compose-infrastructure.md` | Docker Compose, infrastructure topology, profiles, validation, networking, secrets, and runtime boundary analysis. |
| `security-governance.md` | Secure SDLC, secrets, provider approvals, workflow security, container security, supply-chain guardrails, and repo-local security controls. |
| `automation-pipeline-workflow.md` | Automation, pipeline, workflow, hook, CI job, provider action, and loop orchestration analysis. |

## Data Modeling & Storage Strategy

- No runtime data model or database storage is introduced.
- Stage 90 reference documents are the persisted research artifacts.
- README indexes are updated only when the pack structure changes.
- `docs/00.agent-governance/memory/progress.md` records progress and
  validation evidence.

## Interfaces & Data Structures

### Research Document Contract

Each changed or new non-README Stage 90 reference document must include:

- `Overview`
- `Purpose`
- `Repository Role`
- `Scope`
- `Definitions / Facts`
- `Analysis` or an equivalent source-backed interpretation section
- `Potential Follow-up / Gap`
- `Source Rules`
- `Sources`
- `Maintenance`
- `Related Documents`

### Source Entry Contract

Each source entry must include:

- a direct external URL or target-relative repo-local Markdown link
- a short note explaining what the source supports
- no long copied external text
- no secret values, private paths, or raw logs

## API Contract

N/A - this documentation refresh exposes no external API.

## Agent Role & IO Contract

| Role | Input | Output |
| --- | --- | --- |
| Documentation Specialist | Stage 90 templates, existing research pack, repo-local evidence, external sources | Refreshed reference documents, updated README indexes, progress evidence. |
| Research Orchestrator | Official vendor docs, standards, papers, framework docs | Source-backed comparison notes and source freshness caveats. |
| Reviewer | Final diffs, source lists, validation output | Scope, source, template, and language-contract review before completion. |

## Tools & Tool Contract

- Use `rg` and read-only shell commands for repo evidence discovery.
- Use web verification for external facts that may have changed.
- Use `apply_patch` for file edits.
- Do not use scripts to write file bodies where a patch is sufficient.
- Use `git diff --check` for whitespace and patch hygiene.
- Use repository validation scripts for template, link, language, and reference
  contracts.

## Prompt / Policy Contract

- User instruction overrides the Superpowers default design-doc path; this
  design lives in `docs/03.specs/agentic-research-pack-refresh/`.
- External strategy outputs must map into canonical repository stages.
- Research conclusions must remain advisory until a separate active-stage
  change is approved.

## Memory & Context Strategy

- `docs/00.agent-governance/memory/progress.md` records material progress and
  final verification evidence.
- Durable out-of-scope gaps may be recorded as memory notes only if they are
  reusable and not already covered in the research pack.
- Memory notes remain advisory and must not override Stage 00 policy.

## Guardrails

- Do not edit runtime Docker Compose, provider config, secrets, CI workflows,
  branch protection, model policy, or script behavior in this task.
- Do not create duplicate reference files when an existing document can be
  updated without losing focus.
- Do not create active policy, plan, task, runbook, or incident records as part
  of the research refresh unless the user expands the scope.
- Do not claim Gemini first-class subagent parity without current official
  source support.
- Do not treat external framework recommendations as adopted repo policy.

## Evaluation

Evaluation is documentation-contract based:

- Source-backed coverage of requested categories.
- Correct Stage 90 reference boundaries.
- Accurate repo-local evidence mapping.
- No placeholders, duplicated SSoT, or active-policy drift.
- Repository validation gates pass.

## Edge Cases & Error Handling

- If an external source is unavailable, use another official source or record
  the source gap explicitly.
- If official provider documentation conflicts with repo-local provider notes,
  document the conflict as a gap and do not change provider policy.
- If a requested item belongs in active policy, plan, operation, or runtime
  configuration, record it as a follow-up gap instead of editing that surface.
- If validation fails because of unrelated existing issues, record the exact
  failure as out of scope and keep research-pack changes scoped.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback |
| --- | --- |
| Research document becomes active policy | Rewrite it as source-backed reference analysis and move recommendations to gaps. |
| Existing document becomes too broad | Add one targeted reference document and update README indexes. |
| Provider capability is unclear | Re-check official sources and mark the claim as a gap or revalidation need. |
| Stage 90 language or template contract fails | Fix the reference document shape before proceeding. |
| Validation fails due unrelated drift | Record as out of scope and do not patch unrelated files. |

## Verification

Run at minimum:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

For changed reference files, also run targeted scans for incomplete template
markers, broken target-relative links, non-English closed-surface drift where
applicable, and stale provider capability claims.

## Success Criteria & Verification Plan

- **VAL-SPC-001**: This design spec lives under canonical Stage 03 and has a
  matching README.
- **VAL-SPC-002**: Existing research pack documents are refreshed before new
  files are added.
- **VAL-SPC-003**: Requested topics are covered by refreshed existing documents
  or by targeted new reference documents.
- **VAL-SPC-004**: All new or changed reference documents state repository
  role, scope, source rules, sources, maintenance, and related documents.
- **VAL-SPC-005**: No active policy, runtime, secret, provider config, CI
  behavior, or script behavior is changed.
- **VAL-SPC-006**: `docs/00.agent-governance/memory/progress.md` records the
  completed research work and validation evidence.
- **VAL-SPC-007**: Repository validation gates pass, or unrelated failures are
  explicitly recorded as out of scope.

## Related Documents

- [spec README](./README.md)
- [docs/03.specs README](../README.md)
- [agentic engineering research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [research references](../../90.references/research/README.md)
- [reference template](../../99.templates/templates/common/reference.template.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation scope](../../00.agent-governance/scopes/docs.md)
