---
status: active
---

<!-- Target: docs/04.execution/plans/2026-07-06-sdlc-document-contract-corpus-normalization.md -->

# SDLC Document Contract Corpus Normalization Implementation Plan

## Overview

This plan executes the approved Stage 03 design for SDLC document contract
corpus normalization.

The work is contract-first and staged. It starts with stale rule text cleanup,
then extends validator coverage, classifies Stage 03/04 lifecycle policy
questions, reviews operations leaf naming candidates, and closes evidence and
generated indexes. Each wave must produce a separate logical commit where
practical.

## Context

The repository already completed the numbered PRD and Spec path migration,
Stage 99 template/support separation, `_workspace` support-surface contract,
and document restructure disposition model. Follow-up discovery found residual
contract drift in guidance and enforcement coverage:

- stale date-based PRD wording in active guidance;
- stale unnumbered Spec examples in issue-template guidance;
- validator coverage that catches Stage 99 drift but not all active guidance
  surfaces;
- undecided Stage 03 sibling README policy;
- historical Stage 04 plan/task naming asymmetry;
- a small set of operations numeric-dot leaf naming candidates.

This plan turns the Stage 03 design into executable waves without changing
runtime infrastructure, secrets, remote GitHub state, or CI hard gates.

## Goals & In-Scope

- **Goals**:
  - Align active PRD/Spec guidance with the numbered path contract.
  - Extend repo-contract validation for active stale PRD/Spec guidance.
  - Classify Stage 03 README and Stage 04 plan/task lifecycle questions before
    hard enforcement.
  - Review and apply approved operations leaf naming polish without merging
    guide, policy, and runbook roles.
  - Keep Stage 90 and progress evidence synchronized.
- **In Scope**:
  - `docs/01.requirements/README.md`
  - `docs/00.agent-governance/scopes/meta.md`
  - `.github/ISSUE_TEMPLATE/bug_report.yml`
  - `scripts/validation/check-repo-contracts.sh`
  - Stage 03/04/05 README indexes when directly affected
  - exact approved operations leaf naming candidates
  - generated LLM Wiki index/coverage
  - progress memory and task evidence

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite the full Markdown corpus for style.
  - Do not make Stage 03 sibling README files mandatory without a recorded
    policy decision and validator exception plan.
  - Do not hard-enforce Stage 04 plan/task exact-stem pairing until historical
    exceptions are classified.
  - Do not archive or delete active documents without exact disposition,
    replacement, link synchronization, and rollback evidence.
- **Out of Scope**:
  - Docker Compose runtime, service images, deployment state, remote GitHub
    settings, branch protection, CI workflow mutation, provider runtime
    mutation, model policy, secrets, credentials, tokens, private keys, raw
    logs, shell history, and `.env` values.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-SDCN-001 | Clean stale numbered PRD/Spec contract guidance. | `docs/01.requirements/README.md`, `docs/00.agent-governance/scopes/meta.md` | `SDCN-GAP-001`, `SDCN-GAP-002` | Targeted stale-guidance scan and repo contracts pass. |
| PLN-SDCN-002 | Extend validator coverage for active stale guidance. | `scripts/validation/check-repo-contracts.sh`, `.github/ISSUE_TEMPLATE/bug_report.yml` | `SDCN-GAP-003`, `SDCN-GAP-004` | Validator catches representative stale guidance and full repo contracts pass. |
| PLN-SDCN-003 | Classify Stage 03 sibling README and Stage 04 plan/task lifecycle policy. | Stage 90 audit/reference or task evidence, Stage 03/04 indexes if needed | `SDCN-GAP-005`, `SDCN-GAP-006` | Classification table exists; no hard gate added without exception set. |
| PLN-SDCN-004 | Review and apply approved operations leaf naming polish. | Exact `docs/05.operations/**` candidates and parent README links | `SDCN-GAP-007` | Role separation is preserved; traceability and implementation alignment pass. |
| PLN-SDCN-005 | Close evidence and generated indexes. | task evidence, progress memory, generated LLM Wiki index/coverage | `SDCN-GAP-008`, closure criteria | Final checks pass; residual gaps are recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-SDCN-001 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-SDCN-002 | Generated Docs | Verify LLM Wiki generated surfaces. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check`; `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | Both pass. |
| VAL-PLN-SDCN-003 | Traceability | Verify document traceability. | `bash scripts/validation/check-doc-traceability.sh` | `failures=0`. |
| VAL-PLN-SDCN-004 | Implementation Alignment | Verify active docs still match tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0`. |
| VAL-PLN-SDCN-005 | Syntax | Check repo-contract script syntax after validator edits. | `bash -n scripts/validation/check-repo-contracts.sh` | Zero exit status. |
| VAL-PLN-SDCN-006 | Repo Contracts | Run the full repository contract gate. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |
| VAL-PLN-SDCN-007 | Targeted Stale Guidance | Verify obsolete active PRD/Spec examples are gone outside approved historical contexts. | Targeted `rg` commands recorded in task evidence | No unapproved active stale guidance remains. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Validator change flags historical evidence. | High | Keep migration-table and completed-evidence exceptions explicit; fall back to advisory evidence if exception set is not stable. |
| Plan/task naming cleanup rewrites history. | High | Classify first; preserve historical task evidence unless active-consumption conflict is proven. |
| Operations rename breaks links. | Medium | Use `git mv`, update parent README and related links in the same wave, and run traceability/implementation alignment checks. |
| README files become policy owners. | Medium | Move durable rules to Stage 00 or Stage 99 support; README updates remain routing/index text. |
| External sources override local policy. | Medium | Use external sources only as rationale; keep Stage 00 and Stage 99 as policy owners. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Run the verification plan for each wave.
- **Sandbox / Canary Rollout**: N/A for documentation-only waves; validator
  changes must run narrow syntax and targeted stale-guidance checks before full
  repo contracts.
- **Human Approval Gate**: Required before destructive document move/delete,
  CI workflow mutation, remote GitHub mutation, provider runtime mutation,
  runtime infra change, or secret-adjacent work.
- **Rollback Trigger**: Revert the wave commit if repo contracts fail because
  of that wave or an active link target is lost.
- **Prompt / Model Promotion Criteria**: N/A. Agent-facing policy text remains
  routed through Stage 00 and Stage 99 contracts.

## Completion Criteria

- [ ] Wave 1 stale guidance cleanup is complete and verified.
- [ ] Wave 2 validator coverage is complete and verified.
- [ ] Wave 3 lifecycle classification is complete without premature hard gates.
- [ ] Wave 4 operations naming polish is complete for exact approved
      candidates or recorded as residual evidence.
- [ ] Wave 5 closure evidence, LLM Wiki, progress memory, and residual gaps are
      synchronized.
- [ ] Final verification plan passes or any residual failure is recorded with
      owner, scope, and follow-up.

## Related Documents

- **Spec**: [../../03.specs/119-sdlc-document-contract-corpus-normalization/spec.md](../../03.specs/119-sdlc-document-contract-corpus-normalization/spec.md)
- **Task**: [../tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md](../tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md)
- **Numbered path migration spec**: [../../03.specs/099-template-system-numbered-sdlc-paths/spec.md](../../03.specs/099-template-system-numbered-sdlc-paths/spec.md)
- **Document restructure disposition spec**: [../../03.specs/103-document-restructure-audit-contract-archive/spec.md](../../03.specs/103-document-restructure-audit-contract-archive/spec.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
