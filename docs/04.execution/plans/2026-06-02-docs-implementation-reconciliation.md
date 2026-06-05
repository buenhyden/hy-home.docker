---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-06-02-docs-implementation-reconciliation.md -->

# Docs Implementation Reconciliation Plan

## Overview

This document is the implementation plan for comparing active Stage documents from `docs/01.requirements` through `docs/05.operations` against the current tracked implementation and resolving stale, legacy, deprecated-only, and implementation-conflicting content.

Completion for this work is not merely passing link validation. Current-truth claims in active documents must align with the root `docker-compose.yml`, `infra/**`, `scripts/**`, `.github/workflows/**`, `docs/99.templates/**`, Stage 00 governance, and provider/agent adapter surfaces.

## Context

Existing repository validators already strongly check template shape, traceability, provider sync, LLM Wiki freshness, hardening, script ownership, and GitHub workflow security. However, there was no dedicated gate that directly checked whether active Stage documents conflict with the current implementation.

Graphify is advisory because of `surprising_cross_root_inferred_edges=3`. Therefore, use Graphify only as an exploration aid, and corroborate implementation-alignment judgments with tracked source files, Stage 00 governance, Stage 01-05 docs, and validators.

## Goals & In-Scope

- **Goals**:
  - Compare the baseline 498 active Stage 01-05 documents against implementation truth, then run the same gate against the full Stage 01-05 set after this plan/task evidence is added.
  - Record results with `keep`, `update`, `integrate`, or `archive` dispositions.
  - Add validators that prevent recurrence of removed operations template names, archive direct links, and Stage 05 service-doc-to-`infra/**` mismatches.
  - Align CI, governance, scripts catalog, Stage README, and progress evidence with the current validation system.
- **In Scope**:
  - Stage 04 plan/task evidence.
  - `scripts/validation/check-doc-implementation-alignment.sh`.
  - `.github/workflows/ci-quality.yml` docs implementation-alignment job.
  - Local branch protection proposal and GitHub governance job taxonomy updates.
  - Known stale retired consolidated operations template references.
  - Stage 04 README indexes and progress log.
  - Generated LLM Wiki and Graphify surfaces.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not change public runtime API, Compose service behavior, secret values, model policy, or provider adapter contracts.
  - Do not treat optional/commented root includes as unimplemented services when tracked `infra/**` implementation exists.
  - Do not preserve implementation-conflicting whole-document stale truth in active docs.
- **Out of Scope**:
  - Remote GitHub mutation unless a concrete protected-surface mismatch requires a separate audited action.
  - Secret value reading or disclosure.
  - Broad historical rewriting where current-truth claims are not present.

## Disposition Rules

| Disposition | Criteria | Action |
| --- | --- | --- |
| `keep` | Document aligns with tracked implementation or is historical evidence that does not claim stale current truth. | Leave active. |
| `update` | Document responsibility is valid, but template name, path, root include status, script/CI name, or operations state is stale. | Edit in place and record evidence. |
| `integrate` | Duplicate/noncanonical document contains reusable evidence for a canonical active document. | Move evidence to canonical target, then archive old document. |
| `archive` | Whole document is deprecated-only, legacy-only, conflicts with current implementation, or describes a service with no tracked implementation as current truth. | Move to `docs/98.archive/<original-stage>/<same-relative-path>` tombstone and update archive README ledger. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-DIR-001 | Corroborate Graphify advisory output against tracked docs and implementation surfaces. | `graphify-out/GRAPH_REPORT.md`, Stage 00, Stage 01-05, `infra/**`, scripts, CI | REQ-AGG-NFR-05 | Task records advisory status and tracked-source corroboration. |
| PLN-DIR-002 | Add active-doc implementation alignment validator. | `scripts/validation/check-doc-implementation-alignment.sh` | REQ-AGG-NFR-05 | Validator reports the active Stage docs count and `failures=0`. |
| PLN-DIR-003 | Connect validator to CI and governance. | `.github/workflows/ci-quality.yml`, GitHub governance, QA scope, scripts README | REQ-AGG-MET-02 | Repo contracts accept the new job and docs describe local/remote boundary. |
| PLN-DIR-004 | Update known stale template and operations/current-truth references. | Active Stage docs and docs README | REQ-AGG-NFR-05 | Removed template mentions are `0`; archive direct links are `0`. |
| PLN-DIR-005 | Record disposition evidence and index updates. | Stage 04 plan/task READMEs, progress log | REQ-AGG-MET-01 | Stage 04 indexes and progress log point to this evidence. |
| PLN-DIR-006 | Refresh generated knowledge surfaces and run final validation. | LLM Wiki, Graphify, task evidence | REQ-AGG-MET-02 | Test plan commands pass or advisory status is recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-DIR-001 | Hygiene | Check diff whitespace. | `git diff --check` | Zero exit status. |
| VAL-DIR-002 | Implementation Alignment | Validate active docs against tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS with dynamic `stage_docs_total` and `failures=0`. |
| VAL-DIR-003 | Repository Contracts | Validate full repo docs/runtime/CI contracts. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`. |
| VAL-DIR-004 | Traceability | Validate execution/operations traceability. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-DIR-005 | Provider Sync | Confirm provider surfaces remain synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-DIR-006 | Generated Index | Regenerate and verify LLM Wiki after docs/script changes. | `bash scripts/knowledge/generate-llm-wiki-index.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Regenerated output is fresh. |
| VAL-DIR-007 | Compose | Confirm Compose config remains valid. | `bash scripts/validation/validate-docker-compose.sh` | PASS. |
| VAL-DIR-008 | Hardening | Confirm hardening baseline remains green. | `bash scripts/hardening/check-all-hardening.sh` | PASS. |
| VAL-DIR-009 | Graph | Refresh graph and record advisory health. | `/home/hy/.local/bin/graphify update .`; `bash scripts/knowledge/report-graphify-health.sh` | Graph refreshed; advisory status documented. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical evidence is rewritten beyond current-truth corrections. | Medium | Use narrow `update`; archive only whole-document conflicts. |
| Optional root includes are misclassified as unimplemented. | High | Validator distinguishes tracked implementation from active/optional root include state. |
| New CI job is documented as remotely enforced before remote protection changes. | Medium | Local ruleset proposal records the proposed job separately from current remote state. |
| Generated artifacts become stale after adding docs. | Medium | Regenerate LLM Wiki and Graphify before final validation/commit. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Implementation-alignment validator, repo contracts, traceability, provider sync, Compose validation, hardening, LLM Wiki freshness, Graphify health, diff hygiene.
- **Sandbox / Canary Rollout**: N/A. No runtime service behavior is changed.
- **Human Approval Gate**: User approved modification, deletion, integration, improvement, archive, CI, templates, policy, secrets/remote/model/provider surfaces. Concrete secret values and remote mutation remain target-bound.
- **Rollback Trigger**: Revert validator/CI/governance/docs updates if they misclassify tracked implementations or break repository contracts.
- **Prompt / Model Promotion Criteria**: N/A. No model/provider adapter values are changed.

## Completion Criteria

- [x] Stage 04 plan/task evidence exists.
- [x] Active docs implementation-alignment validator exists and passes.
- [x] Known stale consolidated operations template references are removed.
- [x] Archive direct links in active docs remain absent.
- [x] Stage 05 service docs map to tracked `infra/**` implementations or explicit non-service exceptions.
- [x] CI/governance/scripts indexes are updated.
- [x] Generated knowledge surfaces are refreshed or advisory status is recorded.
- [x] Final validation commands pass or a bounded skip/advisory reason is documented.

## Related Documents

- **Task**: [Docs Implementation Reconciliation Task](../tasks/2026-06-02-docs-implementation-reconciliation.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **QA Scope**: [QA scope](../../00.agent-governance/scopes/qa.md)
- **Docs Index**: [Docs index](../../README.md)
- **Archive Index**: [Archive index](../../98.archive/README.md)
- **Scripts Index**: [Scripts index](../../../scripts/README.md)
