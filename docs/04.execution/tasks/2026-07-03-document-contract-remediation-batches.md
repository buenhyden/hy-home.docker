---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md -->

# Task: Document Contract Remediation Batches

## Overview

This task records execution evidence for the document-contract remediation
batches that follow the completed workspace document contract audit pack. The
first work unit creates this evidence file, confirms the current
`WDC-GAP-*` baseline, and preserves protected boundaries before any target
corpus remediation begins.

## Inputs

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Template Contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Execute one remediation batch at a time.
- Do not apply target corpus fixes without the matching batch approval.
- Keep provider, workflow, validator, secret-handling, infra, and target-stage
  edits in separate logical commits.
- Treat Stage 00 governance and Stage 99 template contracts as the source of
  truth; provider files are adapters, not owners.
- Do not inspect secret values, credentials, tokens, certificates, private
  keys, raw logs, shell history, or `.env` values.
- Keep existing infra image/version drift out of documentation batches unless
  an infra-specific task is approved.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` | Approved remediation batch plan and user continuation | Execution evidence | File absent | Task evidence records baseline and future batch status | `git revert` this task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/04.execution/tasks/README.md` | Task-stage routing contract | Task index | Remediation batch task not listed | Active task linked in structure and related documents | `git revert` this task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| Future protected surfaces | Parent plan approval gates | Provider, workflow, validator, secret-handling, infra, and target-stage changes | No remediation applied in T-001 | Future tasks must record per-batch evidence before edits | Revert the specific future batch commit | Redaction boundary must be restated in each future batch before touching protected surfaces |

## Task Table

| Task ID | Description | Type | Parent Plan / Phase | Source Gaps | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create task evidence and confirm current gap-register baseline. | doc | PLN-WDC-RM-001 | All rows | Baseline counts and validation matrix | Codex | Done |
| T-002 | Fix active governance and provider adapter drift. | doc | PLN-WDC-RM-002 | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Provider sync and repo contracts | Codex | Planned |
| T-003 | Normalize README profiles by surface. | doc | PLN-WDC-RM-003 | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | README/template drift checks | Codex | Planned |
| T-004 | Normalize target-stage frontmatter and section profiles. | doc | PLN-WDC-RM-004 | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Inventory rerun and profile exceptions | Codex | Planned |
| T-005 | Decide CI/CD, QA, parser, and Graphify enforcement. | doc/script | PLN-WDC-RM-005 | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Protected-surface checks | Codex | Planned |
| T-006 | Preserve or reclassify historical evidence rows. | doc | PLN-WDC-RM-006 | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Historical evidence review | Codex | Planned |
| T-007 | Execute infra drift only as a separate infra task if approved. | ops | PLN-WDC-RM-007 | WDC-GAP-020, WDC-GAP-021 | Infra-only validation | Codex | Deferred |
| T-008 | Close batch evidence, update register dispositions, regenerate indexes, and commit. | doc | PLN-WDC-RM-008 | All touched rows | Final validation matrix and commit trail | Codex | Planned |

## Baseline Snapshot

| Measure | Command | Result |
| --- | --- | ---: |
| Total `WDC-GAP-*` rows | `rg '^\| WDC-GAP-[0-9]{3} ' docs/90.references/audits/document-contracts/gap-register.md \| wc -l` | 30 |
| `direct-fix` rows | Row count filtered by disposition `direct-fix`. | 0 |
| `batch-fix` rows | Row count filtered by disposition `batch-fix`. | 11 |
| `historical-evidence` rows | Row count filtered by disposition `historical-evidence`. | 4 |
| `out-of-scope-gap` rows | Row count filtered by disposition `out-of-scope-gap`. | 7 |
| `no-action` rows | Row count filtered by disposition `no-action`. | 8 |

## Batch Status

| Batch | Source Rows | Current Status | Boundary |
| --- | --- | --- | --- |
| Governance and provider adapter drift | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Planned | Requires provider/runtime prompt wording approval; no provider runtime config changes. |
| README profile normalization | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | Planned | Requires per-surface approval and redaction-safe handling for `secrets/README.md`. |
| Target-stage frontmatter and section profiles | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Planned | Requires stage/profile decisions before corpus edits. |
| CI/CD, QA, parser, and Graphify decisions | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Planned | Requires protected workflow, script, validator, or pre-commit approval before edits. |
| Historical evidence preservation or reclassification | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Planned | Preserve old truth unless active-consumption conflict is proven. |
| Infra drift follow-up | WDC-GAP-020, WDC-GAP-021 | Deferred | Requires separate infra task and runtime-change approval if Compose changes. |

## Validation Results

| Scope | Command | Result |
| --- | --- | --- |
| Gap baseline | Baseline `rg ... \| wc -l` commands listed in `## Baseline Snapshot` | PASS: register still has 30 rows with disposition distribution `0/11/4/7/8`. |
| Task path pre-check | `test -f docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` before creation | PASS: command exited non-zero before creation, confirming the evidence file was new. |
| Target corpus boundary | Manual diff review | PASS: T-001 creates task evidence and task index only; no target corpus remediation is applied. |
| LLM Wiki regeneration | `bash scripts/knowledge/generate-llm-wiki-index.sh` | PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with 1124 paths after adding this task evidence. |
| Whitespace | `git diff --check` | PASS: no whitespace errors. |
| LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS: generated LLM Wiki index is fresh. |
| Provider surfaces | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS: `failures=0`. |
| Implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS: `failures=0`. |
| Repo contract syntax | `bash -n scripts/validation/check-repo-contracts.sh` | PASS: shell syntax is valid. |
| Full repo contract | `bash scripts/validation/check-repo-contracts.sh` | Expected FAIL: `failures=2`; no task, plan, reference, provider, LLM Wiki, Stage 99, or document-contract remediation failures. Failures remain confined to known out-of-scope infra drift: the Keycloak hardening image mismatch and `infra/tech-stack.versions.json` expected-image drift. |

## Verification Summary

- **Test Commands**: Listed in `## Validation Results`.
- **Eval Commands**: N/A for documentation task evidence.
- **Logs / Evidence Location**: This task document and the source
  `gap-register.md`.
- **Manual Checks**: Confirmed the first unit does not remediate target corpus,
  provider, workflow, validator, secret-handling, runtime, or infra surfaces.

## Related Documents

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Plan**: [Workspace document contract audit pack plan](../plans/2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Spec**: [Workspace document contract audit pack spec](../../03.specs/workspace-document-contract-audit-pack/spec.md)
