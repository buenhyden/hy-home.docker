---
status: active
---

<!-- Target: docs/04.execution/plans/2026-07-02-template-system-reorganization.md -->

# Template System Reorganization Implementation Plan

## Overview

This document is the implementation plan for reorganizing `docs/99.templates`
into a nested template system with separate copyable templates and non-copyable
support governance.

The work follows the approved Stage 03 design in
`docs/03.specs/template-system-reorganization/spec.md`. It updates template
paths, support documents, governance references, validators, and direct
reference fallout while avoiding unrelated runtime or broad document-corpus
rewrites.

## Context

`docs/99.templates` currently stores all template source files in a flat folder.
Its README also mixes catalog, lifecycle, stale-document rules, cross-link
rules, README profile guidance, and template-to-folder mapping. The repository
contract validator mirrors that flat structure through hardcoded required
template paths and non-recursive template discovery.

The approved design separates responsibilities:

- `docs/99.templates/templates/` holds canonical copyable template artifacts.
- `docs/99.templates/support/` holds template governance, frontmatter contract,
  lifecycle vocabulary, selection rules, and external-source rationale.
- `docs/99.templates/README.md` becomes a concise catalog and routing entrypoint.

## Goals & In-Scope

- **Goals**:
  - Move every canonical template into exactly one category folder under
    `docs/99.templates/templates/`.
  - Create support governance documents under `docs/99.templates/support/`.
  - Normalize template-frontmatter guidance and target-document metadata rules.
  - Remove flat legacy template files and stale references to those paths.
  - Update Stage 00 governance, hook guidance, validators, and direct README
    references to the new canonical paths.
  - Record any broad document-corpus normalization outside the first migration
    cycle as a gap.
- **In Scope**:
  - `docs/99.templates/**`
  - `docs/00.agent-governance/rules/**` and relevant hook guidance
  - `scripts/validation/check-repo-contracts.sh`
  - Direct references in stage READMEs and local guidance files
  - `docs/90.references/llm-wiki/index.md`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not change Docker Compose behavior, runtime service configuration,
    provider credentials, secret values, or remote GitHub state.
  - Do not rewrite every existing stage document body to the new template shape.
  - Do not leave flat legacy template shims behind after relocation.
  - Do not use `docs/99.templates/README.md` as the detailed contract body.
- **Out of Scope**:
  - Existing infra hardening image mismatch and tech-stack image drift reported
    by `check-repo-contracts.sh`.
  - Full frontmatter normalization across all active documents unless a touched
    document breaks validation.
  - New CI workflows or new external publishing behavior.

## Work Breakdown

| Task ID | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-TSR-001 | Create Stage 04 task evidence before implementation starts. | `docs/04.execution/tasks/2026-07-02-template-system-reorganization.md`, task README | VAL-SPC-004 | Task file records approved surfaces, phases, and validation evidence placeholders. |
| PLN-TSR-002 | Create `templates/` and `support/` trees and move template files with history-preserving `git mv`. | `docs/99.templates/templates/**`, removed flat `docs/99.templates/*.template.*` paths | VAL-SPC-001, VAL-SPC-003 | `rg --files docs/99.templates` shows canonical nested template paths and no flat template files. |
| PLN-TSR-003 | Replace mixed README governance with focused README plus support documents. | `docs/99.templates/README.md`, `docs/99.templates/support/*.md`, support README | VAL-SPC-002, VAL-SPC-007 | README is catalog-sized; support docs hold contract, governance, frontmatter, lifecycle, selection, and source rationale. |
| PLN-TSR-004 | Normalize template-source and target-document frontmatter rules. | Markdown templates, `frontmatter-contract.md`, `lifecycle-status.md` | VAL-SPC-005 | Template source rules and target document key sets are type-specific and do not duplicate purpose. |
| PLN-TSR-005 | Update repository contract validation for nested templates. | `scripts/validation/check-repo-contracts.sh` | VAL-SPC-004 | Template inventory, markdown template checks, machine-readable contract checks, memory/reference/harness checks use new paths. |
| PLN-TSR-006 | Update Stage 00 governance, hook guidance, and stage README direct references. | Stage 00 rules, `.codex` or hook guidance if referenced, stage READMEs, root docs references | VAL-SPC-004, VAL-SPC-006 | No active direct reference points at removed flat template paths except historical evidence explicitly scoped as such. |
| PLN-TSR-007 | Refresh generated index and record progress/gaps. | `docs/90.references/llm-wiki/index.md`, `docs/00.agent-governance/memory/progress.md` | VAL-SPC-006 | Generated index is fresh; unrelated repo-contract drift remains recorded as a gap. |
| PLN-TSR-008 | Run validation and close task evidence. | Validation outputs, task evidence | VAL-SPC-001 through VAL-SPC-007 | All template-related checks pass; unrelated infra drift is documented without patching infra files. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Hygiene | Check staged diff whitespace. | `git diff --cached --check` | Zero exit status. |
| VAL-PLN-002 | Template Layout | Confirm no flat template source files remain. | `find docs/99.templates -maxdepth 1 -type f -name '*.template.*' -print` | No output. |
| VAL-PLN-003 | Template References | Confirm active direct references use canonical nested template paths or support docs. | `rg -n "docs/99\\.templates/[^\\s)]+\\.template\\.|\\.\\./99\\.templates/[^\\s)]+\\.template\\." docs scripts README.md AGENTS.md RTK.md .github .codex .agents` | No unreviewed flat-path references. |
| VAL-PLN-004 | Generated Index | Verify LLM Wiki index freshness. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-PLN-005 | Traceability | Validate execution and operations traceability. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-PLN-006 | Implementation Alignment | Validate active docs against tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS with `failures=0`. |
| VAL-PLN-007 | Repository Contracts | Validate repository docs, template, governance, and runtime contracts. | `bash scripts/validation/check-repo-contracts.sh` | Template/governance sections pass; unrelated infra drift may remain as recorded gap. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Validator recursion treats support docs as copyable templates. | High | Restrict template validation to `docs/99.templates/templates/**/*.template.*` and validate support docs as normal Stage 99 documentation. |
| Historical plans or tasks contain old flat paths. | Medium | Update active guidance and direct references; leave historical evidence only when it is clearly historical and not current guidance. |
| README grows back into a contract manual. | Medium | Move detailed contract text to `support/` and keep README to catalog, scope, structure, workflow, and related documents. |
| Frontmatter rules become too broad. | Medium | Keep separate key sets for template sources, active stage docs, archives, governance memory, and generated files. |
| Full repo contract remains red from unrelated infra drift. | Medium | Record exact drift as out of scope and do not modify infra files under this plan. |
| Physical moves obscure review. | Low | Use `git mv`, keep logical commits small, and review path-only moves separately from content rewrites. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Diff hygiene, LLM Wiki freshness, doc traceability,
  implementation alignment, repository contract check, and reference search for
  removed flat template paths.
- **Sandbox / Canary Rollout**: N/A. This is a documentation and validation
  migration, not a runtime rollout.
- **Human Approval Gate**: User already approved template, contract, governance,
  protected-surface, destructive cleanup, and logical commit work. Remote
  mutation and secret changes remain out of scope.
- **Rollback Trigger**: Revert the most recent logical commit if nested template
  paths or validator changes make repository contract checks fail for reasons
  caused by this migration.
- **Prompt / Model Promotion Criteria**: N/A. No model or provider runtime
  settings are changed.

## Completion Criteria

- [ ] Stage 04 task evidence exists for this migration.
- [ ] Template files live only under `docs/99.templates/templates/`.
- [ ] Support governance lives under `docs/99.templates/support/`.
- [ ] `docs/99.templates/README.md` is a concise catalog and routing entrypoint.
- [ ] `check-repo-contracts.sh` recognizes the nested template inventory.
- [ ] Active direct references no longer point at removed flat template paths.
- [ ] Generated LLM Wiki index is fresh.
- [ ] Progress log records completion and any unrelated validation gaps.
- [ ] Logical commits separate plan, task, relocation/support, validator/governance, and fallout/progress work.

## Related Documents

- **Spec**: [template system reorganization spec](../../03.specs/template-system-reorganization/spec.md)
- **Spec README**: [template system reorganization README](../../03.specs/template-system-reorganization/README.md)
- **Template Catalog**: [template catalog](../../99.templates/README.md)
- **Documentation Protocol**: [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Task Stage**: [tasks README](../tasks/README.md)
- **Operations**: [operations index](../../05.operations/README.md)
