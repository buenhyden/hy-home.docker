---
status: active
---

<!-- Target: docs/90.references/audits/document-contracts/gap-register.md -->

# Gap Register

## Overview

This register consolidates the approved document-contract audit findings from
the Task 2 through Task 4 reports. It assigns stable `WDC-GAP-*` identifiers,
groups each row by disposition, and proposes later implementation batches
without applying target corpus fixes.

## Purpose

This reference gives future remediation plans one source for document-contract
gaps, closure evidence, historical evidence, and out-of-scope follow-up items.
It exists so later implementation work can start from approved dispositions
instead of rediscovering the audit reports.

## Repository Role

This report supports Stage 04 task evidence for the workspace document contract
audit pack and later implementation planning. It is not active policy, not a
template contract, not a validator specification, and not approval to edit
provider adapters, workflows, validators, runtime config, secret material, or
the target document corpus.

## Scope

### In Scope

- Gap candidates and closure evidence from the document-contract audit reports.
- Approved dispositions: `direct-fix`, `batch-fix`,
  `historical-evidence`, `out-of-scope-gap`, and `no-action`.
- Future remediation batch boundaries, approval needs, validation commands, and
  commit-boundary guidance.
- Evidence links to source reports, commands, and repo-relative paths.

### Out of Scope

- Applying any target corpus fixes during this audit pack.
- Reading or printing secret values, credentials, tokens, certificates,
  private keys, raw logs, shell history, or `.env` values.
- Editing workflows, scripts, validators, provider adapters, runtime config, or
  remote GitHub settings.
- Resolving existing infra image/version drift.
- Rewriting historical execution evidence for style-only reasons.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| GR-001 | `rg -n 'direct-fix\|batch-fix\|historical-evidence\|out-of-scope-gap\|no-action' docs/90.references/audits/document-contracts` | Classified rows were present across the Task 2 inventory reports, Task 3 governance/template reports, and Task 4 automation report. | Confirmed every register candidate has one approved disposition. |
| GR-002 | Targeted reads of every report under `docs/90.references/audits/document-contracts/` | Source rows were deduplicated where later reports repeated the same finding. | Built stable `WDC-GAP-*` rows without changing source reports. |
| GR-003 | Reads of the workspace document contract spec, plan, task evidence, and Stage 90 reference template | Confirmed audit-only boundaries and required reference headings. | Kept this report within the Stage 90 reference contract. |

## Definitions / Facts

- **Direct fix**: A small active guidance or active contract drift with clear
  validation that can be remediated directly in a later approved task.
- **Batch fix**: A corpus or protected-surface change that needs a bounded
  remediation plan, explicit approval, and logical commits.
- **Historical evidence**: Completed specs, plans, tasks, progress notes, or
  archive records that preserve prior truth and should not be rewritten for
  style alone.
- **Out-of-scope gap**: Runtime, infra, secret, remote, parser/tooling, or
  uncertain drift recorded for a separate approved follow-up.
- **No action**: Valid broad reference, intentional template-time instruction,
  generated artifact, managed coupling, or closure evidence.

## Gap Summary

| Disposition | Count | Summary |
| --- | ---: | --- |
| `direct-fix` | 0 | No source report approved a direct fix for this audit pack. |
| `batch-fix` | 11 | Provider/governance wording, README profiles, frontmatter, section naming, dependency-audit coverage, and Graphify enforcement need later scoped batches. |
| `historical-evidence` | 4 | Baselines, archive evidence, and old template-path records should be preserved unless future work proves active consumption. |
| `out-of-scope-gap` | 7 | Examples, parser/tooling limitations, remote branch-protection evidence, Stage 05 metadata decisions, and infra drift need separate approval. |
| `no-action` | 8 | Valid broad references, intentional profiles, managed CI coupling, provider sync coverage, and manual secret-generation boundaries need no remediation. |
| **Total** | **30** | Consolidated register rows from the approved audit reports. |

## Direct-Fix Candidates

| ID | Surface | Gap | Evidence | Disposition | Next Action |
| --- | --- | --- | --- | --- | --- |

No direct-fix candidates were approved in the source reports.

## Batch-Fix Candidates

| ID | Surface | Gap | Evidence | Disposition | Next Action |
| --- | --- | --- | --- | --- | --- |
| WDC-GAP-001 | `.agents/rules/workspace.md`; `.agents/workflows/documentation.md` | Non-generated Gemini adapter rules and workflows repeat Stage 00 owner text and can drift. | `docs/90.references/audits/document-contracts/contract-governance-map.md:99` | `batch-fix` | Include in the active governance and provider drift batch; keep Stage 00 as owner and treat Gemini files as adapters. |
| WDC-GAP-002 | `.claude/agents/doc-writer.md`; `.claude/skills/ops-runbook-agent/skill.md` | Runtime prompts restate DOCS 3, template, README, and section-profile rules that may drift from Stage 00. | `docs/90.references/audits/document-contracts/contract-governance-map.md:100` | `batch-fix` | Review runtime wording in a provider-adapter audit before changing prompt text. |
| WDC-GAP-003 | `projects/README.md`; `projects/storybook/README.md`; `projects/storybook/nextjs/README.md` | Project README surfaces use related-reference profile wording and removed flat README template paths. | `docs/90.references/audits/document-contracts/readme-profile-inventory.md:73`; `docs/90.references/audits/document-contracts/template-application-gaps.md:103` | `batch-fix` | Closed locally in T-003 for the listed project README surfaces. Keep future project READMEs on the canonical common README template path. |
| WDC-GAP-004 | `secrets/README.md` | Secret-handling README uses related-reference profile wording and a removed flat README template path. | `docs/90.references/audits/document-contracts/readme-profile-inventory.md:73`; `docs/90.references/audits/document-contracts/template-application-gaps.md:104` | `batch-fix` | Closed locally in T-003 with a metadata-only secret README edit; do not inspect secret values in future audits. |
| WDC-GAP-005 | `tests/README.md` | Tests README uses a related-reference profile instead of the counted related-documents profile. | `docs/90.references/audits/document-contracts/readme-profile-inventory.md:73`; `docs/90.references/audits/document-contracts/section-profile-inventory.md:165` | `batch-fix` | Closed locally in T-003 by aligning the tests README section profile. |
| WDC-GAP-006 | `*.md` tracked Markdown surfaces | 185 tracked Markdown files lack top frontmatter and need profile-specific routing before any corpus edit. | `docs/90.references/audits/document-contracts/frontmatter-inventory.md:128` | `batch-fix` | Create a profile-routing plan before adding or declining frontmatter by surface. |
| WDC-GAP-007 | `docs/05.operations/guides/06-observability/loki.md`; `docs/05.operations/policies/06-observability/01.retention.md`; `docs/05.operations/policies/06-observability/loki.md` | Three active Stage 05 observability documents still use generic `updated` frontmatter. | `docs/90.references/audits/document-contracts/frontmatter-inventory.md:129`; `docs/90.references/audits/document-contracts/contract-governance-map.md:101` | `batch-fix` | Closed locally in the T-004 operations metadata sub-batch; keep active operations frontmatter lifecycle-only unless a future profile explicitly consumes more keys. |
| WDC-GAP-008 | `docs/01.requirements/**/*.md` | Requirement agent section naming is split between two forms. | `docs/90.references/audits/document-contracts/section-profile-inventory.md:174` | `batch-fix` | Closed locally in the T-004 requirements heading sub-batch by aligning active PRD headings with the PRD template spelling. |
| WDC-GAP-009 | `infra/**/*.md` | Infra validation terminology is split between `Validation` and `Validation Commands`. | `docs/90.references/audits/document-contracts/section-profile-inventory.md:176` | `batch-fix` | Defer to an infra README profile decision before any heading edits. |
| WDC-GAP-010 | `.github/workflows/ci-quality.yml`; `scripts/validation/run-local-qa-gates.sh` | Explicit `npm audit` and `pip audit` commands are not active CI or local gates. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:169` | `batch-fix` | Decide in a future security/QA batch whether to add audit gates or document current Dependabot-based coverage. |
| WDC-GAP-011 | `AGENTS.md`; `scripts/knowledge/report-graphify-health.sh` | Graphify refresh is instruction-based and report-only, not enforced as a freshness gate. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:170` | `batch-fix` | Decide later whether Graphify remains advisory or becomes a hard freshness check. |

## Remediation Updates

| Date | Rows | Status | Evidence | Residual Action |
| --- | --- | --- | --- | --- |
| 2026-07-03 | WDC-GAP-001, WDC-GAP-002 | Local adapter drift remediated | `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` T-002; `GEMINI.md`; `.agents/rules/workspace.md`; `.agents/workflows/documentation.md`; `.claude/agents/doc-writer.md`; `.claude/skills/ops-runbook-agent/skill.md`; `.codex/skills/ops-runbook-agent/skill.md` | Keep future provider edits aligned with Stage 00 owners and `sync-provider-surfaces.sh`. |
| 2026-07-03 | WDC-GAP-022 | Deferred | Remote GitHub state was not reverified in T-002 because no remote GitHub audit approval was part of this local adapter batch. | Re-verify only in a future approved remote GitHub governance audit. |
| 2026-07-03 | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-019 | Local README profile drift remediated | `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` T-003; `projects/README.md`; `projects/storybook/README.md`; `projects/storybook/nextjs/README.md`; `secrets/README.md`; `tests/README.md` | WDC-GAP-017 remains deferred for a future examples/scaffold contract decision. |
| 2026-07-03 | WDC-GAP-007, WDC-GAP-016 | Local operations metadata drift remediated | `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` T-004; `docs/05.operations/guides/06-observability/loki.md`; `docs/05.operations/policies/06-observability/01.retention.md`; `docs/05.operations/policies/06-observability/loki.md`; `docs/05.operations/policies/00-workspace/harness-agent-first-engineering.md` | WDC-GAP-006 and WDC-GAP-009 remain separate target-stage profile sub-batches after the PRD heading cleanup. |
| 2026-07-03 | WDC-GAP-008 | Local PRD heading drift remediated | `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` T-004; `docs/01.requirements/2026-03-26-01-gateway.md`; `docs/01.requirements/2026-03-26-02-auth.md`; `docs/01.requirements/2026-03-26-06-observability.md`; `docs/01.requirements/2026-03-26-07-workflow.md` | WDC-GAP-006 and WDC-GAP-009 remain separate target-stage profile sub-batches. |

## Historical Evidence

| ID | Surface | Gap | Evidence | Disposition | Next Action |
| --- | --- | --- | --- | --- | --- |
| WDC-GAP-012 | `docs/90.references/audits/document-contracts/frontmatter-inventory.md`; `docs/90.references/audits/document-contracts/readme-profile-inventory.md` | Tracked README and README score baselines are audit evidence, not remediation targets. | `docs/90.references/audits/document-contracts/frontmatter-inventory.md:115`; `docs/90.references/audits/document-contracts/readme-profile-inventory.md:58`; `docs/90.references/audits/document-contracts/readme-profile-inventory.md:60` | `historical-evidence` | Preserve as Task 2 baseline evidence; refresh only through a new inventory run. |
| WDC-GAP-013 | `docs/01.requirements/**/*.md` | Requirement section-profile counts record the current PRD baseline. | `docs/90.references/audits/document-contracts/section-profile-inventory.md:153` | `historical-evidence` | Use as comparison evidence for WDC-GAP-008; do not rewrite completed requirements for style alone. |
| WDC-GAP-014 | `docs/98.archive/**/*.md`; `archive/Windows-Network-IP.md` | Archive and legacy archive-heading records preserve historical structure. | `docs/90.references/audits/document-contracts/section-profile-inventory.md:159`; `docs/90.references/audits/document-contracts/section-profile-inventory.md:167` | `historical-evidence` | Preserve unless a future archive/tombstone task proves active references need cleanup. |
| WDC-GAP-015 | `docs/03.specs/**`; `docs/04.execution/**`; `docs/00.agent-governance/memory/progress.md` | Older specs, plans, tasks, and progress entries preserve old template-path evidence. | `docs/90.references/audits/document-contracts/template-application-gaps.md:86`; `docs/90.references/audits/document-contracts/template-application-gaps.md:87`; `docs/90.references/audits/document-contracts/template-application-gaps.md:88`; `docs/90.references/audits/document-contracts/template-application-gaps.md:89`; `docs/90.references/audits/document-contracts/template-application-gaps.md:106` | `historical-evidence` | Keep unless a future task proves an entry is active guidance consumed today. |

## Out-of-Scope Gaps

| ID | Surface | Gap | Evidence | Disposition | Next Action |
| --- | --- | --- | --- | --- | --- |
| WDC-GAP-016 | `docs/05.operations/**/06-observability/*.md`; `docs/05.operations/policies/00-workspace/harness-agent-first-engineering.md` | Non-standard Stage 05 operational metadata needs a profile decision before cleanup. | `docs/90.references/audits/document-contracts/frontmatter-inventory.md:130` | `out-of-scope-gap` | Closed locally in the T-004 operations metadata sub-batch by keeping active Stage 05 frontmatter lifecycle-only. |
| WDC-GAP-017 | `examples/sample-web-service/README.md`; `examples/sample-web-service/service.md` | Example scaffold profile and flat service-template path need an examples-surface contract decision. | `docs/90.references/audits/document-contracts/readme-profile-inventory.md:74`; `docs/90.references/audits/document-contracts/template-application-gaps.md:105` | `out-of-scope-gap` | Defer until examples and scaffold contracts are explicitly in scope. |
| WDC-GAP-018 | `.github/PULL_REQUEST_TEMPLATE.md`; `scripts/README.md`; `secrets/README.md` | Line-based heading scan surfaces fenced or comment-like H1 entries. | `docs/90.references/audits/document-contracts/section-profile-inventory.md:175` | `out-of-scope-gap` | Treat as parser/tooling follow-up, not a content fix. |
| WDC-GAP-019 | `projects/README.md` | Matched project README context still contains a removed operations-stage path literal unrelated to template paths. | `docs/90.references/audits/document-contracts/template-application-gaps.md:96` | `out-of-scope-gap` | Closed locally in T-003 after project README scope approval; no further action for this literal. |
| WDC-GAP-020 | `infra/02-auth/keycloak/**`; `scripts/hardening/check-all-hardening.sh` | Full repo contract currently fails on known Keycloak hardening image drift. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:166` | `out-of-scope-gap` | Carry to a separate infra drift remediation task; do not patch in document-contract audit work. |
| WDC-GAP-021 | `infra/tech-stack.versions.json` | Curated tech-stack image registry is out of sync with Compose declarations. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:167` | `out-of-scope-gap` | Carry to the infra version drift remediation task. |
| WDC-GAP-022 | `.github/rulesets/main-protection.md` | Remote branch-protection evidence is historical and was not reverified in Task 4. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:168` | `out-of-scope-gap` | Re-verify only in a future approved remote GitHub governance audit. |

## No-Action Items

| ID | Surface | Gap | Evidence | Disposition | Next Action |
| --- | --- | --- | --- | --- | --- |
| WDC-GAP-023 | Full tracked Markdown corpus | Previously problematic duplicate-purpose keys are absent. | `docs/90.references/audits/document-contracts/frontmatter-inventory.md:131` | `no-action` | Keep as closure evidence in future audits. |
| WDC-GAP-024 | `.codex/README.md`; `.agents/README.md` | Provider README profiles are intentionally thinner than folder README profiles. | `docs/90.references/audits/document-contracts/readme-profile-inventory.md:75` | `no-action` | Leave unchanged unless a provider contract comparison changes the profile. |
| WDC-GAP-025 | `docs/99.templates/templates/**/README.md` | Template category READMEs use template-source headings. | `docs/90.references/audits/document-contracts/readme-profile-inventory.md:76` | `no-action` | Preserve as template-source profile evidence. |
| WDC-GAP-026 | `docs/05.operations/**/*.md` | Nested operations `Overview` and `Purpose` headings are expected profile evidence. | `docs/90.references/audits/document-contracts/section-profile-inventory.md:177` | `no-action` | Leave unchanged unless a later operations contract comparison proves drift. |
| WDC-GAP-027 | `README.md`; `docs/00.agent-governance/**`; `.agents/**`; `.claude/**`; `.codex/**`; `infra/**`; `docs/90.references/llm-wiki/llm-wiki-index.md`; `scripts/validation/check-repo-contracts.sh` | Broad Stage 99 catalog references and generated or validator-owned references are valid when they do not name removed flat template files. | `docs/90.references/audits/document-contracts/template-application-gaps.md:75`; `docs/90.references/audits/document-contracts/template-application-gaps.md:76`; `docs/90.references/audits/document-contracts/template-application-gaps.md:77`; `docs/90.references/audits/document-contracts/template-application-gaps.md:78`; `docs/90.references/audits/document-contracts/template-application-gaps.md:79`; `docs/90.references/audits/document-contracts/template-application-gaps.md:80`; `docs/90.references/audits/document-contracts/contract-governance-map.md:102` | `no-action` | Do not rewrite broad catalog references. |
| WDC-GAP-028 | `docs/00.agent-governance/rules/github-governance.md`; `.github/workflows/ci-quality.yml`; `.github/rulesets/main-protection.md`; `scripts/validation/check-repo-contracts.sh` | Required CI job definitions are intentionally duplicated and managed as a coupling constraint. | `docs/90.references/audits/document-contracts/contract-governance-map.md:103` | `no-action` | Keep synchronized when job IDs change; no current edit. |
| WDC-GAP-029 | `scripts/operations/sync-provider-surfaces.sh`; `scripts/validation/check-repo-contracts.sh` | Provider sync direct command is local-only but covered indirectly by repo contracts. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:171` | `no-action` | Keep current coverage unless provider drift recurs. |
| WDC-GAP-030 | `scripts/operations/gen-secrets.sh` | Secret generation remains manual by design, with safe metadata-only modes. | `docs/90.references/audits/document-contracts/automation-coverage-map.md:172` | `no-action` | Preserve the manual redaction boundary; never run value-reading mode for audits. |

## Future Implementation Batches

| Batch | Affected Surfaces | Required Approvals | Validation Commands | Commit Boundary Guidance |
| --- | --- | --- | --- | --- |
| 1. Active governance and provider drift fixes | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022; `.agents/**`, `.claude/**`, `.codex/**`, `docs/00.agent-governance/**`, `.github/rulesets/main-protection.md` | Stage 04 task approval for provider/runtime-adapter text; explicit remote GitHub read approval before branch-protection verification; no provider runtime config changes without separate approval. | `git diff --check`; `bash scripts/operations/sync-provider-surfaces.sh --check`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/validation/check-repo-contracts.sh`; remote `gh` checks only after approval. | Keep provider wording, Stage 00 owner text, and remote-evidence updates in separate commits unless one change requires synchronized edits. |
| 2. README profile normalization by surface | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019; `projects/**/README.md`, `secrets/README.md`, `tests/README.md`, `examples/sample-web-service/**` | Per-surface README approval; redaction boundary for `secrets/README.md`; examples/scaffold contract approval before touching `examples/**`. | `rg -n 'docs/99\.templates/(readme\|service)\.template' projects secrets tests examples`; `git diff --check`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/validation/check-repo-contracts.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check`. | Split commits by surface group: projects, secrets/tests, and examples. Do not combine secret-handling docs with unrelated README rewrites. |
| 3. Target-stage frontmatter and section normalization | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016; `docs/01.requirements/**`, `docs/05.operations/**`, `infra/**/*.md`, other tracked Markdown profiles | Stage-specific document approval; operations metadata decision for `updated`, `component`, `runtime_state`, `tier`, and `policy_state`; infra README profile decision. | Re-run the frontmatter and section inventory commands from the source reports; `rg -n '^updated:' docs/05.operations`; `git diff --check`; `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/validation/check-repo-contracts.sh`. | Commit by profile or stage, not by a repository-wide formatting sweep. Keep historical evidence untouched unless explicitly reclassified. |
| 4. CI/CD and QA validator enhancement | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018; `.github/workflows/**`, `scripts/validation/**`, `scripts/knowledge/**`, `.pre-commit-config.yaml` | Explicit approval for workflow, script, validator, and pre-commit changes; security/QA owner approval for dependency-audit gates; tooling decision before hardening Graphify. | `bash -n scripts/validation/check-repo-contracts.sh`; `bash scripts/validation/run-local-qa-gates.sh --list`; `git diff --check`; `bash scripts/validation/check-repo-contracts.sh`; workflow lint/security checks already wired through repo contracts. | Keep dependency-audit decisions, Graphify enforcement, and parser improvements in separate commits with rollback notes. |
| 5. Historical evidence archive or tombstone cleanup | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015; `docs/03.specs/**`, `docs/04.execution/**`, `docs/98.archive/**`, `archive/**`, `docs/00.agent-governance/memory/progress.md` | Approval required only if a future task proves historical evidence is still active guidance or needs tombstone migration. | `git diff --check`; `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check`; `bash scripts/validation/check-repo-contracts.sh`. | Preserve historical meaning. Use archive/tombstone commits only when active links or current guidance require cleanup. |
| 6. Out-of-scope infra drift follow-up | WDC-GAP-020, WDC-GAP-021; `infra/02-auth/keycloak/**`, `infra/tech-stack.versions.json`, Compose declarations, hardening scripts | Infra owner approval and a separate Stage 04 task; Docker Compose/runtime change approval if any declaration changes. | `bash scripts/operations/sync-tech-stack-versions.sh --check`; `bash scripts/hardening/check-all-hardening.sh`; `bash scripts/validation/check-repo-contracts.sh`; `bash scripts/validation/validate-docker-compose.sh` if Compose changes are approved. | Keep infra image/version drift in an infra-only commit or series; do not mix with document-contract register edits. |

## Source Rules

- Prefer source audit reports over memory notes when classifying current gaps.
- Preserve report dispositions unless a later approved task explicitly
  reclassifies a row with new evidence.
- Summarize validation output and command evidence; do not paste raw huge logs.
- Treat remote GitHub state as current only when freshly verified through an
  approved remote audit.
- Treat `secrets/README.md` as policy context only; do not inspect secret
  values for this register.

## Sources

- [Frontmatter inventory](./frontmatter-inventory.md) - Supplies frontmatter, duplicate-purpose key, and metadata gap candidates.
- [Section profile inventory](./section-profile-inventory.md) - Supplies section naming, parser limitation, and profile evidence.
- [README profile inventory](./readme-profile-inventory.md) - Supplies README surface profile candidates and closure evidence.
- [Contract governance map](./contract-governance-map.md) - Supplies governance, provider, rule-duplication, and no-action ownership rows.
- [Template application gaps](./template-application-gaps.md) - Supplies stale template-path, historical, broad-reference, and out-of-scope classifications.
- [Automation coverage map](./automation-coverage-map.md) - Supplies CI/CD, QA, security, supply-chain, remote, Graphify, provider-sync, and infra-drift rows.
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md) - Records execution evidence for this audit pack.
- [Workspace document contract audit pack plan](../../../04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md) - Defines Task 5 and future batch requirements.
- [Workspace document contract audit pack spec](../../../03.specs/workspace-document-contract-audit-pack/spec.md) - Defines the audit-only contract and approved dispositions.
- [Reference template](../../../99.templates/templates/common/reference.template.md) - Defines the Stage 90 reference report contract.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`, with QA Engineer,
  Security Auditor, Infra/DevOps Engineer, and provider-surface reviewers for
  their respective future batches.
- **Review Cadence**: Review before any document-contract remediation plan uses
  these rows, and after any batch changes a listed surface.
- **Update Trigger**: Update when a gap is fixed, reclassified, superseded by a
  new audit report, or split into a more specific approved implementation task.

## Related Documents

- [Document contract audit references](./README.md)
- [Frontmatter inventory](./frontmatter-inventory.md)
- [Section profile inventory](./section-profile-inventory.md)
- [README profile inventory](./readme-profile-inventory.md)
- [Contract governance map](./contract-governance-map.md)
- [Template application gaps](./template-application-gaps.md)
- [Automation coverage map](./automation-coverage-map.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
