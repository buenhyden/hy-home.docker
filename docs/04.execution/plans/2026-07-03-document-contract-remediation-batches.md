---
status: active
---

<!-- Target: docs/04.execution/plans/2026-07-03-document-contract-remediation-batches.md -->

# Document Contract Remediation Batches Implementation Plan

> **For agentic workers:** Use this plan to execute the approved
> `WDC-GAP-*` remediation batches from the document-contract audit register.
> Keep each batch in its own commit boundary and do not combine provider,
> secret-handling, target-corpus, validator, workflow, or infra changes unless
> this plan explicitly says they must be synchronized.

## Overview

This plan turns the document-contract audit pack's future implementation
batches into executable Stage 04 work. The audit pack measured the workspace
document corpus and classified gaps; this plan defines the later remediation
sequence, approvals, validation gates, rollback boundaries, and evidence
requirements.

This plan does not apply fixes by itself. Implementation tasks created from
this plan must record execution evidence under `docs/04.execution/tasks/` and
close each batch with validation results.

## Context

The completed workspace document contract audit pack created a stable gap
register under `docs/90.references/audits/document-contracts/gap-register.md`.
That register classifies 30 rows:

- 11 `batch-fix` rows that need bounded remediation.
- 4 `historical-evidence` rows that should usually be preserved.
- 7 `out-of-scope-gap` rows that need separate approval or different owners.
- 8 `no-action` rows that are closure evidence.

The safe next step is not a broad corpus rewrite. It is to execute the
approved batch-fix rows in small slices, preserving Stage 00 and Stage 99 as
the contract owners and treating provider/runtime, workflow, validator,
secret, and infra surfaces as protected.

## Goals & In-Scope

- **Goals**:
  - Execute document-contract remediation from the audit register without
    losing the gap dispositions.
  - Keep Stage 00 governance and Stage 99 template contracts as the source of
    truth.
  - Normalize active guidance and target documents only within approved batch
    boundaries.
  - Record evidence for any gap that is fixed, reclassified, deferred, or
    intentionally preserved.
  - Preserve known infra drift as out of scope unless an infra-specific task
    is explicitly approved.
- **In Scope**:
  - `docs/90.references/audits/document-contracts/gap-register.md`
  - batch-specific task evidence under `docs/04.execution/tasks/`
  - provider and governance text surfaces listed by WDC-GAP-001 and
    WDC-GAP-002
  - README surfaces listed by WDC-GAP-003 through WDC-GAP-005
  - target-stage frontmatter and section surfaces listed by WDC-GAP-006
    through WDC-GAP-009 and WDC-GAP-016
  - CI/CD, QA, parser, and Graphify decision surfaces listed by WDC-GAP-010,
    WDC-GAP-011, and WDC-GAP-018
  - generated LLM Wiki index when tracked paths or document references change
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite the whole Markdown corpus to satisfy a new style preference.
  - Do not rewrite historical specs, plans, tasks, progress entries, or archive
    evidence unless a future task proves they are active guidance.
  - Do not change Docker Compose runtime behavior in documentation batches.
  - Do not read or print secret values.
  - Do not change remote GitHub settings without explicit remote-action
    approval.
- **Out of Scope**:
  - secret values, credentials, tokens, certificates, private keys, raw logs,
    shell history, and `.env` values
  - remote GitHub mutation
  - provider runtime configuration changes
  - Docker Compose runtime changes outside the infra drift batch
  - broad historical evidence cleanup
  - resolving Keycloak hardening image drift or tech-stack image drift outside
    an infra-specific task

## Work Breakdown

| Task ID | Description | Files / Docs Affected | Source Gaps | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-WDC-RM-001 | Create batch task evidence and confirm current gap-register baseline. | `docs/04.execution/tasks/YYYY-MM-DD-document-contract-remediation-batches.md`, `gap-register.md` | All rows | Task evidence records approved surfaces, redaction boundaries, current gap counts, and no target edits yet. |
| PLN-WDC-RM-002 | Fix active governance and provider adapter drift. | `.agents/**`, `.claude/**`, `.codex/**`, `docs/00.agent-governance/**`, `.github/rulesets/main-protection.md` when approved | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Provider wording points to Stage 00 owner rules; provider sync and repo contracts do not show provider drift. |
| PLN-WDC-RM-003 | Normalize README profiles by surface. | `projects/**/README.md`, `secrets/README.md`, `tests/README.md`; examples only with separate examples approval | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | README profile wording and template links match current contracts; secret README edits remain metadata-only and redaction-safe. |
| PLN-WDC-RM-004 | Normalize target-stage frontmatter and section profiles. | `docs/01.requirements/**`, approved `docs/05.operations/**`, `infra/**/*.md`, and other explicitly routed Markdown profiles | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Frontmatter and section inventories improve or explicitly document preserved exceptions by profile. |
| PLN-WDC-RM-005 | Decide CI/CD, QA, parser, and Graphify enforcement. | `.github/workflows/**`, `scripts/validation/**`, `scripts/knowledge/**`, `.pre-commit-config.yaml` only after protected-surface approval | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Dependency-audit, parser, and Graphify decisions are either implemented with checks or documented as advisory/no-action. |
| PLN-WDC-RM-006 | Preserve or reclassify historical evidence rows. | `docs/03.specs/**`, `docs/04.execution/**`, `docs/98.archive/**`, `archive/**`, progress memory | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Historical evidence remains semantically intact unless a specific active-guidance conflict is proven. |
| PLN-WDC-RM-007 | Execute infra drift only as a separate infra task if approved. | `infra/02-auth/keycloak/**`, `infra/tech-stack.versions.json`, Compose declarations, hardening scripts | WDC-GAP-020, WDC-GAP-021 | Infra checks pass or the drift remains documented out of scope for documentation batches. |
| PLN-WDC-RM-008 | Close batch evidence, update register dispositions, regenerate indexes, and commit. | batch task evidence, `gap-register.md`, progress memory, LLM Wiki index | All touched rows | Every touched gap row has final disposition evidence and validation results. |

## Batch Approval Gates

| Batch | Required Approval Before Editing | Protected Boundary |
| --- | --- | --- |
| Governance and provider adapter text | Approval for provider/runtime prompt wording and Stage 00 rule references | Do not change provider runtime config or credentials. |
| README profile normalization | Per-surface approval; explicit redaction boundary for `secrets/README.md` | Do not inspect files under `secrets/**` other than approved documentation paths. |
| Target-stage frontmatter and sections | Stage-specific document approval and profile decision | Do not bulk-format unrelated documents. |
| CI/CD, QA, parser, and Graphify | Explicit workflow/script/validator/pre-commit approval | Do not add audit gates that require unavailable credentials or external mutation. |
| Historical evidence cleanup | Approval only after active consumption is proven | Preserve old truth unless it harms current guidance. |
| Infra drift | Infra owner approval and runtime-change approval when Compose changes | Keep infra commits separate from documentation remediation. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WDC-RM-001 | Hygiene | Check whitespace in the current diff. | `git diff --check` | Zero exit status. |
| VAL-WDC-RM-002 | LLM Wiki | Verify generated path index freshness after doc path changes. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-WDC-RM-003 | Provider Surface | Verify generated provider surfaces are synchronized after provider-adapter edits. | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS, or drift is intentionally generated and committed in the same provider batch. |
| VAL-WDC-RM-004 | Traceability | Validate plan, task, and operations traceability. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-WDC-RM-005 | Implementation Alignment | Validate active docs against tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS with `failures=0`. |
| VAL-WDC-RM-006 | Repo Contract Syntax | Validate repo-contract script syntax before full execution. | `bash -n scripts/validation/check-repo-contracts.sh` | Zero exit status. |
| VAL-WDC-RM-007 | Repo Contracts | Validate repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | PASS, or failure is limited to known out-of-scope infra drift until the infra batch is approved. |
| VAL-WDC-RM-008 | README Template Drift | Check removed flat README/service template paths in affected surfaces. | `rg -n 'docs/99\\.templates/(readme|service)\\.template' projects secrets tests examples` | No active unreviewed references remain in approved surfaces. |
| VAL-WDC-RM-009 | Operations Metadata | Check generic operations `updated` metadata after operations metadata cleanup. | `rg -n '^updated:' docs/05.operations` | No unapproved active operations metadata drift remains, or exceptions are recorded by profile. |
| VAL-WDC-RM-010 | Gap Register | Confirm touched rows record a final disposition. | `rg -n 'WDC-GAP-00[1-9]|WDC-GAP-01[0-9]|WDC-GAP-02[0-2]' docs/90.references/audits/document-contracts/gap-register.md` | Touched rows have evidence-backed next action or closure wording. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Batch work turns into a broad corpus rewrite. | High | Execute by surface group and commit boundary; stop when a change would cross into an unapproved stage. |
| Provider adapter text becomes a new source of truth. | High | Keep Stage 00 as owner and make provider files import or defer to owner rules where possible. |
| Secret-handling documentation edits accidentally inspect secret material. | High | Limit reads to `secrets/README.md`; never inspect values or generated secret files. |
| Validator or workflow changes break local developer ergonomics. | Medium | Separate advisory documentation from hard gates; run local QA gates before committing script/workflow changes. |
| Historical evidence loses audit meaning. | Medium | Preserve old records unless a specific current-guidance conflict is documented. |
| Full repo contracts remain red from known infra drift. | Medium | Keep infra drift recorded as out of scope until PLN-WDC-RM-007 is approved. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Use the validation plan for every batch before
  committing.
- **Sandbox / Canary Rollout**: N/A for pure documentation batches. For
  workflow, script, validator, or infra changes, run the narrow local gate
  before full repo contracts.
- **Human Approval Gate**: Required before any protected workflow, validator,
  provider runtime, remote GitHub, secret-surface, or infra runtime change.
- **Rollback Trigger**: Revert the latest logical batch commit if validation
  fails for a cause introduced by that batch.
- **Prompt / Model Promotion Criteria**: N/A. Provider text edits in this plan
  do not change model selection or runtime provider credentials.

## Completion Criteria

- [ ] Batch task evidence exists before remediation edits start.
- [ ] Touched `WDC-GAP-*` rows are closed, reclassified, or explicitly
      deferred with evidence.
- [ ] Provider, README, frontmatter, section, CI/CD, QA, historical, and infra
      boundaries remain separated by commit.
- [ ] Generated LLM Wiki index is fresh when path or document references
      change.
- [ ] Progress memory records completed remediation batches and known residual
      gaps.
- [ ] Required validation commands pass, except known out-of-scope infra drift
      until the infra batch is approved.

## Related Documents

- **Audit Gap Register**: [gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Plan**: [workspace document contract audit pack plan](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Task Evidence**: [workspace document contract audit pack task](../tasks/2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Spec**: [workspace document contract audit pack spec](../../03.specs/workspace-document-contract-audit-pack/spec.md)
- **Template Contract**: [template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Stage Authoring Matrix**: [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Provider Sync Script**: [provider surface sync](../../../scripts/operations/sync-provider-surfaces.sh)
- **Repository Contract Validator**: [repo contract validator](../../../scripts/validation/check-repo-contracts.sh)
