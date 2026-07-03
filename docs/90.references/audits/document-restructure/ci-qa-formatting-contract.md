---
status: active
---

<!-- Target: docs/90.references/audits/document-restructure/ci-qa-formatting-contract.md -->

# Reference: CI, QA, and Formatting Contract

## Overview

This report maps current CI/CD, QA, formatting, and validation coverage before
the document restructure implementation batches. It records which checks are
hard gates today and which decisions need future approval.

## Purpose

The approved design requires the audit pack to separate current hard gates,
repo-local soft gates, manual review gates, and future hardening candidates.
This report provides that classification without editing workflows or scripts.

## Repository Role

This report supports `PLN-DRA-002` and the future `PLN-DRA-006` validator and
CI/QA decision batch. It is not active CI policy, not a workflow specification,
and not approval to mutate workflows, scripts, or pre-commit hooks.

## Scope

### In Scope

- Tracked GitHub workflows.
- Repo-local validation, operations, and knowledge scripts relevant to
  documentation contracts.
- LLM Wiki freshness, provider sync, traceability, implementation alignment,
  repo contracts, and Storybook-related gates.
- Formatting and security surfaces visible in tracked workflow/script files.

### Out of Scope

- Editing `.github/workflows/**`, `scripts/**`, or `.pre-commit-config.yaml`.
- Running networked dependency audit commands.
- Mutating remote GitHub branch protection.
- Runtime Compose validation outside a future approved infra batch.

## Definitions / Facts

- **Current hard gate**: a check enforced by current CI or repository contract.
- **Repo-local soft gate**: a local script that can provide evidence but may
  not be a remote required check.
- **Manual review gate**: a policy boundary that requires human approval rather
  than a script.
- **Future hardening candidate**: a potential gate that needs separate
  approval, threshold, and rollback design.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| DRA-CQA-001 | `git ls-files '.github/workflows/*' \| wc -l` | 6 tracked GitHub workflow files. | CI surface baseline. |
| DRA-CQA-002 | `git ls-files '.github/workflows/*'` | `ci-quality.yml`, `generate-changelog.yml`, `greetings.yml`, `pr-labeler.yml`, `stale.yml`, `tech-stack-version-sync.yml`. | Workflow inventory. |
| DRA-CQA-003 | `git ls-files scripts/validation/*.sh scripts/operations/*.sh scripts/knowledge/*.sh \| wc -l` | 15 relevant validation, operations, and knowledge scripts. | Local automation baseline. |
| DRA-CQA-004 | `rg -n 'check-doc-traceability\|check-doc-implementation-alignment\|check-repo-contracts\|sync-provider-surfaces\|generate-llm-wiki-index\|markdown\|lint\|format\|audit\|test\|build\|workflow\|actions/checkout\|permissions:' .github/workflows scripts/validation scripts/operations scripts/knowledge --glob '*.yml' --glob '*.yaml' --glob '*.sh'` | CI quality workflow and local scripts already cover doc traceability, implementation alignment, repo contracts, provider sync, LLM Wiki freshness, Storybook lint/build/test, workflow security, hardening, and advisory Graphify. | Coverage map. |
| DRA-CQA-005 | Reads of `ci-qa-parser-graphify-decision.md` and `gap-register.md` | Dependency-audit hard gates and Graphify hard gates remain future protected-surface decisions unless separately approved. | Prevents silent CI hardening. |

## Coverage Matrix

| Surface | Current Coverage | Gate Type | Future Decision |
| --- | --- | --- | --- |
| LLM Wiki path index | `generate-llm-wiki-index.sh --check`; repo contracts | Current hard/local gate | Keep required for path-changing batches. |
| Provider surfaces | `sync-provider-surfaces.sh --check`; repo contracts | Current hard/local gate | Run after provider-adjacent edits. |
| Docs traceability | `check-doc-traceability.sh`; `ci-quality.yml` | Current hard gate | Keep required. |
| Docs implementation alignment | `check-doc-implementation-alignment.sh`; `ci-quality.yml` | Current hard gate and local evidence | Keep required; remote branch-protection enforcement is documented separately. |
| Repository contracts | `check-repo-contracts.sh`; `ci-quality.yml` | Current hard gate | Keep required. |
| Storybook lint/build/test | `ci-quality.yml`; `check-storybook-contract.sh` | Current hard gate | Out of scope unless web/project files change. |
| Formatting | `git diff --check`; workflow and pre-commit policy surfaces | Current local evidence | Use for every batch. |
| Workflow security | repo contracts inspect permissions, duplicate jobs/steps, pinned checkout, and required workflow shape | Current hard gate | Workflow mutation requires explicit approval. |
| Dependency audit | Dependabot and existing QA coverage; no active `npm audit` / `pip audit` hard gate from prior decision | Future hardening candidate | Requires Security/QA approval. |
| Graphify | `graphify update` instruction after code edits; `report-graphify-health.sh` advisory | Manual/advisory gate | Hard gate deferred until stable. |

## Findings

| ID | Surface | Finding | Disposition | Recommended Batch |
| --- | --- | --- | --- | --- |
| DRA-CQA-001 | `.github/workflows/**` | Current workflow surface is protected and already checked by repository contracts. | `active-canonical` | No workflow edit in audit pack. |
| DRA-CQA-002 | Scripts | Current scripts provide required documentation evidence gates. | `active-canonical` | Run in every batch. |
| DRA-CQA-003 | Dependency audit | Hard `npm audit` / `pip audit` gates are not active and require separate Security/QA approval. | `evidence-preserve` / future hardening | `PLN-DRA-006` only if approved. |
| DRA-CQA-004 | Graphify | Graphify remains advisory and should not block document restructure batches by default. | `evidence-preserve` | No hard gate without separate approval. |
| DRA-CQA-005 | Formatting | `git diff --check` remains the minimum formatting gate for document-only batches. | `active-canonical` | Use in every commit. |

## Source Rules

- Use current tracked workflow and script files for automation truth.
- Do not add CI hard gates from an audit report alone.
- Record manual approvals for workflow, validator, dependency audit, and
  Graphify hardening decisions.
- Do not run networked dependency audit commands during documentation-only
  audit pack work.

## Sources

- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - Defines current remote QA jobs.
- [Local QA gate runner](../../../../scripts/validation/run-local-qa-gates.sh) - Lists local and remote-only gate responsibilities.
- [Repository contract validator](../../../../scripts/validation/check-repo-contracts.sh) - Enforces documentation, workflow, LLM Wiki, and hardening contracts.
- [Document implementation alignment checker](../../../../scripts/validation/check-doc-implementation-alignment.sh) - Checks active docs against tracked implementation surfaces.
- [Provider sync script](../../../../scripts/operations/sync-provider-surfaces.sh) - Checks provider mirror drift.
- [LLM Wiki generator](../../../../scripts/knowledge/generate-llm-wiki-index.sh) - Generates and checks tracked path index.
- [CI, QA, parser, and Graphify decision](../document-contracts/ci-qa-parser-graphify-decision.md) - Supplies prior protected-surface decisions.

## Maintenance

- **Owner**: QA Engineer / Documentation Specialist / Security Auditor.
- **Review Cadence**: Review before `PLN-DRA-006` or any workflow, validator,
  dependency audit, or Graphify hard-gate change.
- **Update Trigger**: Update when CI jobs, local QA scripts, required checks,
  dependency audit policy, or Graphify posture changes.

## Related Documents

- [Document restructure audit references](./README.md)
- [Restructure gap register](./restructure-gap-register.md)
- [Document restructure implementation plan](../../../04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md)
