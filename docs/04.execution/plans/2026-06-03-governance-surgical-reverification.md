---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-06-03-governance-surgical-reverification.md -->

# Governance Surgical Re-Verification + Tech-Stack Drift Closure Implementation Plan

## Overview

This document is the implementation plan for surgical re-verification of shared governance (Stage 00), the Claude harness, Model Policy, and Template Contract, plus closure of the single non-governance blocker found during that process: Dependabot-origin tech-stack version drift. This is cross-cutting governance work, so it references governance documents instead of a parent Spec (`documentation-protocol.md` Section 8.5).

## Context

The `/plan` request assumed a new 3-phase build for unified shared governance, but Phase 1 investigation confirmed that governance, the Claude harness, QA/CI, Template Contract, and Model Policy were already mature, aligned, and verified through 2026-06-02 (`memory/progress.md`). With user approval, the scope was limited to "surgical re-verification + gap closure", and model freshness was reverified on the web.

During re-verification, `check-repo-contracts.sh` was the only check to report `failures=1`. The cause was version drift in 9 components: governance-unrelated Dependabot automatic bumps (`71edcd7d`, `5d0ed12b`) raised compose image tags, but the canonical registry `infra/tech-stack.versions.json` did not follow. With user approval, the registry was synchronized to the actual compose declarations with no runtime or compose changes.

## Goals & In-Scope

- **Goals**:
  - Reverify that governance, the Claude harness, Model Policy, and Template Contract remain aligned and passing.
  - Reconfirm model freshness for Claude/Codex/Gemini as of 2026-06-03 and refresh evidence.
  - Close the tech-stack version drift blocking the aggregate gate through registry synchronization.
  - Record Phase 1 through 4 trace evidence in PLAN/TASK/progress.
- **In Scope**:
  - Synchronize 9 entries in `infra/tech-stack.versions.json` as data-registry-only changes.
  - Prevent recurrence with compose-to-registry sync script coverage and a read-only CI drift gate.
  - Record 2026-06-03 re-verification in the Gemini tier review memory note.
  - Write Stage 04 PLAN/TASK and progress log entries.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Rewriting Stage 00 policies/definitions, editing the Model Policy table, or regenerating provider adapters.
  - Bulk-rewriting `docs/01–05`; Template Contract is already enforced and passing.
- **Out of Scope**:
  - Changing compose files, runtime containers, secrets, or remote GitHub state.
  - Changing Gemini tier policy because `gemini-3.5-pro` was unreleased and gate conditions were not met.
  - CI auto-commit; the repository security contract hard-bans workflow `contents: write`, so this was not adopted and was replaced by a read-only gate plus one-command sync.

## Work Breakdown

| Task    | Description                              | Files / Docs Affected                                                                            | Target REQ          | Validation Criteria                                    |
| ------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------- | ------------------------------------------------------ |
| PLN-001 | Rerun governance-scope QA/CI gates | `scripts/validation/*`, `scripts/hardening/*` | N/A (cross-cutting) | All governance gates have `failures=0`/PASS |
| PLN-002 | Web-reverify model freshness and cross-check repository state | `subagent-protocol.md`, `.claude/agents/*.md` | N/A | Claude/Codex current, Gemini `3.5-pro` not GA, stale models 0 |
| PLN-003 | Synchronize tech-stack drift | `infra/tech-stack.versions.json` | N/A | `check-repo-contracts.sh` has `failures=0` |
| PLN-004 | Record Gemini tier memory re-verification | `memory/2026-05-31-gemini-model-tier-review.md` | N/A | 2026-06-03 re-verification section added and `Last Verified` refreshed |
| PLN-005 | Write trace evidence | this PLAN, paired TASK, two READMEs, `progress.md` | N/A | 4 docs written/refreshed and traceability PASS |
| PLN-006 | Add and register compose-to-registry sync script | `scripts/operations/sync-tech-stack-versions.sh`, `check-repo-contracts.sh`, `scripts/README.md` | N/A | Positive test passes and usage contract PASS |
| PLN-007 | Add read-only CI drift gate | `.github/workflows/tech-stack-version-sync.yml` | N/A | Workflow security contract PASS and `contents: read` |

## Verification Plan

| ID          | Level      | Description                                        | Command / How to Run                                            | Pass Criteria                          |
| ----------- | ---------- | -------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------- |
| VAL-PLN-001 | Structural | Repository contract, including Model Policy and Template Contract | `bash scripts/validation/check-repo-contracts.sh` | `failures=0` |
| VAL-PLN-002 | Structural | Document traceability | `bash scripts/validation/check-doc-traceability.sh` | `failures=0`, `catalog_pairs_total=46` |
| VAL-PLN-003 | Structural | Document-implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0` |
| VAL-PLN-004 | Runtime | Compose validation plus hardening | `validate-docker-compose.sh`, `check-all-hardening.sh` | PASS |
| VAL-PLN-005 | Integrity | JSON validity plus diff hygiene | `python3 -m json.tool`, `git diff --check` | OK / no results |

## Risks & Mitigations

| Risk                                        | Impact | Mitigation                                                       |
| ------------------------------------------- | ------ | ---------------------------------------------------------------- |
| Registry synchronization has unintended runtime impact | Low | Leave compose and runtime unchanged; modify only the data registry used by the drift gate |
| Gemini tier changes without evidence | Medium | Confirm `gemini-3.5-pro` is not GA, leave the table unchanged, and keep the memory log |
| Scope expands into non-governance infrastructure | Medium | Close drift only after user approval and limit changes to 9 items |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Governance Hub**: [Stage 00 README](../../00.agent-governance/README.md)
- **Task**: [Governance Surgical Re-Verification task](../tasks/2026-06-03-governance-surgical-reverification.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
