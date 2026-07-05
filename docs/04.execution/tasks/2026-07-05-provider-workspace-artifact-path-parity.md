---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-05-provider-workspace-artifact-path-parity.md -->

# Task: Provider Workspace Artifact Path Parity

## Overview

This task records execution evidence for aligning provider/runtime artifact
paths with the `_workspace/repo-support/` contract.

## Inputs

- **Parent Plan**: [Provider Workspace Artifact Path Parity Plan](../plans/2026-07-05-provider-workspace-artifact-path-parity.md)
- **Workspace Support Surface Spec**: [Workspace support surface contract](../../03.specs/106-workspace-support-surface-contract/spec.md)
- **Provider Audit Candidate**: [Agentic engineering automation candidates](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)

## Working Rules

- Keep Stage 00 and Stage 99 as policy owners.
- Treat provider files as adapters and runtime-facing guidance.
- Do not read or write secret values, credentials, tokens, private keys, raw
  logs, shell history, or `.env` values.
- Do not change model policy, provider runtime configuration, hook behavior, or
  remote provider settings.
- Commit by logical unit.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 04 evidence | User continued next document/provider cleanup on 2026-07-05 | this task and parent plan | No dedicated provider path parity evidence | Plan/task evidence records provider path parity, validator, and closure results | Revert planning commit | No secret values or raw logs |
| Provider/runtime adapters | User-approved broad provider and contract cleanup; workspace support contract fallout | `.claude/**`, `.codex/**`, `.agents/**` active provider surfaces | Focused scan found stale `_workspace/` artifact paths | Provider/runtime artifact paths now use `_workspace/repo-support/`; generated Codex skill mirrors refreshed | Revert provider parity commit; rerun provider sync | No provider credentials or local auth files |
| Workflow agent design | Workspace support contract fallout | `docs/03.specs/008-workflow/agent-design.md` | Active agent design still names root `_workspace/` output paths | Workflow agent design now records outputs under `_workspace/repo-support/` | Revert provider parity commit | No secret values or raw logs |
| Validator | User-approved governance/validator cleanup | `scripts/validation/check-repo-contracts.sh` | Repo contracts do not block provider root `_workspace/` artifact paths | Repo contracts now block active provider/workflow root `_workspace/` artifact paths outside `_workspace/repo-support/` | Revert validator commit | Path/literal checks only |

## Task Table

| Task ID | Description | Type | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-PWAP-001 | Create Stage 04 plan/task evidence | doc | `PLN-PWAP-001` | Plan/task files and indexes | Documentation Specialist | Done |
| T-PWAP-002 | Normalize provider/runtime artifact paths | provider-doc | `PLN-PWAP-002` | Focused stale path scan; provider sync | Documentation Specialist | Done |
| T-PWAP-003 | Add provider path parity validation | validation | `PLN-PWAP-003` | Repo contracts include provider path parity gate | QA / Validator Maintainer | Done |
| T-PWAP-004 | Validate, update progress, and close evidence | evidence | `PLN-PWAP-004` | Final validation summary and progress memory | Documentation Specialist | Done |

## Phase View

### Phase 1: Planning

- [x] T-PWAP-001 Create Stage 04 plan/task evidence.

### Phase 2: Provider Parity

- [x] T-PWAP-002 Normalize provider/runtime artifact paths.
- [x] T-PWAP-003 Add provider path parity validation.

### Phase 3: Closure

- [x] T-PWAP-004 Validate, update progress, and close evidence.

## Evidence Inventory

| Evidence Class | Evidence Path / Source | Role |
| --- | --- | --- |
| Graphify report | `graphify-out/GRAPH_REPORT.md` | Refreshed with `/home/hy/.local/bin/graphify update .`; advisory due cross-root inferred edges and used only as navigation context. |
| Current provider drift | Focused `_workspace` scans over `.agents`, `.claude`, `.codex` | Shows active provider/runtime stale artifact paths before this batch. |
| Workspace support surface | [Workspace support surface contract](../../03.specs/106-workspace-support-surface-contract/spec.md) | Defines `_workspace/repo-support/` as approved staging path. |
| Provider sync | `scripts/operations/sync-provider-surfaces.sh` | Keeps Codex skill mirrors and Gemini reference indexes aligned. |

## Deviation Log

| Deviation | Reason | Resolution |
| --- | --- | --- |
| None yet | N/A | N/A |

## Verification Summary

Validation results will be appended as each logical unit completes.

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` after planning scaffold | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/validation/check-doc-traceability.sh` after planning scaffold | PASS | `failures=0`. |
| `bash scripts/validation/check-repo-contracts.sh` after planning scaffold | PASS | `failures=0`; changed target-stage docs normalized. |
| `bash scripts/operations/sync-provider-surfaces.sh --write` after provider path update | PASS | Generated Codex skill mirrors and Gemini reference indexes refreshed. |
| `rg --pcre2 -n "_workspace/(?!repo-support\|README\\.md)" .agents .claude .codex docs/03.specs/008-workflow/agent-design.md --glob '*.md' --glob '*.toml' --glob '*.json'` | PASS | No active stale provider/workflow root `_workspace` artifact paths remain. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` after provider path update | PASS | `sync-provider-surfaces: no drift`. |
| `git diff --check` after provider path update | PASS | No whitespace or conflict-marker issues. |
| `bash -n scripts/validation/check-repo-contracts.sh` after validator update | PASS | Shell syntax is valid. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh` | PASS | Regenerated `docs/90.references/llm-wiki/llm-wiki-index.md` with provider path parity task/plan entries. |
| `bash scripts/validation/check-repo-contracts.sh` after validator update | PASS | Provider workspace artifact path parity gate passes; `failures=0`. |
| `/home/hy/.local/bin/graphify update .` | PASS | Refreshed `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json`; HTML viz skipped because graph is over the node limit. |
| `bash scripts/knowledge/report-graphify-health.sh` | PASS | `status=advisory`, contamination `0`, `surprising_cross_root_inferred_edges=2`; corroborate with tracked docs. |
| `git diff --check` final closure | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` final closure | PASS | `sync-provider-surfaces: no drift`. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` final closure | PASS | Generated LLM Wiki index is fresh. |
| `bash scripts/validation/check-doc-traceability.sh` final closure | PASS | `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` final closure | PASS | `failures=0`; active docs align with tracked implementation surfaces. |
| `bash scripts/validation/check-repo-contracts.sh` final closure | PASS | `failures=0`. |

## Related Documents

- **Parent Plan**: [Provider Workspace Artifact Path Parity Plan](../plans/2026-07-05-provider-workspace-artifact-path-parity.md)
- **Workspace Support Surface Spec**: [Workspace support surface contract](../../03.specs/106-workspace-support-surface-contract/spec.md)
- **Workflow Agent Design**: [Workflow agent design](../../03.specs/008-workflow/agent-design.md)
- **Provider Capability Matrix**: [Provider capability matrix](../../00.agent-governance/rules/provider-capability-matrix.md)
