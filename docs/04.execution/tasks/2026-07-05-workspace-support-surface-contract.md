---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-05-workspace-support-surface-contract.md -->

# Task: Workspace Support Surface Contract

## Overview

This document records execution evidence for implementing the `_workspace`
repo-support and protected-surface contract.

## Inputs

- **Parent Spec**: [Workspace Support Surface Contract Spec](../../03.specs/106-workspace-support-surface-contract/spec.md)
- **Parent Plan**: [Workspace Support Surface Contract Plan](../plans/2026-07-05-workspace-support-surface-contract.md)
- **User Approval**: 2026-07-05 approval for Approach A, `_workspace` contract
  first.

## Working Rules

- Keep `_workspace` as ignored repo-support staging, not an active documentation
  stage.
- Do not read, print, summarize, move, or commit secret values.
- Do not store raw logs, shell history, local diagnostics, auth files, tokens,
  credentials, private keys, or secret values under `_workspace`.
- Commit by logical unit.
- Record broader repo-wide template/frontmatter cleanup as follow-up rather
  than expanding this task.

## Approved Surface Evidence

The user approved protected documentation, governance, template-support,
`.gitignore`, and validator changes for this bounded `_workspace` contract.
Runtime, secrets, provider adapter, model policy, CI workflow behavior, remote
GitHub, and Docker Compose mutation remain out of scope.

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 03/04 execution | User approved Approach A on 2026-07-05 | `docs/03.specs/106-workspace-support-surface-contract/`, this plan/task pair | No dedicated `_workspace` contract spec existed | Spec/plan/task created | Revert planning commit | No secret values, raw logs, or shell history |
| `_workspace` contract | User approved `_workspace` role/purpose cleanup | `_workspace/README.md`, `_workspace/repo-support/README.md`, `.gitignore` | `_workspace` directory absent; `.gitignore` had no `_workspace` rule | Tracked contract README files and default-ignore rules added | Revert contract commit | No runtime artifacts or secrets |
| Governance/support contract | User approved contract/governance edits | Stage 00 and Stage 99 direct fallout | Stage 00 used generic `_workspace/` handoff guidance | Stage 00 routes handoffs to `_workspace/repo-support/`; Stage 99 distinguishes repo-support README files from template/target profiles | Revert governance commit | No credentials or token material |
| Validator | User approved rules/environment enforcement | `scripts/validation/check-repo-contracts.sh` | No `_workspace` tracked allowlist | Pending | Revert validator commit | Path-only checks; no file body secret inspection |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-WSC-001 | Create spec, plan, and task scaffold | doc | `VAL-WSC-006` | `PLN-WSC-001` | New Stage 03/04 files; link/contract validation | Documentation Specialist | Done |
| T-WSC-002 | Add `_workspace` contract and ignore boundary | contract | `VAL-WSC-001`, `VAL-WSC-002` | `PLN-WSC-002` | `_workspace` README files; `.gitignore`; focused git status | Documentation Specialist | Done |
| T-WSC-003 | Update Stage 00 and Stage 99 contract wording | governance | `VAL-WSC-003`, `VAL-WSC-004` | `PLN-WSC-003` | Direct fallout docs updated; focused `_workspace` reference search | Documentation Specialist | Done |
| T-WSC-004 | Add validator enforcement | validation | `VAL-WSC-005` | `PLN-WSC-004` | `check-repo-contracts.sh`; negative/positive contract behavior | QA / Validator Maintainer | Pending |
| T-WSC-005 | Validate, update progress, and close evidence | evidence | `VAL-WSC-006` | `PLN-WSC-005` | Final validation summary; progress memory | Documentation Specialist | Pending |

## Phase View

### Phase 1: Planning Scaffold

- [x] T-WSC-001 Create spec, plan, and task scaffold.

### Phase 2: Contract Boundary

- [x] T-WSC-002 Add `_workspace` contract and ignore boundary.

### Phase 3: Governance and Validation

- [x] T-WSC-003 Update Stage 00 and Stage 99 contract wording.
- [ ] T-WSC-004 Add validator enforcement.

### Phase 4: Closure

- [ ] T-WSC-005 Validate, update progress, and close evidence.

## Evidence Inventory

| Evidence Class | Evidence Path / Source | Role |
| --- | --- | --- |
| Graphify advisory context | `graphify-out/GRAPH_REPORT.md` | Graph built from `c1c465c9`; current HEAD is newer, so the graph is navigation-only. |
| Current `_workspace` state | `rg --files _workspace` | No `_workspace` directory existed before this task. |
| Existing handoff guidance | [Subagent protocol](../../00.agent-governance/subagent-protocol.md), [workflow rules](../../00.agent-governance/rules/workflows.md) | Generic `_workspace/` artifact routing to be narrowed to `_workspace/repo-support/`. |
| Security boundary | [Security scope](../../00.agent-governance/scopes/security.md), [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | Source for no secret values, credentials, token-bearing logs, shell history, or private keys. |
| Ignore boundary | [.gitignore](../../../.gitignore), [gitignore documentation](https://www.kernel.org/pub/software/scm/git/docs/gitignore.html), [GitHub Ignoring files](https://docs.github.com/articles/ignoring-files) | Source for shared ignore and re-include behavior. |
| Template/frontmatter contract | [Frontmatter contract](../../99.templates/support/frontmatter-contract.md), [Template governance](../../99.templates/support/template-governance.md) | Source for distinguishing repo-support README files from target-stage documents and template sources. |

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
| `bash scripts/validation/check-repo-contracts.sh` after planning scaffold | PASS | `failures=0`; `changed_template_docs_total=7`, all normalized. |
| `git check-ignore -v _workspace/repo-support/example.txt` after ignore update | PASS | Runtime artifacts below `_workspace/repo-support/` are ignored by `_workspace/**`. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh` after new docs and `_workspace` contracts | PASS | Regenerated `docs/90.references/llm-wiki/llm-wiki-index.md` with 1163 paths. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` after contract README update | PASS | Generated LLM Wiki index is fresh. |
| `bash scripts/validation/check-repo-contracts.sh` after contract README update | PASS | `failures=0`; no repo contract drift after `_workspace` and index updates. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` after governance update | PASS | `sync-provider-surfaces: no drift`. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` after governance update | PASS | Generated LLM Wiki index is fresh. |
| `bash scripts/validation/check-doc-traceability.sh` after governance update | PASS | `failures=0`. |
| `bash scripts/validation/check-repo-contracts.sh` after governance update | PASS | `failures=0`. |
| `rg -nP "_workspace/(?!repo-support|README\\.md)" docs/00.agent-governance docs/99.templates _workspace .gitignore --glob '*.md' --glob '.gitignore' --glob '!docs/00.agent-governance/memory/**'` | PASS | Remaining matches are `.gitignore` default-ignore or contract examples, not active handoff routes. |

## Related Documents

- **Parent Spec**: [Workspace Support Surface Contract Spec](../../03.specs/106-workspace-support-surface-contract/spec.md)
- **Parent Plan**: [Workspace Support Surface Contract Plan](../plans/2026-07-05-workspace-support-surface-contract.md)
- **Subagent Protocol**: [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
- **Environment Constraints**: [Environment constraints](../../00.agent-governance/rules/environment-constraints.md)
- **Template Governance**: [Template governance](../../99.templates/support/template-governance.md)
