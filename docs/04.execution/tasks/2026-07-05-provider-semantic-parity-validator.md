---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md -->

# Task: Provider Semantic Parity Validator

## Overview

This document records implementation and verification evidence for closing the
provider semantic role-scope parity gap.

## Inputs

- **Parent Spec**: [Provider semantic parity validator spec](../../03.specs/107-provider-semantic-parity-validator/spec.md)
- **Parent Plan**: [Provider semantic parity validator plan](../plans/2026-07-05-provider-semantic-parity-validator.md)
- **Automation Candidate**: [Agentic engineering automation candidates](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)

## Working Rules

- Keep Stage 00 as the canonical source of agent role scope.
- Do not change model policy, hook behavior, provider runtime configuration,
  credentials, secrets, remote state, or CI workflow behavior.
- Generated provider adapter metadata may change only to reflect canonical role
  scope.
- Commit by logical unit.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 03/04 evidence | User continued next provider/document cleanup on 2026-07-05 | Spec, plan, task, indexes | `AEA-AUTO-002` had no active-stage implementation evidence | Spec, plan, task, and indexes record the provider semantic parity implementation | Revert planning commit | No secret values or raw logs |
| Provider generator | User-approved provider adapter cleanup and audit candidate | `scripts/operations/sync-provider-surfaces.sh` | Codex agent scope was generated from catalog frontmatter `layer` instead of semantic `Scope import` | Generator now derives agent role scope from Stage 00 `Scope import` before fallback to frontmatter | Revert generator commit; rerun sync | Path/literal metadata only |
| Provider adapters | User-approved provider adapter cleanup | `.codex/agents/*.toml`, `.agents/agents/*.md` | Generated adapter scope could drift from Stage 00 role scope | Codex TOML and Gemini pointer adapter layers now reflect canonical role scopes such as `ops`, `common`, and `infra` | Rerun provider sync from previous generator or revert commit | No credentials or local auth files |
| Validator | User-approved governance/validator cleanup | `scripts/validation/check-repo-contracts.sh` | Repo contracts did not enforce cross-provider role-scope semantic parity | Repo contracts now enforce Claude, Codex, Gemini, and subagent protocol role-scope parity | Revert validator commit | Path/literal checks only |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-PSPV-001 | Create Stage 03/04 evidence | doc | `Contracts` | `PLN-PSPV-001` | Spec/plan/task and indexes | Documentation Specialist | Done |
| T-PSPV-002 | Update provider sync generator | impl | `Config Contract` | `PLN-PSPV-002` | Provider sync `--write` and `--check` | Agentic Workflow Specialist | Done |
| T-PSPV-003 | Add semantic parity validation | validation | `Governance Contract` | `PLN-PSPV-003` | Repo contracts pass with new semantic gate | QA Engineer | Done |
| T-PSPV-004 | Update audit/progress evidence and close | evidence | `Success Criteria` | `PLN-PSPV-004` | Final validation summary and progress memory | Documentation Specialist | Done |

## Phase View

### Phase 1: Planning

- [x] T-PSPV-001 Create Stage 03/04 evidence.

### Phase 2: Implementation

- [x] T-PSPV-002 Update provider sync generator.
- [x] T-PSPV-003 Add semantic parity validation.

### Phase 3: Closure

- [x] T-PSPV-004 Update audit/progress evidence and close.

## Verification Summary

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` after scaffold | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/validation/check-doc-traceability.sh` after scaffold | PASS | `failures=0`. |
| `bash scripts/validation/check-repo-contracts.sh` after scaffold | PASS | `failures=0`; changed target-stage docs normalized. |
| `bash -n scripts/operations/sync-provider-surfaces.sh` | PASS | Generator syntax is valid. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` before regeneration | FAIL (expected) | Drift detected for Codex/Gemini agent adapters whose role scope was still `agentic`. |
| `bash scripts/operations/sync-provider-surfaces.sh --write` | PASS | Generated Codex TOML and Gemini pointer adapters from canonical Stage 00 role scope. |
| `bash -n scripts/operations/sync-provider-surfaces.sh scripts/validation/check-repo-contracts.sh` | PASS | Generator and validator syntax are valid. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` after regeneration | PASS | `sync-provider-surfaces: no drift`. |
| `bash scripts/validation/check-repo-contracts.sh` after validator update | PASS | Semantic role-scope parity gate passes; `failures=0`. |
| `git diff --check` final closure | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` final closure | PASS | Generated LLM Wiki index is fresh after staged files are visible to `git ls-files`. |
| `bash scripts/validation/check-doc-traceability.sh` final closure | PASS | `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` final closure | PASS | `failures=0`; active docs align with tracked implementation surfaces. |
| `bash scripts/validation/check-repo-contracts.sh` final closure | PASS | `failures=0`. |
| `/home/hy/.local/bin/graphify update .` | PASS | Refreshed `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json`; HTML viz skipped because graph is over the node limit. |
| `bash scripts/knowledge/report-graphify-health.sh` | PASS | `status=advisory`, contamination `0`, `surprising_cross_root_inferred_edges=2`; corroborate with tracked docs. |

## Related Documents

- **Parent Spec**: [Provider semantic parity validator spec](../../03.specs/107-provider-semantic-parity-validator/spec.md)
- **Parent Plan**: [Provider semantic parity validator plan](../plans/2026-07-05-provider-semantic-parity-validator.md)
- **Provider capability matrix**: [../../00.agent-governance/rules/provider-capability-matrix.md](../../00.agent-governance/rules/provider-capability-matrix.md)
- **Provider adapter model**: [../../00.agent-governance/providers/agents-md.md](../../00.agent-governance/providers/agents-md.md)
