---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-05-template-system-numbered-sdlc-paths.md -->

# Template System Numbered SDLC Paths Task

## Overview

This document tracks implementation and verification work for the numbered PRD
and Spec path migration. It records path moves, template/support contract
updates, governance and validator updates, cross-link cleanup, and validation
evidence derived from the parent Spec and Plan.

## Inputs

- **Parent Spec**: [Template System Numbered SDLC Paths Spec](../../03.specs/099-template-system-numbered-sdlc-paths/spec.md)
- **Parent Plan**: [Template System Numbered SDLC Paths Plan](../plans/2026-07-05-template-system-numbered-sdlc-paths.md)
- **Template selection**: [Template selection](../../99.templates/support/template-selection.md)

## Working Rules

- Use `git mv` for every PRD and Spec path move.
- Do not create alias files at legacy paths.
- Preserve historical content unless a small body note is required to retain
  provenance after filename removal.
- Keep runtime, secrets, remote GitHub, deployment behavior, and Compose
  behavior out of scope.
- Do not read or record secret values, credentials, tokens, private keys, raw
  logs, shell history, or `.env` values.
- Commit by logical unit.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 01 PRD corpus | User approved full corpus migration on 2026-07-05 | `docs/01.requirements/*.md` | Date-prefixed PRD filenames exist | PRDs use three-digit numbered filenames | Revert PRD move commit | No secrets, raw logs, or `.env` values |
| Stage 03 Spec corpus | User approved full corpus migration on 2026-07-05 | `docs/03.specs/*/` | Two-digit and unnumbered Spec folders exist | Spec folders use three-digit numbered names | Revert Spec move commit | No secrets, raw logs, or `.env` values |
| Stage 99 templates/support | User approved template/support new rule application on 2026-07-05 | `docs/99.templates/**` | PRD and Spec template/support rules include legacy target patterns | Templates/support publish numbered PRD and Spec targets | Revert Stage 99 contract commit | No secrets or runtime config |
| Stage 00 governance | User approved governance new rule application on 2026-07-05 | `docs/00.agent-governance/**` | Some governance examples may reference old Spec or PRD paths | Governance references numbered paths | Revert governance fallout commit | Governance text only |
| Repository validator | User approved validator new rule application on 2026-07-05 | `scripts/validation/check-repo-contracts.sh` | Validator does not enforce numbered PRD/Spec paths | Validator enforces numbered PRD and Spec path contract | Revert validator commit | No credentials or remote settings |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-NSP-001 | Create Stage 04 execution scaffold | doc | `Implementation Handoff` | `PLN-NSP-001` | This plan/task, Stage 04 indexes, progress memory, validation bundle | Documentation Specialist | Done |
| T-NSP-002 | Move PRD corpus to numbered filenames | doc | `PRD Migration Map` | `PLN-NSP-002` | `git mv` path evidence; focused PRD path scan; link rewrite evidence | Documentation Specialist | Done |
| T-NSP-003 | Move Spec corpus to numbered folders | doc | `Spec Migration Map` | `PLN-NSP-003` | `git mv` path evidence; focused Spec folder scan; link rewrite evidence | Documentation Specialist | Todo |
| T-NSP-004 | Update Stage 99 templates and support contracts | doc | `Contract Fallout Surfaces` | `PLN-NSP-004` | Template/support diff; stale target-pattern scan; repo contracts | Documentation Specialist | Todo |
| T-NSP-005 | Update Stage 00 governance and repository validator | doc | `Validator Interfaces` | `PLN-NSP-005` | Validator diff; governance stale-pattern scan; repo contracts | Documentation Specialist | Todo |
| T-NSP-006 | Rewrite remaining links, regenerate index, and close validation | doc | `Verification` | `PLN-NSP-006` | LLM Wiki freshness; provider sync; traceability; alignment; repo contracts | Documentation Specialist | Todo |

## Phase View

### Phase 1: Execution Scaffold

- [x] T-NSP-001 Create Stage 04 execution scaffold.

### Phase 2: Corpus Moves

- [x] T-NSP-002 Move PRD corpus to numbered filenames.
- [ ] T-NSP-003 Move Spec corpus to numbered folders.

### Phase 3: Contract and Validator Updates

- [ ] T-NSP-004 Update Stage 99 templates and support contracts.
- [ ] T-NSP-005 Update Stage 00 governance and repository validator.

### Phase 4: Closure

- [ ] T-NSP-006 Rewrite remaining links, regenerate index, and close
  validation.

## Deviation Log

| Deviation | Reason | Resolution |
| --- | --- | --- |
| Read-only sidecar subagent review could not be spawned. | `multi_agent_v1.spawn_agent` reported `agent thread limit reached`. | Continue controller-led implementation and validation; do not expand write scope. |

## Verification Summary

Validation evidence is updated after each logical implementation batch.

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` after execution scaffold | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` after execution scaffold | PASS | Generated LLM Wiki index is fresh with 1156 paths. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` after execution scaffold | PASS | `sync-provider-surfaces: no drift`. |
| `bash scripts/validation/check-doc-traceability.sh` after execution scaffold | PASS | `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` after execution scaffold | PASS | `failures=0`. |
| `bash scripts/validation/check-repo-contracts.sh` after execution scaffold | PASS | `failures=0`; changed target-stage documents normalized. |
| `git diff --check` after PRD migration | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` after PRD migration | PASS | Generated LLM Wiki index is fresh with 1158 paths. |
| Focused PRD filename regex scan after PRD migration | PASS | `bad_prd_filenames=0`; every PRD except `README.md` uses three-digit filename form. |
| Focused stale PRD path scan after PRD migration | PASS | No active `docs/01.requirements/2026-...` PRD links or PRD target comments remain outside the parent migration table. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` after PRD migration | PASS | `sync-provider-surfaces: no drift`. |
| `bash scripts/validation/check-doc-traceability.sh` after PRD migration | PASS | `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` after PRD migration | PASS | `failures=0`. |
| `bash scripts/validation/check-repo-contracts.sh` after PRD migration | PASS | `failures=0`; 135 changed target-stage documents normalized. |

## Related Documents

- **Parent Spec**: [Template System Numbered SDLC Paths Spec](../../03.specs/099-template-system-numbered-sdlc-paths/spec.md)
- **Parent Plan**: [Template System Numbered SDLC Paths Plan](../plans/2026-07-05-template-system-numbered-sdlc-paths.md)
- **PRD Index**: [Requirements index](../../01.requirements/README.md)
- **Spec Index**: [Spec index](../../03.specs/README.md)
- **Template selection**: [Template selection](../../99.templates/support/template-selection.md)
- **Repository validator**: [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
