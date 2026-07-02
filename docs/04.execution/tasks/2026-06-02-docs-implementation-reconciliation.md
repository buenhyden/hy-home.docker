---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-06-02-docs-implementation-reconciliation.md -->

# Task: Docs Implementation Reconciliation

## Overview

This document records actual work evidence for comparing Stage 01 through Stage 05 active documents against the current tracked implementation and adding implementation-alignment gates.

## Inputs

- **Parent Plan**: [Docs Implementation Reconciliation Plan](../plans/2026-06-02-docs-implementation-reconciliation.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **QA Scope**: [QA scope](../../00.agent-governance/scopes/qa.md)
- **Root Compose**: [Root docker-compose.yml](../../../docker-compose.yml)
- **Scripts README**: [Scripts index](../../../scripts/README.md)

## Working Rules

- Treat tracked repository state as current implementation truth.
- Do not classify optional/commented root includes as unimplemented when tracked `infra/**` service implementation exists.
- Move whole-document conflicts to `docs/98.archive/<original-stage>/<same-relative-path>` tombstones only when the full document is stale current-truth.
- Do not link active docs directly to individual tombstones; active docs may use the archive README/index only.
- Do not read, print, or commit secret values.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| policy | User approved policy/governance updates in this task request. | Stage 00 documentation protocol, QA scope, GitHub governance, stage matrix | No dedicated implementation-alignment gate in Stage 00 docs. | Stage 00 docs point to `check-doc-implementation-alignment.sh` and local/remote evidence boundaries. | Revert governance doc hunks if validator is removed or misclassified. | No secrets involved. |
| CI | User approved CI/CD inspection and update. | `.github/workflows/ci-quality.yml`, `.github/rulesets/main-protection.md` | CI had docs traceability and repo-contract jobs, but no implementation-alignment job. | Added `docs-implementation-alignment`; local ruleset proposal lists it while remote enforcement remains re-verification-bound. | Remove job and required-check proposal if validation contract is withdrawn. | Remote mutation not performed. |
| templates | User approved template-related cleanup. | Active docs and template mapping references | Active docs still mentioned the retired consolidated operations template. | Active docs use `guide.template.md`, `policy.template.md`, and `runbook.template.md`. | Revert text updates if template source changes back. | No secrets involved. |
| secrets/remote/model/provider | User approved these surfaces, but no concrete mutation was required. | N/A | N/A | Verified as metadata/no-change only. | N/A | Secret values not read; remote GitHub not mutated; model/provider values unchanged. |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DIR-001 | Read Graphify report first and treat advisory graph as navigation only. | eval | N/A | PLN-DIR-001 | Graphify report advisory due `surprising_cross_root_inferred_edges=3`. | Codex | Completed |
| T-DIR-002 | Add implementation-alignment validator for active docs. | test | N/A | PLN-DIR-002 | `check-doc-implementation-alignment.sh` added and passes. | Codex | Completed |
| T-DIR-003 | Remove known stale operations template references. | doc | N/A | PLN-DIR-004 | Removed the retired consolidated operations template name from active scan scope; replacement mapping uses guide/policy/runbook templates. | Codex | Completed |
| T-DIR-004 | Wire implementation-alignment check into CI and governance. | ci/doc | N/A | PLN-DIR-003 | CI job, repo-contract job list, local ruleset proposal, QA scope, GitHub governance, scripts README updated. | Codex | Completed |
| T-DIR-005 | Record Stage 04 evidence and index updates. | doc/memory | N/A | PLN-DIR-005 | Plan/task READMEs and progress log updated. | Codex | Completed |
| T-DIR-006 | Run final validation and generated surface refresh. | eval | N/A | PLN-DIR-006 | Verification summary records command outcomes. | Codex | Completed |

## Suggested Types

- `doc`
- `test`
- `ci`
- `eval`
- `memory`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`

## Phase View (Optional)

### Phase 1 - Discovery and Validator

- [x] T-DIR-001 Read Graphify and corroborate against tracked sources.
- [x] T-DIR-002 Add active-doc implementation-alignment validator.

### Phase 2 - Reconciliation

- [x] T-DIR-003 Remove stale template references.
- [x] T-DIR-004 Wire validator into CI/governance/scripts surfaces.
- [x] T-DIR-005 Record Stage 04 evidence and progress.

### Phase 3 - Verification

- [x] T-DIR-006 Run validation and generated-surface refresh.

## Disposition Evidence

| Disposition | Count / Scope | Evidence |
| --- | --- | --- |
| `keep` | Active Stage docs without validator findings after reconciliation. | `stage_docs_total=500`, `failures=0` after adding this plan/task pair. |
| `update` | 3 active docs with 8 removed template-name references, plus governance/scripts/CI/index surfaces updated for the new gate. | Removed-template mention count is `0` after edits. |
| `integrate` | 0 whole-document integrations required in this pass. | No duplicate evidence requiring canonical merge was found by the implementation-alignment gate. |
| `archive` | 0 whole-document archive moves required in this pass. | `archive_direct_links_total=0`; Stage 05 service docs map to tracked implementation or explicit non-service exceptions. |

## Implementation Alignment Results

| Check | Result |
| --- | --- |
| Active Stage docs scanned | `500` after adding this plan/task pair |
| Repo-local Markdown links checked | `3384` |
| Removed consolidated operations template mentions | `0` |
| Active direct links to individual tombstones | `0` |
| Operations service docs checked | `143` |
| Operations service docs with active root include | `49` |
| Operations service docs with optional/commented root include | `60` |
| Validator failures | `0` |

## Verification Summary

- **Test Commands**:
  - `bash scripts/validation/check-doc-implementation-alignment.sh` — PASS (`stage_docs_total=500`; `repo_local_markdown_links_checked=3384`; removed-template mention count `0`; archive direct links `0`; `operations_service_docs_checked=143`; `operations_service_docs_root_active=49`; `operations_service_docs_root_optional=60`; `failures=0`).
  - `git diff --check` — PASS.
  - `bash scripts/validation/check-repo-contracts.sh` — PASS (`failures=0`; `changed_template_docs_total=7`; `normalized_changed_template_docs_total=7`; `target_stage_docs_total=530`; `normalized_target_stage_docs_total=530`; `legacy_target_stage_docs_skipped=0`).
  - `bash scripts/validation/check-doc-traceability.sh` — PASS (`failures=0`; `catalog_pairs_total=46`).
  - `bash scripts/validation/validate-docker-compose.sh` — PASS (`Compose profiles: core`; `services_total=5`).
  - `bash scripts/hardening/check-all-hardening.sh` — PASS (`ALL checks passed successfully`).
- **Eval Commands**:
  - `bash scripts/operations/sync-provider-surfaces.sh` — PASS (`no drift`).
  - `bash scripts/knowledge/generate-llm-wiki-index.sh` — regenerated `docs/90.references/data/llm-wiki/index.md` with 1033 paths.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — PASS.
  - `/home/hy/.local/bin/graphify update .` — refreshed `graphify-out` with 2412 nodes, 2833 edges, and 125 communities.
  - `bash scripts/knowledge/report-graphify-health.sh` — advisory (`manifest_paths_total=825`; `surprising_cross_root_inferred_edges=3`; no volume, gitlink, generated/minified contamination, or meaningless god nodes).
- **Logs / Evidence Location**:
  - This task document.
  - [Progress log](../../00.agent-governance/memory/progress.md)
  - [LLM Wiki index](../../90.references/data/llm-wiki/index.md)
  - [Graphify report](../../../graphify-out/GRAPH_REPORT.md)

## Related Documents

- **Parent Plan**: [Docs Implementation Reconciliation Plan](../plans/2026-06-02-docs-implementation-reconciliation.md)
- **Plans README**: [Execution Plans](../plans/README.md)
- **Tasks README**: [Execution Tasks](./README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **QA Scope**: [QA scope](../../00.agent-governance/scopes/qa.md)
- **GitHub Governance**: [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- **Archive Index**: [Archive index](../../98.archive/README.md)
- **Scripts Index**: [Scripts index](../../../scripts/README.md)
