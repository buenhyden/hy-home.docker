---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md -->

# Task: Agent Governance Missing Items Implementation

## Overview

This document records missing-item strengthening against attachments for `2026-06-02-agent-governance-decision-items-plan.md` and phased implementation evidence.

Past Phase execution artifacts that conflict with the current implementation are removed from the active chain and moved to `docs/98.archive/` tombstones. Current-baseline corrections are reflected as continuation work across Stage 00, Codex harness, Template Contract, QA/CI/CD, and the Stage 04 evidence surface.

## Inputs

- **Parent Plan**: [Agent Governance Decision Items Implementation Plan](../plans/2026-06-02-agent-governance-decision-items-plan.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Template Catalog**: [99.templates](../../99.templates/README.md)

## Working Rules

- Archive completed Phase artifacts when their body conflicts with current tracked implementation.
- Keep Stage 00 as the governance SSoT; do not create duplicate provider-local policy.
- User approved protected surface changes and approval-gated unfinished items on 2026-06-02.
- Retire `.codex/agents/*.md` compatibility prompt context in this approved follow-up.
- Do not change Docker runtime, GitHub remote settings, secrets, deployment, or user-global Codex settings.
- Treat model/reasoning changes and live runtime/deployment/secret/remote changes as separate human approval gates.
- The 2026-06-02 approval closes the bounded repo-tracked gates for HADS profile rollout, Docker hard-validator promotion, Codex Markdown prompt retirement, and protected Stage 00/template/validator surfaces.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add Attachment Gap Coverage and WBS PLN-DI-009 through PLN-DI-016 to the decision-items plan. | doc | N/A | PLN-DI-009..016 | Parent plan includes gap matrix, added WBS rows, verification rows, risks, and completion criteria. | Codex | Completed |
| T-002 | Add Stage 00 clarification duty, current-to-desired governance matrix, skill lifecycle, template deviation audit, and model/config gates. | doc | N/A | PLN-DI-009..014 | `docs/00.agent-governance/README.md`, workflows, checklists, documentation protocol, Stage Authoring Matrix, and function catalog README updated. | Codex | Completed |
| T-003 | Add Codex harness alignment gates around TOML-only adapters and retired Markdown prompt adapters. | doc | N/A | PLN-DI-013..014 | `AGENTS.md`, `.codex/README.md`, Codex provider notes, and repo contracts enforce TOML-only Codex adapters. | Codex | Completed |
| T-004 | Add QA/CI/CD local/remote/skipped-check evidence matrix. | doc | N/A | PLN-DI-015 | QA scope and GitHub governance now map change types to local checks, CI-only gates, hook/script evidence, and skip rationale. | Codex | Completed |
| T-005 | Add template deviation exception criteria without rewriting template sources or historical docs. | doc | N/A | PLN-DI-011 | Template README, documentation protocol, and Stage Authoring Matrix record exception evidence requirements. | Codex | Completed |
| T-006 | Update Stage 04 plan/task indexes and progress log for the continuation task. | doc/memory | N/A | PLN-DI-016 | Plan/task READMEs and progress log updated; LLM Wiki index regenerated with 1029 paths after fresh revalidation. | Codex | Completed |
| T-007 | Run verification commands from the plan and record results, including Graphify advisory reason. | eval | N/A | VAL-DI-001..011 | Verification summary records PASS/advisory outcomes. | Codex | Completed |
| T-008 | Record the 2026-06-02 approval-gate closure scope in the parent plan and task evidence. | doc | N/A | Approved Gate Closure | Parent plan addendum and this task evidence distinguish repo-tracked protected surfaces from live runtime/remote state. | Codex | Completed |
| T-009 | Retire Codex Markdown prompt adapters and make `.codex/agents/*.toml` the sole Codex agent adapter surface. | doc/script | N/A | Codex Markdown prompt retirement | `.codex/agents/*.md` removed; TOML adapters, provider docs, sync script, and repo contracts updated. | Codex | Completed |
| T-010 | Promote Docker hardening from manual boundary to repo-contract hard validator. | script/doc | N/A | Docker hard-validator promotion | `check-repo-contracts.sh` runs `scripts/hardening/check-all-hardening.sh` as a hard gate. | Codex | Completed |
| T-011 | Implement bounded HADS mandatory rollout for `docs/90.references/data/hads/`. | doc/script | N/A | HADS mandatory rollout | HADS profile reference docs added and repo contracts validate HADS profile shape. | Codex | Completed |
| T-012 | Update indexes, progress, and LLM Wiki for approved gate closure. | doc/memory | N/A | Evidence closure | `docs/90.references/README.md`, progress log, and LLM Wiki index updated; LLM Wiki regenerated with 1014 paths. | Codex | Completed |
| T-013 | Run verification for protected surface changes and record results. | eval | N/A | Verification | Verification summary records protected-surface checks. | Codex | Completed |
| T-014 | Add archive stage governance and move conflicting old execution artifacts to tombstones. | doc/script | N/A | PLN-DI-001, PLN-DI-004 | `docs/98.archive/`, archive template, stage matrix, documentation protocol, QA/CI notes, and repo contracts updated. | Codex | Completed |

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
- [x] T-008 Approval-gate closure scope.
- [x] T-009 Codex Markdown prompt retirement.
- [x] T-010 Docker hard-validator promotion.
- [x] T-011 HADS mandatory reference profile.
- [x] T-012 Index, progress, and LLM Wiki refresh for approved gate closure.
- [x] T-013 Protected-surface verification evidence.
- [x] T-014 Archive stage and stale execution tombstones.

## Verification Summary

- **Test Commands**:
  - `git diff --check` — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` — PASS (`failures=0`; `changed_template_docs_total=4`; `normalized_changed_template_docs_total=4`; `target_stage_docs_total=514`; `normalized_target_stage_docs_total=514`).
  - `bash scripts/validation/check-doc-traceability.sh` — PASS (`failures=0`; `catalog_pairs_total=46`).
  - `bash scripts/validation/check-quickwin-baseline.sh` — PASS (`services_total=5`; baseline enforced).
  - `bash scripts/validation/check-template-security-baseline.sh` — PASS (`template_adoption_missing=0`; required security controls enforced).
  - `bash scripts/operations/sync-provider-surfaces.sh` — PASS (`no drift`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh` — regenerated `docs/90.references/data/llm-wiki/index.md` with 1029 paths after fresh revalidation.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/knowledge/report-graphify-health.sh` — advisory (`surprising_cross_root_inferred_edges=3`).
  - `rg -n "gpt-5\\.1|gemini-3-pro|unsupported|TBD|TODO" docs/00.agent-governance .codex AGENTS.md docs/04.execution` — advisory hits only: historical progress/task references, scan command literals, existing `.codex/skills/adr-writing/skill.md` instructional `TBD`, and the QA matrix word `unsupported`; no model/reasoning value was changed.
  - `bash -n scripts/validation/check-repo-contracts.sh scripts/operations/sync-provider-surfaces.sh` — PASS.
  - `bash scripts/hardening/check-all-hardening.sh` — PASS (`Summary: ALL checks passed successfully.`).
  - `bash scripts/operations/sync-provider-surfaces.sh` after Codex prompt retirement — PASS (`no drift`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh` after approved gate closure — regenerated `docs/90.references/data/llm-wiki/index.md` with 1014 paths.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` after approved gate closure — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` after approved gate closure — PASS (`failures=0`; `changed_template_docs_total=6`; `normalized_changed_template_docs_total=6`; `target_stage_docs_total=516`; `normalized_target_stage_docs_total=516`).
  - `rg -n "gpt-5\\.1|gemini-3-pro|unsupported|TBD|TODO|legacy_markdown_adapter" docs/00.agent-governance .codex AGENTS.md docs/04.execution scripts/operations scripts/validation` after approved gate closure — advisory hits only: historical progress/task references, scan command literals, existing validator/QA wording, existing `.codex/skills/adr-writing/skill.md` instructional `TBD`, and no `legacy_markdown_adapter` references.
- **Eval Commands**:
  - `graphify-out/GRAPH_REPORT.md` was read before Graphify health usage; report status is advisory because of `surprising_cross_root_inferred_edges=3`.
  - `.codex/agents/*.toml` and `.codex/agents/*.md` surfaces were inspected by path listing; Markdown prompt adapters were retired, TOML adapter metadata no longer references them, and no model/reasoning values were changed.
  - Graphify advisory claims were corroborated against tracked Stage 00 docs, Codex runtime notes, and Stage 04 task/plan evidence.
  - User approval on 2026-06-02 enabled protected repo-tracked surface changes. Live Docker runtime, deployment, secrets, user-global Codex settings, and remote GitHub protection state were not mutated.
  - Current Stage 01-04 implementation-alignment cleanup archived conflicting old execution artifacts and unimplemented 07-workflow operations docs, regenerated LLM Wiki with 1016 paths, and revalidated repo contracts (`failures=0`), doc traceability (`failures=0`), hardening (`ALL checks passed successfully`), LLM Wiki freshness, and diff hygiene.
  - `graphify update .` was skipped because the `graphify` CLI was unavailable in PATH; `report-graphify-health.sh` remains advisory due `surprising_cross_root_inferred_edges=3`, so completion claims were corroborated against tracked docs and validators.
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
