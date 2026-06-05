---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md -->

# Scripts Lifecycle Contract Cleanup Plan

## Overview

This document is the implementation plan for clarifying script lifecycle, README template alignment, and repository contract wording based on the live audit results for the `scripts/` directory. Because current evidence does not justify deleting any scripts, this work is not deletion; it is cleanup that clarifies the meaning of documentation and validation contracts.

## Context

The user request explicitly granted permission to write under `docs/04.execution/plans`. At the live audit baseline, `scripts/` contained 22 root shell scripts and one `scripts/lib/hardening-lib.sh`; each root script needed to be explained by inventory, lifecycle category, repository reference, or explicit standalone exemption.

Graphify output is advisory for this task. `graphify-out/GRAPH_REPORT.md` includes generated-volume contamination and meaningless god nodes, so conclusions must be corroborated against tracked source files, `scripts/README.md`, `scripts/validation/check-repo-contracts.sh`, and repository validators.

## Current Disposition (2026-05-26)

This plan records the 2026-05-09 cleanup context. It is superseded by the
current purpose-folder script contract:

- Root-level `scripts/*.sh` duplicate wrappers are no longer part of the active
  script surface; current tracked source has zero root shell scripts.
- Canonical script entrypoints live under `scripts/validation/`,
  `scripts/hardening/`, `scripts/hooks/`, `scripts/knowledge/`,
  `scripts/operations/`, and `scripts/lib/`.
- `scripts/README.md`, the retrospective sibling task, and
  `scripts/validation/check-repo-contracts.sh` are the current authority for
  script ownership and duplicate-wrapper rejection.
- Current Graphify health is advisory because of cross-root inferred edges, not
  generated-volume contamination or meaningless god nodes.

## Goals & In-Scope

- **Goals**:
  - Align `scripts/README.md` with the base structure in `docs/99.templates/readme.template.md`.
  - Preserve the script lifecycle table and usage examples.
  - Clarify the meaning of external-reference exemptions in `scripts/validation/check-repo-contracts.sh`.
  - Maintain traceability between the new plan and the parent README.
- **In Scope**:
  - `scripts/README.md`
  - `scripts/validation/check-repo-contracts.sh`
  - `docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md`
  - `docs/04.execution/plans/README.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Root script deletion, rename, or CLI interface changes
  - CI, hook, pre-commit, or Docker Compose execution contract changes
  - `check-repo-contracts.sh` failure condition changes
- **Out of Scope**:
  - Modifying `docs/00.agent-governance/memory/*`
  - Reading or documenting secret values, tokens, private keys, or generated certificate content
  - `graphify-out` generated artifact hand edit
  - Creating new PRD, ARD, ADR, Spec, Task, Operation, or Runbook documents

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add README base sections | `scripts/README.md` | REQ-SCRIPT-001 | `Audience`, `Scope`, `Structure`, `How to Work in This Area` exist |
| PLN-002 | Clarify script lifecycle contract wording | `scripts/README.md` | REQ-SCRIPT-002 | Manual operation and standalone exemption meanings are separated |
| PLN-003 | Clarify external-reference exemption naming | `scripts/validation/check-repo-contracts.sh` | REQ-SCRIPT-003 | `manual_root_scripts` naming is removed and behavior is unchanged |
| PLN-004 | Add plan artifact | `docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md` | REQ-DOC-001 | Plan template required sections and real related links are included |
| PLN-005 | Sync parent README | `docs/04.execution/plans/README.md` | REQ-DOC-002 | New plan is connected to structure and related documents |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Verify repository contract | `bash scripts/validation/check-repo-contracts.sh` | failures=0 |
| VAL-PLN-002 | Structural | Verify docs traceability | `bash scripts/validation/check-doc-traceability.sh` | failures=0 |
| VAL-PLN-003 | Syntax | Verify Bash syntax | `bash -n scripts/*.sh scripts/lib/*.sh .claude/hooks/*.sh` | no syntax errors |
| VAL-PLN-004 | Advisory | Check Graphify corpus health | `bash scripts/knowledge/report-graphify-health.sh` | exits 0; advisory status is not treated as architecture authority |
| VAL-PLN-005 | Optional | Graphify refresh | `graphify update .` | run only if CLI is available after script code changes; otherwise report skipped |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| README normalization removes useful inventory detail | Medium | Preserve the existing inventory, lifecycle table, usage examples, and references. |
| Manual operations are mistaken for reference exemptions | Medium | Use external-reference exemption wording and keep the exemption set explicit. |
| Contract checker behavior changes accidentally | High | Rename variables/messages only and verify with `check-repo-contracts.sh`. |
| Secret examples expose sensitive material | High | Keep examples procedural and avoid generated values, tokens, keys, or certificate bodies. |
| Graphify output is over-trusted | Medium | Treat Graphify as advisory and rely on tracked source plus validators. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository contract, docs traceability, and Bash syntax checks pass.
- **Sandbox / Canary Rollout**: Not applicable; there are no runtime behavior changes.
- **Human Approval Gate**: script deletion, CLI rename, generated secret inspection, or memory maintenance requires a separate explicit request.
- **Rollback Trigger**: validator failure or behavior-changing diff in `check-repo-contracts.sh`.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] `scripts/README.md` includes the required README base sections.
- [x] `scripts/validation/check-repo-contracts.sh` uses clear external-reference exemption wording without behavior changes.
- [x] The new plan is linked from `docs/04.execution/plans/README.md`.
- [x] Required verification commands pass or are explicitly reported as skipped with reason.

## Related Documents

- [scripts README](../../../scripts/README.md)
- [Repository contract checker](../../../scripts/validation/check-repo-contracts.sh)
- [Plan template](../../99.templates/plan.template.md)
- [README template](../../99.templates/readme.template.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Graphify report](../../../graphify-out/GRAPH_REPORT.md)
