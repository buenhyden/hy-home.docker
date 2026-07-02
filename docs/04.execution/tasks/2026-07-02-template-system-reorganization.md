---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-02-template-system-reorganization.md -->

# Task: Template System Reorganization

## Overview

This document tracks implementation and verification work for reorganizing
`docs/99.templates` into a nested template system with separate copyable
templates and non-copyable support governance.

The task follows the approved Stage 03 specification and Stage 04 plan. It is
documentation and validation work, but it touches protected surfaces because the
template system is enforced by governance rules and repository contract checks.

## Inputs

- **Parent Spec**: [Template system reorganization spec](../../03.specs/template-system-reorganization/spec.md)
- **Parent Plan**: [Template system reorganization plan](../plans/2026-07-02-template-system-reorganization.md)
- **Template Catalog**: [Template catalog](../../99.templates/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Repository Contract Validator**: [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)

## Working Rules

- Use logical commits for plan, task, relocation/support, validator/governance,
  and fallout/progress phases.
- Use `git mv` for template relocation so history is preserved.
- Do not leave flat legacy template shims behind after relocation.
- Do not rewrite broad existing stage document bodies unless validation requires
  a minimal fallout fix.
- Record unrelated repo-contract drift as a gap instead of patching runtime or
  infra files.
- Do not store raw logs, secret values, credentials, or shell history.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Templates | User approved template reorganization, destructive cleanup, and legacy deletion | `docs/99.templates/**` | Flat template files and mixed README governance | Templates moved under `templates/`; support rules split under `support/` | Revert the latest logical template commit | No secrets |
| Governance | User approved contract and governance changes | `docs/00.agent-governance/rules/**`, hook guidance | Stage 00 rules reference flat template paths | Writable governance references updated to nested paths | Revert governance/validator alignment commit | No secrets |
| Validation | User approved protected-surface changes | `scripts/validation/check-repo-contracts.sh` | Validator hardcodes flat template paths | Nested template inventory and recursive checks added | Revert validator alignment commit | No secrets |
| Generated index | Required after docs path changes | `docs/90.references/llm-wiki/llm-wiki-index.md` | Index reflects pre-migration paths | Regenerated after moved and added docs | Regenerate with script or revert index commit | No secrets |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create Stage 04 task evidence before implementation starts. | doc | Success Criteria | PLN-TSR-001 | Task evidence committed in `c85e8f44`; LLM Wiki refreshed | Codex | Done |
| T-002 | Move template files into canonical category folders with `git mv`. | doc | Core Design / Proposed Template Inventory | PLN-TSR-002 | `find docs/99.templates -maxdepth 1 -type f -name '*.template.*' -print` returns no output | Codex | Done |
| T-003 | Replace mixed template README governance with support documents. | doc | Core Design / Support Document Roles | PLN-TSR-003 | `docs/99.templates/README.md` is routing-only; support docs contain contract/governance rules | Codex | Done |
| T-004 | Normalize template-source and target-document frontmatter rules. | doc | Data Modeling / Frontmatter Field Families | PLN-TSR-004 | Support frontmatter contract defines type-specific key sets; legacy README metadata snippet removed | Codex | Done |
| T-005 | Update repository contract validation for nested templates. | impl | Validation Interface | PLN-TSR-005 | `check-repo-contracts.sh` template inventory and template globs now use nested template paths | Codex | Done |
| T-006 | Update Stage 00 governance, hook guidance, and active direct references. | doc | Contracts / Validator Parity | PLN-TSR-006 | Writable active direct references updated; `.codex/skills` remains read-only gap if still stale | Codex | Done |
| T-007 | Refresh generated index and record progress/gaps. | doc | Memory & Context Strategy | PLN-TSR-007 | LLM Wiki regenerated after new support docs and moved templates; progress updated | Codex | Done |
| T-008 | Run final validation and close evidence. | ops | Verification | PLN-TSR-008 | Diff hygiene, LLM Wiki, traceability, implementation alignment, and provider sync passed; repo contract has only pre-existing infra drift failures | Codex | Done |

## Suggested Types

- `doc`
- `impl`
- `ops`

## Phase View (Optional)

### Phase 1: Evidence Bootstrap

- [x] T-001 Create task evidence shell

### Phase 2: Template and Support Migration

- [x] T-002 Move template files
- [x] T-003 Create support governance
- [x] T-004 Normalize frontmatter contract

### Phase 3: Validator and Governance Alignment

- [x] T-005 Update repository contract validation
- [x] T-006 Update governance and references

### Phase 4: Final Fallout and Validation

- [x] T-007 Refresh generated index and progress
- [x] T-008 Run final validation and close evidence

## Verification Summary

- **Test Commands**:
  - `git diff --cached --check` -> pass.
  - `find docs/99.templates -maxdepth 1 -type f -name '*.template.*' -print` -> no output.
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check` -> pass.
  - `bash scripts/validation/check-doc-traceability.sh` -> pass, `failures=0`.
  - `bash scripts/validation/check-doc-implementation-alignment.sh` -> pass, `failures=0`.
  - `bash scripts/operations/sync-provider-surfaces.sh --check` -> `no drift`.
  - `bash scripts/validation/check-repo-contracts.sh` -> template/governance/provider checks pass; fails only on pre-existing infra hardening and tech-stack image drift.
- **Eval Commands**: N/A. This is documentation and repository-contract work.
- **Logs / Evidence Location**: This document's Task Table, progress log, and
  final validation summary.

### Current Validation Notes

- `check-repo-contracts.sh` is known to fail outside this task scope on the
  existing Keycloak hardening image mismatch and `infra/tech-stack.versions.json`
  image drift. Do not patch infra files under this task.

### Deviation Notes

- The implementation combined template relocation, support document creation,
  validator alignment, provider skill path fallout, and active direct-reference
  fallout into one implementation commit because moving the template files
  immediately broke active Markdown link checks and provider mirror parity.
  The design, plan, and task evidence remain separate commits.

## Related Documents

- **Parent Spec**: [Template system reorganization spec](../../03.specs/template-system-reorganization/spec.md)
- **Parent Plan**: [Template system reorganization plan](../plans/2026-07-02-template-system-reorganization.md)
- **Template Catalog**: [Template catalog](../../99.templates/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
