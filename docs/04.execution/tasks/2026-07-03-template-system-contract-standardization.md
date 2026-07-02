---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md -->

# Task: Template System Contract Standardization

## Overview

This task records execution evidence for the Stage 99 template-system contract standardization implementation. The work updates support contracts, copyable templates, validator rules, direct fallout references, provider mirrors, and generated indexes according to the approved spec.

## Inputs

- **Parent Spec**: [Template system contract standardization spec](../../03.specs/template-system-contract-standardization/spec.md)
- **Parent Plan**: [Template system contract standardization plan](../plans/2026-07-03-template-system-contract-standardization.md)
- **Template Catalog**: [Template catalog](../../99.templates/README.md)
- **Support Contracts**: [Template contract](../../99.templates/support/template-contract.md), [frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Repository Contract Validator**: [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)

## Working Rules

- Keep support-contract, template-source, validator, direct fallout, and generated-index work in separate commits where practical.
- Preserve the approved task scope; do not edit template sources, scripts, provider surfaces, generated indexes, or unrelated target docs unless that task phase approves them.
- Keep Stage 99 README files as catalog and routing surfaces; durable rules belong in support documents.
- Record unrelated validation failures as gaps instead of patching out-of-scope runtime or infra files.
- Do not store raw logs, secret values, credentials, or shell history.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| docs/99.templates/** | User-approved A+B scope and approved spec | Support contracts and copyable templates | Inventory captured before edits | Updated contracts and templates | git revert this task's commits | No secret values, credentials, tokens, private keys, raw logs, or .env values |
| scripts/validation/check-repo-contracts.sh | User-approved protected-surface change | Template/frontmatter validator rules | Existing validator sections inspected | New checks added or confirmed | git revert validator commit | No secret values, credentials, tokens, private keys, raw logs, or .env values |
| Provider surfaces | Template rules affect agent behavior | .claude/**, .codex/** | Provider sync check | Provider sync no drift | bash scripts/operations/sync-provider-surfaces.sh --write then revert if needed | No credentials or local-only settings |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Capture Stage 99 inventory baseline. | docs | Template System Contract Standardization Spec / Data Modeling | PLN-001 | Inventory command output summarized below | Codex | Done |
| T-002 | Consolidate support contracts. | docs | Template System Contract Standardization Spec / Core Design | PLN-002 | Support docs diff and README durable-rule scan | Codex | Done |
| T-003 | Normalize copyable templates. | docs | Template System Contract Standardization Spec / Interfaces | PLN-003 | Template scan and repo contract | Codex | Planned |
| T-004 | Update validator enforcement. | script | Template System Contract Standardization Spec / Validator Interfaces | PLN-004 | bash -n and repo contract | Codex | Planned |
| T-005 | Apply direct fallout and regenerate indexes. | docs | Template System Contract Standardization Spec / Tools | PLN-005 | Provider sync and LLM Wiki freshness | Codex | Planned |
| T-006 | Close verification evidence. | docs | Template System Contract Standardization Spec / Success Criteria | PLN-006 | Validation matrix complete | Codex | Planned |

## Inventory Baseline

- Template source files: 31 files under `docs/99.templates/templates/`; notable groups are root/category README files plus `common` (4), `governance` (4), `operations` (6), `sdlc` (7), and `spec-contracts` (9).
- Support documents: 7 files under `docs/99.templates/support/`: `README.md`, `external-source-rationale.md`, `frontmatter-contract.md`, `lifecycle-status.md`, `template-contract.md`, `template-governance.md`, and `template-selection.md`.
- Legacy frontmatter key hits: 3 `updated:` metadata hits outside this task's editable scope: `docs/05.operations/guides/06-observability/loki.md`, `docs/05.operations/policies/06-observability/01.retention.md`, and `docs/05.operations/policies/06-observability/loki.md`.

## Implementation Notes

- T-002: Stage 99 support contracts now own durable template-system rules; `docs/99.templates/README.md` remains a catalog and routing surface with links to support.

## Validation Results

| Command | Result |
| --- | --- |
| git diff --check | PASS. |
| rg -n 'README.*must\|README.*required\|README.*forbidden' docs/99.templates/README.md docs/99.templates/templates/*/README.md | PASS: no matches. |
| bash scripts/knowledge/generate-llm-wiki-index.sh --check | FAIL: stale generated LLM Wiki index; generated-index refresh remains outside T-002 and is planned under T-005. |
| bash scripts/operations/sync-provider-surfaces.sh --check | Pending |
| bash scripts/validation/check-doc-traceability.sh | PASS: `failures=0`. |
| bash scripts/validation/check-doc-implementation-alignment.sh | PASS: `failures=0`. |
| TEMPLATE_GATE_BASE=8db0e7f0 bash scripts/validation/check-repo-contracts.sh | FAIL: changed stage document template gate passed; `failures=3` from stale LLM Wiki index plus existing infra hardening and tech-stack drift. |

## Verification Summary

- Test Commands: Listed in ## Validation Results.
- Eval Commands: N/A for documentation contract standardization.
- Manual Checks: Verify support docs own rules and README files remain indexes.

## Related Documents

- Spec: [../../03.specs/template-system-contract-standardization/spec.md](../../03.specs/template-system-contract-standardization/spec.md)
- Plan: [../plans/2026-07-03-template-system-contract-standardization.md](../plans/2026-07-03-template-system-contract-standardization.md)
- Template contract: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- Frontmatter contract: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
