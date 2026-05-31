---
status: draft
---
<!-- Target: docs/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md -->

# Agent Governance Phase 2 Alignment Plan

## Overview (KR)

이 문서는 Phase 1 읽기 전용 조사 결과를 바탕으로, `hy-home.docker`의 공유 AI Agent 거버넌스(Stage 00), Template Contract, Model Policy, QA/CI/CD 정책, Codex 하네스 정합성을 Phase 3에서 안전하게 개선하기 위한 Phase 2 계획서다.

이 계획은 구현을 수행하지 않는다. 사용자 확인이 필요한 고영향 결정은 `Decision Gates`에 격리하고, 승인 전에는 Stage 00, template, provider harness, validator를 변경하지 않는다.

## Context

Phase 1 조사에서 현재 repository는 이미 Stage 00 기반의 단일 공유 거버넌스와 provider harness 구조를 갖추고 있음을 확인했다. 기존 완료 plan인 `2026-05-30-standardizing-agent-governance.md`는 Codex 하네스를 `.codex/agents/*.md` YAML frontmatter 구조로 유지하는 결정을 기록하고 있다.

동시에 새 첨부 지시는 `.codex/agents/*.toml`, `model_reasoning_effort`, 2026-05-29 기준 Model Policy, Stage 00 공통 개념 체계, Template Contract 완전성, QA/CI/CD 단일 정책을 요구한다. 이 중 일부는 현재 repository 정책과 충돌하거나, 검증 스크립트가 통과해도 보장하지 못하는 영역이다.

User-confirmed Phase 2 decisions on 2026-06-01:

- Include `.codex/agents/*.toml` transition in this Phase 2 plan.
- Create a new plan for residual gaps newly identified in Phase 1, preserving prior completed plans as historical evidence.
- Treat the Model Policy date requirement strictly as 2026-05-29; do not replace it with current-docs-only assumptions.

Current evidence from Phase 1:

- `check-repo-contracts.sh`, `check-doc-traceability.sh`, `generate-llm-wiki-index.sh --check`, and provider surface sync passed during read-only investigation.
- `report-graphify-health.sh` was advisory; Graphify findings must be corroborated against tracked source files.
- `.codex/agents/*.md` exists; `.codex/agents/*.toml` does not exist.
- `providers/codex.md` explicitly says not to introduce `.toml` agent definitions for this repository.
- Stage 00 Model Policy defines model IDs but does not currently encode `model_reasoning_effort` as an enforced harness field.
- Validation currently does not prove semantic alignment for status vocabulary, Markdown fence correctness, function/skill catalog depth, or every optional template deviation.

## Decision Gates

These gates capture confirmed decisions and remaining questions before Phase 3 implementation. Open gates must be answered or explicitly recorded as blockers before implementation begins.

| Gate | Status | Decision / Question | Phase 3 Impact |
| --- | --- | --- | --- |
| DG-001 | Confirmed | Plan a Codex harness transition to `.codex/agents/*.toml`. | Changes provider docs, sync script, validator, runtime catalog, and every Codex agent definition. |
| DG-002 | Confirmed | Use this new residual-gap plan; preserve `2026-05-30-standardizing-agent-governance.md` as completed historical evidence. | Avoids rewriting completed execution history while allowing new Phase 1 findings to be planned. |
| DG-003 | Confirmed | Require strict Model Policy evidence as of 2026-05-29. Unsupported or unverifiable model/reasoning claims must remain blocked or verification-required. | Determines whether `model_reasoning_effort` can be enforced in `.toml` and validators. |
| DG-004 | Open | Template deviation policy: normalize all deviations, or only active/high-risk deviations plus explicit exceptions? | Controls blast radius across `docs/01`-`docs/05`, `docs/90`, and `docs/99`. |
| DG-005 | Open | Provider parity model: keep Claude canonical runtime mirror during `.toml` transition, or convert to Stage 00 canonical with provider adapters? | Determines whether `.claude`, `.codex`, and `.agents` synchronization scripts need redesign. |

## Goals & In-Scope

- **Goals**:
  - Convert Phase 1 findings into an implementable, approval-gated Phase 3 roadmap.
  - Keep Stage 00 as the single source of truth for governance, QA/CI/CD, Template Contract, Model Policy, and clarification duty.
  - Plan bounded fixes for validation blind spots instead of assuming green checks prove semantic correctness.
  - Plan Codex harness transition to `.codex/agents/*.toml` without creating a separate Codex governance layer.
  - Preserve historical completed plans and tasks while using this plan for newly identified residual gaps.
  - Require strict 2026-05-29 Model Policy evidence before promoting model or reasoning-effort fields to enforced configuration.
- **In Scope**:
  - `docs/00.agent-governance/**`
  - `docs/99.templates/**`
  - Bounded target-stage docs under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, and `docs/90.references`
  - `AGENTS.md`, `.codex/README.md`, `.codex/agents/**`, `.codex/skills/**`, `.codex/hooks.json`
  - Provider parity docs and sync/validation scripts
  - Execution plan/task traceability for Phase 3

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not implement Stage 00, template, validator, or Codex harness edits during Phase 2.
  - Do not implement `.codex/agents/*.toml` migration during Phase 2.
  - Do not treat validation pass as proof that every policy, template, or runtime behavior is correct.
  - Do not rewrite historical docs merely for style.
- **Out of Scope**:
  - User-global Codex settings under `/home/hy/.codex`
  - Secrets, credentials, private tokens, shell history, or deployment state
  - Docker service lifecycle changes
  - Remote GitHub branch protection mutation

## Current State to Desired State

| Area | Current State | Desired State |
| --- | --- | --- |
| Shared Concepts | Core concepts exist but are distributed and incomplete for the attachment's requested vocabulary. | Stage 00 has one concept map covering Agent, Skill, Rule, Hook, Sub-agent, Output Style, Workflow, Memory, QA, CI/CD, Model Policy, and Template Contract. |
| Clarification Duty | Existing rules require stopping on conflicts, but underspecified planning/config decisions are not centralized everywhere. | Stage 00 and Codex provider guidance require user questions before irreversible planning or implementation when high-impact ambiguity remains. |
| QA & CI/CD | Checks exist and pass, but policy coverage and validator coverage are not the same thing. | One QA/CI/CD policy maps change types to local commands, CI gates, manual evidence, and known non-automatable checks. |
| Template Contract | Template mapping exists, but status vocabulary and some template deviation handling are inconsistent. | Template Contract defines required headings, allowed variants, status vocabulary, and explicit exception rules. |
| Model Policy | Model IDs are defined; `model_reasoning_effort` is not enforced in active Codex agent frontmatter. | Model Policy uses strict 2026-05-29 evidence and defines whether each `.toml` agent requires `model_reasoning_effort`. |
| Codex Harness | Current harness is `.codex/agents/*.md`; attachment requires `.toml` transition planning. | `.codex/agents/*.toml` becomes the planned Codex harness target, with migration, validation, and rollback steps documented before Phase 3. |
| Provider Parity | Claude canonical runtime mirror model is active. | Provider parity is either preserved through an adapted sync strategy or replaced by a Stage 00 canonical adapter model after DG-005 is answered. |
| Skill / Function Catalog | Runtime skills are richer than governance function catalog entries. | Catalog entries describe responsibilities, inputs, outputs, and links to runtime skills without duplicating provider policy. |
| Validation Blind Spots | Validators pass but miss Markdown fence issues, semantic policy conflicts, and some optional template drift. | Validators or manual gates cover the high-risk blind spots that Phase 1 identified. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Encode confirmed user decisions and keep remaining gates explicit. | This plan; future paired task | G1a | DG-001 through DG-003 are fixed plan constraints; DG-004 and DG-005 remain visible blockers until answered. |
| PLN-002 | Plan Stage 00 concept and clarification-duty consolidation. | `docs/00.agent-governance/README.md`, `rules/*.md`, `providers/*.md`, `subagent-protocol.md` | GOV-CONCEPTS | A single concept map and clarification policy can be traced from Stage 00 to provider harnesses. |
| PLN-003 | Plan shared QA & CI/CD policy refinement. | `rules/github-governance.md`, `scopes/qa.md`, `rules/workflows.md`, `.github/**`, `scripts/**` docs | QA-CICD | Each planned change type maps to a smallest meaningful local check and CI/manual evidence. |
| PLN-004 | Plan Template Contract and document exception cleanup. | `docs/99.templates/**`, `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, target-stage docs | TPL-CONTRACT | Status vocabulary, required headings, accepted aliases, and explicit exceptions are documented. |
| PLN-005 | Plan Codex harness transition from `.codex/agents/*.md` to `.codex/agents/*.toml`. | `AGENTS.md`, `.codex/README.md`, `.codex/agents/**`, `.codex/skills/**`, `.codex/hooks.json`, sync scripts, validators | HARNESS-CODEX | Codex implements Stage 00 through `.toml` agents without separate governance; `.md` handling is explicitly migrated, bridged, or retired. |
| PLN-006 | Plan strict 2026-05-29 Model Policy and reasoning-effort handling. | `subagent-protocol.md`, `provider-capability-matrix.md`, provider docs, validators, `.codex/agents/*.toml` | MODEL-POLICY | Allowed model IDs and `model_reasoning_effort` values are backed by 2026-05-29 evidence or marked blocked. |
| PLN-007 | Plan validation blind-spot coverage. | `scripts/validation/check-repo-contracts.sh`, supplemental manual checks, task evidence | QA-BLIND-SPOTS | Markdown fence issues, status vocabulary drift, legacy plan skip, and model/reasoning fields have checks or explicit manual gates. |
| PLN-008 | Plan Phase 3 traceability artifacts. | Future task doc, plans/tasks README entries if required, `progress.md` | TRACE | Phase 3 has a paired task record with commands, results, deviations, and approval evidence. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository contract check after Phase 2 plan creation | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`, or any failure is caused only by this draft plan and recorded. |
| VAL-PLN-002 | Traceability | Document traceability check | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-PLN-003 | Hygiene | Markdown/trailing whitespace diff hygiene | `git diff --check` | No whitespace errors. |
| VAL-PLN-004 | Advisory | Graphify health remains advisory-only unless source corroborates an issue | `bash scripts/knowledge/report-graphify-health.sh` | Status and advisory reasons recorded; no uncorroborated graph-only claims drive implementation. |
| VAL-PLN-005 | Harness Discovery | Confirm current and target Codex harness shapes before Phase 3 | `rg --files .codex/agents --glob '*.md'` and `rg --files .codex/agents --glob '*.toml'` | Current `.md` baseline and missing `.toml` target are recorded as migration evidence. |
| VAL-PLN-006 | Model Policy Discovery | Confirm active Codex model fields before Phase 3 | `rg -n "^model(_reasoning_effort)?:" .codex/agents --glob '*.md' --glob '*.toml'` | Active fields are known; missing reasoning-effort fields are treated as migration requirements, not hidden compliance. |
| VAL-PLN-007 | Historical Model Evidence | Verify strict 2026-05-29 model and reasoning-effort support | Official archived/provider evidence or repository-approved evidence note | Unsupported or unverifiable model/reasoning claims remain blocked. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| `.toml` migration is implemented before Phase 3 approval. | High | Phase 2 records the migration plan only; Phase 3 requires explicit approval against this plan. |
| Historical completed plans are rewritten and lose audit meaning. | Medium | DG-002 defaults to a new residual-gap plan and preserves completed evidence. |
| Model policy overclaims 2026-05-29 support without archived official proof. | High | Strict date evidence is required; unverifiable claims remain blocked or verification-required. |
| Template cleanup expands into a broad rewrite of hundreds of docs. | High | DG-004 limits Phase 3 to active/high-risk deviations unless the user approves broader normalization. |
| Provider parity architecture changes accidentally fork governance. | High | DG-005 keeps Stage 00 as SSoT and requires explicit approval before changing mirror architecture. |
| Validators are expanded to enforce policy that is not yet agreed. | Medium | Add manual gates first; make script enforcement follow approved policy text. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Phase 3 must pass repository contract, traceability, diff hygiene, and any new manual checks defined by this plan.
- **Sandbox / Canary Rollout**: N/A for governance and harness documentation; no Docker runtime changes are planned.
- **Human Approval Gate**: Required after DG-004 and DG-005 are answered or explicitly accepted as Phase 3 blockers.
- **Rollback Trigger**: Revert Phase 3 changes if Stage 00, provider parity, or validation scripts contradict the approved decision gates.
- **Prompt / Model Promotion Criteria**: No model or reasoning-effort field is promoted from advisory to enforced until strict 2026-05-29 evidence and Stage 00 text agree.

## Completion Criteria

- [x] DG-001 through DG-003 answered by the user and reflected as plan constraints.
- [ ] DG-004 and DG-005 answered by the user or explicitly recorded as Phase 3 blockers.
- [ ] Phase 3 implementation scope is bounded to approved decisions.
- [ ] Stage 00, Template Contract, QA/CI/CD, Model Policy, and Codex harness changes are mapped to concrete files.
- [ ] Verification plan is executable and does not assume validation covers semantic correctness by itself.
- [ ] Required Phase 3 task/evidence artifacts are identified.

## Related Documents

- **Prior Plan**: [2026-05-30-standardizing-agent-governance](./2026-05-30-standardizing-agent-governance.md)
- **Prior Claude Verification Plan**: [2026-05-31-claude-harness-governance-verification](./2026-05-31-claude-harness-governance-verification.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Subagent Protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template Catalog**: [99.templates](../../99.templates/README.md)
- **Operations Index**: [Operations index](../../05.operations/README.md)
