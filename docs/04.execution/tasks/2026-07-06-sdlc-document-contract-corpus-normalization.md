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
| Stage 03/04 lifecycle policy | Same approval; policy remains advisory until classified | Stage 90/task evidence and affected README indexes if needed | Sibling README and plan/task pairing questions are not hard-gated | Wave 3 classified sibling README gaps and plan/task filename asymmetry as evidence-preserve surfaces; Stage 03/04 README guidance now states no premature hard gate. | Revert Wave 3 commit | Tracked path metadata only |
| Operations leaf naming | Same approval; destructive path changes require exact candidates | exact `docs/05.operations/**` candidates | Numeric-dot operations leaf names remained in three active Stage 05 leaf files | Wave 4 renamed the three active operations numeric-dot leaves, updated active README/link/Target references, adjusted implementation-alignment non-service stem exceptions, regenerated LLM Wiki outputs, and left historical evidence mentions unchanged. | Revert Wave 4 commit or `git mv` back | Tracked document paths and links only |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-SDCN-001 | Clean stale numbered PRD/Spec guidance text. | doc | `Initial Finding Seeds` | `PLN-SDCN-001` | Targeted stale-guidance scan; repo contracts | Documentation Specialist | Done |
| T-SDCN-002 | Extend validator coverage for stale active PRD/Spec guidance. | validation | `Validator Interfaces` | `PLN-SDCN-002` | Syntax, targeted stale-guidance fixtures, full repo contracts | Validator Maintainer | Done |
| T-SDCN-003 | Classify Stage 03 sibling README and Stage 04 plan/task lifecycle policy. | doc | `Traceability Interfaces` | `PLN-SDCN-003` | Classification evidence; no premature hard gate | Documentation Specialist | Done |
| T-SDCN-004 | Review and apply approved operations leaf naming polish. | ops | `Edge Cases & Error Handling` | `PLN-SDCN-004` | Link sync, traceability, implementation alignment | Operations Reviewer | Done |
| T-SDCN-005 | Close progress, generated indexes, and residual gaps. | validation | `Success Criteria & Verification Plan` | `PLN-SDCN-005` | Final verification summary | QA Engineer | Todo |

## Phase View

### Wave 1: Contract Text Cleanup

- [x] T-SDCN-001 Clean stale numbered PRD/Spec guidance text.

### Wave 2: Validator Coverage

- [x] T-SDCN-002 Extend validator coverage for stale active PRD/Spec guidance.

### Wave 3: Lifecycle Classification

- [x] T-SDCN-003 Classify Stage 03 sibling README and Stage 04 plan/task lifecycle policy.

### Wave 4: Operations Naming Polish

- [x] T-SDCN-004 Review and apply approved operations leaf naming polish.

### Wave 5: Closure

- [ ] T-SDCN-005 Close progress, generated indexes, and residual gaps.

## Lifecycle Classification Evidence

| Surface | Current Evidence | Classification | Decision |
| --- | --- | --- | --- |
| Stage 03 sibling README policy | `42` numbered spec folders exist; `30` have sibling README files; `12` historical/generated snapshot folders currently have `spec.md` without sibling README files. | `evidence-preserve` | Keep sibling README optional for historical folders with valid `spec.md`; recommend README for new/current workstreams that need routing context. Do not add a hard validator until Stage 00/99 records an exception model. |
| Stage 04 plan/task filename pairing | `84` plan docs and `110` task docs exist; exact filename overlap is `60`, with `24` plan-only filenames and `50` task-only filenames by exact-name comparison. | `evidence-preserve` | Keep current link-based traceability as the contract. Do not add exact-stem pairing as a hard gate until historical plan-only/task-only evidence is explicitly migrated, archived, or excepted. |
| Stage 04 README guidance | README already separates plan and task responsibility but did not state filename-pairing limits. | `active-canonical` for routing guidance | Add concise routing guidance that plan/task relation is proven by parent/related links and task evidence, not exact filename equality. |

## Operations Naming Evidence

| Old Path | New Path | Role Bucket | Disposition |
| --- | --- | --- | --- |
| `docs/05.operations/guides/01-gateway/01.setup.md` | `docs/05.operations/guides/01-gateway/setup.md` | Guide | `active-canonical` rename; bucket and document role preserved. |
| `docs/05.operations/guides/06-observability/01.lgtm-stack.md` | `docs/05.operations/guides/06-observability/lgtm-stack.md` | Guide | `active-canonical` rename; bucket and document role preserved. |
| `docs/05.operations/policies/06-observability/01.retention.md` | `docs/05.operations/policies/06-observability/retention.md` | Policy | `active-canonical` rename; bucket and document role preserved. |
| `scripts/validation/check-doc-implementation-alignment.sh` non-service stems | `setup`, `lgtm-stack`, `retention` | Validator support | Direct fallout so renamed operations guide/policy documents remain routing/control docs instead of being treated as service leaf implementation docs. |

## Verification Summary

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` | PASS | No whitespace or conflict-marker failures after adding the Stage 04 plan/task unit. |
| `git diff --cached --check` | PASS | Staged diff hygiene check passed before the Wave 2 commit. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS | Generated LLM Wiki index is fresh at 1230 paths after Wave 4. |
| `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | PASS | Generated LLM Wiki coverage snapshot is fresh at 1229 safe paths after Wave 4. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS | `catalog_pairs_total=46`, `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS | `stage_docs_total=609`, `repo_local_markdown_links_checked=4710`, `failures=0`. |
| `bash -n scripts/validation/check-repo-contracts.sh` | PASS | Repository contract script syntax is valid. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS | Full repository contract gate passed with `failures=0`; changed target-stage docs normalized `13/13`, total target-stage docs normalized `697/697`. |
| Targeted Wave 1 stale-guidance scan | PASS | No stale date-prefixed PRD, old example filename, mixed plan/PRD naming, blanket `layer:` requirement, or flat Stage 99 template-path guidance remains in the edited active guidance files. |
| `.github` Spec placeholder update | PASS | Bug report issue-template placeholder now uses a concrete numbered Spec example path. |
| Extended numbered SDLC guidance scan | PASS | Repo contracts now scan Stage 99, Stage 00 rules/scopes, Stage 01/03 README files, and GitHub issue templates for stale active PRD/Spec target guidance. |
| Targeted Wave 2 stale-guidance scan | PASS | No unapproved legacy PRD date-prefix or unnumbered Spec placeholder guidance remains in the expanded active scan set. |
| Stage 03 sibling README classification | PASS | `42` numbered spec folders checked; `30` have sibling README files and `12` historical/generated snapshot folders remain valid with `spec.md` only. |
| Stage 04 plan/task filename classification | PASS | `84` plan docs, `110` task docs, `60` exact filename overlaps, `24` plan-only filenames, and `50` task-only filenames by exact-name comparison; link-based traceability remains the active contract. |
| No premature lifecycle hard gate | PASS | Wave 3 updated routing guidance and task evidence only; no validator hard gate was added for Stage 03 README or Stage 04 exact-stem pairing. |
| Operations numeric-dot leaf scan | PASS | `find docs/05.operations -type f -name '01.*.md'` returned no active Stage 05 paths after Wave 4. |
| Operations link sync | PASS | Active Stage 05 README, Target comments, policy links, and implementation-alignment non-service stems now use `setup.md`, `lgtm-stack.md`, and `retention.md`; historical evidence references were preserved. |
| `bash -n scripts/validation/check-doc-implementation-alignment.sh` | PASS | Implementation-alignment validator syntax is valid after non-service stem updates. |

## Related Documents

- **Parent Spec**: [SDLC document contract corpus normalization spec](../../03.specs/119-sdlc-document-contract-corpus-normalization/spec.md)
- **Parent Plan**: [SDLC document contract corpus normalization plan](../plans/2026-07-06-sdlc-document-contract-corpus-normalization.md)
- **Document restructure register**: [../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md](../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
