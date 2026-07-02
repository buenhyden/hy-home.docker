---
status: draft
---

<!-- Target: docs/03.specs/agentic-engineering-implementation-audit-pack/spec.md -->

# Agentic Engineering Implementation Audit Pack Technical Specification

## Overview

This document defines the design contract for a Stage 90 reference-audit pack
that assesses how much of the researched agentic engineering model is currently
implemented in `hy-home.docker`.

The audit pack will use `docs/90.references/research/agentic-engineering/` as
its criteria source and repo-local evidence as its implementation source. It
will not change active policy, runtime provider configuration, CI/CD behavior,
or scripts.

## Strategic Boundaries & Non-goals

- This specification covers documentation-only audit reports.
- The target output is a Stage 90 reference-audit snapshot, not an active policy,
  runbook, plan, or task evidence file.
- The audit may identify gaps and automation candidates, but it must not fix
  them during this work.
- No PRD, ARD, or ADR is required because this work creates a reference audit
  view over an existing governance and documentation system.
- No runtime, provider, secret, remote GitHub, CI/CD, hook, script, or Compose
  state will be changed by the audit work.

## Related Inputs

- **User-approved design**: 2026-07-02 conversation approval for a Stage 90
  reference-audit snapshot using an audit-pack structure.
- **Research Pack**:
  [../../90.references/research/agentic-engineering/README.md](../../90.references/research/agentic-engineering/README.md)
- **Workspace Baseline Reference**:
  [../../90.references/research/agentic-engineering/workspace-baseline.md](../../90.references/research/agentic-engineering/workspace-baseline.md)
- **Harness Engineering Reference**:
  [../../90.references/research/agentic-engineering/harness-engineering.md](../../90.references/research/agentic-engineering/harness-engineering.md)
- **Loop Engineering Reference**:
  [../../90.references/research/agentic-engineering/loop-engineering.md](../../90.references/research/agentic-engineering/loop-engineering.md)
- **Provider Comparison Reference**:
  [../../90.references/research/agentic-engineering/provider-implementation-comparison.md](../../90.references/research/agentic-engineering/provider-implementation-comparison.md)
- **Quality / CI / Formatting Reference**:
  [../../90.references/research/agentic-engineering/quality-ci-formatting.md](../../90.references/research/agentic-engineering/quality-ci-formatting.md)
- **Spec-Driven SDLC Reference**:
  [../../90.references/research/agentic-engineering/spec-driven-sdlc.md](../../90.references/research/agentic-engineering/spec-driven-sdlc.md)
- **Stage 90 Contract**: [../../90.references/README.md](../../90.references/README.md)

## Contracts

| Contract | Required Behavior |
| --- | --- |
| Stage boundary | Audit reports live under `docs/90.references/audits/` and do not replace policy, plans, runbooks, task evidence, or runtime truth. |
| Criteria source | Implementation assessment criteria come from the source-backed research pack under `docs/90.references/research/agentic-engineering/`. |
| Evidence source | Implementation status must cite repo-local evidence such as Stage 00 governance, provider notes, runtime surfaces, scripts, CI workflow, templates, and HAFE docs. |
| Gap handling | Missing or partial implementation is recorded as `Gap / Follow-up` or `Automation Candidate`, not fixed in this task. |
| Report consistency | All audit reports use the shared status vocabulary and assessment sections defined here. |
| Language boundary | README files may use Korean human-facing explanations; non-README Stage 90 reference/audit documents use English closed-surface prose. |

## Core Design

### Target Structure

```text
docs/90.references/audits/
├── README.md
└── agentic-engineering/
    ├── README.md
    ├── implementation-overview.md
    ├── harness-engineering-implementation.md
    ├── loop-engineering-implementation.md
    ├── provider-harness-loop-implementation.md
    ├── workspace-rules-environment-implementation.md
    ├── automation-candidates.md
    └── sdlc-quality-formatting-implementation.md
```

### Report Roles

| Report | Role |
| --- | --- |
| `implementation-overview.md` | Cross-category summary matrix and high-level maturity snapshot. |
| `harness-engineering-implementation.md` | Current implementation state for governance, runtime, validation, evidence, and provider harness elements. |
| `loop-engineering-implementation.md` | Current implementation state for discovery, tool, validation, CI, human approval, memory, and eval loops. |
| `provider-harness-loop-implementation.md` | Claude, Codex, and Gemini comparison for harness and loop implementation. |
| `workspace-rules-environment-implementation.md` | Workspace rules, systems, environments, provider-neutral common contracts, and evidence surfaces. |
| `automation-candidates.md` | Pipeline, workflow, validation, freshness, eval, and review automation candidates discovered by the audit. |
| `sdlc-quality-formatting-implementation.md` | Spec-driven development, SDLC, CI/CD, QA, and formatting implementation status. |

## Interfaces & Data Structures

### Assessment Status Vocabulary

| Status | Meaning |
| --- | --- |
| `Implemented` | Repo-local evidence exists and current validator, documentation, or runtime surfaces support the claim. |
| `Partially Implemented` | A surface exists, but provider parity, automation, validation, freshness, or operational linkage is incomplete. |
| `Not Implemented` | The research baseline identifies a relevant capability, but no repo-local implementation artifact was found. |
| `Not Applicable` | The capability is intentionally not needed for this workspace's current purpose. |
| `Unknown / Needs Revalidation` | Current implementation or provider behavior cannot be asserted without renewed evidence. |

### Required Report Sections

Each non-README audit report must include:

- `Overview`
- `Purpose`
- `Repository Role`
- `Scope`
- `Assessment Method`
- `Implementation Status Matrix`
- `Findings`
- `Gap / Follow-up`
- `Automation Candidates` or `Automation Impact`
- `Source Rules`
- `Sources`
- `Maintenance`
- `Related Documents`

## Agent Role & IO Contract

| Role | Input | Output |
| --- | --- | --- |
| Documentation Specialist | Stage 90 templates, research pack, repo-local governance and runtime evidence | Template-compliant Stage 90 audit reports and README indexes. |
| Research Orchestrator | External source-backed research criteria and provider documentation | Criteria traceability and source freshness notes. |
| Reviewer | Final diffs, status matrices, and validation output | Scope, source, and quality review findings before completion. |

## Tools & Tool Contract

- Use `rg` and read-only shell commands for repo evidence discovery.
- Use web verification for provider or external sources that may have changed.
- Use `apply_patch` for file edits.
- Use `git diff --check` for whitespace and patch hygiene.
- Use `bash scripts/validation/check-doc-traceability.sh` for execution and
  operations traceability.
- Use `bash scripts/validation/check-repo-contracts.sh` for template,
  language, reference-stage, governance-memory, and repository contract checks.

## Guardrails

- Do not write active policies, runbooks, implementation plans, or task evidence
  under `docs/90.references/audits/`.
- Do not fix gaps discovered outside the approved Stage 90 documentation scope.
- Do not change provider runtime surfaces, scripts, CI workflows, model policy,
  secrets, Compose files, or remote GitHub state.
- Do not claim Gemini first-class subagent parity unless current official
  sources support it.
- Do not use audit scores as deployment approval gates.

## Verification

The design and later audit-pack implementation use documentation checks rather
than runtime tests.

```bash
git diff --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-repo-contracts.sh
```

## Evaluation

This work is evaluated through document structure, traceability, and repository
contract checks rather than runtime tests.

```bash
git diff --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
```

Known pre-existing infra image/version drift may keep the full repository
contract check red. If that happens, the audit work must record the failure as
out of scope instead of modifying infra files.

## Edge Cases & Error Handling

- If an audit report needs a fact that is absent from the research pack, add a
  small source-backed research refinement before writing the audit claim.
- If a provider source conflicts with repo-local provider notes, document the
  mismatch as `Unknown / Needs Revalidation` or `Gap / Follow-up`.
- If `check-repo-contracts.sh` reports non-Stage-90 failures, record them as
  out-of-scope gaps unless the user explicitly expands scope.
- If a report starts to describe an executable procedure, move that content out
  of the audit scope and keep only the reference finding.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback |
| --- | --- |
| Report becomes active policy | Rewrite it as source-backed implementation status and move policy recommendations to gaps. |
| Provider capability is unclear | Re-check official sources and mark the row `Unknown / Needs Revalidation` if still unresolved. |
| Audit category violates Stage 90 contract | Adjust README language and non-README report sections to the reference template contract. |
| Validation fails due this work | Fix the Stage 90 or spec document shape before proceeding. |
| Validation fails due unrelated infra drift | Record the exact drift as out of scope and do not patch infra files. |

## Success Criteria & Verification Plan

- **VAL-SPC-001**: The design spec and README use canonical Stage 03 paths and
  do not create non-stage Superpowers artifacts.
- **VAL-SPC-002**: The target Stage 90 audit structure is explicit and bounded.
- **VAL-SPC-003**: Each report has a clear source, evidence, gap, and automation
  candidate model.
- **VAL-SPC-004**: The implementation work can be planned as separate logical
  units with separate commits.
- **VAL-SPC-005**: Validation commands and out-of-scope handling are defined.

## Related Documents

- [spec README](./README.md)
- [docs/03.specs README](../README.md)
- [research pack](../../90.references/research/agentic-engineering/README.md)
- [90.references](../../90.references/README.md)
- [reference template](../../99.templates/reference.template.md)
- [README template](../../99.templates/readme.template.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
