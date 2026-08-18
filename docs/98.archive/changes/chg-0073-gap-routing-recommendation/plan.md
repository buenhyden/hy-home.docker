---
status: archived
artifact_id: plan-0073
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/plans/2026-07-05-gap-routing-recommendation.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0073-gap-routing-recommendation/plan.md; migrate 6 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 0a6df4395d05e15f42f1ba8e815632dbab92fba9
preservation_class: git-history
---
<!-- Target: docs/04.execution/plans/2026-07-05-gap-routing-recommendation.md -->

# Gap Routing Recommendation Implementation Plan

## Overview

This plan implements a local advisory gap-to-stage routing recommender and
reference data. It closes `AEA-AUTO-004` by making the Stage 00 manual routing
contract easier to apply before edits.

## Context

The repository already has a manual gap-to-stage routing table in Stage 00.
Audit and review work still requires humans or agents to read the table and
choose the canonical owner. A non-mutating recommender reduces repeated lookup
work while preserving human confirmation.

## Goals & In-Scope

- **Goals**:
  - Add an advisory CLI for text and path based gap routing suggestions.
  - Add Stage 90 governance data reference for the routing contract.
  - Register the script in inventory and repo-contract checks.
  - Update automation candidate status, progress, and generated indexes.
- **In Scope**:
  - `scripts/validation/recommend-gap-routing.sh`
  - `docs/90.references/data/governance/**`
  - Stage 03/04 evidence, Stage 90 indexes, scripts README, repo contracts, and
    progress memory.

## Non-Goals & Out-of-Scope

- No automatic document creation or edits.
- No protected runtime, remote, CI workflow, provider runtime, secret,
  credential, token, or deployment changes.
- No replacement of human review for ambiguous findings.

## Work Breakdown

| Task        | Description                                           | Files / Docs Affected                                                                  | Target REQ                            | Validation Criteria                                     |
| ----------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------- |
| PLN-GRR-001 | Add Stage 03/04 evidence for the recommender.         | `docs/03.specs/109-gap-routing-recommendation/**`, this plan, task evidence, indexes   | VAL-GRR-001                           | Spec, plan, and task are linked and indexed.            |
| PLN-GRR-002 | Add advisory recommender and Stage 90 data reference. | `scripts/validation/recommend-gap-routing.sh`, `docs/90.references/data/governance/**` | VAL-GRR-001, VAL-GRR-002, VAL-GRR-003 | Representative CLI inputs route as expected.            |
| PLN-GRR-003 | Wire inventory and repo-contract checks.              | `scripts/README.md`, `scripts/validation/check-repo-contracts.sh`                      | VAL-GRR-004                           | Repo contracts pass and verify representative behavior. |
| PLN-GRR-004 | Update audit/progress/index evidence and close.       | Stage 90 audit candidate, progress memory, LLM Wiki, Graphify                          | VAL-GRR-004                           | Final validation summary is recorded.                   |

## Verification Plan

| ID          | Level     | Description                       | Command / How to Run                                                                                                                                                              | Pass Criteria                          |
| ----------- | --------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| VAL-PLN-001 | Syntax    | Check script syntax.              | `bash -n scripts/validation/recommend-gap-routing.sh scripts/validation/check-repo-contracts.sh`                                                                                  | No syntax errors.                      |
| VAL-PLN-002 | CLI       | Check operations text routing.    | `bash scripts/validation/recommend-gap-routing.sh --text "runbook recovery procedure is missing rollback evidence"`                                                               | Output suggests `docs/05.operations/`. |
| VAL-PLN-003 | CLI       | Check spec path routing.          | `bash scripts/validation/recommend-gap-routing.sh --files docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md`                                                    | Output suggests `docs/03.specs/`.      |
| VAL-PLN-004 | Contracts | Check full repo contracts.        | `bash scripts/validation/check-repo-contracts.sh`                                                                                                                                 | `failures=0`.                          |
| VAL-PLN-005 | Docs      | Check docs and generated indexes. | `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | All pass.                              |

## Risks & Mitigations

| Risk                                               | Impact | Mitigation                                                                             |
| -------------------------------------------------- | ------ | -------------------------------------------------------------------------------------- |
| Advisory output is mistaken for automatic approval | Medium | Script and reference state that recommendations are advisory only.                     |
| Keyword routing chooses a weak owner               | Medium | Include confidence and reason; ambiguous cases route to Stage 04 task/audit gap first. |
| Sensitive input is echoed                          | Medium | Redact assignment-like token, secret, credential, and private-key patterns.            |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Representative CLI inputs are checked locally and by
  repo contracts.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: User continued the broader audit automation cleanup
  on 2026-07-05.
- **Rollback Trigger**: Revert the logical commit if routing checks cause false
  positives.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Stage 03/04 evidence exists and is indexed.
- [x] Gap routing recommender exists under `scripts/validation/`.
- [x] Stage 90 governance data reference exists.
- [x] Repo contracts verify representative recommender behavior.
- [x] Audit/progress evidence and generated indexes are updated.
- [x] Final validation passes.

## Related Documents

- **Spec**: [../../98.archive/03.specs/109-gap-routing-recommendation/spec.md](../../tombstones/03.specs/spec-0109-gap-routing-recommendation.md)
- **Task**: [../tasks/2026-07-05-gap-routing-recommendation.md](task.md)
- **Gap routing reference**: [../../90.references/data/governance/gap-to-stage-routing.md](../../../90.references/data/governance/ref-0070-gap-to-stage-routing.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
