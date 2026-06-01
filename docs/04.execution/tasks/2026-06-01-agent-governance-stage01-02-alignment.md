---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md -->

# Task: Agent Governance Stage 01/02 Alignment

## Overview (KR)

이 문서는 Phase 1 진단과 Phase 2 alignment plan을 바탕으로 Agent Governance의 Stage 01/02 근거 문서를 추가하고, 기존 Phase 2 계획과 README 색인을 보강한 실행 증거다.

## Inputs

- **Parent PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **Parent ARD**: [Agent Governance Canonical Adapter ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **Parent ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Parent Plan**: [Agent Governance Phase 2 Alignment Plan](../plans/2026-06-01-agent-governance-phase2-alignment.md)

## Working Rules

- Do not rewrite historical Phase 2/3/4 evidence beyond minimum traceability links.
- Do not modify existing tier/service PRD, ARD, or ADR files.
- Do not convert HADS advisory guidance into mandatory template structure.
- Do not mutate Docker runtime, secrets, deployment state, remote GitHub settings, or user-global Codex settings.
- Documentation-only work still requires repository contract, traceability, provider sync, LLM Wiki, diff hygiene, and Graphify advisory checks.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-S12-001 | Add Agent Governance PRD for Stage 01 requirements traceability. | doc | PRD | Phase 2 review | `docs/01.requirements/2026-06-01-agent-governance-standardization.md` | Codex | Completed |
| T-S12-002 | Add ARD and ADR for the Stage 00 canonical adapter model. | doc | ARD/ADR | Phase 2 review | `0027-agent-governance-canonical-adapter.md`, `0027-stage-00-canonical-adapter-model.md` | Codex | Completed |
| T-S12-003 | Update Stage 01/02 README inventories and Phase 2 plan links. | doc | README / Plan | Phase 2 review | Parent indexes and `2026-06-01-agent-governance-phase2-alignment.md` updated. | Codex | Completed |
| T-S12-004 | Record progress and run validation gates. | eval | N/A | Verification | Verification Summary records final results. | Codex | Completed |

## Suggested Types

- `doc`
- `eval`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`

## Phase View (Optional)

### Stage 01/02 Alignment

- [x] T-S12-001 Add PRD.
- [x] T-S12-002 Add ARD/ADR.
- [x] T-S12-003 Sync indexes and links.
- [x] T-S12-004 Run and record validation.

## Verification Summary

- **Test Commands**:
  - `git diff --check` — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` — PASS (`failures=0`; `target_stage_docs_total=511`; `normalized_target_stage_docs_total=511`).
  - `bash scripts/validation/check-doc-traceability.sh` — PASS (`failures=0`; `catalog_pairs_total=46`).
  - `bash scripts/operations/sync-provider-surfaces.sh` — PASS (`no drift`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — PASS.
- **Eval Commands**:
  - Graphify report read first and kept advisory.
  - Stage authoring matrix, PRD/ARD/ADR templates, Stage 01/02 READMEs, Phase 1 diagnostic, and Phase 2 plan inspected.
  - `bash scripts/knowledge/report-graphify-health.sh` — advisory (`surprising_cross_root_inferred_edges=3`).
- **Logs / Evidence Location**:
  - This task document.
  - `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Parent PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **Parent ARD**: [Agent Governance Canonical Adapter ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **Parent ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Parent Plan**: [Agent Governance Phase 2 Alignment Plan](../plans/2026-06-01-agent-governance-phase2-alignment.md)
- **Phase 1 Diagnostic**: [Agent Governance Phase 1 Diagnostic](../plans/2026-06-01-agent-governance-phase1-diagnostic.md)
