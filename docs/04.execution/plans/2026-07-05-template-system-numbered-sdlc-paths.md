---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-template-system-numbered-sdlc-paths.md -->

# Template System Numbered SDLC Paths Implementation Plan

## Overview

This document is the implementation plan for
`docs/03.specs/099-template-system-numbered-sdlc-paths/spec.md`. It sequences
the full migration from date-prefixed PRDs and unnumbered Spec folders to
deterministic three-digit numbered PRD and Spec paths.

The work also updates Stage 99 templates/support contracts, Stage 00 governance
references, repository validators, README indexes, generated reference indexes,
and cross-links that depend on the old path rules.

## Context

The user approved a full corpus migration on 2026-07-05: all
`docs/01.requirements/` PRD files and all `docs/03.specs/` Spec folders must be
renamed to numbered paths, and templates, support contracts, governance, and
validators must publish and enforce the new rules.

The parent Spec defines the migration maps and path ranges. This plan turns
that design into ordered implementation batches that keep path moves, contract
edits, validator edits, and generated-index fallout reviewable.

## Goals & In-Scope

- **Goals**:
  - Move every PRD file to `NNN-slug.md` form.
  - Move every Spec folder to `NNN-slug/` form.
  - Preserve historical content while removing legacy active path rules.
  - Update all repository-local links and README indexes affected by the moves.
  - Update Stage 99 templates and support contracts to use numbered PRD and
    Spec target guidance.
  - Update Stage 00 governance and repository validators to enforce the new
    path contract.
  - Commit by logical unit.
- **In Scope**:
  - `docs/01.requirements/**`
  - `docs/03.specs/**`
  - `docs/04.execution/plans/**`
  - `docs/04.execution/tasks/**`
  - `docs/99.templates/**`
  - Directly affected `docs/00.agent-governance/**`
  - `scripts/validation/check-repo-contracts.sh`
  - README indexes, progress memory, and generated LLM Wiki index

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - No runtime Docker Compose, service, network, secret, or deployment change.
  - No remote GitHub settings or workflow behavior change beyond validator
    references if needed.
  - No broad body rewrite of historical PRDs or Specs for style-only template
    compliance.
  - No duplicate redirect documents at legacy paths.
- **Out of Scope**:
  - Renaming Stage 04 Plan or Task filenames away from their date-prefixed
    execution-evidence rule.
  - Changing architecture requirement or decision numbering contracts.
  - Reading or recording secret values, credentials, tokens, private keys,
    shell history, raw logs, or `.env` values.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-NSP-001 | Create execution scaffold and capture approval boundary | this plan, task evidence, Stage 04 indexes, progress memory | `VAL-NSP-006` | Plan/task are active, indexed, and pass changed-document contract checks. |
| PLN-NSP-002 | Move all PRD files to three-digit numbered filenames | `docs/01.requirements/*.md`, PRD README, cross-links | `VAL-NSP-001`, path contract | Every PRD except `README.md` matches three-digit filename rule and old PRD filenames have no active links. |
| PLN-NSP-003 | Move all Spec folders to three-digit numbered folders | `docs/03.specs/*/`, Spec README, cross-links | `VAL-NSP-002`, path contract | Every Spec folder matches three-digit folder rule and old Spec folder links are rewritten. |
| PLN-NSP-004 | Update Stage 99 template and support path contracts | `docs/99.templates/templates/**`, `docs/99.templates/support/**` | `VAL-NSP-003`, `VAL-NSP-004` | PRD and Spec templates/support mappings publish only numbered target guidance. |
| PLN-NSP-005 | Update governance and validators | `docs/00.agent-governance/**`, `scripts/validation/check-repo-contracts.sh` | `VAL-NSP-004`, `VAL-NSP-006` | Governance references match new paths and repo contracts enforce PRD/Spec numbering. |
| PLN-NSP-006 | Final link rewrite, generated index, and closure validation | README indexes, LLM Wiki index, progress memory, task evidence | `VAL-NSP-005`, `VAL-NSP-006` | Full validation bundle passes or unrelated failures are recorded with evidence. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Check whitespace and conflict markers | `git diff --check` | No output. |
| VAL-PLN-002 | Path contract | Check PRD filenames after migration | `find docs/01.requirements -maxdepth 1 -type f -name '*.md' -printf '%f\n'` plus focused regex review | Only `README.md` or three-digit PRD filenames remain. |
| VAL-PLN-003 | Path contract | Check Spec folders after migration | `find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n'` plus focused regex review | Every Spec folder starts with a three-digit prefix. |
| VAL-PLN-004 | Legacy cleanup | Check stale old path references after link rewrite | `rg -n` focused scans over old PRD filenames and old Spec folder names | No active stale references remain outside explicit historical migration tables. |
| VAL-PLN-005 | Reference index | Check LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Generated index is fresh. |
| VAL-PLN-006 | Provider surface | Confirm provider mirrors remain unchanged | `bash scripts/operations/sync-provider-surfaces.sh --check` | No provider surface drift. |
| VAL-PLN-007 | Traceability | Check execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | `failures=0`. |
| VAL-PLN-008 | Implementation alignment | Check documentation/implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0`. |
| VAL-PLN-009 | Repo contract | Check repository contracts and new path enforcement | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Large path move breaks many relative links | High | Use migration maps from the parent Spec, run focused stale-reference scans, and run repository link/alignment validators after each batch. |
| Validator rejects transitional state during moves | Medium | Commit path moves and validator updates in separate logical batches, but keep task evidence updated so temporary failures are not hidden. |
| Historical evidence loses date provenance | Medium | Preserve dates in document bodies when already present; add a short history note only when the old filename was the only provenance. |
| Duplicate old and new paths coexist | High | Use `git mv`; do not create alias files or redirect docs. |
| Stage 99 templates conflict with support contracts | High | Update support contracts before final validation and ensure template target comments match `template-selection.md`. |
| Subagent review is unavailable | Low | Continue controller-led validation and record the subagent thread-limit deviation in task evidence. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: N/A; this is documentation-system and validator work.
- **Sandbox / Canary Rollout**: N/A; no runtime behavior changes are made.
- **Human Approval Gate**: User approved full corpus migration and
  template/support/governance/validator rule updates on 2026-07-05.
- **Rollback Trigger**: Revert the relevant logical commit if a path batch
  causes unresolved link, validator, or contract drift that cannot be fixed in
  the same phase.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Stage 04 plan and task evidence exist and are indexed.
- [x] All PRD files use numbered filenames.
- [x] All Spec folders use numbered folder names.
- [x] Stage 99 templates/support publish the numbered PRD and Spec contract.
- [x] Stage 00 governance and validators enforce the numbered contract.
- [x] Cross-links, README indexes, generated indexes, and progress memory are
      updated.
- [x] Final validation bundle passes.

## Related Documents

- **Spec**: [Template System Numbered SDLC Paths Spec](../../03.specs/099-template-system-numbered-sdlc-paths/spec.md)
- **Task**: [Template System Numbered SDLC Paths Task](../tasks/2026-07-05-template-system-numbered-sdlc-paths.md)
- **PRD Index**: [Requirements index](../../01.requirements/README.md)
- **Spec Index**: [Spec index](../../03.specs/README.md)
- **Template selection**: [Template selection](../../99.templates/support/template-selection.md)
- **Repository validator**: [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
