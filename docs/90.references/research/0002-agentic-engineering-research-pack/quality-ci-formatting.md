---
status: active
artifact_id: reference:agentic-engineering-research:quality-ci-formatting
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Quality CI and Formatting

## Overview

Quality controls answer different questions. Formatting, linting, syntax,
typing, testing, coverage, security checks, and review must retain their own
oracles and limits rather than being collapsed into a single green-CI claim.

## Purpose

Map the entry-HEAD quality definitions to appropriate adoption and evidence
mechanics, including the capabilities that are configured but not executed by
this documentation unit.

## Scope

This leaf covers tracked pre-commit hooks, CI job declarations, validation
tests, and the Storybook package scripts. It excludes running hooks, hosted CI,
full test discovery, production behavior, and any claim of release acceptance.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `QCF-001` | The tracked pre-commit configuration declares basic file checks, Markdown/YAML/shell/workflow linting, secret scanning, and selected local hooks; hooks have file and stage filters. | tracked configuration | VERIFIED | `.pre-commit-config.yaml` at `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | Identify the hook and stage before relying on it; an installed configuration is not a run. |
| `QCF-002` | The Storybook Next.js package declares lint, typecheck, test, coverage, build, and Storybook-build scripts, while CI declares separate frontend-quality and coverage jobs. | tracked configuration | VERIFIED | `projects/storybook/nextjs/package.json`, `.github/workflows/ci-quality.yml` at entry HEAD | Keep lint/type/build/test/coverage evidence distinct and scoped to that project. |
| `QCF-003` | Retained Prettier/pre-commit, TypeScript/ESLint, and Vitest/Storybook documentation distinguishes formatter/hook behavior, static lint/type checks, coverage, and browser/component testing. | retained official observation | HISTORICAL VERIFIED | retained Task 0001 delivery ledger | A tool's capability does not prove that this workspace ran it, covered the intended risk, or validated user value. |

### QA taxonomy and adoption mechanics

Formatting answers whether a tool can normalize layout; linting applies
domain-specific static rules; syntax checks parser acceptance; type checking
checks declared type relationships. Unit/regression tests exercise controlled
oracles, integration/component tests exercise bounded interactions, and system
or end-to-end evidence needs a representative journey. Coverage measures what
one configured run exercised, not requirement completeness or test quality.
Security checks cover their named class; independent review assesses the
adequacy of evidence and is not replaceable by a command exit code.

For a change, first identify the artifact and applicable owner, then select the
smallest matching check, record the immutable revision and raw outcome, and
escalate gaps to the owning specification or Task. The repository has no shared
Python formatter/linter/type-checker declaration and no standalone end-to-end
journey suite in these measured controls; do not relabel a missing capability
as a passing alternative. Prettier configuration without a tracked invocation
is configuration, not formatting enforcement.

| Control | Declared mechanics | Exact local investigation target | Verification limit |
| --- | --- | --- | --- |
| Formatting | File-normalization hooks and `.editorconfig` guide layout; Prettier has configuration but no tracked shared invocation. | `.pre-commit-config.yaml`, `.editorconfig`, `.prettierrc.json` | Formatting does not assess prose, correctness, or execution. |
| Linting | Markdown, YAML, shell, action, secret, and project ESLint checks target selected file classes. | `.pre-commit-config.yaml`, `projects/storybook/nextjs/package.json` | Lint does not prove parser completeness, behavior, or acceptance. |
| Syntax | JSON/TOML hooks and workflow/static validators parse bounded formats. | `.pre-commit-config.yaml`, `scripts/validation/github_workflow_contract.py` | Parse success does not prove consumer or hosted semantics. |
| Type checking | `tsc --noEmit` is declared for the Storybook Next.js project. | `projects/storybook/nextjs/package.json`, `tsconfig.json` | It does not cover Python, shell, Compose, or runtime behavior. |
| Unit / regression | Validation tests and typed gates contain controlled oracles for selected contracts. | `tests/validation/`, `scripts/validation/ci_gate_runner.py` | File inventory does not prove full discovery or an executed suite. |
| Integration / component | Storybook Vitest scripts cover configured browser/component work. | `projects/storybook/nextjs/package.json`, `vitest.config.ts` | Component evidence is not a product end-to-end journey. |
| System / end-to-end | No standalone journey suite is declared in the measured configuration. | `tests/`, `projects/storybook/nextjs/` | Do not substitute Storybook tests for system validation. |
| Security | Gitleaks, Hadolint, dependency, Compose, hardening, and Zizmor routes cover named classes. | `.pre-commit-config.yaml`, `ci-quality.yml` | A scanner/configuration is not a clean security certification. |
| Independent review | Task review records require evidence-range review after author checks. | `tasks/tsk-0004-canonical-research-refresh.md` | Review does not replace an unexecuted oracle or acceptance authority. |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `QCF-SRC-001` | `QCF-001` | Pre-commit configuration / workspace | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | tracked configuration | `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | 2026-08-28 | Hooks can be filtered, skipped, or unexecuted. |
| `QCF-SRC-002` | `QCF-002` | Frontend scripts and CI definition / workspace | [package scripts](../../../../projects/storybook/nextjs/package.json), [CI workflow](../../../../.github/workflows/ci-quality.yml) | tracked configuration | `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | 2026-08-28 | Declarations do not establish installed dependencies, execution, or hosted success. |
| `QCF-SRC-003` | `QCF-003` | Formatter and hook documentation / Prettier, pre-commit | [Prettier CLI](https://prettier.io/docs/cli), [pre-commit](https://pre-commit.com/) | retained official observation | Task 0001 dated delivery ledger | 2026-08-08T17:45:01+09:00 | Retained formatter/hook observation; no new external request was made. |
| `QCF-SRC-004` | `QCF-003` | Type and lint documentation / TypeScript, ESLint | [TypeScript noEmit](https://www.typescriptlang.org/tsconfig/noEmit.html), [ESLint getting started](https://eslint.org/docs/latest/use/getting-started) | retained official observation | Task 0001 dated delivery ledger | 2026-08-08T17:45:01+09:00 | Retained static-analysis observation; local execution is not inferred. |
| `QCF-SRC-005` | `QCF-003` | Coverage and browser-component documentation / Vitest, Storybook | [Vitest coverage](https://vitest.dev/guide/coverage.html), [Storybook Vitest addon](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon) | retained official observation | Task 0001 dated delivery ledger | 2026-08-08T17:45:01+09:00 | Retained capability observation; it is not end-to-end or production evidence. |

## Maintenance

Remeasure hook inventory, filters, package scripts, test configuration, and CI
jobs whenever their owners change. Revalidate a quality conclusion when its
oracle, inputs, tool version, environment, or acceptance criterion changes.
Keep configuration, execution, review, hosted result, enforcement, and runtime
evidence in separate records.

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Give generated changes an explicit artifact-specific QA route. | Inspect selected gate and Task evidence. | A generic green claim is insufficient. |
| architecture | applies | Review quality attributes and contract changes with their owner. | Inspect traceability and design evidence. | Static checks do not validate architecture fitness. |
| common | applies | Keep shared hooks and conventions narrowly scoped. | Inspect hook filters and stage declarations. | Filtered hooks may not cover a file. |
| docs | applies | Run metadata/link checks appropriate to documentation changes. | Record command and result. | Markdown lint is not factual review. |
| infra | applies | Use declared Compose/security checks for a concrete infra change. | Inspect named gate/oracle. | Static checks do not observe a live target. |
| ops | applies | Require operational acceptance and recovery evidence for release work. | Inspect runbook/event evidence. | CI does not establish release readiness. |
| qa | applies | Preserve the taxonomy from formatter through independent review. | Map each result to its actual oracle. | Coverage is not validation. |
| security | applies | Use the relevant scanner/control and security review. | Record target, version, result, and disposition. | A named scanner is not an absence-of-vulnerabilities claim. |

## Related Documents

- [Automation Pipeline Workflow](./automation-pipeline-workflow.md)
- [Verification and Validation](./verification-validation.md)
