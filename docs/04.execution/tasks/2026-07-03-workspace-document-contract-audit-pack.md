---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md -->

# Task: Workspace Document Contract Audit Pack

## Overview

This task records execution evidence for the workspace document contract audit
pack. The work creates durable audit reports for document profiles,
frontmatter, sections, README profiles, governance contracts, CI/CD, QA,
automation coverage, and future implementation gaps.

## Inputs

- Parent Spec: `docs/03.specs/workspace-document-contract-audit-pack/spec.md`
- Parent Plan: `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
- Template Contract: `docs/99.templates/support/template-contract.md`
- Frontmatter Contract: `docs/99.templates/support/frontmatter-contract.md`
- Stage Authoring Matrix: `docs/00.agent-governance/rules/stage-authoring-matrix.md`

## Working Rules

- Audit first; do not normalize target documents in this task.
- Inspect tracked paths, Markdown structure, workflow YAML, and validator output.
- Do not read or print secret values from `secrets/**`.
- Classify historical evidence separately from active guidance drift.
- Record existing infra image/version drift as out of scope.
- Keep execution evidence here and stable audit reports in `docs/90.references/audits/document-contracts/`.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md` | Approved Stage 03 spec and user approval | Execution evidence | File absent | Task evidence records audit execution | `git revert` audit-pack commits | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/90.references/audits/document-contracts/**` | Approved Stage 03 spec and user approval | Durable audit reports | Bundle absent | Audit reports created and indexed | `git revert` audit-pack commits | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/90.references/audits/README.md` | Approved Stage 03 spec and user approval | Audit category routing | Document-contract bundle not listed | Bundle linked | `git revert` audit-pack commits | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create task evidence and audit bundle skeleton. | docs | Workspace Document Contract Audit Pack Spec / Data Modeling | PLN-001 | Audit skeleton and links | Codex | Done |
| T-002 | Capture document profile inventories. | docs | Workspace Document Contract Audit Pack Spec / Core Design | PLN-002 | Inventory reports with commands and counts | Codex | Done |
| T-003 | Compare governance, contracts, templates, root shims, and provider surfaces. | docs | Workspace Document Contract Audit Pack Spec / Contracts | PLN-003 | Contract map and template-application gap report | Codex | Done |
| T-004 | Map CI/CD, QA, and automation coverage. | docs | Workspace Document Contract Audit Pack Spec / Tool Contract | PLN-004 | Automation coverage map | Codex | Done |
| T-005 | Build final gap register and implementation batch proposal. | docs | Workspace Document Contract Audit Pack Spec / Gap Disposition Rules | PLN-005 | Gap register with dispositions | Codex | Done |
| T-006 | Close evidence, regenerate indexes, validate, and commit. | docs | Workspace Document Contract Audit Pack Spec / Verification | PLN-006 | Validation matrix and commit trail | Codex | Planned |

## Inventory Baseline

- Baseline tracked Markdown count: 930 after Task 2 inventory reports are tracked.
- Baseline README count: 206.
- Baseline workflow count: 6 tracked GitHub workflow files under `.github/workflows/`.
- Existing out-of-scope drift: Known infra hardening and tech-stack expected-image drift remain out of scope.

## Gap Disposition Summary

| Disposition | Count | Notes |
| --- | ---: | --- |
| `direct-fix` | 0 | No source audit report approved a direct fix for Task 5. |
| `batch-fix` | 11 | Provider/governance wording, README profile, frontmatter, section, dependency-audit, and Graphify follow-up rows. |
| `historical-evidence` | 4 | Baselines, archive evidence, and historical template-path records preserved as audit evidence. |
| `out-of-scope-gap` | 7 | Examples, parser/tooling, remote GitHub evidence, Stage 05 metadata decisions, and infra drift deferred to separate approvals. |
| `no-action` | 8 | Closure evidence, intentional profiles, valid broad references, managed CI coupling, provider sync coverage, and manual secret-generation boundary. |
| **Total** | **30** | Consolidated `WDC-GAP-*` rows in `gap-register.md`. |

## Implementation Notes

- Task 2 created `docs/90.references/audits/document-contracts/frontmatter-inventory.md`,
  `docs/90.references/audits/document-contracts/section-profile-inventory.md`,
  and `docs/90.references/audits/document-contracts/readme-profile-inventory.md`.
- Task 2 measurement fix reran the committed-state inventory: 930 tracked
  Markdown files, 745 files with top frontmatter, 185 without top
  frontmatter, 519 `status` keys, and 206 tracked README files.
- Task 2 quality fix aligned the three inventory reports with the Stage 90
  reference document contract and added full reproduction commands for the
  Python frontmatter and section-profile scans.
- Task 3 created `docs/90.references/audits/document-contracts/contract-governance-map.md`
  and `docs/90.references/audits/document-contracts/template-application-gaps.md`.
  `DESIGN.md` was absent in the repository root during Task 3 verification.
- Task 4 created `docs/90.references/audits/document-contracts/automation-coverage-map.md`
  with workflow, QA, formatting, security, supply-chain, unguarded-rule, and
  gap-disposition coverage.
- Task 4 validation confirmed full repository contracts have no Task 4,
  reference-stage, LLM Wiki, provider-surface, workflow-security, or
  script-contract failures. The full contract still fails only on known
  out-of-scope infra drift: Keycloak hardening image mismatch and
  `infra/tech-stack.versions.json` expected-image drift.
- Task 5 created `docs/90.references/audits/document-contracts/gap-register.md`
  with 30 consolidated gap rows and future implementation batches.
- No target corpus fixes were applied in this audit pack. The Task 5 changes
  are limited to the Stage 90 gap register, this Stage 04 task evidence, the
  generated LLM Wiki index when refreshed, and concise governance progress
  evidence if updated.

## Validation Results

| Command | Result |
| --- | --- |
| `test -e DESIGN.md && printf 'DESIGN.md present\n' \|\| printf 'DESIGN.md absent\n'` | PASS: `DESIGN.md absent`. |
| `rg -n 'direct-fix\|batch-fix\|historical-evidence\|out-of-scope-gap\|no-action' docs/90.references/audits/document-contracts` | PASS: approved dispositions found across the document-contract audit reports. |
| `rg -n 'sample row\|example row\|measured gap\|measured finding\|illustrative row' docs/90.references/audits/document-contracts/contract-governance-map.md docs/90.references/audits/document-contracts/template-application-gaps.md` | PASS: no matches. |
| `rg -n 'sample row\|example row\|measured gap\|measured finding\|illustrative row' docs/90.references/audits/document-contracts/gap-register.md` | PASS: no matches; `rg` exited 1 as expected for the negative check. |
| `rg -n 'WDC-GAP-[0-9]{3}' docs/90.references/audits/document-contracts/gap-register.md` | PASS: register IDs are present from `WDC-GAP-001` through `WDC-GAP-030`. |
| `git diff --check` | PASS (exit 0). |
| `git diff --cached --check` | PASS (exit 0, extra staged-diff hygiene check). |
| `bash scripts/knowledge/generate-llm-wiki-index.sh` | PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with 1123 paths after staging the new Task 5 gap register. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS: `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS: `failures=0`. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS: generated LLM Wiki index is fresh. |
| `bash -n scripts/validation/check-repo-contracts.sh` | PASS (exit 0). |
| `git ls-files '.github/workflows/*.yml' '.github/workflows/*.yaml'` | PASS: 6 tracked workflow files measured for Task 4. |
| `rg -n '^(name:\|on:\|permissions:\|jobs:)\|uses:\|pull-requests:\|contents:\|id-token:\|persist-credentials\|actions/checkout\|secrets\.' .github/workflows` | PASS: workflow evidence recorded in `automation-coverage-map.md`; all external `uses:` entries are full-SHA pinned, checkout credentials are not persisted, and token use is limited to built-in `GITHUB_TOKEN`. |
| `git ls-files 'scripts/**/*.sh' 'scripts/*.sh' \| rg '(validation\|operations\|knowledge\|quality\|test\|lint\|format\|security\|audit)'` | PASS: 15 validation, operations, knowledge, QA, and security script paths measured for Task 4. |
| `bash scripts/validation/check-repo-contracts.sh` | Expected FAIL: `failures=2`; no Task 5/reference/LLM/provider/workflow/script failures, only known out-of-scope infra drift from Keycloak hardening image mismatch and `infra/tech-stack.versions.json` expected-image drift. |

## Verification Summary

- Test Commands: Listed in `## Validation Results`.
- Eval Commands: N/A for documentation audit reports.
- Manual Checks: Confirm audit reports classify gaps without editing target
  documents and include the required Stage 90 reference headings.

## Commit Trail

- Pending.

## Related Documents

- Spec: `docs/03.specs/workspace-document-contract-audit-pack/spec.md`
- Plan: `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
- Audit bundle: `docs/90.references/audits/document-contracts/README.md`
