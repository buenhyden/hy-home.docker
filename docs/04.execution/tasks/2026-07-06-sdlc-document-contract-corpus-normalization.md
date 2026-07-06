---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md -->

# Task: SDLC Document Contract Corpus Normalization

## Overview

This document tracks implementation and verification evidence for the SDLC
document contract corpus normalization waves.

The work begins after the Stage 03 design is approved and committed. This task
file records wave status, protected-surface evidence, validation commands, and
residual gaps as the implementation proceeds.

## Inputs

- **Parent Spec**: [SDLC document contract corpus normalization spec](../../03.specs/119-sdlc-document-contract-corpus-normalization/spec.md)
- **Parent Plan**: [SDLC document contract corpus normalization plan](../plans/2026-07-06-sdlc-document-contract-corpus-normalization.md)
- **Document Restructure Register**: [Document restructure gap register](../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md)

## Working Rules

- Keep Stage 00 and Stage 99 as policy owners.
- Keep README files as routing/index surfaces.
- Do not rewrite historical evidence for style alone.
- Do not move, delete, or rename active documents without exact path evidence,
  replacement or archive disposition, README sync, and validation.
- Do not read or record secret values, credentials, tokens, private keys, raw
  logs, shell history, or `.env` values.
- Do not mutate runtime, Compose, CI workflow, provider runtime, remote GitHub,
  or deployment state in this task.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 00/01 guidance | User approved A: contract-first cleanup and then requested next execution | `docs/01.requirements/README.md`, `docs/00.agent-governance/scopes/meta.md` | Subagent and local discovery found stale date-based PRD guidance after numbered PRD migration | Wave 1 updated numbered PRD naming and metadata scope guidance; targeted stale-guidance scan and repo contracts passed. | Revert Wave 1 commit | Tracked guidance text only |
| Validator and GitHub issue template | Same approval; validator changes are protected and require evidence | `scripts/validation/check-repo-contracts.sh`, `.github/ISSUE_TEMPLATE/bug_report.yml` | Existing validator passes but does not catch all stale active guidance surfaces | Wave 2 updated the issue-template Spec placeholder and expanded active stale-guidance scan surfaces; targeted scan returned no matches and repo contracts passed. | Revert Wave 2 commit | Tracked examples, no remote GitHub mutation |
| Stage 03/04 lifecycle policy | Same approval; policy remains advisory until classified | Stage 90/task evidence and affected README indexes if needed | Sibling README and plan/task pairing questions are not hard-gated | To be recorded in Wave 3 | Revert Wave 3 commit | Tracked path metadata only |
| Operations leaf naming | Same approval; destructive path changes require exact candidates | exact `docs/05.operations/**` candidates | Numeric-dot operations leaf names remain in a small candidate set | To be recorded in Wave 4 | Revert Wave 4 commit or `git mv` back | Tracked document paths and links only |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-SDCN-001 | Clean stale numbered PRD/Spec guidance text. | doc | `Initial Finding Seeds` | `PLN-SDCN-001` | Targeted stale-guidance scan; repo contracts | Documentation Specialist | Done |
| T-SDCN-002 | Extend validator coverage for stale active PRD/Spec guidance. | validation | `Validator Interfaces` | `PLN-SDCN-002` | Syntax, targeted stale-guidance fixtures, full repo contracts | Validator Maintainer | Done |
| T-SDCN-003 | Classify Stage 03 sibling README and Stage 04 plan/task lifecycle policy. | doc | `Traceability Interfaces` | `PLN-SDCN-003` | Classification evidence; no premature hard gate | Documentation Specialist | Todo |
| T-SDCN-004 | Review and apply approved operations leaf naming polish. | ops | `Edge Cases & Error Handling` | `PLN-SDCN-004` | Link sync, traceability, implementation alignment | Operations Reviewer | Todo |
| T-SDCN-005 | Close progress, generated indexes, and residual gaps. | validation | `Success Criteria & Verification Plan` | `PLN-SDCN-005` | Final verification summary | QA Engineer | Todo |

## Phase View

### Wave 1: Contract Text Cleanup

- [x] T-SDCN-001 Clean stale numbered PRD/Spec guidance text.

### Wave 2: Validator Coverage

- [x] T-SDCN-002 Extend validator coverage for stale active PRD/Spec guidance.

### Wave 3: Lifecycle Classification

- [ ] T-SDCN-003 Classify Stage 03 sibling README and Stage 04 plan/task lifecycle policy.

### Wave 4: Operations Naming Polish

- [ ] T-SDCN-004 Review and apply approved operations leaf naming polish.

### Wave 5: Closure

- [ ] T-SDCN-005 Close progress, generated indexes, and residual gaps.

## Verification Summary

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` | PASS | No whitespace or conflict-marker failures after adding the Stage 04 plan/task unit. |
| `git diff --cached --check` | PASS | Staged diff hygiene check passed before the Wave 2 commit. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS | Generated LLM Wiki index is fresh after Wave 2. |
| `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | PASS | Generated LLM Wiki coverage snapshot is fresh at 1229 safe paths after Wave 2. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS | `catalog_pairs_total=46`, `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS | `stage_docs_total=609`, `repo_local_markdown_links_checked=4710`, `failures=0`. |
| `bash -n scripts/validation/check-repo-contracts.sh` | PASS | Repository contract script syntax is valid. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS | Full repository contract gate passed with `failures=0`; changed target-stage docs normalized `1/1`, total target-stage docs normalized `697/697`. |
| Targeted Wave 1 stale-guidance scan | PASS | No stale date-prefixed PRD, old example filename, mixed plan/PRD naming, blanket `layer:` requirement, or flat Stage 99 template-path guidance remains in the edited active guidance files. |
| `.github` Spec placeholder update | PASS | Bug report issue-template placeholder now uses a concrete numbered Spec example path. |
| Extended numbered SDLC guidance scan | PASS | Repo contracts now scan Stage 99, Stage 00 rules/scopes, Stage 01/03 README files, and GitHub issue templates for stale active PRD/Spec target guidance. |
| Targeted Wave 2 stale-guidance scan | PASS | No unapproved legacy PRD date-prefix or unnumbered Spec placeholder guidance remains in the expanded active scan set. |

## Related Documents

- **Parent Spec**: [SDLC document contract corpus normalization spec](../../03.specs/119-sdlc-document-contract-corpus-normalization/spec.md)
- **Parent Plan**: [SDLC document contract corpus normalization plan](../plans/2026-07-06-sdlc-document-contract-corpus-normalization.md)
- **Document restructure register**: [../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md](../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
