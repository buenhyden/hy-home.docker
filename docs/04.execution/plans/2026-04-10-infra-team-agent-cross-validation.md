---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md -->

# Infra Team Agent Cross-Validation Plan

## Overview

This document is the implementation plan for settling the team-agent cross-validation design that runs immediately after infra changes into canonical stage paths. It migrates the existing `docs/superpowers` content into `docs/03.specs/07-workflow/agent-design.md` and this plan document, while also tightening local governance rules to prevent nonstandard path recurrence.

## Context

Existing cross-validation documents were located under `docs/superpowers/specs` and `docs/superpowers/plans`, bypassing the stage taxonomy and template contract. This state disperses spec/plan search paths and can repeat the problem of future skills creating active documents in nonstandard locations.

## Goals & In-Scope

- **Goals**:
- `DOC-AGT-001`: Keep the active agent design document only at `docs/03.specs/07-workflow/agent-design.md`.
  - `DOC-AGT-002`: Keep the active implementation plan document at `docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md`.
  - `DOC-AGT-003`: Make repo-local governance forbid active spec/plan creation under nonstandard `docs/*` paths.
  - `DOC-AGT-004`: Align README and traceability against the new canonical paths.
- **In Scope**:
  - Write canonical `agent-design.md`
  - Write canonical `plan.md`
  - governance rule hardening
  - README sync
  - Remove `docs/superpowers`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Creating new PRD/ARD/ADR documents dedicated to infra-team-agent
  - Modifying the global skills repository
  - Changing runtime behavior in `.claude/agents/` or `.claude/skills/`
- **Out of Scope**:
  - Restructuring other workflow tier specs/plans
  - Large-scale rewrites of provider overlays (`CLAUDE.md`, `GEMINI.md`)

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Rewrite `docs/superpowers` spec content into a template-based canonical agent design | `docs/03.specs/07-workflow/agent-design.md`, `docs/03.specs/07-workflow/spec.md` | `DOC-AGT-001` | New agent design includes required sections and `## Related Documents`. |
| PLN-002 | Normalize `docs/superpowers` plan content into the canonical plan document | `docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md` | `DOC-AGT-002` | New plan includes Work Breakdown, Verification Plan, and Risks sections. |
| PLN-003 | Add non-stage active path prohibition rules to local governance | `AGENTS.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/00.agent-governance/scopes/docs.md` | `DOC-AGT-003` | Rule documents specify canonical paths and forbidden paths. |
| PLN-004 | Sync stage READMEs against the actual structure | `docs/README.md`, `docs/03.specs/README.md`, `docs/04.execution/plans/README.md` | `DOC-AGT-004` | README structure descriptions match the actual file state. |
| PLN-005 | Remove legacy `docs/superpowers` documents and directories and clean up residual references | `docs/superpowers/**` | `DOC-AGT-001`, `DOC-AGT-002` | No active `docs/superpowers` references remain in the repository. |
| PLN-006 | Verify document traceability and path consistency | changed docs set, validation scripts | `DOC-AGT-001`, `DOC-AGT-002`, `DOC-AGT-003`, `DOC-AGT-004` | `check-doc-traceability.sh` passes and `docs/superpowers` path removal is confirmed |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | canonical agent design exists in the stage path | `test -f docs/03.specs/07-workflow/agent-design.md` | exit code 0 |
| VAL-PLN-002 | Structural | canonical plan exists in the stage path | `test -f docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md` | exit code 0 |
| VAL-PLN-003 | Content | changed docs include required related-doc sections | `rg -n "^## Related Documents" AGENTS.md docs/00.agent-governance/scopes/docs.md docs/00.agent-governance/rules/documentation-protocol.md docs/03.specs/07-workflow/agent-design.md docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md` | every changed doc matched |
| VAL-PLN-004 | Hygiene | no active `docs/superpowers` references remain | `rg -n "docs/superpowers" docs AGENTS.md CLAUDE.md .claude \|\| true` plus manual review | matches are limited to completed migration evidence; no `docs/superpowers` directory exists |
| VAL-PLN-005 | Traceability | repository doc traceability check passes | `bash scripts/validation/check-doc-traceability.sh` | script exits successfully |
| VAL-PLN-006 | Filesystem | legacy directory removed | `test ! -d docs/superpowers` | exit code 0 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Legacy references survive in README or plan text | Medium | Use repo-wide `rg` against `docs/superpowers` before completion |
| Canonical doc is too governance-heavy for `07-workflow` | Medium | Keep runtime behavior in `.claude/` and keep the new agent design focused on orchestration contract only |
| README structure drifts from actual files again | Medium | Update folder structure blocks in the same change set and verify with `find` output |
| Missing upstream PRD/ARD/ADR causes ambiguity | Low | Explicitly document that no dedicated upstream stage docs are created for this capability |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: canonical `agent-design.md` must define deterministic `PASS|WARN|BLOCK` terminal states
- **Sandbox / Canary Rollout**: not applicable for docs-only migration
- **Human Approval Gate**: user-approved removal of `docs/superpowers`
- **Rollback Trigger**: any traceability script failure or unresolved legacy reference
- **Prompt / Model Promotion Criteria**: not applicable

## Completion Criteria

- [x] Canonical `agent-design.md` created under `docs/03.specs/07-workflow/`
- [x] Canonical plan created under `docs/04.execution/plans/`
- [x] Governance rules updated to forbid non-stage active docs
- [x] README files synced to actual structure
- [x] `docs/superpowers` removed
- [x] Verification passed

## Related Documents

- **Spec**: [../03.specs/07-workflow/agent-design.md](../../03.specs/07-workflow/agent-design.md)
- **Task**: [Infra team agent cross-validation task](../tasks/2026-04-10-infra-team-agent-cross-validation.md)
- **Workflow Parent Spec**: [../03.specs/07-workflow/spec.md](../../03.specs/07-workflow/spec.md)
- **PRD Context**: [../01.requirements/2026-03-28-07-workflow-optimization-hardening.md](../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD Context**: [../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md)
- **Documentation Protocol**: [../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
