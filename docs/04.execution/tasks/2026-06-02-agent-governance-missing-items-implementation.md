---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md -->

# Task: Agent Governance Missing Items Implementation

## Overview (KR)

이 문서는 `2026-06-02-agent-governance-decision-items-plan.md`에 대한 첨부 문서 대비 누락 항목 보강과 단계적 구현 evidence를 기록한다.

Phase 1/2 historical artifacts는 수정하지 않고, 현재 기준 보정은 Stage 00, Codex harness, Template Contract, QA/CI/CD, Stage 04 evidence surface에 continuation 형태로 반영한다.

## Inputs

- **Parent Plan**: [Agent Governance Decision Items Implementation Plan](../plans/2026-06-02-agent-governance-decision-items-plan.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Template Catalog**: [99.templates](../../99.templates/README.md)

## Working Rules

- Preserve completed Phase 1/2 historical documents.
- Keep Stage 00 as the governance SSoT; do not create duplicate provider-local policy.
- Keep `.codex/agents/*.md` as compatibility prompt context until a separate approved retirement plan exists.
- Do not change Docker runtime, GitHub remote settings, secrets, deployment, or user-global Codex settings.
- Treat HADS mandatory rollout, Docker hard-validator promotion, Codex Markdown prompt retirement, and model/reasoning changes as separate human approval gates.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add Attachment Gap Coverage and WBS PLN-DI-009 through PLN-DI-016 to the decision-items plan. | doc | N/A | PLN-DI-009..016 | Parent plan includes gap matrix, added WBS rows, verification rows, risks, and completion criteria. | Codex | Completed |
| T-002 | Add Stage 00 clarification duty, current-to-desired governance matrix, skill lifecycle, template deviation audit, and model/config gates. | doc | N/A | PLN-DI-009..014 | `docs/00.agent-governance/README.md`, workflows, checklists, documentation protocol, Stage Authoring Matrix, and function catalog README updated. | Codex | Completed |
| T-003 | Add Codex harness alignment gates without retiring compatibility Markdown prompts or changing TOML adapters. | doc | N/A | PLN-DI-013..014 | `AGENTS.md`, `.codex/README.md`, and Codex provider notes updated; `.codex/agents/*.toml` unchanged. | Codex | Completed |
| T-004 | Add QA/CI/CD local/remote/skipped-check evidence matrix. | doc | N/A | PLN-DI-015 | QA scope and GitHub governance now map change types to local checks, CI-only gates, hook/script evidence, and skip rationale. | Codex | Completed |
| T-005 | Add template deviation exception criteria without rewriting template sources or historical docs. | doc | N/A | PLN-DI-011 | Template README, documentation protocol, and Stage Authoring Matrix record exception evidence requirements. | Codex | Completed |
| T-006 | Update Stage 04 plan/task indexes and progress log for the continuation task. | doc/memory | N/A | PLN-DI-016 | Plan/task READMEs and progress log updated; LLM Wiki index regenerated with 1029 paths after fresh revalidation. | Codex | Completed |
| T-007 | Run verification commands from the plan and record results, including Graphify advisory reason. | eval | N/A | VAL-DI-001..011 | Verification summary records PASS/advisory outcomes. | Codex | Completed |

## Suggested Types

- `doc`
- `eval`
- `memory`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`

## Phase View (Optional)

### Stage 00 -> Template Contract -> Skills -> Codex Harness -> QA/CI/CD -> Evidence

- [x] T-001 Plan gap coverage.
- [x] T-002 Stage 00 governance gates.
- [x] T-003 Codex harness alignment.
- [x] T-004 QA/CI/CD evidence matrix.
- [x] T-005 Template deviation criteria.
- [x] T-006 Index, progress, and LLM Wiki updates.
- [x] T-007 Verification evidence.

## Verification Summary

- **Test Commands**:
  - `git diff --check` — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` — PASS (`failures=0`; `changed_template_docs_total=4`; `normalized_changed_template_docs_total=4`; `target_stage_docs_total=514`; `normalized_target_stage_docs_total=514`).
  - `bash scripts/validation/check-doc-traceability.sh` — PASS (`failures=0`; `catalog_pairs_total=46`).
  - `bash scripts/validation/check-quickwin-baseline.sh` — PASS (`services_total=5`; baseline enforced).
  - `bash scripts/validation/check-template-security-baseline.sh` — PASS (`template_adoption_missing=0`; required security controls enforced).
  - `bash scripts/operations/sync-provider-surfaces.sh` — PASS (`no drift`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh` — regenerated `docs/90.references/llm-wiki/index.md` with 1029 paths after fresh revalidation.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/knowledge/report-graphify-health.sh` — advisory (`surprising_cross_root_inferred_edges=3`).
  - `rg -n "gpt-5\\.1|gemini-3-pro|unsupported|TBD|TODO" docs/00.agent-governance .codex AGENTS.md docs/04.execution` — advisory hits only: historical progress/task references, scan command literals, existing `.codex/skills/adr-writing/skill.md` instructional `TBD`, and the QA matrix word `unsupported`; no model/reasoning value was changed.
- **Eval Commands**:
  - `graphify-out/GRAPH_REPORT.md` was read before Graphify health usage; report status is advisory because of `surprising_cross_root_inferred_edges=3`.
  - `.codex/agents/*.toml` and `.codex/agents/*.md` surfaces were inspected by path listing; no adapter/model/reasoning edits were made.
  - Graphify advisory claims were corroborated against tracked Stage 00 docs, Codex runtime notes, and Stage 04 task/plan evidence.
- **Logs / Evidence Location**:
  - This task document.
  - [Progress log](../../00.agent-governance/memory/progress.md)

## Related Documents

- **Parent Plan**: [Agent Governance Decision Items Implementation Plan](../plans/2026-06-02-agent-governance-decision-items-plan.md)
- **Plans README**: [Execution Plans](../plans/README.md)
- **Tasks README**: [Execution Tasks](./README.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **QA Scope**: [Quality Assurance Scope](../../00.agent-governance/scopes/qa.md)
- **Template Catalog**: [99.templates](../../99.templates/README.md)
