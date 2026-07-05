---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md -->

# Contract Governance Map

## Overview

This report maps where document contract rules currently live across root
shims, Stage 00 governance, Stage 99 template support, provider adapters,
GitHub workflow surfaces, and repository validators. It records ownership and
duplication risks without moving rules or editing the target corpus.

## Purpose

This reference preserves Task 3 governance comparison evidence for the
workspace document contract audit pack. It helps later remediation work decide
which owner should change before touching provider surfaces, templates,
validators, or target documents.

## Repository Role

This report supports Stage 04 task evidence and the final document-contract gap
register. It is not active policy, not a validator specification, and not a
replacement for `docs/00.agent-governance/` or `docs/99.templates/support/`.

## Scope

In scope: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, root `README.md`,
`docs/00.agent-governance/**`, `docs/99.templates/**`, `.agents/`,
`.claude/`, `.codex/`, `.github/`, and `scripts/**` as ownership evidence.

Out of scope: moving rules, editing provider adapters, changing validators,
normalizing target documents, reading secret values, or resolving existing
infra image/version drift.

## Definitions / Facts

- **Contract owner**: the canonical file or folder that should define a rule.
- **Adapter surface**: provider-specific runtime text or configuration that
  exposes a Stage 00 rule without becoming a separate policy source.
- **Validator surface**: script or workflow logic that enforces or reports a
  contract.
- **Rule duplication candidate**: repeated guidance that may be intentional
  routing today but should be reviewed before future policy changes.
- **Approved dispositions**: `direct-fix`, `batch-fix`,
  `historical-evidence`, `out-of-scope-gap`, and `no-action`.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| CG-001 | `rg -n 'docs/99\.templates/(readme\|service\|runbook\|incident\|postmortem\|plan\|task\|spec\|adr\|prd\|ard)\.template\|type:\|owner:\|updated:\|document_type:\|template_type:' AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs/00.agent-governance docs/99.templates` | 8 regex matches across 4 files; matches were OpenAPI schema `type:` fields, CI `scan-type`, and historical progress notes. | Checked active governance/provider surfaces for flat template paths and duplicate-purpose metadata terms. |
| CG-002 | `rg -n --pcre2 'docs/99\.templates/(?!templates/\|support/)\|Use templates from docs/99\.templates\|Read the matching template from docs/99\.templates\|load the mapped template from docs/99\.templates' ...` | 200 matches across 113 files; Task 3 classifies stale template application details in `template-application-gaps.md`. | Separated governance ownership from target-document application drift. |
| CG-003 | `rg -n 'frontmatter\|template\|README\|governance\|contract\|policy\|rule\|validation\|validator\|CI\|QA\|Formatting\|formatting\|SDLC' docs/00.agent-governance docs/99.templates AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | 5,830 matches across 177 files. | Identified rule owners and duplication candidates; report uses aggregated evidence instead of raw logs. |
| CG-004 | Targeted reads of `docs/00.agent-governance/README.md`, `rules/documentation-protocol.md`, provider notes, Stage 99 support docs, `scripts/operations/sync-provider-surfaces.sh`, `scripts/validation/check-repo-contracts.sh`, and `.github/workflows/ci-quality.yml`. | Confirmed current owner boundaries and validator coverage. | Anchored ownership rows to canonical source files. |

## Contract Owners

| Contract Area | Current Owner | Supporting Surfaces | Evidence | Disposition |
| --- | --- | --- | --- | --- |
| Root instruction routing | `AGENTS.md` plus root `CLAUDE.md` and `GEMINI.md` as thin shims | `docs/00.agent-governance/providers/*.md` | `AGENTS.md` delegates to bootstrap and says detailed Template Contract, QA/CI, and provider rules live in Stage 00; `CLAUDE.md` and `GEMINI.md` route to provider notes. | no-action |
| Agent governance SSoT | `docs/00.agent-governance/` | Root shims, provider overlays, runtime adapters | `docs/00.agent-governance/README.md` states that Stage 00 owns policy, provider overlays, agent catalog contracts, and validation expectations. | no-action |
| Stage and template mapping | `docs/00.agent-governance/rules/stage-authoring-matrix.md` and `docs/00.agent-governance/rules/documentation-protocol.md` | `docs/99.templates/support/template-selection.md` | Stage rows map target locations to canonical nested templates; documentation protocol lists document type to template mappings. | no-action |
| Template source and target-document rules | `docs/99.templates/support/template-contract.md` | `docs/99.templates/templates/**`, `docs/99.templates/README.md` | Template Contract separates copyable forms under `templates/` from support rules and says README files are indexes/routing surfaces. | no-action |
| Frontmatter key ownership | `docs/99.templates/support/frontmatter-contract.md` | `scripts/validation/check-repo-contracts.sh` | Frontmatter Contract disallows duplicate-purpose keys such as `type`, `owner`, `updated`, `document_type`, and `template_type` on template/support surfaces; repo contracts enforce Stage 99 template/frontmatter rules. | no-action |
| Template change governance | `docs/99.templates/support/template-governance.md` | Task evidence and repo-contract validators | Template Governance names support contracts, validators, Stage 00, and target documents as separate change surfaces. | no-action |
| Provider adapter parity | `docs/00.agent-governance/providers/agents-md.md`, `providers/claude.md`, `providers/codex.md`, `providers/gemini.md` | `.claude/`, `.codex/`, `.agents/`, `scripts/operations/sync-provider-surfaces.sh` | Provider-neutral notes state provider adapters may not redefine QA rules, Template Contract rules, Model Policy, or workflow policy; sync script regenerates Codex and Gemini adapter surfaces from Stage 00. | no-action |
| QA/CI and GitHub policy | `docs/00.agent-governance/rules/github-governance.md`, `scopes/qa.md`, `.github/workflows/ci-quality.yml` | `scripts/validation/check-repo-contracts.sh`, local validation scripts | GitHub governance defines required quality gates; `ci-quality.yml` runs docs traceability, implementation alignment, repo contracts, template/security, quickwin, pre-commit, frontend, coverage, and zizmor jobs. | no-action |
| Repository contract enforcement | `scripts/validation/check-repo-contracts.sh` | `.github/workflows/ci-quality.yml`, task verification commands | The validator enforces required template inventory, Stage 99 template/frontmatter rules, changed target-stage template gates, provider parity, reference-stage contracts, LLM Wiki freshness, script inventory, and infra drift checks. | no-action |
| LLM Wiki freshness | `scripts/knowledge/generate-llm-wiki-index.sh` | `docs/90.references/llm-wiki/llm-wiki-index.md` | Generator builds the tracked safe path index from `git ls-files` and excludes secret contents and generated dependency trees. | no-action |

## Potential Conflicts

| Conflict Candidate | Evidence | Assessment | Disposition |
| --- | --- | --- | --- |
| Broad `docs/99.templates/` references coexist with canonical nested template paths | `README.md` uses broad catalog links; `documentation-protocol.md` and `stage-authoring-matrix.md` map nested template paths. | No conflict when the broad reference points to the Stage 99 catalog or support surface. Concrete flat file paths are classified in `template-application-gaps.md`. | no-action |
| Gemini `.agents/` native rules/workflows can look like independent policy | `.agents/README.md` says `.agents/rules/` and `.agents/workflows/` are native Gemini surfaces; `providers/agents-md.md` says provider adapters must not redefine governance. | The current README states Stage 00 remains policy SSoT, but `.agents/rules/workspace.md` repeats model routing and artifact path guidance outside the sync script's generated set. | batch-fix |
| Runtime prompts restate template and README rules | `.claude/agents/doc-writer.md` embeds DOCS 3 task principles while also saying the imported scope is the policy SSoT. | The prompt is an adapter surface, not the owner. Repeated wording should be reviewed when Stage 00 template rules change. | batch-fix |
| Legacy `updated` frontmatter remains in active Stage 05 documents | Task 2 inventory found `updated:` in `docs/05.operations/guides/06-observability/loki.md`, `docs/05.operations/policies/06-observability/01.retention.md`, and `docs/05.operations/policies/06-observability/loki.md`. | Frontmatter Contract treats generic `updated` as duplicate-purpose metadata unless a profile explicitly consumes it. | batch-fix |
| Required job definitions are intentionally duplicated | `github-governance.md`, `.github/workflows/ci-quality.yml`, `.github/rulesets/main-protection.md`, and `check-repo-contracts.sh` must stay synchronized. | This is an intentional coupling constraint, not drift. | no-action |

## Rule Duplication Candidates

| Rule Family | Duplicate Surfaces | Why It Exists | Review Risk | Disposition |
| --- | --- | --- | --- | --- |
| Template-first authoring | `documentation-protocol.md`, `stage-authoring-matrix.md`, `scopes/docs.md`, `hookify.enforce-docs-templates.md`, provider notes, doc-writer and ops-runbook skills | Agents need the rule at bootstrap, scope, hook, and runtime-adapter layers. | Wording can drift when template paths change. | batch-fix |
| README sync and related documents | `documentation-protocol.md`, `scopes/docs.md`, `.claude/agents/doc-writer.md`, `check-repo-contracts.sh` | The rule is both authoring guidance and validation coverage. | Runtime prompts may preserve old wording after Stage 00 changes. | batch-fix |
| Model policy | `subagent-protocol.md`, provider notes, provider adapter files, `.agents/rules/workspace.md`, sync script | Model values must be visible to runtime adapters. | Non-generated `.agents/rules/workspace.md` can drift from Stage 00 and sync-script values. | batch-fix |
| QA/CI gate taxonomy | `github-governance.md`, root `README.md`, `.github/workflows/ci-quality.yml`, `check-repo-contracts.sh`, `.github/rulesets/main-protection.md` | CI jobs, local validators, and branch-protection docs must agree. | Missing synchronized edits can create false completion claims. | no-action |
| Stage 90 reference contract | `reference.template.md`, `check-repo-contracts.sh`, existing audit inventory reports | The template defines shape and the validator enforces required headings. | New reports can miss the reference-only role unless authors load the template. | no-action |

## Gaps For Register

| Gap ID | Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- | --- |
| GOV-001 | Review non-generated Gemini `.agents/rules` and `.agents/workflows` for drift from Stage 00 owner text. | `.agents/rules/workspace.md` repeats model routing and artifact path rules; `.agents/workflows/documentation.md` describes documentation generation workflow. | batch-fix | Add a provider-surface review batch; keep Stage 00 as owner and leave Gemini native files as adapters. |
| GOV-002 | Review runtime prompts that embed DOCS 3 and template rules. | `.claude/agents/doc-writer.md` and ops-runbook skills restate template, README, and section-profile rules. | batch-fix | Add to a future provider-adapter wording audit, not this target-corpus audit task. |
| GOV-003 | Resolve or explicitly profile the three active Stage 05 `updated` metadata keys. | `rg -n 'updated:'` finds three Stage 05 observability files with generic `updated` frontmatter. | batch-fix | Carry forward from Task 2 into the final gap register. |
| GOV-004 | Preserve broad Stage 99 catalog references that do not name removed flat template files. | Root README, Stage 00 governance, infra READMEs, provider notes, and support/template files use broad `docs/99.templates/` references. | no-action | Record as closure evidence; do not rewrite broad catalog references. |
| GOV-005 | Keep required CI job duplication synchronized. | Required jobs are listed in `github-governance.md`, `ci-quality.yml`, `.github/rulesets/main-protection.md`, and `check-repo-contracts.sh`. | no-action | Treat as a managed coupling constraint already enforced by repo contracts. |

## Sources

- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md) - Defines Task 3 scope and required verification.
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - Defines stage-level template ownership.
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - Defines template-first, language, frontmatter status, and DOCS 3 rules.
- [Template contract](../../../99.templates/support/template-contract.md) - Defines source-template and target-document boundaries.
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - Defines metadata key ownership.
- [Template governance](../../../99.templates/support/template-governance.md) - Defines change boundaries and validator ownership.
- [Template selection](../../../99.templates/support/template-selection.md) - Maps target paths to canonical templates.
- [Provider-neutral notes](../../../00.agent-governance/providers/agents-md.md) - Defines provider adapter parity.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - Defines local CI job execution.
- [Repository contract validator](../../../../scripts/validation/check-repo-contracts.sh) - Enforces repository contracts.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`.
- **Review Cadence**: Review when template contracts, provider adapters, or
  repository validators change.
- **Update Trigger**: Update when Task 4 automation coverage or Task 5 final
  gap register supersedes an ownership classification here.

## Related Documents

- [Document contract audit references](./README.md)
- [Template application gaps](./template-application-gaps.md)
- [Frontmatter inventory](./frontmatter-inventory.md)
- [Section profile inventory](./section-profile-inventory.md)
- [README profile inventory](./readme-profile-inventory.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
